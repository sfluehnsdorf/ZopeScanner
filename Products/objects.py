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

__doc__ = """ZopeScanner ObjectScanner"""

__version__ = '$Revision: 1.3 $'[11:-2]


# =============================================================================
# Module Imports

from resources.imports import DTMLFile


# =============================================================================
# ObjectScanner Mix-in Class

class ObjectScanner:
    """ObjectScanner Mix-in Class"""

    scan_object_form = DTMLFile('objects', globals())

    def scan_object(self, path=''):
        """Scan Objects

        Perform a scan starting with the OFS' physical root object, traversing
        along the specified by path.
        """

        breadcrumbs = [
            self.breadcrumbs_root,
            ('scan_object_form', 'Objects')
            ]

        if path == '/':
            path = ''

        return self.scan(breadcrumbs, self.getPhysicalRoot(), path)
