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

__doc__ = """ZopeScanner SourceScanner"""

__version__ = '$Revision: 1.3 $'[11:-2]


# =============================================================================
# Module Imports

from resources.imports import DTMLFile, INSTANCE_HOME, SOFTWARE_HOME,\
    ZOPE_HOME, abspath, ctime, exists, isdir, join, listdir, normpath, prefix,\
    realpath, split, splitext, stat, version


# =============================================================================
# File Extensions Mapping

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
    'zexp': ('txt', 'Zope Configuration Markup Language'),
    'zexp': ('hex', 'Zope Export'),
    'zip': ('hex', 'ZIP Archive'),
    'zpt': ('txt', 'ZPT (Page Template)'),
    }


# =============================================================================
# SourceScanner Mix-in Class

class SourceScanner:
    """SourceScanner Mix-in Class"""

    scan_source_form = DTMLFile('sources', globals())

    def scan_source(self, path=''):
        """Scan Source Files

        Perform a scan of source files of the Zope server and Python language,
        starting, traversing along the specified by path. This method only
        processes options and prepares for the actual file reading. See the
        scan_source_file() method below for actual file access.
        """

        breadcrumbs = [
            self.breadcrumbs_root,
            ('scan_source_form', 'Source Files')
            ]

        if path == '/':
            path = ''

        if path:
            result = {}

            basepath = path.split('/')[0]
            if basepath == 'instance':
                breadcrumbs.append(('scan_source_form?path=instance',
                                    'INSTANCE HOME'))
            elif basepath == 'software':
                breadcrumbs.append(('scan_source_form?path=software',
                                    'SOFTWARE HOME'))
            elif basepath == 'zope':
                breadcrumbs.append(('scan_source_form?path=zope',
                                    'Zope Server Code'))
            elif basepath == 'python':
                breadcrumbs.append(('scan_source_form?path=python',
                                    'Python Module Code'))
            else:
                breadcrumbs.append(('scan_source_form?path=%s' % basepath,
                                    basepath))

            parts = []
            parts_path = path.split('/')[0]
            for part in path.split('/')[1:]:
                parts_path = parts_path + '/' + part
                parts.append((parts_path, part))
                breadcrumbs.append(('scan_source_form?path=' + parts_path,
                                    part))
            result['breadcrumbs'] = breadcrumbs
            result['path_parts'] = parts
            return result

        result = {}
        result['breadcrumbs'] = breadcrumbs
        return result

    def get_source_path(self, path):

        pathroot = path.split('/')[0]

        if pathroot == 'instance':
            basepath = INSTANCE_HOME
        elif pathroot == 'software':
            basepath = SOFTWARE_HOME
        elif pathroot == 'zope':
            basepath = ZOPE_HOME
        elif pathroot == 'python':
            basepath = normpath('%s/lib/python%s' % (prefix, version[:3]))
            if not exists(basepath):
                basepath = normpath('%s/Lib' % prefix)
        else:
            return None

        filepath = basepath
        path_parts = path.split('/')
        if len(path_parts) > 1:
            filepath = join(filepath, '/'.join(path_parts[1:]))

        filepath = normpath(abspath(filepath))
        if not filepath.startswith(basepath):
            filepath = basepath

        return filepath

    def scan_source_file(self, path=''):
        """Scan Zope source file specified by path"""

        result = {}

        filepath = self.get_source_path(path)

        if not filepath:
            result['message'] = 'Invalid root path!'

        elif realpath(filepath) != normpath(filepath):
            result['message'] = 'Refusing to follow symbolic links!'

        elif isdir(filepath):
            result['filetype'] = 'dir'
            contents = []
            for subfilename in listdir(filepath):
                subfilepath = join(filepath, subfilename)
                subfileinfo = stat(subfilepath)
                if isdir(subfilepath):
                    subfiletype = 'Directory'
                else:
                    extension = splitext(subfilepath)[1].lower()[1:]
                    if extension in extensions:
                        subfiletype = extensions[extension][1]
                    else:
                        subfiletype = '<em>Unknown</em>'
                contents.append({
                    'filename': subfilename,
                    'filetype': subfiletype,
                    'size': subfileinfo[6],
                    'atime': ctime(subfileinfo[7]),
                    'mtime': ctime(subfileinfo[8]),
                    'ctime': ctime(subfileinfo[9]),
                    })
            result['contents'] = contents

        elif exists(filepath):
            extension = splitext(filepath)[1].lower()[1:]
            if extension in extensions:
                filetype = extensions[extension][0]
            else:
                filetype = 'hex'
            if filetype == 'txt':
                filehandle = open(filepath, 'r')
                result['contents'] = filehandle.read()
                filehandle.close()
            elif filetype == 'img':
                filehandle = open(filepath, 'rb')
                result['contents'] = filehandle.read()
                filehandle.close()
            else:
                filehandle = open(filepath, 'rb')
                result['contents'] = filehandle.read()
                filehandle.close()
            result['filetype'] = filetype

        else:
            result['message'] = 'File not found!'

        return result

    def retrieve_source_file(self, path):
        """Retrieve specified source file"""

        filepath = self.get_source_path(path)
        if filepath and realpath(filepath) == filepath:
            extension = splitext(filepath)[1].lower()[1:]
            if extension in extensions and extensions[extension][0] ==\
                    'img':
                filehandle = open(filepath, 'rb')
                result = filehandle.read()
                filehandle.close()
                return result
