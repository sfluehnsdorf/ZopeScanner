"""ZopeScanner - Zope Product."""


from Products.ZopeScanner.imports_zope import ApplicationManager
from Products.ZopeScanner.imports_zope import Implicit
from Products.ZopeScanner.imports_zope import Item

from Products.ZopeScanner.logs import LogScanner
from Products.ZopeScanner.modules import ModuleScanner
from Products.ZopeScanner.objects import ObjectScanner
from Products.ZopeScanner.products import ProductScanner
from Products.ZopeScanner.shared import Shared
from Products.ZopeScanner.sources import SourceScanner
from Products.ZopeScanner.system import SystemScanner
from Products.ZopeScanner.values import ValueScanner


class ZopeScanner(
    LogScanner, ModuleScanner, ObjectScanner, ProductScanner, SourceScanner,
    SystemScanner, ValueScanner, Shared, Item, Implicit
):
    """ZopeScanner Product Class.

    Bundles up all Scanner classes and provides identity, icons, and menu
    options for the ZMI (Zope Management Interface).

    The method locked_in_version() is needed for backwards compatability.
    """

    # identity
    id = 'ZopeScanner'
    name = 'ZopeScanner'
    title = 'ZopeScanner'
    meta_type = 'ZopeScanner'

    # icons for ZopeScanner in both major icon formats
    icon = 'misc_/ZopeScanner/ZopeScanner.png'
    zmi_icon = 'fas fa-microscope'

    # manage options menu items lead to the six scanners
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

        Needed for compatibility with Zope's former versioning system.
        Since Zope-2.0.0, until Zope-2.11.8.
        """
        return 0


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

    # TODO: install_ZopeScanner() add ZopeScanner to all manage_options
    # add ZopeScanner to manage_options of Control Panel's components. Each
    # component redefines the menu, could all be detected by iterating through
    # attributes of Control Panel and analzing their manage_options
    # individually, adding an adapted option if appropriate.
    options = list(ApplicationManager.manage_options)
    options.append({
        'label': 'ZopeScanner',
        'action': scanner.id + '/manage_workspace'})
    ApplicationManager.manage_options = tuple(options)

    # since Python-2.3.0
    try:
        import logging
        logging.getLogger('ZopeScanner').warn('ZopeScanner installed')
        # TODO: check how logging.getLogger().warn() can fail
    except ImportError:
        # since Zope-2.0.0, until Zope-2.5.0
        try:
            import zLOG
            zLOG.LOG('ZopeScanner', zLOG.WARNING, 'ZopeScanner installed')
            # TODO: check how zLOG.LOG() can fail
        # until Zope-1.10.4
        except ImportError:
            # no logfile is available so write to both stderr and stdout
            import sys
            sys.stderr.write('ZopeScanner installed\n')
            sys.stderr.flush()
            sys.stdout.write('ZopeScanner installed\n')
            sys.stdout.flush()
