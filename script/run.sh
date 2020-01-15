#!/bin/bash
echo never > /sys/kernel/mm/redhat_transparent_hugepage/defrag
/etc/init.d/mysql start
/etc/init.d/cloudera-scm-agent start
/etc/init.d/cloudera-scm-server start 
tailf /var/log/cloudera-scm-server/cloudera-scm-server.log
