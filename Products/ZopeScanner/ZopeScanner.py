"""ZopeScanner."""


from Products.ZopeScanner.imports_zope import ApplicationManager
from Products.ZopeScanner.imports_zope import DTMLFile
from Products.ZopeScanner.imports_zope import Implicit
from Products.ZopeScanner.imports_zope import Item

from Products.ZopeScanner.logs import LogScanner
from Products.ZopeScanner.modules import ModuleScanner
from Products.ZopeScanner.objects import ObjectScanner
from Products.ZopeScanner.products import ProductScanner
from Products.ZopeScanner.sources import SourceScanner
from Products.ZopeScanner.system import SystemScanner
from Products.ZopeScanner.values import ValueScanner


class ZopeScanner(
    LogScanner, ModuleScanner, ObjectScanner, ProductScanner, SourceScanner,
    SystemScanner, ValueScanner, Item, Implicit
):
    """ZopeScanner Product Class."""

    id = 'ZopeScanner'
    name = 'ZopeScanner'
    title = 'ZopeScanner'
    meta_type = 'ZopeScanner'

    icon = 'misc_/ZopeScanner/ZopeScanner.png'
    zmi_icon = 'fas fa-microscope'

    manage_options = (
        {'label': 'System', 'action': 'scan_system_form'},
        {'label': 'Products', 'action': 'scan_products_form'},
        {'label': 'Objects', 'action': 'scan_objects_form'},
        {'label': 'Modules', 'action': 'scan_modules_form'},
        {'label': 'Sources', 'action': 'scan_sources_form'},
        {'label': 'Log Files', 'action': 'scan_logfiles_form'},
    )

    def locked_in_version(self):
        """Return 1 (True) if this instance was modified in any version.

        Needed for compatibility with Zope's legacy versioning system.
        Since Zope-2.0.0, until Zope-2.11.8.
        """
        return 0

    def scanner_url(self):
        """Return this instance's absolute URL."""
        return self.absolute_url()

    scanner_css = DTMLFile('resources/css', globals())

    scanner_js = DTMLFile('resources/js', globals())

    def scanner_unicode(self, REQUEST):
        """Force encoding of the response to Unicode."""
        REQUEST.RESPONSE.setHeader('Content-Type', 'text/html;charset=UTF8')
        try:
            return unicode('')
        except NameError:
            return ''

    breadcrumbs_html = DTMLFile('resources/breadcrumbs', globals())


def install_ZopeScanner(context):
    """Install ZopeScanner.

    Create a new instance of the ZopeScanner and add it to the Control Panel of
    the Zope server. This way there can only be exactly one instance of
    ZopeScanner on a Zope server. Also, there is a test if the server is
    configured to run in development mode to avoid this Product to be installed
    on a production server.
    """
    scanner = ZopeScanner()
    setattr(ApplicationManager, scanner.id, scanner)
    try:
        objects = list(ApplicationManager._objects)
        objects.append({'id': scanner.id, 'meta_type': scanner.meta_type})
        ApplicationManager._objects = tuple(objects)
    except AttributeError:
        pass
    options = list(ApplicationManager.manage_options)
    options.append({
        'label': 'ZopeScanner',
        'action': scanner.id + '/manage_workspace'})
    ApplicationManager.manage_options = tuple(options)
