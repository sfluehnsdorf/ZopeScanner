"""ZopeScanner - ProductScanner."""


from Products.ZopeScanner.imports_zope import DTMLFile

from Products.ZopeScanner.shared import get_object_from_path
from Products.ZopeScanner.shared import sort_by_key


# =============================================================================
# ProductScanner Mix-in Class


class ProductScanner:
    """ProductScanner Mix-in Class."""

    scan_products_form = DTMLFile('resources/products', globals())

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

        # iterate over base classes and identify packages
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

        # update report
        report.update({
            'packages': packages,
            'base_classes': base_classes,
        })

        if '/' in path:
            report.update(self.scan_object(
                breadcrumbs, form_id, base_class_instances, path, url_prefix))
            return report

        # base class view
        elif path:
            parts, base_class = get_object_from_path(Products.meta_types, path)
            report['base_class'] = {}
            report['base_class'].update(base_class)

            # determine order and provide navigation hints
            order_index = None
            order_map = {}
            meta_index = int(path)
            for order in range(len(base_classes)):
                order_map[order] = base_classes[order]
                if base_classes[order]['index'] == meta_index:
                    order_index = order
            report['base_class'].update({
                'index': meta_index,
                'prev': order_map[(order_index - 1) % len(base_classes)],
                'next': order_map[(order_index + 1) % len(base_classes)],
            })

            # update report with base class information
            format_type_and_value = self.format_type_and_value
            report['base_class'].update({
                'action': format_type_and_value(
                    base_class.get('action'), form_id, None, None),
                'container_filter': format_type_and_value(
                    base_class.get('container_filter'), form_id, None, None),
                'instance': format_type_and_value(
                    base_class.get('instance'), form_id, None, None),
                'interfaces': format_type_and_value(
                    base_class.get('interfaces'), form_id, None, None),
                'name': base_class.get('name', None),
                'permission': format_type_and_value(
                    base_class.get('permission'), form_id, None, None),
                'product': base_class.get('product', None),
                'visibility': format_type_and_value(
                    base_class.get('visibility'), form_id, None, None),
            })

            # update breadcrumbs
            breadcrumbs.append((meta_index, base_class.get('name', None)))

            # update report with object report
            report.update(self.scan_object(
                breadcrumbs, form_id, base_class_instances, path, url_prefix))

        return report
