"""The  Parser  Class  implements  a  basic  configuration  file  parser
language which provides a structure similar to what you  would  find  on
Microsoft Windows INI files.

You can use this to write  Python  programs which can be customized by
end users easily.

"""

import sys
if sys.version_info[:2] < (2, 7):
    raise SystemExit('Sorry, require Python >= 2.7')

import codecs
import collections
import locale
import re

if sys.version_info[0] == 3:
    import configparser as ConfigParser
else:
    import ConfigParser

__version__ = (0, 0, 1)
__author__ = 'Lorenzo Cocchi <lorenzo.cocchi@softecspa.it>'


class Parser(ConfigParser.SafeConfigParser):

    def __init__(self, filenames, option_lower_case=True,
                 allow_no_value=False, encoding=None):
        """Keywords arguments:

        filenames         -- list of named configuration files,
                             a single filename is also allowed.
        option_lower_case -- if False (default: True) returns not lower-case
                             version of option
        allow_no_value    -- if True (default: False), options without
                              (if python >= 2.7) values are accepted
        encoding          -- charset, default locale encoding or 'utf-8'

        """

        if encoding is None:
            encoding = locale.getpreferredencoding() or 'utf-8'

        ConfigParser.SafeConfigParser.__init__(
            self, allow_no_value=allow_no_value)

        if option_lower_case is False:
            self.optionxform = str

        if isinstance(filenames, str):
            filenames = [filenames]

        for filename in filenames:
            with codecs.open(filename, 'r', encoding=encoding) as fh:
                self.readfp(fh)

    def get_sections(self, pattern=None):
        """Keywords arguments:

        pattern -- regexp pattern

        Returns list:
            [section1, section2, section3]

        """
        if pattern is None:
            return self.sections()

        p = re.compile(pattern)
        return [i for i in self.sections() if p.match(i)]

    def get_items(self, section, strip_quotes=False):
        """Keywords arguments:

        section      -- section name
        strip_quotes -- remove ' or " at the beginning or at the end of the
                        value

        Returns list of tuple
            [('opt1', 'val1'), ('opt2', 'val2')]

        """
        if strip_quotes is False:
            return self.items(section)
        else:
            return [(k, v.strip('\'"')) for (k, v) in self.items(section)]

    def get_nmdict(self, section, strip_quotes=False):
        """Keywords arguments:

        section      -- section name
        strip_quotes -- remove ' or " at the beginning or at the end of the
                        value

        Returns dict, ordered if python >= 2.7:
            {'name1:' 'value1', 'name2': 'value2' }

        """
        if not hasattr(collections, 'OrderedDict'):
            return {k: v for (k, v) in self.get_items(section, strip_quotes)}
        else:
            return collections.OrderedDict(
                self.get_items(section, strip_quotes))
