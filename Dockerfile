FROM centos:7.3.1611
ENV TZ=Asia/Taipei
ENV HOSTNSME ethon.cloudera.com
RUN yum -y update; yum clean all
RUN echo  "vm.swappiness = 1" >> /etc/sysctl.conf
RUN yum install -y java-1.8.0-openjdk-devel vim wget curl git bind-utils tmux sudo ssh openssh-server 
RUN wget https://archive.cloudera.com/cm5/redhat/7/x86_64/cm/cloudera-manager.repo -P /etc/yum.repos.d/
RUN yum install -y cloudera-manager-daemons cloudera-manager-agent cloudera-manager-server
ADD script root/script
ADD conf root/conf
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
EXPOSE 7180
ENTRYPOINT ["/bin/sh","run.sh"]
