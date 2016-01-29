#!/usr/bin/python
# -*- coding: utf-8 -*-
#
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

from glob import glob

# check to see if we're root
if os.geteuid() != 0:
    print >> sys.stderr, 'You must run this as root!'
    exit(1)

if len(sys.argv) < 2:
    sys.exit("This script requires a single argument. See the script comments.\
             ")

PKGS_DIR = sys.argv[1]
PKGS_DIR = os.path.abspath(PKGS_DIR)

for product in os.listdir(PKGS_DIR):
    product_path = os.path.join(PKGS_DIR, product)
    if not os.path.isdir(product_path):
        continue
    install_pkg_path_glob = glob(os.path.join(product_path, "Build/*Install.pkg"))
    uninstall_pkg_path_glob = glob(os.path.join(product_path, "Build/*Uninstall.pkg"
                                                ))

    if not install_pkg_path_glob or not uninstall_pkg_path_glob:
        print >> sys.stderr, ("'%s' doesn't look like a CCP package, skipping"
                              % product_path)
        continue

    install_pkg_path = install_pkg_path_glob[0]
    uninstall_pkg_path = uninstall_pkg_path_glob[0]

    cmd = [
        "/usr/bin/hdiutil",
        "create",
        "-puppetstrings",
        "-verbose",
        "-srcFolder",
        "{0}".format(product_path),
        "{0}/{1}.dmg".format(PKGS_DIR, product),
        ]
    subprocess.call(cmd)
