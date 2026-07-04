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

__doc__ = """ZopeScanner Scanning Resources"""

__version__ = '$Revision: 1.3 $'[11:-2]



# ============================================================================
# Imports

from imports import aq_inner, aq_parent, ctime, DTMLFile, getSecurityManager,\
  html_quote, maxint, Permission, Prefix, UnownableOwner, unpack



# ============================================================================
# Scanning Resources Mix-in Class

class Scanning:
    """Scanning Resources Mix-in Class"""

    def scan(self, breadcrumbs, root_object, path):
        result = {}
        form_id = breadcrumbs[1][0]
        parts, object = self.get_object(root_object, path)

        result['path_info'] = self.get_path_info(form_id, parts)
        if object:
            result['object_info'] = self.scan_object_info(form_id, path, object)
            result['sub_objects'] = self.scan_subobjects(form_id, path, object)
            result['manage_options'] = self.scan_manage_options(form_id, path, object)
            result['properties'] = self.scan_properties(form_id, path, object)
            result['permissions'] = self.scan_permissions(form_id, path, object)
            result['roles'] = self.scan_roles(form_id, path, object)
            result['ownership'] = self.scan_ownership(form_id, path, object)
            result['undoable'] = self.scan_undoable(form_id, path, object)
            result['history'] = self.scan_history(form_id, path, object)
            result['forms_images'] = self.scan_forms_and_images(form_id, path, object)
            result['callable'] = self.scan_callable(form_id, path, object)
            result['sequence_items'] = self.scan_sequence_items(form_id, path, object)
            result['mapping_items'] = self.scan_mapping_items(form_id, path, object)
            result['attr_dict'] = self.scan_attr_dict(form_id, path, object)
            result['attr_dir'] = self.scan_attr_dir(form_id, path, object)
            result['attr_dir_jumps'] = self.get_attr_dir_jumps(form_id, object)

        part_path = '%s?path=' % form_id
        get_object_id = self.get_object_id
        for key, object in parts[1:]:
            part_path = '%s/%s' % (part_path, key)
            if object:
                part_label = get_object_id(object) or key
            else:
                part_label = key
            breadcrumbs.append((part_path, part_label))
        result['breadcrumbs'] = breadcrumbs

        return result

    def get_path_info(self, form_id, parts):
        result = []
        path = ''
        get_link_url = self.get_link_url
        get_object_label = self.get_object_label
        for key, object in parts:
            id, title = label = get_object_label(object)
            if key:
                path = '%s/%s' % (path, key)
            if not id:
                id = key
            if not object:
                title = '<span class="error">Object could not be retrieved.</span>'
            result.append((get_link_url(form_id, path), key, self.format_label(label), id, title))
        return result

    def scan_object_info(self, form_id, path, object):
        result = []
        get_link_url = self.get_link_url
        format_value = self.format_value
        try:
            result.append(('repr(object)', html_quote(repr(object))))
        except:
            result.append(('repr(object)', '<em>n/a</em>'))
        try:
            result.append(('type(object)', html_quote(str(type(object)))))
        except:
            result.append(('type(object)', '<em>n/a</em>'))
        try:
            result.append(('object.__class__', format_value(object.__class__, form_id, path, '__class__')))
        except:
            result.append(('object.__class__', '<em>n/a</em>'))
        try:
            result.append(('object.__module__', format_value(object.__module__, form_id, path, '__module__')))
        except:
            result.append(('object.__module__', '<em>n/a</em>'))
        try:
            result.append(('object.__doc__', format_value(object.__doc__, form_id, path, '__doc__')))
        except:
            result.append(('object.__doc__', '<em>n/a</em>'))
        try:
            result.append(('object.id', format_value(object.id, form_id, path, 'id')))
        except:
            result.append(('object.id', '<em>n/a</em>'))
        try:
            result.append(('object.id()', format_value(object.id(), form_id, path, 'id')))
        except:
            result.append(('object.id()', '<em>n/a</em>'))
        try:
            result.append(('object.getId()', format_value(object.getId(), form_id, path, 'getId')))
        except:
            result.append(('object.getId()', '<em>n/a</em>'))
        try:
            result.append(('object.title', format_value(object.title, form_id, path, 'title')))
        except:
            result.append(('object.title', '<em>n/a</em>'))
        try:
            result.append(('object.title_and_id()', format_value(object.title_and_id(), form_id, path, 'title_and_id')))
        except:
            result.append(('object.title_and_id()', '<em>n/a</em>'))
        try:
            result.append(('object.title_or_id()', format_value(object.title_or_id(), form_id, path, 'title_or_id')))
        except:
            result.append(('object.title_or_id()', '<em>n/a</em>'))
        try:
            result.append(('object.meta_type', format_value(object.meta_type, form_id, path, 'meta_type')))
        except:
            result.append(('object.meta_type', '<em>n/a</em>'))
        try:
            result.append(('object.icon', '<b>Icon</b>: <img src="%s" /><br />%s' % (object.icon, format_value(object.icon, form_id, path, 'icon'))))
        except:
            result.append(('object.icon', '<em>n/a</em>'))
        try:
            formatted_url = '<b>URL</b>: ' + html_quote(repr(object.absolute_url()))
            urlParts = urlparse(object.absolute_url())
            prefix = urlunparse((urlParts[0], urlParts[1], '', '', '', ''))
            formatted_url = formatted_url + '<br /><a href="%s">view</a>, <a href="%s/manage">manage</a>: %s' % (prefix, prefix, prefix)
            for part in urlParts[2].split('/'):
                if part:
                    prefix = prefix + '/' + part
                    formatted_url = formatted_url + '<br /><a href="%s">view</a>, <a href="%s/manage">manage</a>: %s' % (prefix, prefix, prefix)
            result.append(('object.absolute_url()', formatted_url))
        except:
            result.append(('object.absolute_url()', '<em>n/a</em>'))
        return result

    def scan_subobjects(self, form_id, path, object):
        try:
            result = []
            format_value = self.format_value
            get_object_id = self.get_object_id
            get_object_title = self.get_object_title
            for id, object in object.objectItems():
                result.append((id, format_value(object, form_id, path, id)))
            result.sort(self.sort_by_first_value)
            return result
        except:
            return []

    def scan_manage_options(self, form_id, path, object):
        try:
            result = []
            format_value = self.format_value
            for manage_option in object.manage_options:
                id = manage_option.get('action', '<em>n/a</em>')
                result.append((id, self.format_value(manage_option, form_id, path, id)))
            return result
        except:
            return []

    def scan_properties(self, form_id, path, object):
        format_value = self.format_value
        try:
            result = []
            for property in object._properties:
                result.append((property['id'], format_value(property, form_id, path, property['id'])))
            result.sort(self.sort_by_first_value)
            return result
        except:
            try:
                result = []
                for id, value in object.propertyItems():
                    result.append((id, format_value(value, form_id, path, id)))
                result.sort(self.sort_by_first_value)
                return result
            except:
                return []

    def scan_permissions(self, form_id, path, object):
        try:
            validRoles = object.valid_roles()
            result = [validRoles, ]
            for permission in object.ac_inherited_permissions(1):
                name, value = permission[: 2]
                permissionObject = Permission(name, value, object)
                permissionRoles = permissionObject.getRoles(default = [])
                if isinstance(permissionRoles, list):
                    aquired = True
                    roles = []
                else:
                    aquired = False
                    roles = permissionRoles
                result.append((name, aquired, roles))
            return result
        except:
            return []

    def scan_roles(self, form_id, path, object):
        try:
            result = []
            format_value = self.format_value
            permission_map = {}
            for permission in object.ac_inherited_permissions(1):
                name, value = permission[: 2]
                permissionObject = Permission(name, value, object)
                permissionRoles = permissionObject.getRoles(default = [])
                if isinstance(permissionRoles, list):
                    permission_map[name] = None
                else:
                    permission_map[name] = permissionRoles
            for validRole in object.valid_roles():
                aquireds = []
                permissions = []
                unsetpermissions = []
                for key in permission_map.keys():
                    if permission_map[key] is None:
                        aquireds.append(key)
                    elif validRole in permission_map[key]:
                        permissions.append(key)
                    else:
                        unsetpermissions.append(key)
                aquireds.sort()
                permissions.sort()
                unsetpermissions.sort()
                result.append((validRole, aquireds, permissions, unsetpermissions))
            return result
        except:
            return []

    def scan_ownership(self, form_id, path, object):
        try:
            format_value = self.format_value
            owner = object.getOwnerTuple()
            if owner is None:
                return (('owner', format_value(None, form_id, None, None)),)
            elif owner is UnownableOwner:
                return (('owner', '<em>Unownable</em>'),)
            else:
                result = []
                result.append(('owner', format_value(owner[1], form_id, None, None)))
                result.append(('path to UserFolder', format_value('/' + '/'.join(owner[0]), form_id, None, None)))
                result.append(('explicitly owned', format_value(hasattr(object, '_owner'), form_id, None, None)))
                result.append(('user can change ownership type', format_value(getSecurityManager().checkPermission('Take ownership', object), form_id, None, None)))
                return result
        except:
            return []

    def scan_undoable(self, form_id, path, object):
        try:
            result = []
            format_value = self.format_value
            spec = {'user_name': Prefix('')}
            if getattr(aq_parent(aq_inner(object)), '_p_jar', None) == object._p_jar:
                opath = '/'.join(object.getPhysicalPath())
                if opath:
                    spec['description'] = Prefix(opath)
            transactions = object._p_jar.db().undoInfo(0, maxint, spec)
            for transaction in transactions:
                transaction['ctime'] = ctime(transaction['time'])
                result.append((transaction['time'], format_value(transaction, form_id, None, None)))
            result.sort(self.sort_by_first_value)
            return result
        except:
            return []

    def scan_history(self, form_id, path, object):
        try:
            result = []
            format_value = self.format_value
            revisions = object._p_jar.db().history(object._p_oid, None, maxint)
            if revisions:
                for revision in revisions:
                    key = '.'.join(map(str, unpack(">HHHH", revision['tid'])))
                    revision['ctime'] = ctime(revision['time'])
                    result.append((key, format_value(revision, form_id, None, None)))
                result.sort(self.sort_by_first_value)
                return result
            else:
                return (('', "<em>Storage doesn't support history</em>"),)
        except:
            return []

    def scan_forms_and_images(self, form_id, path, object):
        result = []
        format_form_and_image_classes = self.format_form_and_image_classes
        for id in dir(object):
            try:
                value = getattr(object, id)
                try:
                    url = '%s/%s' % (object.absolute_url(), id)
                except:
                    url = None
                result.append((id, self.format_form_and_image_classes(value, form_id, path, id), url))
            except:
                pass
        result.sort(self.sort_by_first_value)
        return result

    def scan_callable(self, form_id, path, object):
        result = []
        format_value = self.format_value
        for id in dir(object):
            try:
                value = getattr(object, id)
                if hasattr(value, '__call__'):
                    result.append((id, format_value(value, form_id, path, id)))
            except:
                pass
        result.sort(self.sort_by_first_value)
        return result

    def scan_sequence_items(self, form_id, path, object):
        try:
            result = []
            if len(object):
                format_value = self.format_value
                for id in range(len(object)):
                    try:
                        result.append((id, '%s' % format_value(object[id], form_id, path, id)))
                    except:
                        result.append((id, '<em>n/a</em>'))
            return result
        except:
            return []

    def scan_mapping_items(self, form_id, path, object):
        try:
            result = []
            format_value = self.format_value
            keys = object.keys()
            keys.sort()
            for id in keys:
                try:
                    result.append((id, '%s' % format_value(object.get(id, None), form_id, path, id)))
                except:
                    result.append((id, '<em>n/a</em>'))
            return result
        except:
            return []

    def scan_attr_dict(self, form_id, path, object):
        try:
            result = []
            format_value = self.format_value
            for id in object.__dict__.keys():
                try:
                    result.append((id, format_value(getattr(object, id), form_id, path, id)))
                except:
                    result.append((id, '<em>n/a</em>'))
            result.sort(self.sort_by_first_value)
            return result
        except:
            return []

    def scan_attr_dir(self, form_id, path, object):
        result = []
        format_value = self.format_value
        for id in dir(object):
            try:
                result.append((id, format_value(getattr(object, id), form_id, path, id)))
            except:
                result.append((id, '<em>n/a</em>'))
        result.sort(self.sort_by_first_value)
        return result

    def get_attr_dir_jumps(self, form_id, object):
        result = []
        ids = dir(object)
        ids.sort()
        for index in range(0, len(ids), 25):
            result.append((ids[index], '%s - %s' % (ids[index], ids[min(len(ids) - 1, index + 24)])))
        return result
