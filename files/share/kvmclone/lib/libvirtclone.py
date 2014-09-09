import os
import re
import subprocess
import tempfile
from libsp import CheckOutput

__version__ = (0, 0, 1)
__author__ = 'Lorenzo Cocchi <lorenzo.cocchi@softecspa.it>'


class VirtClone(CheckOutput):

    def __init__(self, stderr_to_stdout=True, sudo=False, shell=False):
        super(VirtClone, self).__init__(stderr_to_stdout, sudo, shell)

    def guest_is_alive(self, guest_name):
        e_pattern = '{}\s+running'.format(re.escape(guest_name))
        pattern = re.compile(e_pattern)
        cmd = 'virsh list'
        guest_status = self.check_output(cmd)

        if pattern.search(guest_status, re.MULTILINE):
            return True
        return False

    # Ubuntu 14.04
    # def guest_is_alive(self, guest_name):
    #    pattern = re.escape(guest_name)
    #    cmd = 'virsh list --state-running --name'
    #    guest_status = self.check_output(cmd)
    #
    #    if re.search(pattern, guest_status, re.MULTILINE):
    #        return True
    #    return False

    def lv_size(self, lv_path, unit='B'):
        cmd = 'lvs -o lv_size --unit={} --noheading {}'.format(unit, lv_path)
        _size = self.check_output(cmd)
        size = re.sub('^\s+(.+)', r'\1', str(_size).strip())
        return size

    def lv_create(self, lv_size, vg_name, lv_name):
        cmd = 'lvcreate --size {} {} -n {}'.format(lv_size, vg_name, lv_name)
        return self.check_output(cmd)

    def qemu_disk_size(self, disk_path):
        cmd = 'qemu-img info {}'.format(disk_path)
        output = self.check_output(cmd)
        pattern = re.compile('\(([0-9]+)\sbytes\)')
        _size = pattern.search(output)
        size = '{}{}'.format(_size.group(1), 'B')
        return size

    def guest_disk_name(self, guest_name, suffix='disk'):
        name = guest_name.split('.')[0]
        disk_name = '{}_{}'.format(name, suffix)
        return disk_name

    def virt_clone(self, src_guest_name, dst_guest_name, dst_guest_disk,
                   write_xml_only=False, xml_path='/etc/libvirt/qemu'):

        virt_clone = 'virt-clone -o {} -n {} -f {}'.format(src_guest_name,
                                                           dst_guest_name,
                                                           dst_guest_disk)

        if write_xml_only is True:
            xml_filename = '{}/{}.{}'.format(xml_path, dst_guest_name, 'xml')
            if os.path.exists(xml_filename) is True:
                raise OSError('{}: {}'.format(xml_filename, 'already exists!'))

            virt_clone_xml = '{} --print-xml'.format(virt_clone)
            reload_libvirt = 'service libvirt-bin reload'
            xml_out = self.check_output(virt_clone_xml)

            tmpfile = tempfile.NamedTemporaryFile(dir='/tmp', delete=False)
            tmpfile.write(xml_out)
            tmpfile.flush()

            copy = 'cp {} {}'.format(tmpfile.name, xml_filename)

            try:
                self.check_output(copy)
            except subprocess.CalledProcessError:
                raise
            finally:
                tmpfile.unlink(tmpfile.name)

            libvirt_out = self.check_output(reload_libvirt)
            if libvirt_out == '':
                return 'reloading libvirt-bin'
            else:
                return libvirt_out

        return self.check_output(virt_clone)

    def virt_resize_method(self, src_disk_size, dst_disk_size):
        if dst_disk_size > src_disk_size:
            if (dst_disk_size - src_disk_size) > 161:
                return '--expand'
        elif dst_disk_size < src_disk_size:
            return '--shrink'

    def virt_resize(self, src_guest_disk, dst_guest_disk, method, partition,
                    lv, lv_expand=False):

        cmd = 'virt-resize {} {} {} {}'.format(src_guest_disk,
                                               dst_guest_disk,
                                               method,
                                               partition)
        if lv_expand is True:
            cmd = '{} --LV-expand {}'.format(cmd, lv)

        return self.check_output(cmd)

    def sysprep(self, sysprep_enable, domain, sysprep_script=None):
        cmd = 'virt-sysprep -d {} --enable {}'.format(domain, sysprep_enable)

        if re.search(',?hostname,?', sysprep_enable):
            cmd = '{} --hostname {}'.format(cmd, domain)

        if re.search(',?script,?', sysprep_enable):
            if sysprep_script is None:
                raise OSError('virt-sysprep required PATH of sysprep script')
            cmd = '{} --script {}'.format(cmd, sysprep_script)

        return self.check_output(cmd)
