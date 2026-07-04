# -*- coding: utf8 -*-
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

__doc__ = """ZopeScanner ConfigScanner"""

__version__ = '$Revision: 1.3 $'[11:-2]


# =============================================================================
# Module Imports

from resources.imports import DTMLFile, getConfiguration


# =============================================================================
# ConfigScanner Mix-in Class

class ConfigScanner:
    """ConfigScanner Mix-in Class"""

    scan_config_form = DTMLFile('config', globals())

    def scan_config(self, path=''):
        """Scan Server Configuration

        Perform a scan starting at the Zope server's configuration object,
        traversing along the specified by path.
        """

        config = getConfiguration()

        breadcrumbs = [
            self.breadcrumbs_root,
            ('scan_config_form', 'Configuration')
            ]

        if path == '/':
            path = ''

        if path:
            return self.scan(breadcrumbs, config, path)

        configitems = []
        format_value = self.format_value
        keys = config.__dict__.keys()
        keys.sort()
        for key in keys:
            configitems.append((
                key,
                format_value(getattr(config, key), 'scan_config_form', '', key)
                ))

        return {
            'breadcrumbs': breadcrumbs,
            'configitems': configitems,
            }
