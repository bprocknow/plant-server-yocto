#!/bin/bash

pushd /var/lib/homeassistant

# Generate configuration.yaml and ui-lovelace.yaml from plants.yaml
python3 gen_config_ui.py

systemctl restart homeassistant

popd
