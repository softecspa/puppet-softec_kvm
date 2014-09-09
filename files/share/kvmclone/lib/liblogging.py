#!/usr/bin/env python

import logging
import logging.handlers
import sys

# https://docs.python.org/2.7/howto/logging-cookbook.html
# parte del codice su gentile concessione di Andrea Cappelli
# TODO: logging.handlers.TimedRotatingFileHandler

__version__ = (0, 0, 1)
__author__ = 'Lorenzo Cocchi <lorenzo.cocchi@softecspa.it>'


def setup_logging(name=None, filename=False, filemode='a', log_level='INFO',
                  fmt=None, datefmt=None, rotate=False, rotate_max_bytes=1024,
                  rotate_backup_count=10):
    """

    Level       Numeric value
    CRITICAL    50
    ERROR       40
    WARNING     30
    INFO        20
    DEBUG       10
    NOTSET      0

    """
    logger = logging.getLogger(name)

    if fmt is None:
        fmt = '%(asctime)s [%(levelname)s] %(name)s.%(module)s: %(message)s'

    formatter = logging.Formatter(fmt, datefmt)

    if filename is False:
        # to sys.stderr
        handler = logging.StreamHandler()
    elif filename == '-':
        # to sys.stdout
        handler = logging.StreamHandler(stream=sys.stdout)
    elif filename:
        if not rotate:
            handler = logging.FileHandler(filename, mode=filemode)
        else:
            handler = logging.handlers.RotatingFileHandler(
                filename,
                mode=filemode,
                maxBytes=rotate_max_bytes,
                backupCount=rotate_backup_count
            )
    else:
        handler = logging.NullHandler()

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, log_level))

    return logger


if __name__ == '__main__':
    log = setup_logging(name=__name__, log_level='DEBUG')
    for level in ('debug', 'info', 'warn', 'error', 'critical'):
        getattr(log, level)('foobar')
