SUMMARY = "Home Automation Image"
LICENSE = "MIT"

inherit core-image

TIMEZONE = "America/Chicago"

# 200 MiB of additional storage for config and runtime data
IMAGE_ROOTFS_EXTRA_SPACE = "204800"

IMAGE_FEATURES += " \
	ssh-server-dropbear \
	"

IMAGE_INSTALL += " \
	glibc \
	pixman \
	xinit \
	xhost \
	xauth \
	xserver-xorg-module-libwfb \
	xserver-xorg-video-nvidia \
	xserver-xorg \
	xset \
	xf86-input-libinput \
	packagegroup-core-boot \
	chromium-x11 \
	chromium-launcher \
	python3-homeassistant \
	python3-appdaemon \
	systemd \
	systemd-analyze \
	vim \
	pciutils \
	dhcp-client \
	tzdata \
	ntp \
	ntpdate \
	xrandr \
	xinput \
	libinput \
	python3-pyserial \
	python3-pyserial-asyncio \
	python3-appdaemon \
	dropbear \
	"

