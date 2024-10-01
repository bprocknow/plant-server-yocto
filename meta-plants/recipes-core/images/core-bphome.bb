SUMMARY = "Home Automation Image"
LICENSE = "MIT"

inherit core-image

IMAGE_INSTALL += " \
	packagegroup-core-boot \
	systemd \
	systemd-analyze \
	vim \
	pciutils \
	dhcp-client \
	"

