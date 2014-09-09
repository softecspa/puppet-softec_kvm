#!/bin/bash

####################################################
# Lorenzo Cocchi <lorenzo.cocchi@softecspa.it>     #
# Wrapper per eseguire script tramite virt-sysprep #
# Esegue i file con estensione `.sh` all'interno   #
#  di ${SCRIPTS_DIR}                               #
#                                                  #
# NOTE: lo script deve essere eseguibile           #
# Utilizzo:                                        #
#  virt-sysprep -d domain-name --enable script \   #
#    --script PATH/SELF                            #
####################################################

# deve essere un PATH assoluto!
SCRIPTS_DIR="/home/fuffax/kvmclone/bin/sysprep-scripts"

for item in $(ls ${SCRIPTS_DIR}); do
    script_="${SCRIPTS_DIR}/${item}"
    if (echo ${script_} | egrep -q '\.sh$'); then
        /bin/bash ${script_}
    fi
done
