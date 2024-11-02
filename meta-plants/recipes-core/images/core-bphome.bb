SUMMARY = "Home Automation Image"
LICENSE = "MIT"

inherit core-image

# 200 MiB of additional storage for config and runtime data
IMAGE_ROOTFS_EXTRA_SPACE = "204800"

IMAGE_INSTALL += " \
	xserver-xorg \
	xinit \
	xserver-xorg-video-nvidia \
	xf86-input-libinput \
	packagegroup-core-boot \
	chromium-x11 \
	python3-homeassistant \
	python3-appdaemon \
	systemd \
	systemd-analyze \
	vim \
	pciutils \
	dhcp-client \
	"

