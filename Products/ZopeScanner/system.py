"""Zope Scanner - SystemScanner."""


from Products.ZopeScanner.imports_python import architecture
from Products.ZopeScanner.imports_python import basename
from Products.ZopeScanner.imports_python import cpu_count
from Products.ZopeScanner.imports_python import environ
from Products.ZopeScanner.imports_python import executable
from Products.ZopeScanner.imports_python import freedesktop_os_release
from Products.ZopeScanner.imports_python import get_ident
from Products.ZopeScanner.imports_python import getpid
from Products.ZopeScanner.imports_python import python_build
from Products.ZopeScanner.imports_python import python_compiler
from Products.ZopeScanner.imports_python import python_version
from Products.ZopeScanner.imports_python import socket_map
from Products.ZopeScanner.imports_python import time
from Products.ZopeScanner.imports_python import uname
from Products.ZopeScanner.imports_python import version

from Products.ZopeScanner.imports_zope import DTMLFile
from Products.ZopeScanner.imports_zope import getConfiguration
from Products.ZopeScanner.imports_zope import getZopeVersion

from Products.ZopeScanner.shared import sort_by_key

from Products.ZopeScanner.values import format_duration
from Products.ZopeScanner.values import format_filesize
from Products.ZopeScanner.values import guess_value_type


INSTANCE_HOME = environ.get('INSTANCE_HOME')
SOFTWARE_HOME = environ.get('SOFTWARE_HOME')
ZOPE_HOME = environ.get('ZOPE_HOME')


# =============================================================================
# SystemScanner Class


