#/bin/bash

echo $1 > /sys/devices/2200000.gpio/gpiochip0/gpio/gpio396/value

python3 /var/lib/homeassistant/ambient_lights.py $1
