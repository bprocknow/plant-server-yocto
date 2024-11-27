#!/bin/sh
# wifi-start.sh

# Start wpa_supplicant
wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant.conf

# Obtain an IP address
dhclient wlan0

