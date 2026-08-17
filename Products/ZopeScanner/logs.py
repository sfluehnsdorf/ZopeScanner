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


# =============================================================================

# number of lines to display
default_max_lines = 50

# columns in a standard httpd access log file
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


# =============================================================================
# LogScanner Mix-in Class


class LogScanner:
    """LogScanner Mix-in Class."""

    scan_logfiles_form = DTMLFile(
        'resources/logs', globals(), default_max_lines=default_max_lines)

    def get_logfile_lines(self, path, max_lines):
        """Update log file's lines.

        Endpoint that provides data returns lines from the end of a log file.
        Used by auto refresh feature of the LogScanner.
        """
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

        Return lines from the end of the specified path. The path is checked
        for validity and must be of the identified list of Zope maintained log
        files.
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

        # handle log files
        if log_files:
            for log_file in log_files:
                log_files_map[log_file['filepath']] = log_file

            # map path to log file
            if path in log_files_map:
                current_log_file = log_files_map[path]

            # choose a default log file
            if not current_log_file:
                current_log_file = log_files[0]

            lines = self._read_logfile(current_log_file['filepath'], max_lines)

        # process lines from log file
        if lines:
            columns, lines = self._process_logfile_lines(lines)

        # extend breadcrumbs with selected log file
        if current_log_file:
            breadcrumbs = breadcrumbs + [(
                current_log_file['filepath'], current_log_file['filename'])]

        # update report
        report.update({
            'columns': columns,
            'log_files': log_files,
            'log_files_map': log_files_map,
            'lines': lines,
            'current_log_file': current_log_file,
        })
        return report

    # TODO: class LogScanner - make _list_logfiles() a private function
    def _list_logfiles(self):
        """Identify all log files handled by Python or Zope."""
        result = []

        try:  # since Python-2.3.0
            import logging
        except ImportError:
            logging = None

        # Python's logging
        if logging:
            handlers = []

            # since Python-3.12.0
            if hasattr(logging, 'getHandlerNames'):
                for name in logging.getHandlerNames():
                    handler = logging.getHandlerByName(name)
                    handlers.append(handler)

            # since Python-2.4.2
            elif hasattr(logging, '_handlerList'):
                logging._acquireLock()
                for weak_handler in logging._handlerList:
                    handler = weak_handler()
                    if handler is not None:
                        handlers.append(handler)
                logging._releaseLock()

            # since Python-2.3.0
            elif hasattr(logging, '_handlers'):
                logging._acquireLock()
                for handler in logging._handlers.keys():
                    handlers.append(handler)
                logging._releaseLock()

            # add all handlers with filenames to result
            for handler in handlers:
                if hasattr(handler, 'baseFilename'):
                    result.append({
                        'filepath': handler.baseFilename,
                        'filename': basename(handler.baseFilename),
                    })

        # Zope's zLOG
        elif MinimalLogger:
            destination = MinimalLogger._log_dest

            # add handler to result (there can only be one)
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

    # TODO: class LogScanner - make _read_logfile() a private function
    def _read_logfile(self, filepath, max_lines):
        """Read lines from the end of the specified file."""
        lines = []

        # verify validity of filepath
        filepath_found = False
        for log_file in self._list_logfiles():
            if filepath == log_file['filepath']:
                filepath_found = True
                break

        # read a limited number of lines from the end of the file by using a
        # rotating buffer
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

    # TODO: class LogScanner - make _process_logfile_lines() a private function
    def _process_logfile_lines(self, source):
        """Identify log file format and reformat result accordingly."""
        lines = []
        first_line = source[0]

        # access log file
        if match(access_pattern, first_line):
            columns = access_pattern_columns[:]

            # iterate over each line
            for line in source:

                # attempt to split into columns
                matched_object = match(access_pattern, line)
                if matched_object:
                    lines.append(matched_object.groups())
                else:
                    lines.append([line])

        # format into a single column
        else:
            for line in source:
                lines.append([line])
            columns = ['Line']

        return columns, lines
