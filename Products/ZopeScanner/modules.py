"""Zope Scanner - ModuleScanner."""


from Products.ZopeScanner.imports_python import environ
from Products.ZopeScanner.imports_python import exists
from Products.ZopeScanner.imports_python import join
from Products.ZopeScanner.imports_python import modules
from Products.ZopeScanner.imports_python import splitext

from Products.ZopeScanner.imports_zope import DTMLFile


INSTANCE_HOME = environ.get('INSTANCE_HOME')
SOFTWARE_HOME = environ.get('SOFTWARE_HOME')
ZOPE_HOME = environ.get('ZOPE_HOME')


# =============================================================================
# ModuleScanner Mix-in Class


class ModuleScanner:
    """ModuleScanner Mix-in Class."""

    scan_modules_form = DTMLFile('resources/modules', globals())

    def scan_modules(self, path=''):
        """Scan Modules.

        Perform a scan starting with the list of known Python modules,
        traversing along the specified by path.
        """
        breadcrumbs = [('scan_modules_form', 'Module Scanner')]
        form_id = breadcrumbs[0][0]
        url_prefix = '%s/%s' % (self.scanner_url(), form_id)
        report = {
            'breadcrumbs': breadcrumbs,
            'form_id': form_id,
            'url_prefix': url_prefix,
        }

        path = path != '/' and path or ''

        # identify all modules with their respective packages
        module_records = {}  # information about each module
        module_packages = {}  # modules' top most parents
        module_instances = {}  # required for path traversal
        module_names = list(modules.keys())
        module_names.sort()
        for name in list(module_names):

            module_filename = None
            try:
                module = modules[name]
                module_filename = module.__file__
            except Exception:  # TODO: review Exception
                module_filename = None
            if not module_filename:
                module_names.remove(name)
                continue

            filename_base = splitext(module_filename)[0]
            source_filename = None
            for extension in ['.py', '.c']:
                if exists(join(filename_base + extension)):
                    source_filename = join(filename_base + extension)
                    break

            package = str(name).split('.')[0]
            module_packages[package] = module_packages.get(
                package, []) + [name]
            module_records[name] = {
                'package': package,
                'name': name,
                'module_filename': module_filename,
                'source_filename': source_filename,
            }
            module_instances[name] = modules.get(name)

        # update report
        report['modules'] = module_packages.items()

        if '/' in path:
            module_name = path.split('/')[0]
            breadcrumbs.append((
                '%s?path=%s' % (form_id, module_name),
                module_name))
            report.update(self.scan_object(
                breadcrumbs, form_id, module_instances, path, url_prefix))
            return report

        elif path:
            index = module_names.index(path)
            module = modules.get(path)

            # update report with module record
            module_record = module_records[path]
            report['module'] = {}
            report['module'].update(module_record)

            # update report with navigation hints
            report['module'].update({
                'prev': module_names[(index - 1) % len(module_names)],
                'next': module_names[(index + 1) % len(module_names)],
                'module': module,
                'docstring': module and module.__doc__,
            })

            # update breadcrumbs
            breadcrumbs.append((
                '%s?path=%s' % (form_id, path), path))

            # update report with object scan
            report.update(self.scan_object(
                breadcrumbs, form_id, module_instances, path,
                url_prefix))

        return report
