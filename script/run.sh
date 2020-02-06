#!/bin/bash
echo never > /sys/kernel/mm/transparent_hugepage/defrag
#get_now_hostnsme=$(hostname)
#new_hostname=$HOSTNAME
#echo $new_hostname > /etc/hostname
#sed -i 's/$get_now_hostnsme/$new_hostname/g' /etc/hosts
/etc/init.d/cloudera-quickstart-init start
/usr/sbin/sshd
/etc/init.d/mysql start
/etc/init.d/cloudera-scm-agent start
/etc/init.d/cloudera-scm-server start 
#tailf /var/log/cloudera-scm-server/cloudera-scm-server.log
while [ `curl -s -X GET -u "admin:admin"  http://localhost:7180/api/version` -z ] ;
    do
    echo "waiting 10s for CM to come up..";
    sleep 10;
done
python2.7 cdh5_install_cluster.py
#python2.7 create_cluster.py ./cm-deployment.json 
#sh ./CM_service_change.sh stop 
#tailf /var/log/cloudera-scm-server/cloudera-scm-server.log
exec bash
