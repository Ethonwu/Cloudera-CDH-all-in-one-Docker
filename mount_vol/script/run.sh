#!/bin/bash
echo never > /sys/kernel/mm/transparent_hugepage/defrag
/etc/init.d/cloudera-quickstart-init start
/usr/sbin/sshd
/etc/init.d/mysql start
/etc/init.d/cloudera-scm-agent start
/etc/init.d/cloudera-scm-server start 
while [ `curl -s -X GET -u "admin:admin"  http://localhost:7180/api/version` -z ] ;
    do
    echo "waiting 10s for CM to come up..";
    sleep 10;
done
sh CM_service_change.sh start
exec bash
