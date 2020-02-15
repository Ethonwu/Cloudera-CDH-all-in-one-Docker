#!/bin/bash
#curl -X POST -u "admin:admin" http://127.0.0.1:7180/api/v19/cm/service/commands/$1
curl -X POST -u "admin:admin" http://127.0.0.1:7180/api/v19/clusters/Cluster%201/commands/$1

