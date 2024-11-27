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
            plants.append({'plant_name': plant_name, 'plant_id': sanitize_plant_id(plant_name), 'days_between_watering': days_between_watering})
    return plants

def generate_configuration_yaml(plants):
    config_lines = []
    # Add default_config, http, lovelace
    config_lines.append('default_config:\n')
    config_lines.append('http:')
    config_lines.append('  server_host: 0.0.0.0')
    config_lines.append('  server_port: 8123\n')
    config_lines.append('lovelace:')
    config_lines.append('  mode: yaml\n')
    # input_datetime:
    config_lines.append('input_datetime:')
    for plant in plants:
        config_lines.append(f'  last_watered_{plant["plant_id"]}:')
        config_lines.append(f'    name: Last watered date {plant["plant_name"]}')
        config_lines.append('    has_date: true')
        config_lines.append('    has_time: true')
    config_lines.append('')

    # sensor:
    config_lines.append('sensor:')
    config_lines.append('  - platform: time_date')
    config_lines.append('    display_options:')
    config_lines.append("      - 'date'")
    config_lines.append("      - 'time'")
    config_lines.append('  - platform: template')
    config_lines.append('    sensors:')
    config_lines.append('      current_datetime:')
    config_lines.append('        friendly_name: "Current time and date"')
    config_lines.append('        value_template: >')
    config_lines.append("          {{ now().strftime('%Y-%m-%d %H-%M-%s') }}")
    config_lines.append('        entity_id: sensor.time')
    for plant in plants:
        config_lines.append(f'      next_water_days_{plant["plant_id"]}:')
        config_lines.append(f'        friendly_name: "Next watering for {plant["plant_name"]}"')
        config_lines.append('        value_template: >')
        config_lines.append(f"          {{{{ ((as_timestamp(states('input_datetime.last_watered_{plant['plant_id']}')) / 86400) + {plant['days_between_watering']}) - (as_timestamp(now()) / 86400) }}}}")
        config_lines.append('        entity_id:')
        config_lines.append(f'          - input_datetime.last_watered_{plant["plant_id"]}')
        config_lines.append('          - sensor.time')
    config_lines.append('')

    # binary_sensor:
    config_lines.append('binary_sensor:')
    config_lines.append('  - platform: template')
    config_lines.append('    sensors:')
    for plant in plants:
        config_lines.append(f'      needs_watering_{plant["plant_id"]}:')
        config_lines.append(f'        friendly_name: "{plant["plant_name"]} needs watering"')
        config_lines.append('        value_template: >')
        config_lines.append(f"          {{{{ (as_timestamp(states('input_datetime.last_watered_{plant['plant_id']}')) + ({plant['days_between_watering']} * 86400)) <= (as_timestamp(now())) }}}}")
    config_lines.append('')

    # script:
    config_lines.append('script:')
    for plant in plants:
        config_lines.append(f'  water_{plant["plant_id"]}:')
        config_lines.append(f'    alias: Water {plant["plant_name"]}')
        config_lines.append('    sequence:')
        config_lines.append('      - service: input_datetime.set_datetime')
        config_lines.append('        data_template:')
        config_lines.append(f'          entity_id: input_datetime.last_watered_{plant["plant_id"]}')
        config_lines.append("          datetime: \"{{ now().strftime('%Y-%m-%d %H:%M:%S') }}\"")
    config_lines.append('')

    return '\n'.join(config_lines)

def generate_ui_lovelace_yaml(plants):
    ui_lines = []
    ui_lines.append('title: Home\n')
    ui_lines.append('views:')
    ui_lines.append('  - path: default_view')
    ui_lines.append('    title: Home')
    ui_lines.append('    cards:')
    ui_lines.append('      - type: markdown')
    ui_lines.append('        content: >')
    ui_lines.append("          # {{ states('sensor.date') }} | {{ states('sensor.time') }}")
    ui_lines.append('      - type: entities')
    ui_lines.append('        title: Plant Watering Schedule')
    ui_lines.append('        entities:')
    for plant in plants:
        ui_lines.append(f'          - entity: input_datetime.last_watered_{plant["plant_id"]}')
        ui_lines.append(f'            name: Last time {plant["plant_name"]} was watered')
        ui_lines.append(f'          - entity: sensor.next_water_days_{plant["plant_id"]}')
        ui_lines.append(f'            name: {plant["plant_name"]} next watering date')
        ui_lines.append(f'          - entity: binary_sensor.needs_watering_{plant["plant_id"]}')
        ui_lines.append(f'            name: {plant["plant_name"]} needs watering today')
        ui_lines.append(f'          - type: call-service')
        ui_lines.append(f'            name: Water {plant["plant_name"]}')
        ui_lines.append('            icon: mdi:water')
        ui_lines.append(f'            action_name: Water {plant["plant_name"]} now')
        ui_lines.append(f'            service: script.water_{plant["plant_id"]}')
    ui_lines.append('')

    return '\n'.join(ui_lines)

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

