FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

RDEPENDS_${PN} += "bash"

SRC_URI += " \
	file://configha.service \
	file://gen_config_ui.py \
	file://plants.yaml \
	file://secrets.yaml \
	file://init_ha.sh \
"

# Add any required Python packages
RDEPENDS_${PN} += " \
    python3-requests \
    python3-aiohttp \
"

do_install_append() {
    install -d ${D}${localstatedir}/lib/homeassistant/
    install -d ${D}${systemd_system_unitdir}/
    install -m 0644 ${WORKDIR}/configha.service ${D}${systemd_system_unitdir}/configha.service
    install -m 0644 ${WORKDIR}/gen_config_ui.py ${D}${localstatedir}/lib/homeassistant/
    install -m 0644 ${WORKDIR}/plants.yaml ${D}${localstatedir}/lib/homeassistant/
    install -m 0644 ${WORKDIR}/secrets.yaml ${D}${localstatedir}/lib/homeassistant/
    install -m 0755 ${WORKDIR}/init_ha.sh ${D}${localstatedir}/lib/homeassistant/
}

SYSTEMD_SERVICE_${PN} += " \
	configha.service \
	"

FILES_${PN} += " \
	${systemd_system_unitdir}/configha.service \
	${localstatedir}/lib/homeassistant/gen_config_ui.py \
	${localstatedir}/lib/homeassistant/plants.yaml \
	${localstatedir}/lib/homeassistant/secrets.yaml \
	${localstatedir}/lib/homeassistant/init_ha.sh \
        "

