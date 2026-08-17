"""ZopeScanner - SourceScanner.

Perform scans of source files of the Zope server and Python
language.
"""


from Products.ZopeScanner.imports_python import abspath
from Products.ZopeScanner.imports_python import ceil
from Products.ZopeScanner.imports_python import environ
from Products.ZopeScanner.imports_python import exists
from Products.ZopeScanner.imports_python import isdir
from Products.ZopeScanner.imports_python import join
from Products.ZopeScanner.imports_python import listdir
from Products.ZopeScanner.imports_python import normpath
from Products.ZopeScanner.imports_python import prefix
from Products.ZopeScanner.imports_python import realpath
from Products.ZopeScanner.imports_python import splitext
from Products.ZopeScanner.imports_python import stat
from Products.ZopeScanner.imports_python import version

from Products.ZopeScanner.imports_zope import DTMLFile

from Products.ZopeScanner.shared import sort_by_key

from Products.ZopeScanner.values import format_filesize
from Products.ZopeScanner.values import format_datetime


INSTANCE_HOME = environ.get('INSTANCE_HOME')
SOFTWARE_HOME = environ.get('SOFTWARE_HOME')
ZOPE_HOME = environ.get('ZOPE_HOME')


# =============================================================================
# SourceScanner File Extensions Mapping

# TODO: sources.py - revise file identification
# - create _guess_source_file_type()
# - use python library if possible
# - extend with zope related file formats


extensions = {
    'bak': ('hex', 'Backup'),
    'bat': ('txt', 'Batch Script'),
    'conf': ('txt', 'Configuration'),
    'dll': ('hex', 'Dynamic Link Library'),
    'dtml': ('txt', 'DTML (Document Template Markup Language)'),
    'exe': ('hex', 'Executable'),
    'fs': ('hex', 'Zope Database'),
    'gif': ('img', 'GIF Image'),
    'gz': ('hex', 'Gzip Archive'),
    'htm': ('txt', 'HTML (Hypertext Markup Language)'),
    'html': ('txt', 'HTML (Hypertext Markup Language)'),
    'ico': ('img', 'Icon'),
    'index': ('img', 'Zope Database Index'),
    'jar': ('img', 'Java'),
    'jpe': ('img', 'JPEG/JFIF Image'),
    'jpeg': ('img', 'JPEG/JFIF Image'),
    'jpg': ('img', 'JPEG/JFIF Image'),
    'lock': ('img', 'Lock'),
    'log': ('txt', 'Log File'),
    'pid': ('img', 'Process Identifier'),
    'png': ('img', 'PNG Image'),
    'pt': ('txt', 'ZPT (Page Template)'),
    'py': ('txt', 'Python Source'),
    'pyc': ('hex', 'Compiled Python'),
    'pyd': ('hex', 'Python Dynamic Module'),
    'pyo': ('hex', 'Python Optimized Code'),
    'pys': ('txt', 'Python Script'),
    'pyw': ('txt', 'Python Source (Windows)'),
    'sh': ('txt', 'Shell Script'),
    'so': ('hex', 'Shared Object'),
    'stx': ('txt', 'Structured Text'),
    'tar': ('hex', 'Tape Archive'),
    'tgz': ('hex', 'Tape/Gzip Archive'),
    'tif': ('img', 'TIFF Image'),
    'tiff': ('img', 'TIFF Image'),
    'txt': ('txt', 'Plain Text'),
    'xbm': ('img', 'XBM Image'),
    'xml': ('txt', 'XML (Extensible Markup Language)'),
    # 'zexp': ('txt', 'Zope Configuration Markup Language'),
    'zexp': ('hex', 'Zope Export'),
    'zip': ('hex', 'ZIP Archive'),
    'zpt': ('txt', 'ZPT (Page Template)'),
}


# =============================================================================
# SourceScanner Root Paths


def __get_sources_rootpaths():
    """Return a list of valid root paths.

    This list is fixed and may not be extended. The Source Browser will refuse
    any access outside these root paths.
    """
    result = []

    if environ.get('INSTANCE_HOME'):
        result.append({
            'key': 'instance',
            'label': "INSTANCE HOME",
            'path': environ.get('INSTANCE_HOME'),
        })

    if environ.get('SOFTWARE_HOME'):
        result.append({
            'key': 'software',
            'label': "SOFTWARE HOME",
            'path': environ.get('SOFTWARE_HOME'),
        })

    if environ.get('ZOPE_HOME'):
        result.append({
            'key': 'zope',
            'label': "ZOPE HOME",
            'path': environ.get('ZOPE_HOME'),
        })

    rootpath = normpath('%s/lib/python%s' % (prefix, version[:3]))
    if not exists(rootpath):
        rootpath = normpath('%s/Lib' % prefix)
    result.append({
        'key': 'python',
        'label': "Python Source",
        'path': rootpath,
    })

    return result


rootpaths = __get_sources_rootpaths()

rootpath_map = {}
for item in rootpaths:
    rootpath_map[item['key']] = item


# =============================================================================
# SourceScanner Mix-in Class


