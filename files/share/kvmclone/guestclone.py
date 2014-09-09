#!/usr/bin/env python

import os
import sys

if sys.version_info[:2] < (2, 7):
    raise SystemExit('Sorry, this script require Python >= 2.7')

libpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
try:
    sys.path.insert(0, os.path.realpath(os.environ['MYLIBDIR']))
except KeyError:
    sys.path.insert(0, libpath)

try:
    import argparse
    import libargparse
    import libconfigparser3
    import liblogging
    import libvirtclone
    from libutils2 import _join, fmt_called_processor_error
except ImportError as e:
    raise SystemExit('{} {}'.format('Import Error:', e))

import subprocess
import traceback

__version__ = (0, 0, 1)
__author__ = 'Lorenzo Cocchi <lorenzo.cocchi@softecspa.it>'


def parse_argv(parent_parser):
    parser = argparse.ArgumentParser(description='Kvm Guest Clone',
                                     parents=[parent_parser])
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def default_configfile():
    file_realpath = os.path.realpath(__file__)
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(file_realpath)), 'conf')
    file_name = os.path.splitext(os.path.split(__file__)[1])[0]
    config_name = '{}.{}'.format(file_name, 'conf')
    config_file = os.path.join(config_path, config_name)

    return config_file


def main():
    parent_parser = libargparse.parse_argv()
    parent_parser.set_defaults(config_file=default_configfile())
    args = parse_argv(parent_parser)

    (config_file,
     guest_name,
     log_level,
     sudo,
     dst_lv_size,
     os_variant) = (args.config_file,
                    args.guest_name,
                    args.log_level,
                    args.sudo,
                    args.lv_size,
                    args.os_variant)

    scriptname = os.path.basename(__file__)

    # objects
    log_fmt = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    log = liblogging.setup_logging(name=scriptname,
                                   filename='-',
                                   log_level=log_level,
                                   fmt=log_fmt)
    clone = libvirtclone.VirtClone(sudo=sudo)

    try:
        configparser = libconfigparser3.Parser(config_file)
        hv = configparser.get_nmdict('hypervisor')
        guest = configparser.get_nmdict(os_variant)

        src_guest_name = guest['name']
        src_guest_disk_path = guest['disk_path']
        src_guest_disk_size = None
        src_guest_disk_type = guest['disk_type']
        src_guest_partition = guest['partition']
        src_guest_lgvol = guest['lg_vol']
        sysprep_execute = guest['sysprep_execute']
        sysprep_enable = guest['sysprep_enable']
        sysprep_script = guest.get('sysprep_script', None)

        dst_lv_name = clone.guest_disk_name(guest_name)
        dst_vg_name = hv['vg_name']

        # il guest di origine deve essere spento
        if clone.guest_is_alive(src_guest_name) is True:
            log.error('{} {}'.format(src_guest_name, 'must be shut off!'))
            sys.exit(1)

        if src_guest_disk_type == 'lvm':
            get_size = clone.lv_size
        elif src_guest_disk_type == 'qemu':
            get_size = clone.qemu_disk_size
        else:
            log.error('disk_type must to be `lvm` or `qemu`')
            sys.exit(1)

        # dimensione del Logical Volume di destinazione
        if dst_lv_size is not None:
            dst_guest_disk_size = dst_lv_size
        else:
            src_guest_disk_size = get_size(src_guest_disk_path)
            dst_guest_disk_size = src_guest_disk_size

        # creazione del Logical Volume
        lv_create_stdout = clone.lv_create(dst_guest_disk_size,
                                           dst_vg_name,
                                           dst_lv_name)
        log.info(lv_create_stdout.strip())

        # full PATH del Logical Volume di destinazione
        dst_guest_disk = os.path.join('/dev', dst_vg_name, dst_lv_name)

        # variabili con dimensioni del disco di origine e destinazione
        if src_guest_disk_size is None:
            src_guest_disk_size = get_size(src_guest_disk_path)
            dst_guest_disk_size = get_size(dst_guest_disk)

        resize_method = clone.virt_resize_method(
            int(src_guest_disk_size[:-1]), int(dst_guest_disk_size[:-1]))

        write_xml_only = False if resize_method is None else True
        log.info('disk clone, please wait...')

        write_xml_only_str = '{}={}'.format('write_xml_only', write_xml_only)
        log.debug(_join(['virt-clone', src_guest_name, guest_name,
                         dst_guest_disk, write_xml_only_str]))

        virt_clone_stdout = clone.virt_clone(src_guest_name,
                                             guest_name,
                                             dst_guest_disk,
                                             write_xml_only)
        log.debug(virt_clone_stdout)

        if write_xml_only is True or resize_method is not None:
            log.debug(_join(['virt-resize', src_guest_disk_path,
                             dst_guest_disk, resize_method,
                             src_guest_partition, src_guest_lgvol,
                             'lv_expand=False']))

            resize_stdout = clone.virt_resize(src_guest_disk_path,
                                              dst_guest_disk,
                                              resize_method,
                                              src_guest_partition,
                                              src_guest_lgvol,
                                              lv_expand=False,)
            log.debug(resize_stdout.rstrip())

        log.info('disk clone successfully')

        if sysprep_execute == 'True':
            log.info('starting sysprep')
            sysprep_out = clone.sysprep(sysprep_enable,
                                        guest_name,
                                        sysprep_script)
            log.debug(sysprep_out)
            log.info('sysprep successfully')

        log.info('clone successfully')
    except subprocess.CalledProcessError as e:
        log.error(fmt_called_processor_error(e))
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        sys.exti(1)
    except Exception as e:
        los = traceback.format_exception_only(type(e), e)
        log.error(_join(los))
        sys.exit(1)


if __name__ == '__main__':
    main()
