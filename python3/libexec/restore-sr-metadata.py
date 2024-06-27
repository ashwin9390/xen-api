#!/usr/bin/python3
# Restore SR metadata and VDI names from an XML file
# (c) Anil Madhavapeddy, Citrix Systems Inc, 2008

import atexit
import io
import getopt
import sys
from xml.dom.minidom import parse

import XenAPI

sys.stdout = io.open(sys.stdout.fileno(), 'w', encoding='utf-8')
sys.stderr = io.open(sys.stderr.fileno(), 'w', encoding='utf-8')


def logout():
    try:
        session.xenapi.session.logout()
    except Exception as e:
        print("Logout failed: {}".format(e))


atexit.register(logout)


def usage():
    print("%s -f <input file> -u <sr uuid>" % sys.argv[0], file=sys.stderr)
    sys.exit(1)


def main(argv):
    session = XenAPI.xapi_local()
    session.xenapi.login_with_password(
        "", "", "1.0", "xen-api-scripts-restore-sr-metadata"
    )

    try:
        opts, _ = getopt.getopt(argv, "hf:u:", [])#args replaced with _
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    infile = None
    sruuid = None
    for o, a in opts:
        if o == "-f":
            infile = a
        if o == "-u":
            sruuid = a

    if infile is  None:
        usage()

    try:
        doc = parse(infile)
    except Exception as e:
        print("Error parsing {}: {}".format(infile, e), file=sys.stderr)
        sys.exit(1)

    if doc.documentElement.tagName != "meta":
        print("Unexpected root element while parsing %s" % infile, file=sys.stderr)
        sys.exit(1)

    for srxml in doc.documentElement.childNodes:
        try:
            uuid = srxml.getAttribute("uuid")
            name_label = srxml.getAttribute("name_label")
            name_descr = srxml.getAttribute("name_description")
        except Exception as e:
            print("Unexpected error parsing SR tag: {}".format(e), file=sys.stderr)
            continue
        # only set attributes on the selected SR passed in on cmd line
        if sruuid is None or sruuid == "all" or sruuid == uuid:
            try:
                srref = session.xenapi.SR.get_by_uuid(uuid)
                print("Setting SR (%s):" % uuid)
                session.xenapi.SR.set_name_label(srref, name_label)
                print("  Name: %s " % name_label)
                session.xenapi.SR.set_name_description(srref, name_descr)
                print("  Description: %s" % name_descr)
            except Exception as e:
                error_message = "Error setting SR data for: {} ({})\nException occurred: {}".format(uuid, name_label, str(e))
                print(error_message, file=sys.stderr)
                sys.exit(1)
            # go through all the SR VDIs and set the name_label and description
            for vdixml in srxml.childNodes:
                try:
                    vdi_uuid = vdixml.getAttribute("uuid")
                    vdi_label = vdixml.getAttribute("name_label")
                    vdi_descr = vdixml.getAttribute("name_description")
                except Exception as e:
                    print("Error parsing VDI tag:{}".format(e), file=sys.stderr)
                    continue
                try:
                    vdiref = session.xenapi.VDI.get_by_uuid(vdi_uuid)
                    print("Setting VDI (%s):" % vdi_uuid)
                    session.xenapi.VDI.set_name_label(vdiref, vdi_label)
                    print("  Name: %s" % vdi_label)
                    session.xenapi.VDI.set_name_description(vdiref, vdi_descr)
                    print("  Description: %s" % vdi_descr)
                except Exception as e:
                    print("Error setting VDI data for: {} ({})".format(vdi_uuid, name_label), file=sys.stderr)
                    continue


if __name__ == "__main__":
    main(sys.argv[1:])
