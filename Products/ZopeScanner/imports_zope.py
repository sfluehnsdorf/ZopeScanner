"""Zope Scanner - Zope Imports.

All imports from Zope are centralized in this module. As any change to the API
requires adaptation, this is where any workaround is done.

Every symbol imported as on their own line intentionally. As the syntax for
importing between the different major releases of Python varies substantially,
this is the only format that is human readable and style guide complaint.
"""


__all__ = [
    'ApplicationManager',
    'DTMLFile',
    'DateTime',
    'HTML',
    'HTMLFile',
    'ImageFile',
    'Implicit',
    'Item',
    'MinimalLogger',
    'PageTemplate',
    'PageTemplateFile',
    'Permission',
    'Prefix',
    'UnownableOwner',
    'aq_base',
    'aq_inner',
    'aq_parent',
    'getConfiguration',
    'getSecurityManager',
    'getZopeVersion',
    'html_quote',
]


from AccessControl.Owned import UnownableOwner
from AccessControl.Permission import Permission
from AccessControl.SecurityManagement import getSecurityManager
from Acquisition import Implicit
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from App.ApplicationManager import ApplicationManager
from App.ImageFile import ImageFile
from App.special_dtml import DTMLFile
from App.version_txt import getZopeVersion
from DateTime import DateTime
from DocumentTemplate.html_quote import html_quote
from DocumentTemplate.DT_HTML import HTML
from DocumentTemplate.DT_HTML import HTMLFile
from OFS.SimpleItem import Item

try:  # App.config.getConfiguration - since Zope-2.7.0
    from App.config import getConfiguration
except ImportError:
    getConfiguration = None

try:  # since Zope-2.5.0
    from Products.PageTemplates.PageTemplate import PageTemplate
    from Products.PageTemplates.PageTemplateFile import \
        PageTemplateFile
except ImportError:
    PageTemplate = None
    PageTemplateFile = None

try:  # opeUndo.Prefix.Prefix - since Zope-2.6.1
    from ZopeUndo.Prefix import Prefix
except ImportError:
    Prefix = None

try:  # zLOG.MinimalLogger - since Zope-2.0.0, until Zope-2.5.0
    from zLOG import MinimalLogger
except ImportError:
    MinimalLogger = None
