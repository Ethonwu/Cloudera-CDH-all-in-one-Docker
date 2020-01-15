#!/bin/bash
    DOCKER=true
#
# Configure Cloudera QuickStart environment
#
# chkconfig: 345 70 30
# description: Configure Cloudera QuickStart environment
#
### BEGIN INIT INFO
# Provides:          cloudera-quickstart-init
# Short-Description: Configure Cloudera QuickStart environment
# Default-Start:     3 4 5
# Default-Stop:      0 1 2 6
# Required-Start:    $network
# Required-Stop:     $network
# Should-Start:
# Should-Stop:
### END INIT INFO

set -vx

if [ "$1" == "start" ] ; then
    if [ "${EC2}" == 'true' ]; then
        FIRST_BOOT_FLAG=/var/lib/cloudera-quickstart/.ec2-key-installed
        if [ ! -f "${FIRST_BOOT_FLAG}" ]; then
            METADATA_API=http://169.254.169.254/latest/meta-data
            KEY_URL=${METADATA_API}/public-keys/0/openssh-key
            SSH_DIR=/home/cloudera/.ssh
            mkdir -p ${SSH_DIR}
            chown cloudera:cloudera ${SSH_DIR}
            curl ${KEY_URL} >> ${SSH_DIR}/authorized_keys
            touch ${FIRST_BOOT_FLAG}
        fi
    fi
    if [ "${DOCKER}" != 'true' ]; then
        if [ -f /sys/kernel/mm/redhat_transparent_hugepage/defrag ]; then
            echo never > /sys/kernel/mm/redhat_transparent_hugepage/defrag
        fi

        cloudera-quickstart-ip
        HOSTNAME=quickstart.cloudera
        hostname ${HOSTNAME}
        sed -i -e "s/HOSTNAME=.*/HOSTNAME=${HOSTNAME}/" /etc/sysconfig/network
    fi

    (
        cd /var/lib/cloudera-quickstart/tutorial;
        nohup python -m SimpleHTTPServer 80 &
    )

    # TODO: check for expired CM license and update config.js accordingly
fi

