class softec_kvm (
  $extra_packages          = params_lookup( 'extra_packages' ),
  $enable_softec_guest_xml = params_lookup( 'enable_softec_guest_xml' ),
) inherits softec_kvm::params{
  include kvm

  package { $softec_kvm::extra_packages :
    ensure  => present
  }

  file { '/usr/share/kvmclone':
    ensure  =>  directory,
    source  =>  'puppet:///modules/softec_kvm/share/kvmclone',
    mode    =>  '0755',
    recurse =>  true,
    ignore  =>  '.pyc',
    owner   =>  'root',
    group   =>  'root',
  }

  file { '/usr/local/bin/guestclone':
    ensure  =>  'link',
    target  =>  '/usr/share/kvmclone/guestclone.py',
    require =>  [ File['/usr/share/kvmclone'], ],
  }

  if $enable_softec_guest_xml {
    nfs::mount { '/mnt/backup_vm':
      ensure         => absent,
      server         => 'str-vdisk.tetsuya.backplane',
      share          => '/backup_manipolo',
      client_options => $nfs_mount_options,
    } ->

    file { '/etc/libvirt/qemu/lucid.softecspa.it.xml':
      ensure => present,
      source => 'puppet:///modules/softec_private/etc/libvirt/qemu/lucid.softecspa.it.xml',
      owner  => 'root',
      group  => 'root',
      mode   => '0600',
      notify => Service['libvirt-bin'],
    } ->

    file { '/etc/libvirt/qemu/precise.softecspa.it.xml':
      ensure => present,
      source => 'puppet:///modules/softec_private/etc/libvirt/qemu/precise.softecspa.it.xml',
      owner  => 'root',
      group  => 'root',
      mode   => '0600',
      notify => Service['libvirt-bin'],
    }

    service { 'libvirt-bin':
      ensure => running
    }
  }
}
