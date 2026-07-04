# -*- coding: utf8 -*-
u"""ZopeScanner Product.

# =============================================================================
#
#                            Z o p e  S c a n n e r
#
# -----------------------------------------------------------------------------
# Copyright (c) 2009 - 2014, Sebastian Lühnsdorf - Web-Solutions
# For more information see the README.txt file or visit www.zope.biz
# -----------------------------------------------------------------------------
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).
#
# A copy of the ZPL should accompany this distribution.
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
# =============================================================================
"""


# =============================================================================
# Imports

from config import ConfigScanner
from logs import LogScanner
from modules import ModuleScanner
from objects import ObjectScanner
from products import ProductScanner
from resources import ScannerResources
from resources.imports import ApplicationManager, DTMLFile, DevelopmentMode,\
    Implicit, Item, getLogger
from servers import ServerScanner
from sources import SourceScanner


# =============================================================================
# ZopeScanner Product Class

class ZopeScanner(
    ConfigScanner, LogScanner, ModuleScanner, ObjectScanner, ProductScanner,
    ServerScanner, SourceScanner, ScannerResources, Item, Implicit
):
    """ZopeScanner Product Class."""

    # -------------------------------------------------------------------------
    # Zope Assetts

    id = 'ZopeScanner'
    name = 'ZopeScanner'
    title = 'ZopeScanner'
    meta_type = 'ZopeScanner'
    icon = 'misc_/ZopeScanner/ZopeScanner.png'

    manage_options = (
        {'label': 'ZopeScanner', 'action': 'scanner_main_form'},
        {'label': 'Config', 'action': 'scan_config_form'},
        {'label': 'Servers', 'action': 'scan_server_form'},
        {'label': 'Products', 'action': 'scan_product_form'},
        {'label': 'Objects', 'action': 'scan_object_form'},
        {'label': 'Modules', 'action': 'scan_module_form'},
        {'label': 'Sources', 'action': 'scan_source_form'},
        {'label': 'Log Files', 'action': 'scan_logfile_form'},
    )

    def locked_in_version(self):
        """Lorem Ipsum."""
        return 0

    # -------------------------------------------------------------------------
    # Product Assetts

    def scanner_url(self):
        """Lorem Ipsum."""
        return self.absolute_url()

    # -------------------------------------------------------------------------
    # User Interface Assetts

    breadcrumbs_root = ('scanner_main_form', 'ZopeScanner')

    scanner_main_form = DTMLFile('ZopeScanner', globals())

    # -------------------------------------------------------------------------
    # User Interface Customisation

    batch_size = 20
    group_lists = True
    use_js = True

    def set_options(self, REQUEST):
        """Store user interface options.

        Store changes to options of the user interface either in cookies on a
        per user level or as global defaults in attributes of the Product.
        """
        #

        # format options
        try:
            batch_size = int(REQUEST.form.get('batch_size', 20))
        except:
            batch_size = 20
        group_lists = REQUEST.form.get('group_lists', None) and True or False
        use_js = REQUEST.form.get('use_js', None) and True or False

        # store options as defaults
        if REQUEST.form.get('set_defaults', None):
            self.batch_size = batch_size
            self.group_lists = group_lists
            self.use_js = use_js

        # store options in cookies
        else:
            REQUEST.RESPONSE.setCookie('ZopeScanner_batch_size', batch_size)
            REQUEST.RESPONSE.setCookie('ZopeScanner_group_lists', group_lists)
            REQUEST.RESPONSE.setCookie('ZopeScanner_use_js', use_js)

        # redirect
        REQUEST.RESPONSE.redirect('%s/scanner_main_form' % self.scanner_url())


def install_ZopeScanner(context):
    """Install ZopeScanner.

    Create a new instance of the ZopeScanner and add it to the Control Panel of
    the Zope server. This way there can only be exactly one instance of
    ZopeScanner on a Zope server. Also, there is a test if the server is
    configured to run in development mode to avoid this Product to be installed
    on a production server.
    """
    logger = getLogger('ZopeScanner')

    if DevelopmentMode:
        scanner = ZopeScanner()
        setattr(ApplicationManager, scanner.id, scanner)
        objects = list(ApplicationManager._objects)
        objects.append({'id': scanner.id, 'meta_type': scanner.meta_type})
        ApplicationManager._objects = tuple(objects)
        logger.info('Installed into Control_Panel.')

    else:
        logger.info('Not installed, since not in development (debug) mode.')
