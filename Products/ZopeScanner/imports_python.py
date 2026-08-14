"""Zope Scanner - Python Imports.

All imports from Python are centralized in this module. As any change to the
API requires adaptation, this is where any workaround is done.

Every symbol imported as on their own line intentionally. As the syntax for
importing between the different major releases of Python varies substantially,
this is the only format that is human readable and style guide complaint.
"""


__all__ = [
    'abspath',
    'architecture',
    'basename',
    'ceil',
    'compile',
    'cpu_count',
    'environ',
    'exc_info',
    'executable',
    'exists',
    'freedesktop_os_release',
    'get_ident',
    'getpid',
    'gmtime',
    'isdir',
    'join',
    'listdir',
    'match',
    'maxsize',
    'modules',
    'normpath',
    'platform',
    'prefix',
    'python_build',
    'python_compiler',
    'python_version',
    'realpath',
    'signature',
    'socket_map',
    'splitext',
    'stat',
    'stderr',
    'strftime',
    'time',
    'uname',
    'unpack',
    'version',
    'writes',
]


# =============================================================================
# Python imports


from math import ceil
from os import environ
from os import getpid
from os import listdir
from os import stat
from os.path import abspath
from os.path import basename
from os.path import exists
from os.path import isdir
from os.path import join
from os.path import normpath
from os.path import realpath
from os.path import splitext
from re import compile
from re import match
from struct import unpack
from sys import exc_info
from sys import executable
from sys import modules
from sys import platform
from sys import prefix
from sys import stderr
from sys import version
from time import gmtime
from time import strftime
from time import time

try:  # asyncore.socket_map until Python-2.6.0
    from asyncore import socket_map
except ImportError:
    socket_map = None

try:  # inspect.signature - since Python-2.1.3
    from inspect import signature
except ImportError:
    signature = None

try:  # json.writes - since Python-2.6.0
    from json import writes
except ImportError:

    def _json_encode(data):
        if data is None:
            return 'null'
        elif data is True:
            return 'true'
        elif data is False:
            return 'false'
        elif (
            isinstance(data, type(1)) or
            isinstance(data, type(1.1))
        ):
            return data
        elif isinstance(data, type('')):
            for raw, encoded in [
                # backslashes (must be done first)
                ('\\', '\\\\'),
                # double quotes
                ('"', '\\"'),
                # standard control characters
                ('\n', '\\n'),
                ('\r', '\\r'),
                ('\t', '\\t'),
                ('\b', '\\b'),
                ('\x0c', '\\f'),  # \x0c = form feed
            ]:
                data = data.replace(raw, encoded)
            return '"%s"' % data
        elif (
            isinstance(data, type([])) or
            isinstance(data, type(()))
        ):
            items = []
            for item in data:
                items.append(_json_encode(item))
            return '[%s]' % ','.join(items)
        elif isinstance(data, type({})):
            items = []
            for key, value in data.items():
                items.append('%s:%s' % (
                    _json_encode(key), _json_encode(value)))
            return '{%s}' % ','.join(items)

    writes = _json_encode

try:  # os.cpu_count - since Python-2.6.0
    from os import cpu_count
except ImportError:
    cpu_count = None

try:  # platform.* - since Python-2.3.0
    from platform import architecture
    from platform import python_build
    from platform import python_compiler
    from platform import python_version
    from platform import uname
