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

__doc__ = """ZopeScanner ServerScanner"""

__version__ = '$Revision: 1.3 $'[11:-2]


# =============================================================================
# Imports

from resources.imports import DTMLFile, socket_map


# =============================================================================
# ServerScanner Mix-in Class

class ServerScanner:
    """ServerScanner Mix-in Class"""

    scan_server_form = DTMLFile('servers', globals())

    def scan_server(self, path=''):
        """Scan Servers

        Perform a scan starting with the list of active servers, traversing
        along the specified by path.
        """

        breadcrumbs = [
            self.breadcrumbs_root,
            ('scan_server_form', 'Servers'),
            ]

        if path == '/':
            path = ''

        if path:
            return self.scan(breadcrumbs, socket_map, path)

        servers = []
        format_value = self.format_value
        for key, value in socket_map.items():
            try:
                name = '%s' % getattr(value, 'SERVER_IDENT')
            except:
                name = '<em>n/a</em>'
            sclass = format_value(value, 'scan_server_form', '', str(key))
            try:
                hostname = '%s' % getattr(value, 'hostname')
            except:
                hostname = '<em>n/a</em>'
            try:
                ip = '%s' % getattr(value, 'ip')
            except:
                ip = '<em>n/a</em>'
            try:
                port = '%s' % getattr(value, 'port')
            except:
                port = '<em>n/a</em>'
            servers.append({
                'key': key,
                'name': name,
                'sclass': sclass,
                'hostname': hostname,
                'ip': ip,
                'port': port,
                })

        return {
            'breadcrumbs': breadcrumbs,
            'servers': servers,
            }
