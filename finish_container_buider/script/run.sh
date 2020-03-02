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
run_id=$(sh CM_service_change.sh start | jq '.id')
echo "Command id is : $run_id"
echo "waiting for start all service..";
while [ $(curl -s -X GET -u "admin:admin" http://127.0.0.1:7180/api/v19/commands/$run_id | jq '.success') = 'null' ] ;
    do
    echo -ne '[ᗧ·····························]\r'
    sleep 1
    echo -ne '[    ᗧ·························]\r'
    sleep 1
    echo -ne '[         ᗧ····················]\r'
    sleep 1
    echo -ne '[              ᗧ···············]\r'
    sleep 1
    echo -ne '[                   ᗧ··········]\r'
    sleep 1
    echo -ne '[                       ᗧ······]\r'
    sleep 1
    echo -ne '[                             ᗧ]\r'
    sleep 1
    echo -ne '[·····························ᗤ]\r'
    sleep 1
    echo -ne '[·························ᗤ    ]\r'
    sleep 1
    echo -ne '[··················ᗤ           ]\r'
    sleep 1
    echo -ne '[···············ᗤ              ]\r'
    sleep 1
    echo -ne '[···········ᗤ                  ]\r'
    sleep 1
    echo -ne '[·······ᗤ                      ]\r'
    sleep 1
    echo -ne '[···ᗤ                          ]\r'
    sleep 1
    echo -ne '[ᗤ                             ]\r'
    sleep 1
done
echo -ne "Successful start service\n"
exec bash
