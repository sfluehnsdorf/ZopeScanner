"""Zope Scanner - ValueScanner."""


from Products.ZopeScanner.imports_python import gmtime
from Products.ZopeScanner.imports_python import strftime

from Products.ZopeScanner.imports_zope import DTMLFile
from Products.ZopeScanner.imports_zope import HTML
from Products.ZopeScanner.imports_zope import HTMLFile
from Products.ZopeScanner.imports_zope import ImageFile
from Products.ZopeScanner.imports_zope import Item
from Products.ZopeScanner.imports_zope import PageTemplate
from Products.ZopeScanner.imports_zope import PageTemplateFile
from Products.ZopeScanner.imports_zope import html_quote


__all__ = [
    'format_datetime',
    'format_duration',
    'format_filesize',
    'guess_value_type',
]


# =============================================================================
# Generic Formatters


def format_datetime(ts=None, zdt=None):
    """Convert date and time to UTC timezone and format human readable."""
    if ts:
        return strftime('%Y-%m-%d %H:%M:%S', gmtime(ts))
    elif zdt:
        return zdt.utcdatetime().ISO()


def format_duration(seconds):
    """Format a duration in human readable format."""
    result = []
    days = int(seconds / 86400)
    seconds = seconds - (days * 86400)
    hours = int(seconds / 3600)
    seconds = seconds - (hours * 3600)
    minutes = int(seconds / 60)
    seconds = seconds - (minutes * 60)
    if days:
        result.append('%d day%s' % (days, days != 1 and 's' or ''))
    if hours:
        result.append('%d hour%s' % (hours, hours != 1 and 's' or ''))
    if minutes:
        result.append(
            '%d minute%s' % (minutes, minutes != 1 and 's' or ''))
    if seconds:
        result.append(
            '%d second%s' % (seconds, seconds != 1 and 's' or ''))
    return ', '.join(result)


def format_filesize(size):
    """Format a filesize in human readable format."""
    if size >= 1073741824:
        return '%.1f GB' % (size / 1073741824.0)
    if size >= 1048576:
        return '%.1f MB' % (size / 1048576.0)
    if size >= 1024:
        return '%.1f KB' % (size / 1024.0)
    if size >= 1024:
        return '%d KB' % size
    return '%d B' % size


# =============================================================================
# Value Types


# TODO: values.py - finish value type lists
# - see https://docs.python.org/2.7/reference/datamodel.html#types
# - see https://docs.python.org/2.7/library/stdtypes.html#other-built-in-types
# - ... so much more! need to review all Python versions? maybe be smarter?


zope_form_types = (
    DTMLFile,
    HTML,
    HTMLFile,
)

if PageTemplate and PageTemplateFile:
    zope_form_types = zope_form_types + (
        PageTemplate,
        PageTemplateFile,
    )


zope_image_types = (
    ImageFile,
)


mapping_types = (
    dict,
)


sequence_types = (
    list,
    tuple,
)


string_types = (
    str,
)

try:  # only Python-2.x.x
    _string_types = _string_types + (unicode,)  # noqa F821
except NameError:
    pass

try:  # since Python-3.0.0
    _string_types = _string_types + (bytes,)  # noqa F821
except NameError:
    pass


number_types = (
    int,
    float,
    complex,
)

try:  # until Python-3.0.0
    _number_types = _number_types + (long,)  # noqa F821
except NameError:
    pass


def guess_value_type(value):
    """Analyze a value and return category and type."""
    result = {
        'category': 'object',
        'type': type(value),
        'type_name': type(value).__name__,
    }
    try:
        result['class'] = value.__class__
    except Exception:  # TODO: review Exception
        pass
    try:
        result['class_name'] = str(value.__class__.__name__)
    except Exception:  # TODO: review Exception
        pass
    result['name'] = result.get('class_name', result['type_name'])

    if isinstance(value, zope_form_types):
        result['category'] = 'zope_form'
    elif isinstance(value, zope_image_types):
        result['category'] = 'zope_image'
    elif isinstance(value, Item):
        result['category'] = 'zope_ofs'
        result['type_name'] = str(value.meta_type)

    elif isinstance(value, mapping_types):
        result['category'] = 'mapping'
    elif isinstance(value, sequence_types):
        result['category'] = 'sequence'
    elif isinstance(value, string_types):
        result['category'] = 'string'
    elif isinstance(value, number_types):
        result['category'] = 'number'

    elif isinstance(value, type(bool)):
        result['category'] = 'boolean'
    elif value is None:
        result['category'] = 'none'

    return result


# =============================================================================
# Value Formatting


