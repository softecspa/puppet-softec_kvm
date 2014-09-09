class softec_kvm::params {
  case $::operatingsystem {
    'ubuntu', 'debian': {
      $extra_packages = ['ubuntu-virt-server', 'virtinst', 'vlan',
                         'cpu-checker', 'libguestfs-tools', 'kpartx',
                         'virt-top', 'guestmount',]
      $acpid_package  = 'acpid'
    }
    default : {
      fail("Operating system ${::operatingsystem} is not supported")
    }
  }
}
