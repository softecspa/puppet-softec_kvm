#!/bin/bash

set -x

################################################
# Lorenzo Cocchi <lorenzo.cocchi@softecspa.it> #
# fix hostname, virt-sysprep lo mette in fqdn  #
################################################

SELF=$(basename $0)

fix_hostname() {
    local file_=${1:-'etc/hostname'}
    sed -i.bak -r 's/^((\w|\d)+(-\w+)?).*/\1\n/g' ${file_}
}

fix_hostname

[ $? -ne 0 ] && \
    { echo "${SELF}: error when fixing hostname"; exit 1; }
