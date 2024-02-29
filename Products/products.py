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

__doc__ = """ZopeScanner ProductScanner"""

__version__ = '$Revision: 1.3 $'[11:-2]


# =============================================================================
# Module Imports

from resources.imports import DTMLFile, Products


# =============================================================================
# ProductScanner Mix-in Class

class ProductScanner:
    """ProductScanner Mix-in Class"""

    scan_product_form = DTMLFile('products', globals())

    def scan_product(self, path=''):
        """Scan Products

        Perform a scan starting with the list of installed Product and the list
        of registered Product base classes, traversing along the specified by
        path.
        """

        breadcrumbs = [
            self.breadcrumbs_root,
            ('scan_product_form', 'Products')
            ]

        if path == '/':
            path = ''

        if path:
            return self.scan(breadcrumbs, Products.meta_types, path)

        installedproducts = {}
        for id in self.getPhysicalRoot().Control_Panel.Products.objectIds():
            installedproducts[id] = []
        for data in Products.meta_types:
            product_info = installedproducts.get(data['product'], [])
            product_info.append(data['name'])
            installedproducts[data['product']] = product_info
        installedproducts = installedproducts.items()
        installedproducts.sort()

        baseclasses = []
        basepath = '/Control_Panel/Products'
        format_value = self.format_value
        get_link_url = self.get_link_url
        meta_types = Products.meta_types
        index = 0
        for value in meta_types:
            key = value.get('name', None)
            if key:
                name = '<a href="%s">%s</a>' % (
                    get_link_url('scan_product_form', '', str(index)),
                    key
                    )
            else:
                name = '<em>n/a</em>'
            product = value.get('product', None)
            if product:
                product_info = '<a href="%s">%s</a>' % (
                    get_link_url('scan_object_form', '/Control_Panel/Products',
                                 product),
                    product
                    )
            else:
                product_info = '<em>n/a</em>'
            baseclasses.append({
                'action': value.get('action', '<em>n/a</em>'),
                'container_filter': format_value(
                    value.get('container_filter', None),
                    'scan_product_form', '/%s' % index,
                    'container_filter'
                    ),
                'instance': format_value(
                    value.get('instance', None),
                    'scan_product_form',
                    '/%s' % index,
                    'instance'
                    ),
                'interfaces': format_value(
                    value.get('interfaces', None),
                    'scan_product_form',
                    '/%s' % index,
                    'interfaces'
                    ),
                'key': key,
                'name': name,
                'permission': value.get('permission', '<em>n/a</em>'),
                'product': product_info,
                'visibility': format_value(
                    value.get('visibility', None),
                    'scan_product_form',
                    '/%s' % index,
                    'visibility'
                    ),
                })
            index = index + 1

        def sort_baseclasses(x, y):
            return cmp(x['key'], y['key'])

        baseclasses.sort(sort_baseclasses)

        return {
            'breadcrumbs': breadcrumbs,
            'installedproducts': installedproducts,
            'baseclasses': baseclasses,
            }
