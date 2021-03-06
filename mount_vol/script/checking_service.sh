export HADOOP_USER_NAME="hdfs"
hive -e "CREATE TABLE justin(id INT, name STRING) ROW FORMAT DELIMITED FIELDS TERMINATED BY ' ' STORED AS TEXTFILE;"
echo "1 justin" > /tmp/test
hadoop fs -put /tmp/test /user/hive/warehouse/justin/
hive -e "select * from justin where id=1;"
sleep 5
hadoop jar /opt/cloudera/parcels/CDH/lib/hadoop-0.20-mapreduce/hadoop-examples.jar pi 1 1
echo "create 'test', 'cf'" | hbase shell
echo "list 'test'" | hbase shell
echo "put 'test', 'row1', 'cf:a', 'value1'" |  hbase shell
echo "scan 'test'" | hbase shell
sleep 5
impala-shell -q "invalidate metadata;"
sleep 10
impala-shell -q "select * from justin;"



