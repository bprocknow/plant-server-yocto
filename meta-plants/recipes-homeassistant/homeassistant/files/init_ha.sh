#!/bin/bash

# Enable gpios for controlling plant lights and ambient lights
# Pin 29 on J21 header of nvidia jetson tx2
echo 398 > /sys/class/gpio/export
# Pin 37 on J21 header of nvidia jetson tx2
echo 396 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio398/direction
echo out > /sys/class/gpio/gpio396/direction

chmod 666 /sys/devices/2200000.gpio/gpiochip0/gpio/gpio398/value
chmod 666 /sys/devices/2200000.gpio/gpiochip0/gpio/gpio396/value
chmod 666 /dev/ttyS0

pushd /var/lib/homeassistant

# Generate configuration.yaml and ui-lovelace.yaml from plants.yaml
python3 gen_config_ui.py

sleep 15

systemctl restart homeassistant

popd

