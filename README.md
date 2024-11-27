# plant-server-yocto

Environment:
meta-browser requires binutils-2.53, which is old.  A fedora34 container has this dependency.

Package Dependencies (Fedora):
gcc python3 wget git cpio diffstat gawk perl file

---------------------------------

Installing poky buildtools:

./poky/scripts/install-buildtools

Source the poky environment:

. poky/buildtools/environment
. poky/oe-init-build-env ./build-plants/

Building the image:
bitbake core-\<bphome?\>

----------------------------------

Connecting to WIFI:
TODO:  Make an application that is started (part of homeassistant?) that asks for WIFI login.

1. Modify \/etc/wpa\_supplicant\/wpa\_supplicant.conf

network={
    ssid="MyNetworkSSID"
    psk="MyNetworkPassword"
}

2. Start wpa\_supplicant with the updated configuration:
wpa\_supplicant -B -i \<interface> -c \/etc/wpa\_supplicant\/wpa\_supplicant.conf

3. Obtain an IP address with DHCP:
dhclient \<interface\>

4. Verify the connection:
ping www.google.com

----------------------------------

Programming the NVIDIA Jetson TX2 Board:

With the Jetson shutdown and unplugged from power, plug in the:

HDMI port to a monitor
Ethernet port to a router you are connected to on your Mac(can be wired or wireless - I used wireless, but ran into a small problem which I provide a solution to later on)
Micro USB port with the provided USB cable, and connect that to your Mac - which we call the Host
USB port to a hub(ideally) with mouse and keyboard. If not, just to a mouse or keyword and switch when needed
Antennas that came with the Jetson
Finally, the power cable

Press and release the Power Button (furthest to the Right, of the 4 buttons onboard)
Hold down the Forced Recovery button (says 'REC' on the pcb)
With REC held down, press and release the reset button (says 'RST' on the pcb)
Hold REC for 2 more seconds, and release

Run the deploy.sh script:
./deploy.sh core-<bphome> jetson-tx2-devkit
