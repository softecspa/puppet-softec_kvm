class softec_kvm::guest (
  $acpid_package = params_lookup( 'acpid_package' ),
) inherits softec_kvm::params {

  package { $softec_kvm::guest::acpid_package :
    ensure  => installed
  }

# serve er far funzionare la console di virsh se la macchina e' installata tramite ISO.
  case $::lsbdistcodename  {
    'hardy': {
      file {'/etc/event.d/ttyS0':
        ensure  => present,
        mode    => 644,
        owner   => 'root',
        group   => 'root',
        source  => 'puppet:///modules/kvm/etc/ttyS0.conf',
      }

      file_line {'start-ttyS0':
        path  => '/etc/rc.local',
        line  => 'initctl start ttyS0'
      }
    }
    default : {
      file { '/etc/init/ttyS0.conf':
        ensure  => present,
        mode    => 644,
        owner   => 'root',
        group   => 'root',
        source  => 'puppet:///modules/kvm/etc/ttyS0.conf',
      }
    }
  }
}
