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

__doc__ = """ZopeScanner LogScanner"""

__version__ = '$Revision: 1.3 $'[11:-2]


# =============================================================================
# Module Imports

from resources.imports import DTMLFile, INSTANCE_HOME, compile, ctime, exists,\
    join, match


# =============================================================================
# Regular Expressions

access_pattern = compile('(.*) - (.*) \[(.*)\] "(.*)" (.*) (.*) "(.*)" "(.*)"')
event_pattern = compile('(\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d) (.*?) (.*)')


# =============================================================================
# LogScanner Mix-in Class

class LogScanner:
    """LogScanner Mix-in Class"""

    scan_logfile_form = DTMLFile('logs', globals())

    def scan_logfile(self, path='', REQUEST=None):
        """Scan Log File

        Scan the log file specified by path, applying a variety of batch and
        filter options. This method only processes options and prepares for the
        actual log file reading. See the read_logfile() method below for actual
        file access.
        """

        breadcrumbs = [
            self.breadcrumbs_root,
            ('scan_logfile_form', 'Log Files')
            ]

        if path == '/':
            path = ''

        if path:
            now = self.ZopeTime()
            try:
                date_start = REQUEST.get('date_start', 'x')
                if self.ZopeTime(date_start) > now:
                    raise
            except:
                date_start = '%4d-%02d-%02d' % (now.year(), now.month(),
                                                now.day())
            try:
                date_end = REQUEST.get('date_end', 'x')
                if self.ZopeTime(date_end) > now or self.ZopeTime(date_end) <\
                        self.ZopeTime(date_start):
                    raise
            except:
                date_end = '%4d-%02d-%02d' % (now.year(), now.month(),
                                              now.day())
            result = {
                'log_batch_start': int(REQUEST.get('log_batch_start', 0)),
                'log_batch_size': int(REQUEST.get('log_batch_size',
                                                  self.batch_size)),
                'keywords': REQUEST.get('keywords', ''),
                'match_type': REQUEST.get('match_type', 'phrase'),
                'match_case': REQUEST.get('match_case', None),
                'date_start': date_start,
                'date_end': date_end,
                }
            if path == 'access.log':
                result['breadcrumbs'] = breadcrumbs + [
                    ('scan_logfile_form?path=access.log', 'Access Log')
                    ]
            elif path == 'error.log':
                result['breadcrumbs'] = breadcrumbs + [
                    ('scan_logfile_form?path=error.log', 'Error Log')
                    ]
            elif path == 'event.log':
                result['breadcrumbs'] = breadcrumbs + [
                    ('scan_logfile_form?path=event.log', 'Event Log')
                    ]
            else:
                REQUEST.RESPONSE.redirect('%s/scan_logfile_form' %
                                          self.scanner_url())
            return result

        result = {}
        result['breadcrumbs'] = breadcrumbs
        return result

    def read_logfile(self, path, batch_start, batch_size, keywords, match_type,
                     match_case, date_start, date_end):
        """Read Log File

        Read the specified log file and limit and filter the resulting lines
        according to the specified options. This method ensures that only the
        intended files can be read.
        """

        columns = []
        lines = []

        date_start = self.ZopeTime(date_start).earliestTime()
        date_end = self.ZopeTime(date_end).latestTime()

        def match_none(line):
            return True

        def match_phrase(line):
            line = match_case and line or line.lower()
            if term in line:
                return True
            return False

        def match_all_words(line):
            line = match_case and line or line.lower()
            for term in terms:
                if not term in line:
                    return False
            return True

        def match_any_words(line):
            line = match_case and line or line.lower()
            for term in terms:
                if term in line:
                    return True
            return False

        if match_type == 'phrase':
            match_keywords = match_phrase
            term = match_case and keywords.strip() or keywords.lower().strip()
        elif match_type == 'all_words':
            match_keywords = match_all_words
            terms = match_case and keywords.strip().split(' ') or\
                keywords.lower().strip().split(' ')
        elif match_type == 'any_words':
            match_keywords = match_any_words
            terms = match_case and keywords.strip().split(' ') or\
                keywords.lower().strip().split(' ')
        else:
            match_keywords = match_none

        if path == 'access.log':
            filename = join(INSTANCE_HOME, 'log', 'Z2.log')
            if exists(filename):
                columns = ['IP', 'User', 'Date & Time', 'Request String',
                           'Code', 'Size', 'URL', 'Client']
                filehandle = open(filename, 'r')
                filelines = filehandle.readlines()
                filehandle.close()
                for fileline in filelines:
                    matchobject = match(access_pattern, fileline.strip())
                    if matchobject:
                        date = self.ZopeTime(matchobject.group(3))
                        if (date >= date_start and date <= date_end) and\
                                match_keywords(fileline):
                            lines.append(matchobject.groups())
                print date_start, date, date_end

        elif path == 'error.log':
            rootObject = self.getPhysicalRoot()
            errorLog = getattr(rootObject, '__error_log__', None)
            if errorLog:
                columns = ['Date & Time', 'Username', 'User Id', 'URL',
                           'Exception Type', 'Exception Value']
                entries = errorLog.getLogEntries()
                entries.reverse()
                for entry in entries:
                    date = self.ZopeTime(ctime(entry['time']))
                    if (date >= date_start and date <= date_end) and match_keywords(' '.join(map(lambda value: str(value), entry.values()))):
                        lines.append((ctime(entry['time']), entry['username'],
                                      entry['userid'], entry['url'],
                                      entry['type'], entry['value']))

        elif path == 'event.log':
            filename = join(INSTANCE_HOME, 'log', 'event.log')
            if exists(filename):
                columns = ['Date & Time', 'Level', 'Message']
                filehandle = open(filename, 'r')
                filelines = filehandle.readlines()
                filehandle.close()
                for fileline in filelines:
                    matchobject = match(event_pattern, fileline.strip())
                    if matchobject:
                        date = self.ZopeTime(matchobject.group(1))
                        if (date >= date_start and date <= date_end) and\
                                match_keywords(fileline):
                            lines.append(matchobject.groups())
                    elif fileline.strip() != '------' and lines:
                        line = list(lines[-1])
                        line[-1] = line[-1] + '\n' + fileline.strip()
                        lines[-1] = line
        lines.reverse()
        return {
            'columns': columns,
            'lines': lines[batch_start: batch_start + batch_size],
            'length': len(lines),
            }
