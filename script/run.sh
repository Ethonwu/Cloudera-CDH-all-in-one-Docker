#!/bin/bash
echo never > /sys/kernel/mm/transparent_hugepage/defrag
#get_now_hostnsme=$(hostname)
#new_hostname=$HOSTNAME
#echo $new_hostname > /etc/hostname
#sed -i 's/$get_now_hostnsme/$new_hostname/g' /etc/hosts
/etc/init.d/cloudera-quickstart-init start
/usr/sbin/sshd
/etc/init.d/mysql start
wget https://archive.cloudera.com/spark2/csd/SPARK2_ON_YARN-2.4.0.cloudera1.jar -P /opt/cloudera/csd/
chown cloudera-scm:cloudera-scm /opt/cloudera/csd/*
chmod 644 /opt/cloudera/csd/*
/etc/init.d/cloudera-scm-agent start
/etc/init.d/cloudera-scm-server start 
#tailf /var/log/cloudera-scm-server/cloudera-scm-server.log
while [ `curl -s -X GET -u "admin:admin"  http://localhost:7180/api/version` -z ] ;
    do
    echo "waiting 10s for CM to come up..";
    sleep 10;
done
python2.7 create_cluster.py
#curl -X POST -u admin:admin -H "Content-Type: application/json" -d @cdh5_service_template.json http://127.0.0.1:7180/api/v19/cm/importClusterTemplate?addRepositories=true
curl -X POST -u admin:admin -H "Content-Type: application/json" -d @new.json http://127.0.0.1:7180/api/v19/cm/importClusterTemplate?addRepositories=true
#sh ./CM_service_change.sh stop 
exec bash
