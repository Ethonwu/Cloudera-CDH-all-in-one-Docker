FROM centos:7.3.1611
ENV HOSTNAME athemaster.training.com
WORKDIR /root
COPY . .
RUN mv conf/*.repo /etc/yum.repos.d/ && mkdir -p /usr/share/java/ && mv script/mysql-connector-java.jar /usr/share/java/ && \
    mv script/cloudera-quickstart-ip /usr/bin/ && mv script/cloudera-quickstart-init /etc/init.d/

# Install package
RUN yum clean all && yum makecache && yum update -y && yum install -y java-1.8.0-openjdk-devel vim wget git bind-utils tmux sudo ssh openssh-server python-pip python3 cloudera-manager-daemons cloudera-manager-agent cloudera-manager-server python-pip python3 MariaDB-server MariaDB-client jq
RUN pip install --upgrade pip && pip install cm_client cm_api && pip3.6 install --upgrade pip && pip3.6 install cm_client cm_api

# Cloudera Manager & DB setting 
RUN cat /root/conf/mariadb.config > /etc/my.cnf && mkdir -p /var/log/mariadb/ && chown mysql:mysql -R /var/log/mariadb/ && chmod 755 -R /var/log/mariadb/ \
    && /etc/init.d/mysql start && mysql -u root < /root/script/create_db.sql && mysql -u root < /root/script/secure_mariadb.sql && mv conf/db.properties /etc/cloudera-scm-server/ && chmod 755 /etc/cloudera-scm-server/db.properties
RUN mkdir -p /opt/cloudera && chown cloudera-scm:cloudera-scm -R /opt/cloudera/ && mkdir -p /opt/cloudera/parcel-cache/  /opt/cloudera/parcels/.flood/ \
    && chmod 755 -R * /opt/cloudera/ && chown cloudera-scm:cloudera-scm -R /opt/cloudera/csd/ /opt/cloudera/parcel-repo/ /opt/cloudera/parcels/.flood/ 

# Env setting 
RUN echo  "vm.swappiness = 1" >> /etc/sysctl.conf && echo "cloudera" | passwd --stdin root && ssh-keygen -f ~/myRSAkey -t rsa -N "" && mkdir ~/.ssh && cat ~/myRSAkey.pub >> ~/.ssh/authorized_keys
RUN chmod 400 ~/.ssh/authorized_keys && chmod +x script/run.sh
RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && echo "LANG=en_US.UTF-8" > /etc/locale.config && localedef -i en_US -f UTF-8 en_US.UTF-8
WORKDIR /root/script
ENTRYPOINT ["/bin/sh","run.sh"]
