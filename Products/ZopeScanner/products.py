"""ZopeScanner - ProductScanner."""


from Products.ZopeScanner.imports_zope import DTMLFile

from Products.ZopeScanner.shared import get_object_from_path
from Products.ZopeScanner.shared import sort_by_key


class ProductScanner:
    """ProductScanner Mix-in Class."""

    scan_products_form = DTMLFile('resources/products', globals())

    scan_product_class_form = DTMLFile('resources/product_class', globals())

    def scan_products(self, path=''):
        """Scan products.

        Perform a scan starting with the list of installed Product and the list
        of registered Product base classes, traversing along the specified by
        path.
        """
        import Products

        breadcrumbs = [('scan_products_form', 'Products Scanner')]
        form_id = breadcrumbs[0][0]
        url_prefix = '%s/%s' % (self.scanner_url(), form_id)
        report = {
            'breadcrumbs': breadcrumbs,
            'form_id': form_id,
            'url_prefix': url_prefix,
        }

        path = path != '/' and path or ''

        base_classes = []
        base_class_instances = []
        packages = {}
        index = 0
        for base_class in Products.meta_types:
            name = base_class.get('name')
            product = base_class.get('product')
            packages[product] = packages.get(product, []) + [(name, index)]
            base_classes.append({
                'name': name,
                'product': product,
                'index': index,
            })
            base_class_instances.append(base_class.get('instance'))
            index = index + 1
        base_classes = sort_by_key(base_classes, 'name')

        report.update({
            'packages': packages,
            'base_classes': base_classes,
        })

        if '/' in path:
            report.update(self.scan_object(
                breadcrumbs, form_id, base_class_instances, path, url_prefix))
            return report

        elif path:
            parts, base_class = get_object_from_path(Products.meta_types, path)
            order_index = None
            order_map = {}
            meta_index = int(path)
            for order in range(len(base_classes)):
                order_map[order] = base_classes[order]
                if base_classes[order]['index'] == meta_index:
                    order_index = order
            report['base_class'] = {
                'index': meta_index,
                'prev': order_map[(order_index - 1) % len(base_classes)],
                'next': order_map[(order_index + 1) % len(base_classes)],
            }
            format_type_and_value = self.format_type_and_value
            for key, value, shall_format_type_and_value in [
                ('action', base_class.get('action', None), True),
                ('container_filter', base_class.get(
                    'container_filter', None), True),
                ('instance', base_class.get('instance', None), True),
                ('interfaces', base_class.get('interfaces', None), True),
                ('name', base_class.get('name', None), False),
                ('permission', base_class.get('permission', None), True),
                ('product', base_class.get('product', None), False),
                ('visibility', base_class.get('visibility', None), True),
            ]:
                report['base_class'][key] = (
                    shall_format_type_and_value and
                    format_type_and_value(value, form_id, None, None) or
                    value)
            breadcrumbs.append((meta_index, base_class.get('name', None)))
            report.update(self.scan_object(
                breadcrumbs, form_id, base_class_instances, path, url_prefix))

        return report
