#/bin/bash

echo $1 > /sys/devices/2200000.gpio/gpiochip0/gpio/gpio398/value

python3 /var/lib/homeassistant/plant_lights.py $1
