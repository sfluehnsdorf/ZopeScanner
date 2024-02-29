# -*- coding: utf8 -*-
u"""ZopeScanner ModuleScanner.
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
"""

__doc__ = """ZopeScanner ModuleScanner"""

__version__ = '$Revision: 1.3 $'[11:-2]


# =============================================================================
# Imports

from resources.imports import exists, DTMLFile, INSTANCE_HOME, modules,\
    normpath, prefix, SOFTWARE_HOME, split, ZOPE_HOME


# =============================================================================
# ModuleScanner Mix-in Class

class ModuleScanner:
    """ModuleScanner Mix-in Class."""

    scan_module_form = DTMLFile('modules', globals())

    def scan_module(self, path=''):
        """Scan Modules.

        Perform a scan starting with the list of known Python modules,
        traversing along the specified by path.
        """
        breadcrumbs = [
            self.breadcrumbs_root,
            ('scan_module_form', 'Modules')
        ]

        if path == '/':
            path = ''

        if path:
            return self.scan(breadcrumbs, modules, path)

        result = {}
        result['breadcrumbs'] = breadcrumbs

        xerrors = {}  # TODO: check to see causes for exceptions...

        format_value = self.format_value
        keys = modules.keys()
        keys.sort()
        module_map = {}
        for key in keys:
            try:
                filename = modules.get(key, None).__file__

                def formatpath(filename):
                    parts = []
                    while split(filename)[0]:
                        parts.append(split(filename)[1])
                        filename = split(filename)[0]
                    parts.append(filename)
                    parts.reverse()
                    path = '/'.join(parts)
                    if path.endswith('pyc'):
                        return path[:-1]
                    return path

                if filename.startswith(INSTANCE_HOME):
                    filename = '<a href="scan_source_form?path=%s">%s</a>' % (
                        'instance/' + formatpath(
                            filename[len(INSTANCE_HOME) + 1:]),
                        filename
                    )
                elif filename.startswith(SOFTWARE_HOME):
                    filename = '<a href="scan_source_form?path=%s">%s</a>' % (
                        'software/' + formatpath(
                            filename[len(SOFTWARE_HOME) + 1:]),
                        filename
                    )
                elif filename.startswith(ZOPE_HOME):
                    filename = '<a href="scan_source_form?path=%s">%s</a>' % (
                        'zope/' + formatpath(filename[len(ZOPE_HOME) + 1:]),
                        filename
                    )
                else:
                    pythonhome = normpath('%s/lib/python%s' % (
                        prefix, version[:3]  # TODO: version does not exist???
                    ))
                    if not exists(pythonhome):
                        pythonhome = normpath('%s/Lib' % prefix)
                    if filename.startswith(pythonhome):
                        filename = (
                            '<a href="scan_source_form?path=%s">%s</a>' % (
                                'python/' + formatpath(
                                    filename[len(pythonhome) + 1:]),
                                filename
                            )
                        )

            except Exception, e:
                filename = '<em>%s</em><br>%s' % (e, e.__dict__)
                xerrors[key] = '<em>%s</em><br>%s' % (e, e.__dict__)
            root_module = str(key).split('.')[0]
            module_map[root_module] = module_map.get(root_module, []) + [(
                key,
                format_value(modules.get(key, None), breadcrumbs[0], '', key),
                filename
            )]
        module_map = {'x': map(lambda x: [x[0], x[1], ''], xerrors.items())}
        result['modules'] = module_map.items()

        return result
