"""Zope Scanner - ObjectScanner."""


from Products.ZopeScanner.imports_python import exc_info
from Products.ZopeScanner.imports_python import maxsize
from Products.ZopeScanner.imports_python import signature
from Products.ZopeScanner.imports_python import unpack

from Products.ZopeScanner.imports_zope import DTMLFile
from Products.ZopeScanner.imports_zope import Item
from Products.ZopeScanner.imports_zope import Permission
from Products.ZopeScanner.imports_zope import Prefix
from Products.ZopeScanner.imports_zope import UnownableOwner
from Products.ZopeScanner.imports_zope import aq_base
from Products.ZopeScanner.imports_zope import aq_inner
from Products.ZopeScanner.imports_zope import aq_parent
from Products.ZopeScanner.imports_zope import getSecurityManager
from Products.ZopeScanner.imports_zope import html_quote

from Products.ZopeScanner.shared import ObjectRetrievalError
from Products.ZopeScanner.shared import get_id_of_object
from Products.ZopeScanner.shared import get_object_from_path
from Products.ZopeScanner.shared import sort_by_key
from Products.ZopeScanner.shared import token_sort_by_key

from Products.ZopeScanner.values import format_datetime
from Products.ZopeScanner.values import format_filesize
from Products.ZopeScanner.values import guess_value_type


# =============================================================================
# ObjectScanner Mix-in Class


