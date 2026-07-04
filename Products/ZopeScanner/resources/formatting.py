# -*- coding: iso-8859-15 -*-
# ============================================================================
#
#                          Z o p e   S c a n n e r
#
# ------------------------------------------------------------------------------
# Copyright (c) 2009-2012, Sebastian Lühnsdorf - Web-Solutions
# For more information see the README.txt file or visit www.zope.biz/scanner
# ------------------------------------------------------------------------------
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
# ============================================================================

__doc__ = """ZopeScanner Formatting Resources

$Id: resources/formatting.py 8 2012-12-09 11:37:00Z sfluehnsdorf $
"""

__version__ = '$Revision: 1.3 $'[11:-2]



# ============================================================================
# Imports

from imports import DTMLFile, html_quote


_table = '''<div class="box"><table width="100%" cellspacing="0" cellpadding="2" border="0">\n'''
_table_end = '''</table></div>\n'''
_th_row = '''  <tr class="list-header">\n'''
_th_row_end = '''  </tr>\n'''
_th = '''    <th align="left" valign="top"><div class="list-item">'''
_th_fw = '''    <th align="left" valign="top" width="80%"><div class="list-item">'''
_th_end = '''</div></th>\n'''
_td_row_odd = '''  <tr class="hover row-normal">\n'''
_td_row_even = '''  <tr class="hover row-hilite">\n'''
_td_rows = [_td_row_even, _td_row_odd]
_td_row_end = '''  </tr>\n'''
_td = '''    <td align="left" valign="top"><div class="list-item">'''
_td_end = '''</div></td>\n'''


