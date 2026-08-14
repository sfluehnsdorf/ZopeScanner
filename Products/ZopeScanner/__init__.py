"""Zope Scanner."""


from Products.ZopeScanner.imports_zope import ImageFile

from Products.ZopeScanner.ZopeScanner import install_ZopeScanner


def initialize(context):
    """Initialize Product package."""
    install_ZopeScanner(context)


misc_ = {
    'ZopeScanner.png': ImageFile('resources/icon.png', globals()),
}
