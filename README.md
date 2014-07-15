puppet-softec\_kvm
=================

wrapper of puppetlabs-kvm module with some customization.

####Table of Contents

1. [Module Description - What the module does and why it is useful](#module-description)
2. [Setup - The basics of getting started with [Modulename]](#setup)
 * [Setup requirements](#setup-requirements)
3. [Limitations - OS compatibility, etc.](#limitations)

##Module Description
this module install qemu-kvm through puppetlabs-vm module. In addiction it install:

* ubuntu-virt-server
 * virtinst
 * vlan

Module also add the define softec\_kvm::guest to use on guest machines. It fix console access in case of guests instaleld by ISO.

##Setup
on Dom0:
    include softec_kvm

on guests
    include softec_kvm::guests


###Setup Requirements
Module requires puppetlabs-kvm module

## Limitations
Module only works on Ubuntu|Debian
