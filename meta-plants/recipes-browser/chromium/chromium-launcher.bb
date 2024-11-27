DESCRIPTION = "Chromium browser launcher service and script"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

inherit systemd

SRC_URI += " \
	file://chromium.service \
	file://xinitrc \
	file://99-touchscreen.conf \
"

do_install_append() {
    install -d ${D}${systemd_system_unitdir}
    install -d ${D}/home/root/
    install -d ${D}${sysconfdir}/X11/xorg.conf.d
    install -m 644 ${WORKDIR}/chromium.service ${D}${systemd_system_unitdir}/chromium.service
    install -m 644 ${WORKDIR}/xinitrc ${D}/home/root/.xinitrc
    install -m 644 ${WORKDIR}/99-touchscreen.conf ${D}${sysconfdir}/X11/xorg.conf.d/99-touchscreen.conf
}

SYSTEMD_AUTO_ENABLE_${PN} = "enable"
SYSTEMD_SERVICE_${PN} = "chromium.service"

FILES_${PN} += "${systemd_system_unitdir}/chromium.service \
		/home/root/.xinitrc \
		${sysconfdir}/X11/xorg.conf.d/99-touchscreen.conf \
               "

