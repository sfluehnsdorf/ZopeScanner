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

__doc__ = """ZopeScanner Objects Resources"""

__version__ = '$Revision: 1.3 $'[11:-2]



# ============================================================================
# Objects Resources Mix-in Class

class Objects:
    """Objects Resources Mix-in Class"""

    def get_object(self, root_object, path):
        """Return the object specfied by a root object and path to traverse"""
        if path and path[0] != '/':
            path = '/' + path
        index = 0
        object = root_object
        parts = [('', object), ]
        while index < len(path):
            if path[index] == '/':
                id = ''
                index = index + 1
                while index < len(path) and path[index] != '/':
                    id = id + path[index]
                    index = index + 1
                try:
                    id = int(id)
                    object = object[id]
                except:
                    try:
                        object = object.get(id)
                    except:
                        try:
                            object = getattr(object, id)
                        except:
                            object = None
                parts.append((id, object))
            else:
                break
        return parts, object

    def get_object_id(self, object):
        """Return id of an object"""
        id = None
        try:
            id = object.getId()
        except:
            try:
                id = object.id()
            except:
                try:
                    id = object.id
                except:
                    pass
        # if not id:
        #     id = repr(object)
        return id

    def get_object_title(self, object):
        """Return title of an object"""
        title = None
        try:
            title = object.title()
        except:
            try:
                title = object.title
            except:
                pass
        if not title:
            try:
                title = object.__name__
            except:
                pass
        return title

    def get_object_label(self, object):
        """Return id and title of an object"""
        return self.get_object_id(object), self.get_object_title(object)
