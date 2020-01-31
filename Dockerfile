FROM centos:7.3.1611
ENV HOSTNAME ethon.cloudera.com
RUN yum -y update; yum clean all
RUN echo  "vm.swappiness = 1" >> /etc/sysctl.conf
RUN yum install -y java-1.8.0-openjdk-devel vim wget curl git bind-utils tmux sudo ssh openssh-server 
RUN wget https://archive.cloudera.com/cm5/redhat/7/x86_64/cm/cloudera-manager.repo -P /etc/yum.repos.d/
RUN yum install -y cloudera-manager-daemons cloudera-manager-agent cloudera-manager-server
ADD script root/script
ADD conf root/conf
ADD cloudera-quickstart-ip usr/bin/
ADD cloudera-quickstart-init etc/init.d/
RUN cp /root/conf/maria.repo /etc/yum.repos.d/
RUN yum clean all && rm -rf /var/cache/yum/ && yum repolist && yum install -y MariaDB-server MariaDB-client
WORKDIR root/script/
RUN cat /root/conf/mariadb.config > /etc/my.cnf
RUN mkdir -p /var/log/mariadb/ && chown mysql:mysql -R /var/log/mariadb/ && chmod 755 -R /var/log/mariadb/
RUN wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.46.tar.gz -P ~
RUN tar zxf ~/mysql-connector-java-5.1.46.tar.gz -C ~
RUN mkdir -p /usr/share/java/
RUN cp ~/mysql-connector-java-5.1.46/mysql-connector-java-5.1.46-bin.jar /usr/share/java/mysql-connector-java.jar
RUN rm -rf ~/mysql-connector-java-5.1.46*
RUN /etc/init.d/mysql start && mysql -u root < /root/script/create_db.sql && mysql -u root < /root/script/secure_mariadb.sql && /usr/share/cmf/schema/scm_prepare_database.sh mysql scm scm cloudera
RUN chmod +x /root/script/run.sh
RUN echo "cloudera" | passwd --stdin root 
RUN /usr/sbin/sshd-keygen -A
RUN yum install -y epel-release && yum install -y python-pip && pip install --upgrade pip && pip install cm_client
RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
RUN echo "LANG=en_US.UTF-8" > /etc/locale.config
RUN localedef -i en_US -f UTF-8 en_US.UTF-8
RUN mkdir -p /opt/cloudera && chmod 755 -R /opt/cloudera && chown cloudera-scm:cloudera-scm -R /opt/cloudera/
WORKDIR /opt/cloudera
RUN ls /opt/cloudera/
RUN mkdir parcel-cache/ parcels/ && mkdir parcels/.flood/
RUN chmod 755 -R *
RUN chown cloudera-scm:cloudera-scm -R csd/ parcel-repo/ parcels/.flood/
#WORKDIR /opt/cloudera/parcel-repo/
#WORKDIR /root/
#RUN wget -q  http://archive.cloudera.com/cdh5/parcels/5.16.2/CDH-5.16.2-1.cdh5.16.2.p0.8-el7.parcel && wget -q http://archive.cloudera.com/cdh5/parcels/5.16.2/CDH-5.16.2-1.cdh5.16.2.p0.8-el7.parcel.sha1 && wget -q http://archive.cloudera.com/cdh5/parcels/5.16.2/manifest.json
#WORKDIR /opt/cloudera/parcel-repo/
#RUN chown cloudera-scm:cloudera-scm -R *
#RUN chmod 755 *
EXPOSE 7180
WORKDIR /root/
#ENTRYPOINT ["/bin/sh","run.sh"]
CMD ['/bin/sh']