class SystemScanner:
    """SystemScanner Mix-in Class."""

    scan_system_form = DTMLFile('resources/system', globals())

    def scan_system(self, path=''):
        """Scan system."""
        breadcrumbs = [('scan_system_form', 'System Scanner')]
        form_id = breadcrumbs[0][0]
        url_prefix = '%s/%s' % (self.scanner_url(), form_id)
        report = {
            'breadcrumbs': breadcrumbs,
            'form_id': form_id,
            'url_prefix': url_prefix,
        }

        report.update({
            'host': self.scan_system_host(form_id, path),
            'software': self.scan_system_software(form_id, path),
            'servers': self.scan_system_servers(form_id, path),
            'databases': self.scan_system_databases(form_id, path),
            'dav_locks': self.scan_system_dav_locks(form_id, path),
            'reference_counts': self.scan_system_reference_counts(
                form_id, path),
            'zodb_connections': self.scan_system_zodb_connections(
                form_id, path),
            'config_items': self.scan_system_config(form_id, path),
            'environ_items': self.scan_system_environ(form_id, path),
        })
        return report

    def scan_system_host(self, form_id, path):
        """Scan system host."""
        host = {}
        uname_result = uname()
        if uname_result:
            host.update({
                'hostname': uname_result[1],
                'os_system': uname_result[0],
                'os_version': uname_result[3],
                'os_release': uname_result[2],
                'os_machine': uname_result[4],
                'os_processor': uname_result[5],
            })
            if cpu_count:
                host['cpu_cores'] = cpu_count()
            if uname_result[0] == "Linux":
                if freedesktop_os_release:
                    distro = freedesktop_os_release()
                    host['distro_name'] = distro.get('NAME', None)
                    host['distro_version'] = distro.get('VERSION', None)
        # TODO: add support for psutil
        return host

    def scan_system_software(self, form_id, path):
        """Scan system software."""
        zope_version = getZopeVersion()
        zope_runtime = format_duration(int(
            time() - self.getPhysicalRoot().Control_Panel.process_start))

        software = {
            'python': version,
            'python_version': python_version and python_version(),
            'python_compiler': python_compiler and python_compiler(),
            'python_build_no': python_build and python_build()[0],
            'python_build_date': python_build and python_build()[1],
            'python_arch_bits': architecture and architecture()[0],
            'python_arch_linkage': architecture and architecture()[1],
            'python_executable': executable,
            'zope': '%d.%d.%d%s' % (
                zope_version[0],
                zope_version[1],
                zope_version[2],
                zope_version[3] and
                ' %s%s' % (
                    zope_version[3],
                    zope_version[4] != -1 and
                    zope_version[4] or
                    '',
                ) or
                ''
            ),
            'zope_runtime': zope_runtime,
            'zope_pid': getpid(),
            'zope_thread': get_ident(),
            'INSTANCE_HOME': INSTANCE_HOME,  # TODO: format as link to source
            'SOFTWARE_HOME': SOFTWARE_HOME,  # TODO: format as link to source
            'ZOPE_HOME': ZOPE_HOME,  # TODO: format as link to source
        }
        return software

    def scan_system_servers(self, form_id, path, order_by='key'):
        """Scan servers.

        Perform a scan starting with the list of active servers, traversing
        along the specified by path.
        """
        servers = []
        if socket_map is not None:
            format_type_and_value = self.format_type_and_value
            for key, value in socket_map.items():
                try:
                    name = '%s' % getattr(value, 'SERVER_IDENT')
                except Exception:  # TODO: review Exception
                    name = ''
                sclass = format_type_and_value(
                    value, 'scan_server_form', '', str(key))
                try:
                    hostname = '%s' % getattr(value, 'hostname')
                except Exception:  # TODO: review Exception
                    hostname = ''
                try:
                    ip = '%s' % getattr(value, 'ip')
                except Exception:  # TODO: review Exception
                    ip = ''
                try:
                    port = '%s' % getattr(value, 'port')
                except Exception:  # TODO: review Exception
                    port = ''
                servers.append({
                    'key': key,
                    'name': name,
                    'sclass': sclass,
                    'hostname': hostname,
                    'ip': ip,
                    'port': port,
                })
            servers = sort_by_key(servers, order_by)
        else:
            servers = None
        return servers

    def scan_system_databases(self, form_id, path):
        """Scan system databases."""
        databases = []
        if getConfiguration:
            configuration = getConfiguration()
            names = configuration.dbtab.listDatabaseNames()
            names.sort()
            mount_paths = {}
            for item in configuration.dbtab.listMountPaths():
                mount_paths[item[1]] = item[0]
            for name in names:
                database = configuration.dbtab.getDatabase(name=name)
                try:
                    object_count = database.objectCount()
                except Exception:  # TODO: review Exception
                    object_count = None
                databases.append({
                    'name': name,
                    'mount_point': mount_paths[name],
                    'location': database.getName(),
                    # TODO: format as link to source if path, not text
                    'size': format_filesize(database.getSize()),
                    'object_count': object_count,
                })
        else:
            databases.append({
                'name': basename(
                    self.getPhysicalRoot().Control_Panel.db_name()),
                'mount_point': '/',
                'location': self.getPhysicalRoot().Control_Panel.db_name(),
                'size': format_filesize(
                    self.getPhysicalRoot().Control_Panel.db_size()),
                'object_count': None,
            })
        return databases

    def scan_system_dav_locks(self, form_id, path):
        """Scan system DAV locks."""
        return []  # TODO: scan_system_dav_locks()

    def scan_system_reference_counts(self, form_id, path):
        """Scan system Reference Counts."""
        return []  # TODO: scan_system_reference_counts()

    def scan_system_zodb_connections(self, form_id, path):
        """Scan system ZODB Connections."""
        return []  # TODO: scan_system_zodb_connections()

    def scan_system_config(self, form_id, path, order_by='key'):
        """Scan server configuration."""
        config_items = []
        format_type_and_value = self.format_type_and_value
        if getConfiguration:
            config = getConfiguration()
            keys = list(config.__dict__.keys())
            keys.sort()
            for key in keys:
                value = getattr(config, key)
                config_type = guess_value_type(value)
                formatted_value = format_type_and_value(
                    value, form_id, path, key, value_type=config_type)
                config_items.append({
                    'key': key,
                    'type': config_type['name'],
                    'value': formatted_value,
                })
        else:
            for key in [
                # Zope installation
                'INSTANCE_HOME',
                'SOFTWARE_HOME',
                'ZOPE_HOME',
                'FORCE_PRODUCT_LOAD',
                'FORCE_PRODUCT_LOAD',
                # Profiling
                'PROFILE_PUBLISHER',
                # SiteAccess
                'SUPPRESS_ACCESSRULE',
                'SUPPRESS_SITEROOT',
                # ZEO
                'CLIENT_HOME',
                'ZEO_CLIENT',
                # Debugging and Logging
                'EVENT_LOG_FORMAT',
                'STUPID_LOG_FORMAT',
                'EVENT_LOG_FILE',
                'STUPID_LOG_FILE',
                'EVENT_LOG_SEVERITY',
                'STUPID_LOG_SEVERITY',
                'ZSYSLOG',
                'ZSYSLOG_FACILITY',
                'ZSYSLOG_SERVER',
                'ZSYSLOG_ACCESS',
                'ZSYSLOG_ACCESS_FACILITY',
                'ZSYSLOG_ACCESS_SERVER',
                'Z_DEBUG_MODE',
                'BOBO_DEBUG_MODE',
                # Miscellaneous
                'Z_REALM',
                'BOBO_REALM',
                # Security related
                'NO_SECURITY',
                'ZOPE_SECURITY_POLICY',
                'ZSP_OWNEROUS_SKIP',
                'ZSP_AUTHENTICATED_SKIP',
                'DISALLOW_LOCAL_PRODUCTS',
                # ZODB related
                'ZOPE_DATABASE_QUOTA',
                'ZOPE_READ_ONLY',
                # Session related
                'ZSESSION_ADD_NOTIFY',
                'ZSESSION_DEL_NOTIFY',
                'ZSESSION_TIMEOUT_MINS',
                'ZSESSION_OBJECT_LIMIT',
                # WebDAV
                'WEBDAV_SOURCE_PORT_CLIENTS',
                # Structured Text
                'STX_DEFAULT_LEVEL',
                # DTML
                'ZOPE_DTML_REQUEST_AUTOQUOTE',
                # Esoteric
                'Z_MAX_STACK_SIZE',
                'FORCE_PRODUCT_RELOAD',
            ]:
                value = environ.get(key)
                config_type = guess_value_type(value)
                formatted_value = format_type_and_value(
                    value, form_id, path, key, value_type=config_type)
                config_items.append({
                    'key': key,
                    'type': config_type['name'],
                    'value': formatted_value,
                })
        config_items = sort_by_key(config_items, order_by)
        return config_items

    def scan_system_environ(self, form_id, path):
        """Scan OS environment."""
        environment_items = []
        keys = list(environ.keys())
        keys.sort()
        format_type_and_value = self.format_type_and_value
        for key in keys:
            value = environ[key]
            environment_type = guess_value_type(value)
            formatted_value = format_type_and_value(
                value, form_id, path, key, value_type=environment_type)
            environment_items.append({
                'key': key,
                'type': environment_type['name'],
                'value': formatted_value,
            })
        return environment_items
