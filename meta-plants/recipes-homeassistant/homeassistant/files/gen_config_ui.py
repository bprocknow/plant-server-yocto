import re

def sanitize_plant_id(plant_name):
    # Convert to lowercase, replace spaces with underscores, remove non-alphanumeric characters
    plant_id = plant_name.lower()
    plant_id = re.sub(r'\s+', '_', plant_id)
    plant_id = re.sub(r'[^\w_]', '', plant_id)
    return plant_id

def read_plants_file(filename):
    plants = []
    with open(filename, 'r') as f:
        for line in f:
            # Remove comments and whitespace
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Assuming delimiter is comma
            parts = re.split(r'[,]', line)
            if len(parts) != 2:
                print(f"Invalid line in plants.yaml: {line}")
                continue
            plant_name = parts[0].strip()
            days_between_watering = parts[1].strip()
            try:
                days_between_watering = int(days_between_watering)
            except ValueError:
                print(f"Invalid days between watering for plant {plant_name}")
                continue
            plants.append({
                'plant_name': plant_name,
                'plant_id': sanitize_plant_id(plant_name),
                'days_between_watering': days_between_watering
            })
    return plants

def generate_configuration_yaml(plants):
    config_yaml = '''default_config:

http:
  server_host: 0.0.0.0
  server_port: 8123

lovelace:
  mode: yaml

input_datetime:
'''
    for plant in plants:
        config_yaml += f'''  last_watered_{plant["plant_id"]}:
    name: Last watered date {plant["plant_name"]}
    has_date: true
    has_time: true
'''
    config_yaml += '''
sensor:
  - platform: time_date
    display_options:
      - 'date'
      - 'time'
  - platform: template
    sensors:
      current_datetime:
        friendly_name: "Current time and date"
        value_template: >
          {{ now().strftime('%Y-%m-%d %H-%M-%S') }}
        entity_id: sensor.time
'''
    for plant in plants:
        config_yaml += f'''      next_water_days_{plant["plant_id"]}:
        friendly_name: "Next watering for {plant["plant_name"]}"
        value_template: >
          {{{{ (((as_timestamp(states('input_datetime.last_watered_{plant["plant_id"]}')) / 86400) + {plant["days_between_watering"]}) - (as_timestamp(now()) / 86400)) | float | round(2) }}}}
        entity_id:
          - input_datetime.last_watered_{plant["plant_id"]}
          - sensor.time
'''
    config_yaml += '''
binary_sensor:
  - platform: template
    sensors:
'''
    for plant in plants:
        config_yaml += f'''      needs_watering_{plant["plant_id"]}:
        friendly_name: "{plant["plant_name"]} needs watering"
        value_template: >
          {{{{ (as_timestamp(states('input_datetime.last_watered_{plant["plant_id"]}')) + ({plant["days_between_watering"]} * 86400)) <= as_timestamp(now()) }}}}
'''
    config_yaml += '''
input_boolean:
  plant_lights_toggle:
    name: Plant Lights Input Toggle
    initial: off
  ambient_lights_toggle:
    name: Ambient Lights Input Toggle
    initial: off

shell_command:
  plant_light_cmd: /bin/bash /var/lib/homeassistant/plant_lights.sh {{ parameter }}
  ambient_light_cmd: /bin/bash /var/lib/homeassistant/ambient_lights.sh {{ parameter }}

automation:
  - alias: Plant lights on
    trigger:
        - platform: state
          entity_id: input_boolean.plant_lights_toggle
          to: 'on'
    action:
      - service: shell_command.plant_light_cmd
        data:
          parameter: '1'
  - alias: Plant lights off
    trigger:
        - platform: state
          entity_id: input_boolean.plant_lights_toggle
          to: 'off'
    action:
      - service: shell_command.plant_light_cmd
        data:
          parameter: '0'
  - alias: Ambient lights on
    trigger:
        - platform: state
          entity_id: input_boolean.ambient_lights_toggle
          to: 'on'
    action:
      - service: shell_command.ambient_light_cmd
        data:
          parameter: '1'
  - alias: Ambient lights off
    trigger:
        - platform: state
          entity_id: input_boolean.ambient_lights_toggle
          to: 'off'
    action:
      - service: shell_command.ambient_light_cmd
        data:
          parameter: '0'

script:
'''
    for plant in plants:
        config_yaml += f'''  water_{plant["plant_id"]}:
    alias: Water {plant["plant_name"]}
    sequence:
      - service: input_datetime.set_datetime
        data_template:
          entity_id: input_datetime.last_watered_{plant["plant_id"]}
          datetime: "{{{{ now().strftime('%Y-%m-%d %H:%M:%S') }}}}"
'''
    return config_yaml

def generate_ui_lovelace_yaml(plants):
    ui_yaml = '''title: Home

views:
  - path: default_view
    title: Home
    cards:
      - type: vertical-stack
        cards:
        - type: markdown
          content: >
            # {{ states('sensor.date') }} | {{ states('sensor.time') }}
        - type: entities
          title: Light Control Panel
          entities:
            - entity: input_boolean.plant_lights_toggle
              name: Plant Light Switch
            - entity: input_boolean.ambient_lights_toggle
              name: Ambient Light Switch
'''
    for plant in plants:
        ui_yaml += f'''        - type: entities
          title: {plant["plant_name"]} Schedule
          entities:
            - entity: input_datetime.last_watered_{plant["plant_id"]}
              name: Last time {plant["plant_name"]} was watered
            - entity: sensor.next_water_days_{plant["plant_id"]}
              name: {plant["plant_name"]} next watering date
            - entity: binary_sensor.needs_watering_{plant["plant_id"]}
              name: {plant["plant_name"]} needs watering today
            - type: call-service
              name: Water {plant["plant_name"]}
              icon: mdi:water
              action_name: Water {plant["plant_name"]} now
              service: script.water_{plant["plant_id"]}
'''
    return ui_yaml

def main():
    plants = read_plants_file('plants.yaml')
    config_yaml = generate_configuration_yaml(plants)
    ui_yaml = generate_ui_lovelace_yaml(plants)

    with open('configuration.yaml', 'w') as f:
        f.write(config_yaml)

    with open('ui-lovelace.yaml', 'w') as f:
        f.write(ui_yaml)

if __name__ == '__main__':
    main()

