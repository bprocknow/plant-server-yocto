# plant-server-yocto

Environment:
Supported distribution (snip from dunfell poky):
```
SANITY_TESTED_DISTROS ?= " \
            poky-2.7 \n \
            poky-3.0 \n \
            poky-3.1 \n \
            ubuntu-18.04 \n \
            ubuntu-20.04 \n \
            ubuntu-22.04 \n \
            fedora-37 \n \
            debian-11 \n \
            opensuseleap-15.3 \n \
            almalinux-8.8 \n \
            "
```

Package Dependencies (Fedora):
gcc python3 wget git cpio diffstat gawk perl file

---------------------------------

Installing poky buildtools:

./poky/scripts/install-buildtools

Source the poky environment:

. poky/buildtools/environment

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

Run the deploy.sh script
./deploy.sh core-<bphome> jetson-tx2-devkit