class SourceScanner:
    """SourceScanner Mix-in Class."""

    scan_sources_form = DTMLFile('resources/sources', globals())

    def scan_sources(self, form):
        """Scan source files.

        Perform a scan of source files of the Zope server and Python language,
        starting, traversing along the specified by path. This method only
        processes options and prepares for the actual file reading. See the
        scan_source_file() method below for actual file access.
        """
        # initialise scanner form parameters
        breadcrumbs = [('scan_sources_form', 'Source File Scanner')]
        form_id = breadcrumbs[0][0]
        url_prefix = '%s/%s' % (self.scanner_url(), form_id)
        report = {
            'breadcrumbs': breadcrumbs,
            'form_id': form_id,
            'url_prefix': url_prefix,
        }

        # parameters for directory view
        order_by = form.get('order_by', 'name')
        show_hidden_files = form.get('show_hidden_files', False)

        # parameters for hexdump view
        bytes_per_row = max(8, min(64, int(form.get('bytes_per_row', 16))))
        bytes_per_page = max(1024, min(128 * 1024, int(
            form.get('bytes_per_page', 4 * 1024))))
        page_number = int(form.get('page_number', 1))

        link_params = {

            'order_by': order_by,
            'show_hidden_files': show_hidden_files,

            'bytes_per_row': bytes_per_row,
            'bytes_per_page': bytes_per_page,
            'page_number': page_number,

        }
        report['link_params'] = link_params
        report.update(link_params)

        # add list of rootpaths without filepaths to report
        filtered_rootpaths = []
        for rootpath in rootpaths:
            filtered_rootpaths.append((
                rootpath['key'], rootpath['label']))
        report['rootpaths'] = filtered_rootpaths

        # initialise and normalise path
        path = form.get('path', '')
        path = path != '/' and path or ''

        # we have a path and need to deduce the respective filepath
        if path:

            # determine rootpath
            step_path = path.split('/')[0]
            rootpath = rootpath_map.get(step_path, None)
            if rootpath is None:
                raise ValueError('invalid path')

            # generate filepath and breadcrumbs from path
            breadcrumbs.append((
                'scan_sources_form?path=' + step_path, rootpath['label']))
            filepath = rootpath['path']
            for step_name in path.split('/')[1:]:
                step_path = step_path + '/' + step_name
                filepath = join(filepath, step_name)
                breadcrumbs.append((
                    'scan_sources_form?path=' + step_path, step_name))

            # ensure that we are still, where we want to be, and not outside of
            # the designated root directory via ".." in path
            filepath = normpath(abspath(filepath))
            if not filepath.startswith(rootpath['path']):
                raise ValueError('invalid path')

            if realpath(filepath) != normpath(filepath):
                raise TypeError('refusing to follow symbolic links')

        # we have no path, so start with the first rootpath
        else:
            rootpath = rootpaths[0]
            path = rootpath['key']
            filepath = rootpath['path']
            breadcrumbs.append((
                'scan_sources_form?path=' + path, rootpath['label']))

        # update report
        report['filename'] = path.split('/')[-1]
        report['rootpath_key'] = rootpath['key']
        report['breadcrumbs'] = breadcrumbs
        report['path'] = path

        # directory
        if isdir(filepath):

            # iterate over files in directory and create a list of information
            # about each file
            files = []
            for subname in listdir(filepath):
                if subname[0] == '.' and not show_hidden_files:
                    continue
                subpath = join(filepath, subname)
                subinfo = stat(subpath)
                subtype = '<em>Unknown</em>'

                # identify type of file
                # TODO: scan_sources() - replace with new file identification
                if isdir(subpath):
                    subtype = 'Directory'
                else:
                    extension = splitext(subname)[1].lower()[1:]
                    if extension in extensions:
                        subtype = extensions[extension][1]

                # store file information
                files.append({
                    'name': subname,
                    'filepath': subpath,
                    'type': subtype,
                    'size': subinfo[6],
                    'size_formatted': format_filesize(subinfo[6]) or '',
                    'atime': format_datetime(ts=subinfo[7]),
                    'mtime': format_datetime(ts=subinfo[8]),
                    'ctime': format_datetime(ts=subinfo[9]),
                })
            files = sort_by_key(files, order_by)

            # update report
            report['directory'] = files

        # file archive
        # TODO: scan_sources() - file archive scan

        # audio file
        # TODO: scan_sources() - audio file scan

        # image file
        # TODO: scan_sources() - image file scan

        # video file
        # TODO: scan_sources() - video file scan

        # source file
        # TODO: scan_sources() - source file scan

        # text file
        # TODO: scan_sources() - text file scan

        # hexdump file
        else:
            # use a rotating buffer to capture bytes from start to end. iterate
            # until eof to determine file size.
            hexdump = {}
            contents = ''
            content_start = (page_number - 1) * bytes_per_page
            content_end = page_number * bytes_per_page
            buffer = [None] * bytes_per_page
            index = 0
            total_size = 0
            try:
                filehandle = open(filepath, 'r')
                while 1:
                    character = filehandle.read(1)
                    if not character:
                        break
                    buffer[index] = character
                    if (
                        total_size >= content_start and
                        total_size < content_end
                    ):
                        contents = contents + character
                    index = (index + 1) % bytes_per_page
                    total_size = total_size + 1
                filehandle.close()
            except Exception:  # TODO: review Exception
                pass
            total_pages = int(ceil(1.0 * total_size / bytes_per_page))

            # update report
            hexdump['contents'] = contents
            hexdump['total_size'] = total_size
            hexdump['total_pages'] = total_pages
            report['hexdump'] = hexdump

        return report
