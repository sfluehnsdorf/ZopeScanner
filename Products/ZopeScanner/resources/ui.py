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

__doc__ = """ZopeScanner User Interface Resources"""

__version__ = '$Revision: 1.3 $'[11:-2]



# ============================================================================
# Imports

from imports import DTMLFile, ImageFile



# ============================================================================
# User Interface Resources Mix-in Class

class UserInterface:
    """User Interface Resources Mix-in Class"""

    scanner_css = DTMLFile('css', globals())
    scanner_js = DTMLFile('js', globals())

    breadcrumbs_html = DTMLFile('breadcrumbs', globals())
    breadcrumbs_image = ImageFile('breadcrumbs.png', globals())

    banner_bg_image = ImageFile('banner_bg.png', globals())
    banner_fg_image = ImageFile('banner_fg.jpg', globals())
    banner_fg_low_image = ImageFile('banner_fg_low.jpg', globals())

    view_on_image = ImageFile('view_on.png', globals())
    view_off_image = ImageFile('view_off.png', globals())

    top_jump_image = ImageFile('top_jump.png', globals())

    batch_first_image = ImageFile('batch_first.png', globals())
    batch_prev_image = ImageFile('batch_prev.png', globals())
    batch_next_image = ImageFile('batch_next.png', globals())
    batch_last_image = ImageFile('batch_last.png', globals())

    image_bg_image = ImageFile('image_bg.png', globals())
    image_tl_image = ImageFile('image_tl.png', globals())
    image_tr_image = ImageFile('image_tr.png', globals())
    image_bl_image = ImageFile('image_bl.png', globals())
    image_br_image = ImageFile('image_br.png', globals())

    def jsify(self, key):
        """Filter for ASCII characters in a key"""
        jskey = ''
        for char in key:
            if char.lower() in 'abcdefghijklmnopqrstuvwxyz0123456789':
                jskey = jskey + char
        return jskey