class ValueScanner:
    """ValueScanner Mix-in Class."""

    def format_type_and_value(
        self, value, form_id, path, object_id, force_format=None,
        value_type=None, css_class=None
    ):
        """Format type and value for safe inclusion in HTML.

        The type of value and the format to use are determined automatically by
        default but may be overriden. Custom CSS classes may be specified,
        which will be included to the formatted output.
        """
        type_name = None
        formatted_value = None

        if value_type is None:
            value_type = guess_value_type(value)

        use_format = force_format or value_type['category']

        def format_object(value, form_id, path, object_id):
            """Format an object."""
            formatted_value = html_quote(repr(value))
            if path is not None and object_id is not None:
                formatted_value = '<a href="%s/%s?path=%s/%s">%s</a>' % (
                    self.scanner_url(), form_id, path, object_id,
                    formatted_value)
            return formatted_value

            # since , until Zope-2.13.30
        def format_icon(value, use_format):
            """Format a Zope icon according to specified format."""
            # since Zope-4.0.0
            if use_format == 'zope_icon_zmi_icon':
                return (
                    '<span class="icon"><i class="%s"></i></span>' % value)

            # since Zope-2.5.0, until Zope-2.13.30
            elif use_format == 'zope_icon_om_icons':
                formatted_value = ''
                for item in value:
                    formatted_value = formatted_value + (
                        '<span class="icon"><img src="%s"></span>' % value)
                return formatted_value

            # until Zope-2.13.30
            elif use_format == 'zope_icon_icon':
                return (
                    '<span class="icon"><img src="%s"></span>' % value)

        def format_icon_of_object(value):
            """Identify the type of Zope icon and format accordingly."""
            if hasattr(value, 'zmi_icon'):
                return format_icon(value.zmi_icon, 'zope_icon_zmi_icon')
            elif hasattr(value, 'om_icons'):
                return format_icon(value.om_icons(), 'zope_icon_om_icons')
            elif hasattr(value, 'icon'):
                return format_icon(value.icon, 'zope_icon_icon')

        # Zope icons
        if use_format.startswith('zope_icon_'):
            type_name = 'icon'
            formatted_value = '%s %s' % (
                format_icon(value, use_format),
                '<code>%s</code>' % html_quote(repr(value)),
            )

        # Zope web forms
        elif use_format == 'zope_form':
            type_name = 'form'
            # TODO: format_type_and_value - zope_form
            formatted_value = format_object(value, form_id, path, object_id)

        # Zope imagery
        elif use_format == 'zope_image':
            type_name = 'image'
            # TODO: format_type_and_value - zope_image
            formatted_value = format_object(value, form_id, path, object_id)

        # Zope OFS object
        elif use_format.startswith('zope_ofs'):
            type_name = 'OFS object'
            formatted_value = '%s %s' % (
                format_icon_of_object(value),
                format_object(value, form_id, path, object_id),
            )

        # mapping
        elif use_format == 'mapping':
            type_name = value_type['type_name']
            items = []
            for key, value in value.items():
                items.append('%s: %s' % (repr(key), self.format_type_and_value(
                    value, form_id,
                    path and ('%s/%s' % (path, object_id)), key)))
            formatted_value = '{%s}' % ', '.join(items)

        # sequences
        elif use_format == 'sequence':
            type_name = value_type['type_name']
            items = []
            for index in range(len(value)):
                items.append(self.format_type_and_value(
                    value[index], form_id,
                    path and ('%s/%s' % (path, object_id)), index))
            formatted_value = ', '.join(items)

        # strings
        elif use_format == 'string':
            type_name = value_type['type_name']
            formatted_value = html_quote(repr(value))
            # TODO: format_type_and_value() - implement formatted strings?
            # formatted_value = html_quote(str(value)).replace(
            #   '\\n', '<br>').replace('\\t', '&nbsp;' * 4)
            # css:
            #   .formatted_value[data-format="string"] {white-space: preserve;}

        # numeric (int, float, ...)
        elif use_format == 'number':
            type_name = value_type['type_name']
            formatted_value = str(value)

        # booleans - True, False
        elif use_format == 'boolean':
            type_name = 'boolean'
            formatted_value = repr(value)

        # None
        elif use_format == 'none':
            type_name = 'None'
            formatted_value = None

        # 'placeholder' (used for development only)
        elif use_format == 'placeholder':
            type_name = 'placeholder'
            formatted_value = (
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
                "do eiusmod tempor incididunt ut labore et dolore magna "
                "aliqua.")

        # some type of generic object
        elif use_format == 'object':
            type_name = 'object'
            formatted_value = format_object(value, form_id, path, object_id)

        # TODO format_type_and_value() - handle unknown types
        # - maybe handle expection from guess_value_type()

        # return string with the type and value formatted safe for HTML.
        return '<span class="type_and_value">%s%s</span>' % (
            type_name and
            ('<span class="value_type">%s</span>' % type_name) or
            '',
            '<span class="formatted_value%s"%s%s>%s</span>' % (
                css_class and
                (' %s' % css_class) or
                '',
                type_name and
                (' data-type="%s"' % type_name) or
                '',
                use_format and
                (' data-format="%s"' % use_format) or
                '',
                formatted_value
            )
        )