class ObjectScanner:
    """ObjectScanner Mix-in Class."""

    scan_objects_form = DTMLFile('resources/objects', globals())

    def scan_objects(self, path=''):
        """Scan objects.

        Perform a scan starting with the OFS' physical root object.
        """
        breadcrumbs = [('scan_objects_form', 'Object Scanner')]
        form_id = breadcrumbs[0][0]
        url_prefix = '%s/%s' % (self.scanner_url(), form_id)
        report = {
            'breadcrumbs': breadcrumbs,
            'form_id': form_id,
            'url_prefix': url_prefix,
        }

        path = path != '/' and path or ''

        report.update(self.scan_object(
            breadcrumbs, form_id, self.getPhysicalRoot(), path, url_prefix))
        return report

    # -------------------------------------------------------------------------
    # Public Interace

    object_form = DTMLFile('resources/object', globals())

    def scan_object(self, breadcrumbs, form_id, root_object, path, url_prefix):
        """Scan the specified object.

        form_id - identifies the scanner's form, e.g. of the SystemScanner
        breadcrumbs - list of steps of traversal
        root_object - the scanner's root object used for traversal
        path - the traversable path
        url_prefix - used for links for in forms
        """
        # TODO: scan_object() - revise context (breadcrumbs, form_id, etc.)
        # - current system with breadcrumbs, form_id, root_object, path, and
        #   url_prefix has redundancues and is error-prone
        # TODO: scan_object() - url_prefix - unused here?
        result = {}

        # retrieve object
        try:
            parents, specimen = get_object_from_path(root_object, path)
        except ObjectRetrievalError:
            exception = exc_info()[1]
            result.update({
                'exception': exception
            })
            parents = exception.parents
            specimen = None

        object_record = None
        if specimen:

            # scan generic object
            object_record = {
                'info': self._scan_object_info(
                    form_id, path, specimen),
                'callables': self._scan_object_callables(
                    form_id, path, specimen),
                'attributes': self._scan_object_attributes(
                    form_id, path, specimen),
                'sequence_items': self._scan_object_sequence_items(
                    form_id, path, specimen),
                'mapping_items': self._scan_object_mapping_items(
                    form_id, path, specimen),
            }

            # scan Zope OFS object
            if isinstance(specimen, Item):
                object_record.update({
                    'ofs_info': self._scan_object_ofs_info(
                        form_id, path, specimen),
                    'sub_objects': self._scan_object_sub_objects(
                        form_id, path, specimen),
                    'properties': self._scan_object_properties(
                        form_id, path, specimen),
                    'permissions': self._scan_object_permissions(
                        form_id, path, specimen),
                    'roles': self._scan_object_roles(
                        form_id, path, specimen),
                    'ownership': self._scan_object_ownership(
                        form_id, path, specimen),
                    'undoable': self._scan_object_undoable(
                        form_id, path, specimen),
                    'history': self._scan_object_history(
                        form_id, path, specimen),
                    'forms_images': self._scan_object_forms_images(
                        form_id, path, specimen),
                    'manage_options': self._scan_object_manage_options(
                        form_id, path, specimen),
                })

            # identify object
            object_type = (
                hasattr(specimen, '__class__') and
                specimen.__class__.__name__ or
                type(specimen).__name__)

            object_id = get_id_of_object(specimen)

            object_title = None
            if isinstance(specimen, Item):
                object_title = getattr(specimen, 'title', None)

            # update object record
            object_record.update({
                'path': path,
                'type': object_type,
                'id': object_id,
                'title': object_title,
            })

        # update breadcrumbs
        step_path = str(breadcrumbs[len(breadcrumbs) - 1][0])
        step_path = step_path + (
            '?path=' not in step_path and
            '?path=' or
            ''
        )
        for key, item in parents[len(breadcrumbs):]:
            step_path = '%s/%s' % (step_path, key)
            step_label = get_id_of_object(item) or key
            breadcrumbs.append((step_path, step_label))

        # update record
        result.update({
            'breadcrumbs': breadcrumbs,
            'object': object_record,
        })

        return result

    # -------------------------------------------------------------------------

    def _scan_object_info(self, form_id, path, specimen):
        """Return identifying information of specimen."""
        format_type_and_value = self.format_type_and_value
        result = []
        result.append(('repr', html_quote(repr(specimen))))
        result.append(('type_name', type(specimen).__name__))
        result.append(('type', format_type_and_value(
            type(specimen), form_id, None, None)))
        try:
            result.append(('name', format_type_and_value(
                specimen.__name__, form_id, path, '__name__')))
        except Exception:  # TODO: specify Exception
            pass
        try:
            result.append(('class', format_type_and_value(
                specimen.__class__, form_id, path, '__class__')))
        except Exception:  # TODO: specify Exception
            pass
        try:
            module_name = specimen.__module__
            result.append(('module', (
                '<a href="%s/scan_modules_form?path=%s">%s</a>' % (
                    self.scanner_url(), module_name, module_name))))
        except Exception:  # TODO: specify Exception
            pass
        try:
            result.append(('doc', format_type_and_value(
                specimen.__doc__, form_id, path, '__doc__')))
        except Exception:  # TODO: specify Exception
            pass
        try:
            result.append(('file', format_type_and_value(
                specimen.__module__.__file__, form_id, path, '__file__')))
        except Exception:  # TODO: specify Exception
            pass
        return result

    def _scan_object_callables(self, form_id, path, specimen):
        """Return list of callables of specimen."""
        result = []
        for key in dir(specimen):
            try:
                value = getattr(specimen, key, None)
            except Exception:  # TODO: review Exception
                pass
            if (
                # callable(value) or
                (callable(value) and getattr(value, '__func__', None)) or
                guess_value_type(value)['type'] == 'callable'
            ):
                doc_string = getattr(value, '__doc__', None)
                doc_string = doc_string and doc_string.strip()
                callable_args = None
                callable_return = None
                if signature:
                    try:
                        # callable_args = str(signature(value.__func__))
                        callable_signature = signature(value.__func__)
                        callable_args = str(callable_signature)
                        callable_return = (
                            (
                                callable_signature.return_annotation is not
                                callable_signature.empty
                            ) and
                            str(callable_signature.return_annotation) or
                            None)
                    except Exception:
                        pass
                result.append({
                    'name': key,
                    'args': callable_args,
                    'returns': callable_return,
                    'doc_string': doc_string,
                })
        result = token_sort_by_key(result, 'name')
        return result

    def _scan_object_attributes(self, form_id, path, specimen):
        """Return list of attributes of specimen."""
        result = []
        instance_attribute_keys = []
        if hasattr(specimen, '__dict__'):
            instance_attribute_keys = specimen.__dict__.keys()
        format_type_and_value = self.format_type_and_value
        for key in dir(specimen):
            if not hasattr(specimen, key):
                continue  # TODO: _scan_object_attributes() - handle missing
                # what's going on here? name was provided by dir(), maybe
                # happening with C-classes?
            value = getattr(specimen, key)
            attr_type = guess_value_type(value)
            formatted_value = format_type_and_value(value, form_id, path, key)
            result.append({
                'name': key,
                'instance_attr': (
                    key in instance_attribute_keys and
                    '__dict__' or
                    None),
                'type': attr_type['name'],
                'value': formatted_value,
            })
        result = token_sort_by_key(result, 'name')
        return result

    def _scan_object_sequence_items(self, form_id, path, specimen):
        """Return sequenced items of specimen."""
        result = []
        try:
            if guess_value_type(specimen)[0] != 'sequence':
                raise TypeError('not a sequence')
            format_type_and_value = self.format_type_and_value
            for index in range(len(specimen)):
                try:
                    result.append((index, format_type_and_value(
                        specimen[index], form_id, path, index)))
                except Exception:  # TODO: review Exception
                    pass
        except Exception:  # TODO: review Exception
            pass
        return result

    def _scan_object_mapping_items(self, form_id, path, specimen):
        """Return mapped items of specimen."""
        result = []
        try:
            if hasattr(specimen, 'keys'):
                format_type_and_value = self.format_type_and_value
                for key in specimen.keys():
                    result.append((key, format_type_and_value(
                        specimen.get(key, None), form_id, path, key)))
        except Exception:  # TODO: review Exception
            pass
        result = sort_by_key(result, 0)
        return result

    # -------------------------------------------------------------------------

    def _scan_object_ofs_info(self, form_id, path, specimen):
        """Return identifying information of OFS object."""
        result = []
        format_type_and_value = self.format_type_and_value
        try:
            result.append(('id', format_type_and_value(
                specimen.id, form_id, path, 'id')))
        except Exception:  # TODO: review Exception
            pass
        try:
            result.append(('id_func', format_type_and_value(
                specimen.id(), form_id, path, 'id')))
        except Exception:  # TODO: review Exception
            pass
        try:
            result.append(('getId', format_type_and_value(
                specimen.getId(), form_id, path, 'getId')))
        except Exception:  # TODO: review Exception
            pass
        try:
            result.append(('title', format_type_and_value(
                specimen.title, form_id, path, 'title')))
        except Exception:  # TODO: review Exception
            pass
        try:
            result.append(('title_and_id', format_type_and_value(
                specimen.title_and_id(), form_id, path, 'title_and_id')))
        except Exception:  # TODO: review Exception
            pass
        try:
            result.append(('title_or_id', format_type_and_value(
                specimen.title_or_id(), form_id, path, 'title_or_id')))
        except Exception:  # TODO: review Exception
            pass
        try:
            result.append(('meta_type', format_type_and_value(
                specimen.meta_type, form_id, path, 'meta_type')))
        except Exception:  # TODO: review Exception
            pass
        try:
            result.append(('icon', format_type_and_value(
                specimen.icon, form_id, path, 'icon',
                force_format='zope_icon_icon')))
        except Exception:  # TODO: review Exception
            pass
        try:
            result.append(('om_icons', format_type_and_value(
                specimen.om_icons, form_id, path, 'om_icons',
                force_format='zope_icon_om_icons')))
        except Exception:  # TODO: review Exception
            pass
        try:
            result.append(('zmi_icon', format_type_and_value(
                specimen.zmi_icon, form_id, path, 'zmi_icon',
                force_format='zope_icon_zmi_icon')))
        except Exception:  # TODO: review Exception
            pass
        try:
            result.append(('absolute_url', format_type_and_value(
                specimen.absolute_url(), form_id, path, 'absolute_url')))
        except Exception:  # TODO: review Exception
            pass
        # TODO: _scan_object_ofs_info() - absolute_url() as breadcrumbs
        # - split on / starting with server root's absolute_url
        return result

    def _scan_object_sub_objects(self, form_id, path, specimen):
        """Return contained OFS objects of OFS container object."""
        result = []
        root_url = self.getPhysicalRoot().absolute_url()
        for object_id, ofs_object in specimen.objectItems():

            # since Zope-4.0.0
            zmi_icon = getattr(ofs_object, 'zmi_icon', None)
            zmi_icon_formatted = (
                zmi_icon and
                '<i class="%s"></i>' % zmi_icon or
                '')

            # since Zope-2.5.0, until Zope-2.13.30
            om_icons = getattr(ofs_object, 'om_icons', None)
            om_icons_formatted = ''
            if om_icons:
                for om_icon in om_icons():
                    om_icons_formatted = om_icons_formatted + (
                        '<img src="%s/%s">' % (root_url, om_icon['path']))

            # until Zope-2.13.30
            icon = getattr(ofs_object, 'icon', None)
            icon_formatted = (
                icon and
                '<img src="%s/%s">' % (root_url, icon) or
                '')

            size = (
                hasattr(aq_base(ofs_object), 'get_size') and
                ofs_object.get_size() or
                None
            )

            modified = getattr(ofs_object, '_p_mtime', None)

            # since Zope-2.4.0
            lock = None
            if hasattr(ofs_object, 'wl_isLocked'):
                lock = ofs_object.wl_isLocked() and True or False

            result.append({
                'id': object_id,
                'title': ofs_object.title,
                'lock': lock,
                'zmi_icon': zmi_icon,
                'zmi_icon_formatted': zmi_icon_formatted,
                'om_icons': om_icons,
                'om_icons_formatted': om_icons_formatted,
                'icon': icon,
                'icon_formatted': icon_formatted,
                'meta_type': ofs_object.meta_type,
                'size': size or '',
                'size_formatted': size and format_filesize(size) or '',
                'modified': modified and format_datetime(ts=modified) or '',
                # TODO: _scan_object_sub_objects() - position in OrderedFolder
            })

        result = sort_by_key(result, 'id')
        return result

    def _scan_object_properties(self, form_id, path, specimen):
        """Return Properties (custom attributes) of OFS object."""
        result = []
        zope_properties = []
        try:
            for item in specimen._properties:
                zope_properties.append((item['id'], item))
        except Exception:  # TODO: review Exception
            return None
        for key, item in zope_properties:
            result.append({
                'id': key,
                'title': item.get('title', None),
                'type': item.get('type', None),
                'mode': item.get('mode', None),
                'options': '',
                # TODO: _scan_object_properties() - property's options
                # - select_variable, etc.
            })
        result = sort_by_key(result, 'id')
        return result

    def _scan_object_permissions(self, form_id, path, specimen):
        """Return local and acquired permissions of OFS object."""
        result = {}
        try:
            result['valid_roles'] = specimen.valid_roles()
            permissions = []
            for item in specimen.ac_inherited_permissions(1):
                name, value = item[: 2]
                permission_object = Permission(name, value, specimen)
                permission_roles = permission_object.getRoles(default=[])
                if isinstance(permission_roles, list):
                    acquired = True
                    # TODO: _scan_object_permissions() - get acquired roles
                    roles = []
                else:
                    acquired = False
                    roles = permission_roles
                permissions.append({
                    'name': name,
                    'acquired': acquired,
                    'roles': roles,
                })
            result['permissions'] = permissions
            return result
        except Exception:  # TODO: review Exception
            return None

    def _scan_object_roles(self, form_id, path, specimen):
        """Return local and acquired roles of OFS object."""
        result = []
        try:
            permission_map = {}
            for permission in specimen.ac_inherited_permissions(1):
                name, value = permission[: 2]
                permission_object = Permission(name, value, specimen)
                permission_roles = permission_object.getRoles(default=[])
                if isinstance(permission_roles, list):
                    permission_map[name] = None
                else:
                    permission_map[name] = permission_roles
            for valid_role in specimen.valid_roles():
                permissions = []
                acquired_permissions = []
                assigned_permissions = []
                unassigned_permissions = []
                for key in permission_map.keys():
                    if permission_map[key] is None:
                        # TODO: _scan_object_roles() get_acquired_permission
                        # permissions.append((key, 'allow_acq'))
                        permissions.append((key, 'deny_acq'))
                    elif valid_role in permission_map[key]:
                        permissions.append((key, 'allow'))
                    else:
                        permissions.append((key, 'deny'))
                acquired_permissions.sort()
                assigned_permissions.sort()
                unassigned_permissions.sort()
                result.append({
                    'role': valid_role,
                    'permissions': permissions,
                })
            return result
        except Exception:  # TODO: review Exception
            return None

    def _scan_object_ownership(self, form_id, path, specimen):
        """Return ownership information of OFS object."""
        result = []
        if hasattr(specimen, 'getOwnerTuple'):
            owner = specimen.getOwnerTuple()
            format_type_and_value = self.format_type_and_value
            if owner is None:
                result.append(('owner', format_type_and_value(
                    None, form_id, None, None)))
            elif owner is UnownableOwner:
                result.append((
                    'owner', '<em>Unownable</em>'))
            else:
                result = []
                result.append(('owner', format_type_and_value(
                    owner[1], form_id, None, None)))
                result.append(('path to UserFolder', format_type_and_value(
                    '/' + '/'.join(owner[0]), form_id, None, None)))
                result.append(('explicitly owned', format_type_and_value(
                    hasattr(specimen, '_owner'), form_id, None, None)))
                result.append((
                    'user can change ownership type',
                    format_type_and_value(
                        getSecurityManager().checkPermission(
                            'Take ownership', specimen),
                        form_id, None, None)))
        return result

    def _scan_object_undoable(self, form_id, path, specimen):
        """Return list of undoable transactions (object changes).

        Undo reverts the state of the ZODB to an earlier transation, which can
        have an unexpected side effects. It should be used sparingly, ideally
        only ever in a development environment.
        """
        result = []
        if Prefix:
            specifications = {'user_name': Prefix and Prefix('') or None}
            if (
                getattr(aq_parent(aq_inner(specimen)), '_p_jar', None) ==
                specimen._p_jar
            ):
                opath = '/'.join(specimen.getPhysicalPath())
                if opath:
                    specifications['description'] = Prefix(opath)
            transactions = specimen._p_jar.db().undoInfo(
                0, maxsize, specifications)
            format_type_and_value = self.format_type_and_value
            for transaction in transactions:
                size = transaction.get('size')
                result.append({
                    'datetime': format_datetime(ts=transaction['time']),
                    'id': format_type_and_value(
                        transaction['id'], form_id, None, None),
                    'description': format_type_and_value(
                        transaction['description'], form_id, None, None),
                    'username': format_type_and_value(
                        transaction['user_name'], form_id, None, None),
                    'size': size or '',
                    'size_formatted': size and format_filesize(size) or '',
                })
        result = sort_by_key(result, 'datetime')
        return result

    def _scan_object_history(self, form_id, path, specimen):
        """Return list of historical revisions (content changes) of OFS object.

        Historical revisions allow reviewing chanes done to the content of an
        object for which the ZMI provides a diff-style comparison.
        """
        result = []
        try:
            # TODO: _scan_object_history() - fix
            revisions = specimen._p_jar.db().history(
                specimen._p_oid, None, maxsize)
            if revisions:
                format_type_and_value = self.format_type_and_value
                for revision in revisions:
                    serial = '.'.join(map(str, unpack(">HHHH", revision.get(
                        'serial', revision.get('tid')))))
                    result.append({
                        'datetime': format_datetime(ts=revision['time']),
                        'serial': serial,
                        'revision': html_quote(repr(revision)),
                        'f_revision': format_type_and_value(
                            revision, form_id, None, None),
                    })
            else:
                pass  # TODO: _scan_object_history() review
                # - comment was "history not supported"
        except Exception:  # TODO: review Exception
            pass
        result = sort_by_key(result, 'serial')
        return result

    def _scan_object_manage_options(self, form_id, path, specimen):
        """Return list of management options (ZMI menu options) of OFS object.

        Supports the MutliTabs Product, which is patch for hierarchical ZMI
        menus.
        """

        def iterate_manage_options(options, prefix=''):
            result = []
            for index in range(len(options)):
                option = options[index]
                number = '%s%s' % (prefix, index + 1)
                result.append({
                    'number': number,
                    'action': option.get('action', None),
                    'label': option.get('label', None),
                })
                if 'sub' in option:
                    result.extend(iterate_manage_options(
                        option['sub'], number + '.'))
            return result

        result = []
        try:
            result.extend(iterate_manage_options(specimen.manage_options))
        except Exception:  # TODO: review Exception
            pass
        return result

    def _scan_object_forms_images(self, form_id, path, specimen):
        """Return list of forms and images of the ZMI and/or public UI."""
        result = []
        format_type_and_value = self.format_type_and_value
        for key in dir(specimen):
            try:
                value = getattr(specimen, key, None)
            except Exception:  # TODO: review Exception
                pass
            if value:
                value_type = guess_value_type(value)
                if value_type['category'] in ['zope_form', 'zope_image']:
                    result.append({
                        'name': key,
                        'type': value_type['name'],
                        'value': format_type_and_value(
                            value, form_id, path, key, value_type=value_type),
                    })
        return result
