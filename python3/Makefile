include ../config.mk

IPROG=install -m 755
IDATA=install -m 644

SITE3_DIR=$(shell python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

install:
	mkdir -p $(DESTDIR)$(OPTDIR)/bin
	mkdir -p $(DESTDIR)$(SITE3_DIR)
	mkdir -p $(DESTDIR)$(LIBEXECDIR)


	$(IDATA) packages/observer.py $(DESTDIR)$(SITE3_DIR)/

	$(IPROG) libexec/usb_reset.py $(DESTDIR)$(LIBEXECDIR)
	$(IPROG) libexec/usb_scan.py $(DESTDIR)$(LIBEXECDIR)
	$(IPROG) libexec/nbd_client_manager.py $(DESTDIR)$(LIBEXECDIR)
	$(IPROG) bin/hfx_filename $(DESTDIR)$(OPTDIR)/bin
	$(IPROG) bin/perfmon $(DESTDIR)$(OPTDIR)/bin
	mkdir -p $(DESTDIR)$(ETCXENDIR)/bugtool/observer
	$(IPROG) mail-alarm $(DESTDIR)$(LIBEXECDIR)
	mkdir -p $(DESTDIR)$(OPTDIR)/debug
	$(IPROG) xe-scsi-dev-map $(DESTDIR)$(OPTDIR)/bin
	$(IPROG) xe-reset-networking $(DESTDIR)$(OPTDIR)/bin
	$(IPROG) static-vdis $(DESTDIR)$(OPTDIR)/bin
	mkdir -p $(DESTDIR)$(OPTDIR)/packages/iso #omg XX
	$(IPROG) host-display $(DESTDIR)$(LIBEXECDIR)
	$(IPROG) link-vms-by-sr.py $(DESTDIR)$(LIBEXECDIR)
	$(IPROG) print-custom-templates $(DESTDIR)$(LIBEXECDIR)
	$(IPROG) probe-device-for-file $(DESTDIR)$(LIBEXECDIR)
	mkdir -p $(DESTDIR)$(EXTENSIONDIR)
	$(IPROG) extensions/pool_update.precheck $(DESTDIR)$(EXTENSIONDIR)
	$(IPROG) extensions/pool_update.apply $(DESTDIR)$(EXTENSIONDIR)
	mkdir -p $(DESTDIR)$(PLUGINDIR)
	$(IPROG) plugins/perfmon $(DESTDIR)$(PLUGINDIR)
	$(IPROG) plugins/extauth-hook $(DESTDIR)$(PLUGINDIR)
	$(IPROG) plugins/extauth-hook-AD.py $(DESTDIR)$(PLUGINDIR)
	$(IPROG) plugins/install-supp-pack $(DESTDIR)$(PLUGINDIR)
	$(IPROG) plugins/disk-space $(DESTDIR)$(PLUGINDIR)
	$(IPROG) plugins/openvswitch-config-update $(DESTDIR)$(PLUGINDIR)
# templates
        $(IPROG) templates/debian $(DESTDIR)$(OPTDIR)/packages/post-install-scripts/debian-etch
        $(IPROG) templates/debug $(DESTDIR)$(OPTDIR)/packages/post-install-scripts
# example/python
ifneq ($(BUILD_PY2), NO)
        $(IDATA) examples/python/XenAPIPlugin.py $(DESTDIR)$(SITE_DIR)/
        $(IDATA) examples/python/XenAPI/XenAPI.py $(DESTDIR)$(SITE_DIR)/
        $(IDATA) examples/python/inventory.py $(DESTDIR)$(SITE_DIR)/
        $(IDATA) examples/python/exportimport.py $(DESTDIR)$(SITE_DIR)/
        $(IDATA) examples/python/lvhd-api-test.py $(DESTDIR)$(SITE_DIR)/
        $(IDATA) examples/python/mini-xenrt.py $(DESTDIR)$(SITE_DIR)/
        $(IDATA) examples/python/renameif.py $(DESTDIR)$(SITE_DIR)/
        $(IDATA) examples/python/smapiv2.py $(DESTDIR)$(SITE_DIR)/
        $(IDATA) examples/python/storage.py $(DESTDIR)$(SITE_DIR)/
endif
        $(IPROG) examples/python/echo.py $(DESTDIR)$(PLUGINDIR)/echo
	$(IPROG) examples/python/shell.py $(DESTDIR)$(LIBEXECDIR)/shell.py
# poweron
        $(IPROG) poweron/wlan.py $(DESTDIR)$(PLUGINDIR)/wlan.py
	$(IPROG) poweron/wlan.py $(DESTDIR)$(PLUGINDIR)/wake-on-lan
	$(IPROG) poweron/DRAC.py $(DESTDIR)$(PLUGINDIR)/DRAC.py
	$(IPROG) poweron/power-on.py $(DESTDIR)$(PLUGINDIR)/power-on-host