class Formatting:

    report_form = DTMLFile('report', globals())

    def group_list(self, listitems):
        result = []
        batch_size = self.batch_size
        listitems_len = len(listitems)
        for batch_start in range(0, listitems_len, batch_size):
            batch_end = min(batch_start + batch_size, listitems_len)
            result.append((
                listitems[batch_start][0],
                '%s - %s' % (listitems[batch_start][0], listitems[batch_end - 1][0]),
                listitems[batch_start: batch_end]
            ))
        return result

    def format_value(self, value, form_id, path, id):
        value_type = type(value)
        if value_type is self._none_type:
            return self._format_none(value, form_id, path, id)
        elif value_type in self._sequence_types.keys():
            return self._format_sequence(value, form_id, path, id)
        elif value_type in self._mapping_types.keys():
            return self._format_mapping(value, form_id, path, id)
        elif value_type in self._linkable_types.keys():
            return self._format_linkable(value, form_id, path, id)
        elif value_type is self._boolean_type:
            return self._format_boolean(value, form_id, path, id)
        elif value_type in self._misc_types.keys():
            return self._format_misc(value, form_id, path, id)
        else:
            return self._format_other(value, form_id, path, id)

    def _format_none(self, value, form_id, path, id):
        return ""  # TODO

    def _format_sequence(self, value, form_id, path, id):
        return ""  # TODO

    def _format_mapping(self, value, form_id, path, id):
        return ""  # TODO

    def _format_linkable(self, value, form_id, path, id):
        return ""  # TODO

    def _format_boolean(self, value, form_id, path, id):
        return ""  # TODO

    def _format_misc(self, value, form_id, path, id):
        return ""  # TODO

    def _format_other(self, value, form_id, path, id):
        return ""  # TODO

    def format_label(self, label):
        id, title = label
        return '%s (%s)' % (id and html_quote(id) or '<em>Unnamed</em>', title and html_quote(title) or '<em>Untitled</em>')

    def format_value(self, value, form_id, path, id):
        value_type = type(value)
        if value_type is self._none_type:
            return '<em>None</em>'
        elif value_type in self._sequence_types.keys():
            return self.format_sequence(value, form_id, path, id)
        elif value_type in self._mapping_types.keys():
            return self.format_mapping(value, form_id, path, id)
        elif value_type in self._linkable_types.keys():
            return self.format_linkable(value, form_id, path, id)
        elif value_type is self._boolean_type:
            return self.format_boolean(value, form_id, path, id)
        elif value_type in self._misc_types.keys():
            return self.format_misc(value, form_id, path, id)
        else:
            return self.format_other(value, form_id, path, id)

    def format_sequence(self, value, form_id, path, id):
        format_value = self.format_value
        counter = 1
        result = '<b>%s</b>:<br />' % self._sequence_types[type(value)]
        result = result + _table
        result = result + _th_row + _th + '#' + _th_end + _th_fw + 'Item' + _th_end + _th_row_end
        for item in value:
            result = result + _td_rows[counter % 2] + _td + str(counter) + _td_end + _td + format_value(item, form_id, '%s/%s' % (path, id), counter - 1) + _td_end + _td_row_end
            counter = counter + 1
        result = result + _table_end
        return result

    def format_mapping(self, value, form_id, path, id):
        format_value = self.format_value
        counter = 1
        keys = value.keys()
        keys.sort()
        result = '<b>%s</b>:<br />' % self._mapping_types[type(value)]
        result = result + _table
        result = result + _th_row + _th + 'Key' + _th_end + _th_fw + 'Value' + _th_end + _th_row_end
        for key in keys:
            result = result + _td_rows[counter % 2] + _td + format_value(key, form_id, None, None) + _td_end + _td + format_value(value[key], form_id, '%s/%s' % (path, id), key) + _td_end + _td_row_end
            counter = counter + 1
        result = result + _table_end
        return result

    def format_linkable(self, value, form_id, path, id):
        try:
            result = '<b>%s</b>: <a href="%s">%s</a>' % (self._linkable_types[type(value)], self.get_link_url(form_id, path, id), html_quote(repr(value)))
        except:
            result = '<b>%s</b>: %s' % (self._linkable_types[type(value)], html_quote(repr(value)))
        try:
            if value.__doc__:
                #result = result + '<br /><em>%s</code></em>' % html_quote(repr(value.__doc__))
                result = result + '<br /><pre style="margin: 0;"><code>%s</code></pre>' % html_quote(value.__doc__)
        except:
            pass
        return result

    def format_boolean(self, value, form_id, path, id):
        return '<b>Boolean</b>: <span style="background: %s">&nbsp; &nbsp;</span> %s' % (value and '#00aa00' or '#dd0000', html_quote(repr(value)))

    def format_misc(self, value, form_id, path, id):
        return '<b>%s</b>: %s' % (self._misc_types[type(value)], html_quote(repr(value)))

    def format_form_and_image_classes(self, value, form_id, path, id):
        if value.__class__ in self._form_and_image_classes.keys():
            return '<b>%s</b>: <a href="%s">%s</a>' % (self._form_and_image_classes[value.__class__], self.get_link_url(form_id, path, id), html_quote(repr(value)))
        else:
            raise

    def format_other(self, value, form_id, path, id):
        try:
            result = self.format_image_classes(self, value, form_id, path, id)
        except:
            if hasattr(value, 'meta_type'):
                try:
                    result = '<b>%s</b>: <a href="%s"><img src="%s" border="0" /> %s</a>' % (value.meta_type, self.get_link_url(form_id, path, id), value.icon, self.format_label(self.get_object_label(value)))
                except:
                    result = '<b>%s</b>: <img src="%s" border="0" /> %s' % (value.meta_type, value.icon, self.format_label(self.get_object_label(value)))
            else:
                try:
                    result = '<b>Unknown</b>: <a href="%s">%s</a>' % (self.get_link_url(form_id, path, id), html_quote(repr(value)))
                except:
                    result = '<b>Unknown</b>: %s' % html_quote(repr(value))
        try:
            if value.__doc__:
                #result = result + '<br /><em>%s</em>' % html_quote(repr(value.__doc__))
                result = result + '<br /><pre style="margin: 0;"><code>%s</code></pre>' % html_quote(value.__doc__)
        except:
            pass
        return result

