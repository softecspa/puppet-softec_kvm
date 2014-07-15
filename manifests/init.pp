class softec_kvm (
  $extra_packages = params_lookup( 'extra_packages' ),

) inherits softec_kvm::params{
  include kvm

  package { $softec_kvm::extra_packages :
    ensure  => present
  }
}
