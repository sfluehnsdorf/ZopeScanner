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

__doc__ = """ZopeScanner Resources"""

__version__ = '$Revision: 1.3 $'[11:-2]



# ============================================================================
# Imports

from formatting import Formatting
from helpers import Helpers
from imports import Imports
from objects import Objects
from scanning import Scanning
from ui import UserInterface



# ============================================================================
# Scanner Resources Mix-in Class

class ScannerResources(Helpers, Objects, Scanning, Formatting, UserInterface, Imports):
    """Scanner Resources Mix-in Class"""
    pass
