import shlex
import subprocess

__version__ = (0, 0, 1)
__author__ = 'Lorenzo Cocchi <lorenzo.cocchi@softecspa.it>'


class CheckOutput(object):

    def __init__(self, stderr_to_stdout=True, sudo=False, shell=False):
        self.stderr_to_stdout = stderr_to_stdout
        self.sudo = sudo
        self.shell = shell

    def check_output(self, cmd):
        if self.sudo is True:
            cmd = '{} {}'.format('sudo', cmd)

        cmd = shlex.split(cmd) if self.shell is False else cmd
        stderr = subprocess.PIPE

        if self.stderr_to_stdout is True:
            stderr = subprocess.STDOUT

        return subprocess.check_output(cmd, shell=self.shell, stderr=stderr)
