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

__doc__ = """ZopeScanner Import Resources

$Id: resources/imports.py 8 2012-12-09 11:37:00Z sfluehnsdorf $
"""

__version__ = '$Revision: 1.3 $'[11:-2]



# ============================================================================
# Imports

from asyncore import socket_map
from logging import getLogger
from os import listdir, stat
from os.path import abspath, exists, isdir, join, normpath, realpath, split, splitext
from re import compile, match
from struct import unpack
from sys import maxint, modules, prefix, version
from time import ctime
from types import BooleanType, BufferType, BuiltinFunctionType,\
  BuiltinMethodType, ClassType, DictProxyType, DictType, EllipsisType,\
  FileType, FloatType, FunctionType, GeneratorType, InstanceType, IntType,\
  LambdaType, ListType, LongType, MethodType, ModuleType, NoneType,\
  NotImplementedType, ObjectType, SliceType, StringType, TupleType, TypeType,\
  UnboundMethodType, XRangeType

from AccessControl.Owned import UnownableOwner
from AccessControl.Permission import Permission
from AccessControl.SecurityManagement import getSecurityManager
from Acquisition import aq_parent, aq_inner, Implicit
from App.ApplicationManager import ApplicationManager
from App.config import getConfiguration
from Globals import DevelopmentMode, DTMLFile, HTML, HTMLFile, ImageFile, INSTANCE_HOME, MessageDialog, SOFTWARE_HOME, ZOPE_HOME
from OFS.SimpleItem import Item
from Products.PythonScripts.standard import html_quote
from ZopeUndo.Prefix import Prefix

import Products



# ============================================================================
# Failsafe Imports

_notImported = []

try:
    from types import ComplexType
except:
    ComplexType = _notImported

try:
    from types import UnicodeType
except:
    UnicodeType = _notImported

try:
    from types import CodeType
except:
    CodeType = _notImported

try:
    from types import TracebackType, FrameType
except:
    TracebackType = _notImported
    FrameType = _notImported


class Imports:

    _none_type = NoneType

    _boolean_type = BooleanType

    _sequence_types = {
        ListType: 'List',
        TupleType: 'Tuple',
    }

    _mapping_types = {
        DictType: 'Dict',
        DictProxyType: 'DictProxy',
    }

    _linkable_types = {
        BuiltinFunctionType: 'BuiltinFunction',
        BuiltinMethodType: 'BuiltinMethod',
        ClassType: 'Class',
        FunctionType: 'Function',
        GeneratorType: 'Generator',
        InstanceType: 'Instance',
        LambdaType: 'Lambda',
        MethodType: 'Method',
        ModuleType: 'Module',
        ObjectType: 'Object',
        UnboundMethodType: 'UnboundMethod',
    }

    _misc_types = {
        BufferType: 'Buffer',
        CodeType: 'Code',
        ComplexType: 'Complex',
        EllipsisType: 'Ellipsis',
        FileType: 'File',
        FloatType: 'Float',
        FrameType: 'Frame',
        IntType: 'Int',
        LongType: 'Long',
        NotImplementedType: 'NotImplemented',
        SliceType: 'Slice',
        StringType: 'String',
        TracebackType: 'Traceback',
        TypeType: 'Type',
        UnicodeType: 'Unicode',
        XRangeType: 'XRange',
    }

    _form_and_image_classes = {
        HTML: 'HTML',
        HTMLFile: 'HTMLFile',
        DTMLFile: 'DTMLFile',
        ImageFile: 'ImageFile',
        MessageDialog: 'MessageDialog',
    }

