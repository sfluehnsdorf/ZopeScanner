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

__doc__ = """ZopeScanner Product Initialisation"""

__version__ = '$Revision: 1.3 $'[11:-2]


# =============================================================================
# Module Imports

from resources.imports import ImageFile
from ZopeScanner import install_ZopeScanner


# =============================================================================
# Product Initialisation

def initialize(context):
    """Install Product"""

    install_ZopeScanner(context)


# =============================================================================
# Product Assetts

misc_ = {
    'ZopeScanner.png': ImageFile('ZopeScanner.png', globals()),
    }
