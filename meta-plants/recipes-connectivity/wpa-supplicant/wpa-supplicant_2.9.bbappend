FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

inherit systemd

SRC_URI += " \
	file://wpa_supplicant.conf \
	file://wifi-start.sh \
	file://wifi.service \
"

do_install_append() {
    # Install wpa_supplicant.conf
    install -d ${D}${sysconfdir}/
    install -m 600 ${WORKDIR}/wpa_supplicant.conf ${D}${sysconfdir}/wpa_supplicant.conf

    # Install wifi-start.sh
    install -d ${D}${bindir}
    install -m 755 ${WORKDIR}/wifi-start.sh ${D}${bindir}/wifi-start.sh

    # Install wifi.service
    install -d ${D}${systemd_system_unitdir}
    install -m 644 ${WORKDIR}/wifi.service ${D}${systemd_system_unitdir}/wifi.service
}

SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE_${PN} = "wifi.service"

RDEPENDS_${PN} = "wpa-supplicant dhcp-client"

FILES_${PN} += "${sysconfdir}/wpa_supplicant.conf \
                ${bindir}/wifi-start.sh \
                ${systemd_system_unitdir}/wifi.service \
               "

