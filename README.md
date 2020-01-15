## Cloudera CDH all in one Docker
* OS : CentOS 7.3
* DB : MariaDB
* Cloudera Manager Version : 5.16.2
* CDH Version : 5.16.2
---
## Start Cloudera Manager 
### Usage 
```bash
docker build . -t cloudera
docker run --privileged=true -it -p 7180:7180 cloudera:latest
```
---
## Reference 
### Some script and service scripts reference
1. https://github.com/wangxf2000/OneNodeCDHCluster
2. Cloudera Quick start Docker image
---
## TODO
* [ ] Hugepage sys kernel setting
* [ ] Use CM API install CM Service and All CDH Service and Depoly
* [ ] Upload to Dockerhub , and tag each type of stage , such as : CM Ready , Hive Impala tag , Spark2 Tag ...