except ImportError:
    architecture = None

    try:
        from os import uname
    except ImportError:

        def uname():
            """Return tuple of strings identifying the underlying platform.

            This is a minimal implementation as a failsafe. It returns a tuple
            of (system, node, release, version, machine, processor).
            """
            system = platform
            release = ''
            version = ''
            node = ''
            machine = ''
            processor = ''

            try:
                from socket import gethostname
                node = gethostname()
            except ImportError:
                pass

            # skipping a lot (!) of code from Python's implementation, thus a
            # rather limited report must suffice here.

            return (system, node, release, version, machine, processor)

    def _sys_version(sys_version=None):
        """Return a parsed version of Python's sys.version.

        Returns a parsed version of Python's sys.version as tuple (name,
        version, branch, revision, buildno, builddate, compiler) referring to
        the Python implementation name, version, branch, revision, build
        number, build date/time as string and the compiler identification
        string.

        Note that unlike the Python sys.version, the returned value for the
        Python version will always include the patchlevel (it defaults to
        '.0').

        The function returns empty strings for tuple entries that cannot be
        determined.

        sys_version may be given to parse an alternative version string, e.g.
        if the version was read from a different Python interpreter.
        """
        import re
        import sys

        # Get the Python version
        if sys_version is None:
            sys_version = sys.version

        if platform.startswith('java'):
            # Jython
            pattern = (
                r'([\w.+]+)\s*'  # "version<space>"
                r'\(#?([^,]+)'  # "(#buildno"
                r'(?:,\s*([\w ]*)'  # ", builddate"
                r'(?:,\s*([\w :]*))?)?\)\s*'  # ", buildtime)<space>"
                r'\[([^\]]+)\]?')  # "[compiler]"
            try:
                jython_sys_version_parser = re.compile(pattern, re.ASCII)
            except Exception:  # TODO: specify Exception
                jython_sys_version_parser = re.compile(pattern)
            name = 'Jython'
            match = jython_sys_version_parser.match(sys_version)
            if match is None:
                raise ValueError(
                    'failed to parse Jython sys.version: %s' %
                    repr(sys_version))
            version, buildno, builddate, buildtime, _ = match.groups()
            if builddate is None:
                builddate = ''
            compiler = platform

        elif sys_version.count("PyPy"):
            # PyPy
            pypy_sys_version_parser = re.compile(
                r'([\w.+]+)\s*'
                r'\(#?([^,]+),\s*([\w ]+),\s*([\w :]+)\)\s*'
                r'\[PyPy [^\]]+\]?')

            name = "PyPy"
            match = pypy_sys_version_parser.match(sys_version)
            if match is None:
                raise ValueError("failed to parse PyPy sys.version: %s" %
                                 repr(sys_version))
            version, buildno, builddate, buildtime = match.groups()
            compiler = ""

        else:
            # CPython
            pattern = (
                r'([\w.+]+)\s*'  # "version<space>"
                r'(?:free-threading build\s+)?'
                # "free-threading-build<space>"
                r'\(#?([^,]+)'  # "(#buildno"
                r'(?:,\s*([\w ]*)'  # ", builddate"
                r'(?:,\s*([\w :]*))?)?\)\s*'  # ", buildtime)<space>"
                r'\[([^\]]+)\]?')  # "[compiler]"
            try:
                cpython_sys_version_parser = re.compile(pattern, re.ASCII)
            except Exception:  # TODO: specify Exception
                cpython_sys_version_parser = re.compile(pattern)
            match = cpython_sys_version_parser.match(sys_version)
            if match is None:
                raise ValueError(
                    'failed to parse CPython sys.version: %s' %
                    repr(sys_version))
            version, buildno, builddate, buildtime, compiler = \
                match.groups()
            name = 'CPython'
            if builddate is None:
                builddate = ''
            elif buildtime:
                builddate = builddate + ' ' + buildtime

        if hasattr(sys, '_git'):
            _, branch, revision = sys._git
        elif hasattr(sys, '_mercurial'):
            _, branch, revision = sys._mercurial
        else:
            branch = ''
            revision = ''

        # Add the patchlevel version if missing
        patchlevel = version.split('.')
        if len(patchlevel) == 2:
            patchlevel.append('0')
            version = '.'.join(patchlevel)

        return (
            name, version, branch, revision, buildno, builddate, compiler)

    def python_version():
        """Return Python version as string 'major.minor.patchlevel'."""
        return _sys_version()[1]

    def python_build():
        """Return tuple of Python build number and date as strings."""
        return _sys_version()[4:6]

    def python_compiler():
        """Return string identifying the compiler used for compiling Python."""
        return _sys_version()[6]

try:  # platform.freedesktop_os_release - since Python-3.10.0
    from platform import freedesktop_os_release
except ImportError:
    freedesktop_os_release = None

try:  # sys.maxsize - since Python-3.0.0
    from sys import maxsize
except ImportError:
    from sys import maxint
    maxsize = maxint

try:  # thread.get_ident - since Python-3.0.0
    from thread import get_ident
except ImportError:
    from threading import current_thread

    def get_ident():
        """Return the current thread's ident."""
        return current_thread().ident
