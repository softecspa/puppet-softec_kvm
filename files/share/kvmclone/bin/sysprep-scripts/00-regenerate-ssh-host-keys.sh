#!/bin/bash

set -x

################################################
# Lorenzo Cocchi <lorenzo.cocchi@softecspa.it> #
# rigenerazione SSH host keys                  #
################################################

SELF=$(basename $0)

regenerate_ssh_host_keys() {
    rm -f etc/ssh/ssh_host_rsa_key{,.pub}   2>/dev/null
    rm -f etc/ssh/ssh_host_dsa_key{,.pub}   2>/dev/null
    rm -f etc/ssh/ssh_host_ecdsa_key{,.pub} 2>/dev/null

    ssh-keygen -q -h -N '' -t rsa   -f etc/ssh/ssh_host_rsa_key
    ssh-keygen -q -h -N '' -t dsa   -f etc/ssh/ssh_host_dsa_key
    ssh-keygen -q -h -N '' -t ecdsa -f etc/ssh/ssh_host_ecdsa_key
}

regenerate_ssh_host_keys

[ $? -ne 0 ] && \
    { echo "${SELF}: error when generating ssh host keys"; exit 1; }
