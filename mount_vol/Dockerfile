FROM ethonwu/cloudera-cdh5-quickstart:running
RUN rm -rf /opt/cloudera
ADD _data/cloudera /opt/cloudera
ADD _data/dfs /opt/
ADD _data/yarn /opt/
ADD _data/impala /opt/
RUN rm -rf /root/script/run.sh
ADD run.sh /root/script/
RUN ls -al /root/script/
WORKDIR /opt/cloudera
RUN ls /opt/cloudera/
RUN chmod 755 -R *
RUN chown cloudera-scm:cloudera-scm -R csd/ parcel-repo/ parcels/.flood/
WORKDIR /root/script
CMD ['/bin/sh']
