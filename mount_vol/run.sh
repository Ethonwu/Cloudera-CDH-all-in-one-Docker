#!/bin/bash
echo never > /sys/kernel/mm/transparent_hugepage/defrag
/etc/init.d/cloudera-quickstart-init start
/usr/sbin/sshd
/etc/init.d/mysql start
/etc/init.d/cloudera-scm-agent start
/etc/init.d/cloudera-scm-server
exec bash
