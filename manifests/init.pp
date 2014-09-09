class softec_kvm (
  $extra_packages = params_lookup( 'extra_packages' ),

) inherits softec_kvm::params{
  include kvm

  package { $softec_kvm::extra_packages :
    ensure  => present
  }

  file { '/usr/share/kvmclone':
    source  =>  'puppet:///modules/softec_kvm/share/kvmclone',
    ensure  =>  directory,
    mode    =>  0755,
    recurse =>  true,
    ignore  =>  '.pyc',
    owner   =>  'root',
    group   =>  'root',
  }

  file { '/usr/local/bin/guestclone':
    ensure    =>  'link',
    target    =>  '/usr/share/kvmclone/guestclone.py',
    require   =>  [ File['/usr/share/kvmclone'], ],
  }

}
