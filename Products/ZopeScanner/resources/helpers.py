# -*- coding: iso-8859-15 -*-
# ============================================================================
#
#                          Z o p e   S c a n n e r
#
# ------------------------------------------------------------------------------
# Copyright (c) 2009-2012, Sebastian Lühnsdorf - Web-Solutions
# For more information see the README.txt file or visit www.zope.biz/scanner
# ------------------------------------------------------------------------------
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
# ============================================================================

__doc__ = """ZopeScanner Helpers"""

__version__ = '$Revision: 1.3 $'[11:-2]



# ============================================================================
# User Interface Resources Mix-in Class

class Helpers:

    def get_link_url(self, form_id, *ids):
        """Return a formatted link based on the specified form and ids"""
        if not form_id:
            raise
        base = '%s/%s?path=' % (self.scanner_url(), form_id)
        if ids:
            base = base + '/'.join(ids)
        return base

    def sort_by_first_value(self, x, y):
        """Sort a sequence of sequences on the first item """
        return cmp(x[0], y[0])
