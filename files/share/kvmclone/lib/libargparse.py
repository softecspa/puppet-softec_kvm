try:
    import argparse
except ImportError as e:
    raise SystemExit('{} {}'.format('Import Error:', e))

__version__ = (0, 0, 1)
__author__ = 'Lorenzo Cocchi <lorenzo.cocchi@softecspa.it>'


class ArgParseBaseAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.func(parser, values))


class CheckLvmSizeSuffix(ArgParseBaseAction):
    def func(self, parser, values):
        suffix = 'bBsSkKmMgGtTpPeE'
        if values[-1] not in list(suffix):
            return parser.error('{} {}'.format(
                'valid Logical Volume suffix are:', ','.join(list(suffix))))
        return values


def parse_argv():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-c', '--config-file', action='store',
                        dest='config_file', type=str,
                        help='path of the configuration file')

    parser.add_argument('-n', '--guest-name', action='store',
                        dest='guest_name', type=str,
                        required=True, help='name of the new guest '
                        'virtual machine instance')

    parser.add_argument('-S', '--sudo', action='store_true', dest='sudo',
                        help='execute shell command with sudo, default False')

    parser.add_argument('-s', '--lv-size', action=CheckLvmSizeSuffix,
                        dest='lv_size', type=str,
                        help='Logical Volume size of the new guest')

    group0 = parser.add_argument_group('Log Level')
    group0.add_argument('-l', '--log-level', action='store', dest='log_level',
                        help='log level, default INFO', default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                 'CRITICAL'],)

    group1 = parser.add_argument_group('Guest Os Template')
    group1.add_argument('-o', '--os-template',
                        required=True, help='Guest Os Template',
                        choices=['ubuntulucid', 'ubuntuprecise',
                                 'ubuntutrusty'],
                        dest='os_variant')

    parser.add_argument('-v', '--version', help='print version and exit',
                        action="version",
                        version='{v[0]}.{v[1]}.{v[2]}'.format(v=__version__))
    return parser
