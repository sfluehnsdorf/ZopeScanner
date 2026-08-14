"""Zope Scanner - LogScanner."""


from Products.ZopeScanner.imports_python import basename
from Products.ZopeScanner.imports_python import compile
from Products.ZopeScanner.imports_python import environ
from Products.ZopeScanner.imports_python import exists
from Products.ZopeScanner.imports_python import match
from Products.ZopeScanner.imports_python import stderr
from Products.ZopeScanner.imports_python import writes

from Products.ZopeScanner.imports_zope import DTMLFile
from Products.ZopeScanner.imports_zope import MinimalLogger

from Products.ZopeScanner.shared import sort_by_key


INSTANCE_HOME = environ.get('INSTANCE_HOME')


default_max_lines = 50

access_pattern = compile(
    r'(.*) - (.*) \[(.*)\] "(.*)" (.*) (.*) "(.*)" "(.*)"')
access_pattern_columns = [
    'Client IP',
    'User',
    'Date/Time',
    'Request',
    'Status',
    'Size',
    'Referrer',
    'Client',
]


class LogScanner:
    """LogScanner Mix-in Class."""

    scan_logfiles_form = DTMLFile(
        'resources/logs', globals(), default_max_lines=default_max_lines)

    def get_logfile_lines(self, path, max_lines):
        """Update log file's lines."""
        lines = []
        columns = []
        if path and max_lines:
            lines = self._read_logfile(path, int(max_lines))
            if lines:
                columns, lines = self._process_logfile_lines(lines)
        return writes({
            'columns': columns,
            'columns_len': len(columns),
            'lines': lines,
            'lines_len': len(lines),
        })

    def scan_logfiles(
        self, path='', max_lines=default_max_lines, REQUEST=None
    ):
        """Scan log files.

        Scan the log file specified by path, applying a variety of batch and
        filter options. This method only processes options and prepares for the
        actual log file reading. See the _read_logfile() method for actual file
        access.
        """
        breadcrumbs = [('scan_logfile_form', 'Log File Scanner')]
        form_id = breadcrumbs[0][0]
        url_prefix = '%s/%s' % (self.scanner_url(), form_id)
        report = {
            'breadcrumbs': breadcrumbs,
            'form_id': form_id,
            'url_prefix': url_prefix,
        }

        path = path != '/' and path or ''
        max_lines = int(max_lines) or default_max_lines
        current_log_file = None

        lines = []
        columns = []
        log_files = self._list_logfiles()
        log_files_map = {}
        if log_files:
            for log_file in log_files:
                log_files_map[log_file['filepath']] = log_file
            if path in log_files_map:
                current_log_file = log_files_map[path]
            if not current_log_file:
                current_log_file = log_files[0]
            lines = self._read_logfile(current_log_file['filepath'], max_lines)
        if lines:
            columns, lines = self._process_logfile_lines(lines)
        if current_log_file:
            breadcrumbs = breadcrumbs + [(
                current_log_file['filepath'], current_log_file['filename'])]

        report.update({
            'columns': columns,
            'log_files': log_files,
            'log_files_map': log_files_map,
            'lines': lines,
            'current_log_file': current_log_file,
        })
        return report

    def _read_logfile(self, filepath, max_lines):
        """Scan log file."""
        lines = []
        filepath_found = 0
        for log_file in self._list_logfiles():
            if filepath == log_file['filepath']:
                filepath_found = 1
                break
        if (
            filepath_found and
            exists(filepath)
        ):
            buffer = [None] * max_lines
            index = 0
            total_lines = 0
            filehandle = open(filepath, 'r')
            try:
                while 1:
                    line = filehandle.readline()
                    if not line:
                        break
                    buffer[index] = line.rstrip()
                    index = (index + 1) % max_lines
                    total_lines = total_lines + 1
            except Exception:  # TODO: review Exception
                pass
            if total_lines == 0:
                lines = []
            elif total_lines < max_lines:
                lines = buffer[:total_lines]
            else:
                lines = buffer[index:] + buffer[:index]
            filehandle.close()
        return lines

    def _list_logfiles(self):
        result = []
        try:  # since Python-2.3.0
            import logging
        except ImportError:
            logging = None
        if logging:
            handlers = []
            if hasattr(logging, 'getHandlerNames'):
                for name in logging.getHandlerNames():
                    handler = logging.getHandlerByName(name)
                    handlers.append(handler)
            elif hasattr(logging, '_handlerList'):
                logging._acquireLock()
                for weak_handler in logging._handlerList:
                    handler = weak_handler()
                    if handler is not None:
                        handlers.append(handler)
                logging._releaseLock()
            elif hasattr(logging, '_handlers'):
                logging._acquireLock()
                for handler in logging._handlers.keys():
                    handlers.append(handler)
                logging._releaseLock()
            for handler in handlers:
                if hasattr(handler, 'baseFilename'):
                    result.append({
                        'filepath': handler.baseFilename,
                        'filename': basename(handler.baseFilename),
                    })
        elif MinimalLogger:
            destination = MinimalLogger._log_dest
            if (
                destination and
                destination is not stderr
            ):
                filepath = str(MinimalLogger._log_dest.name)
                result.append({
                    'filepath': filepath,
                    'filename': basename(filepath),
                })
        result = sort_by_key(result, 'filename')
        return result

    def _process_logfile_lines(self, source):
        lines = []
        first_line = source[0]
        if match(access_pattern, first_line):
            columns = access_pattern_columns[:]
            for line in source:
                matched_object = match(access_pattern, line)
                if matched_object:
                    lines.append(matched_object.groups())
                else:
                    lines.append([line])
        else:
            for line in source:
                lines.append([line])
            columns = ['Line']
        return columns, lines
