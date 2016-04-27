#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import os
import subprocess
import sys
import re
import xml.etree.ElementTree as ET

from glob import glob

if len(sys.argv) < 2:
    sys.exit("This script requires a single argument.")

PKGS_DIR = sys.argv[1]
PKGS_DIR = os.path.abspath(PKGS_DIR)

for product_dirname in os.walk(PKGS_DIR).next()[1]:
    product = os.path.join(PKGS_DIR, product_dirname)
    if not os.path.isdir(product):
        continue
    install_pkg_path_glob = glob(os.path.join(product, "Build/*Install.pkg"))
    uninstall_pkg_path_glob = glob(os.path.join(product, "Build/*Uninstall.pkg"
                                                ))
    ccp_file_path_glob = glob(os.path.join(product, "*.ccp"))

    if not install_pkg_path_glob or not uninstall_pkg_path_glob:
        print >> sys.stderr, ("'%s' doesn't look like a CCP package, skipping"
                              % product)
        continue

    install_pkg_path = install_pkg_path_glob[0]
    uninstall_pkg_path = uninstall_pkg_path_glob[0]
    ccp_file_path = ccp_file_path_glob[0]
    tree = ET.parse(ccp_file_path)

    media_list = tree.findall(".//Media")
    for media in media_list:
        display_name = media.find(".//prodName").text
        display_name = "Adobe {0}".format(display_name)
        item_name = re.sub('[()\s]', '', display_name)

    cmd = [
        "../aamporter.py",
        "--build-product-plist",
        "{0}".format(ccp_file_path),
        "--munki-update-for={0}".format(item_name),
        ]

    subprocess.call(cmd)
