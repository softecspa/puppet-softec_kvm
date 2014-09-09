import types

__version__ = (0, 0, 1)
__author__ = 'Lorenzo Cocchi <lorenzo.cocchi@softecspa.it>'


def _join(iterable, sep=' ', strip_newline=True):
    if isinstance(iterable, (list, tuple, types.GeneratorType)):
        if strip_newline is not True:
            return sep.join(str(i) for i in iterable)
        return sep.join(str(i).strip() for i in iterable)

    return iterable


def fmt_called_processor_error(class_subprocess_called_process_error):
    c = class_subprocess_called_process_error
    fmt_ = '"{}" ({} {}) {}'.format(_join(c.cmd),
                                    'exit status',
                                    c.returncode,
                                    c.output.strip())
    return fmt_
