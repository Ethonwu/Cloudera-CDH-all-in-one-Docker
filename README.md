## Cloudera CDH all in one Docker
* OS : CentOS 7.3
* DB : MariaDB
* Cloudera Manager Version : 5.16.2
* CDH Version : 5.16.2
---
## Usage 
### Open and run

```bash
docker run -v /root/.ssh:/root/.ssh -v /etc/ssh:/etc/ssh -v /etc/sshd:/etc/sshd --privileged=true --sysctl net.ipv6.conf.all.disable_ipv6=1 -it -p 7180:7180 -p 8888:8888 -p 2222:22 ethonwu/cloudera-cdh5-quickstart:finish_install
```
### 0 to All service build 

```bash
git clone https://github.com/Ethonwu/Cloudera-CDH-all-in-one-Docker
cd Cloudera-CDH-all-in-one-Docker
docker build . -t cloudera_tmp
docker volume create --name cloudera_tmp
docker run -v cloudera:/opt/ --privileged=true --sysctl net.ipv6.conf.all.disable_ipv6=1 -it -p 7180:7180 -p 8888:8888 cloudera_tmp
docker tag -m "Install finfsh" cloudera_tmp cloudera 
cd mount_vol/
docker build . -t cloudera_run
docker run -v /root/.ssh:/root/.ssh -v /etc/ssh:/etc/ssh -v /etc/sshd:/etc/sshd --privileged=true --sysctl net.ipv6.conf.all.disable_ipv6=1 -it -p 7180:7180 -p 8888:8888 -p 2222:22 cloudera_run
```

###  Run on all service ready container 
#### If use AWS or GCP , need using ssh login container 

```
docker run -v /root/.ssh:/root/.ssh -v /etc/ssh:/etc/ssh -v /etc/sshd:/etc/sshd --privileged=true --sysctl net.ipv6.conf.all.disable_ipv6=1 -it -p 7180:7180 -p 8888:8888 -p 2222:22 ethonwu/cloudera-cdh5-quickstart:running
```


---
## Reference 
### Some script and service scripts reference
1. https://github.com/wangxf2000/OneNodeCDHCluster
2. Cloudera Quick start Docker image
---
## TODO
* [ ] Tag each type of stage , such as : CM Ready , Hive Impala tag , Spark2 Tag ...
* [ ] Troubleshooting docker volume create problem
* [x] Hugepage sys kernel setting
* [x] Location bug fix 
* [x] Use CM API install CM Service and All CDH Service and Depoly
* [x] Hostname bug 
* [x] Python deploy CMS
* [x] Upload to Dockerhub 
* [x] Can using ssh login 







