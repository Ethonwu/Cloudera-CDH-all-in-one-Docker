import json


template = {}


## products repositories    ##
products = [ 
 {"version" : "5.16.2-1.cdh5.16.2.p0.8","product" : "CDH"},
 {"version" : "2.4.0.cloudera1-1.cdh5.13.3.p0.1007356","product" : "SPARK2"}   ]

#print type(products[0])
#print products[0]

template['cdhVersion'] = "5.16.2"
template['displayName'] = "Cluster 1"
template['cmVersion'] = "5.16.2"
template['repositories'] = ["http://archive.cloudera.com/spark2/parcels/2.4.0.cloudera1/", "https://archive.cloudera.com/cdh5/parcels/5.16.2/"]
template['products'] = products


## instantiator   ##
instantiator = {}

instantiator['clusterName'] = template['displayName']
#hosts = []
# Here need to group each node where have same role
host_list = [
{ "hostName" : "ethon.cloudera.com", "hostTemplateRefName" : "HostTemplate-0-from-ethon.cloudera.com"},

        ]

#hosts.append(host_list)

instantiator['hosts'] = host_list

variables = [

{ "name" : "hdfs-NAMENODE-BASE-dfs_name_dir_list", "value" : "/opt/dfs/nn" } , 
{ "name" : "hdfs-SECONDARYNAMENODE-BASE-fs_checkpoint_dir_list", "value" : "/opt/dfs/snn" }, 
{ "name" : "hive-hive_metastore_database_host", "value" : "ethon.cloudera.com" }, 
{ "name" : "hive-hive_metastore_database_password", "value" : "cloudera" }, 
{ "name" : "hue-database_host", "value" : "ethon.cloudera.com" }, 
{ "name" : "hue-database_password", "value" : "cloudera" }, 
{ "name" : "hue-database_type", "value" : "mysql" }, 
{ "name" : "impala-IMPALAD-BASE-scratch_dirs", "value" : "/opt/impala/impalad" }, 
{ "name" : "oozie-OOZIE_SERVER-BASE-oozie_database_host", "value" : "ethon.cloudera.com" }, 
{ "name" : "oozie-OOZIE_SERVER-BASE-oozie_database_password", "value" : "cloudera" }, 
{ "name" : "oozie-OOZIE_SERVER-BASE-oozie_database_type", "value" : "mysql" }, 
{ "name" : "oozie-OOZIE_SERVER-BASE-oozie_database_user", "value" : "oozie" }, 
{ "name" : "yarn-NODEMANAGER-BASE-yarn_nodemanager_local_dirs", "value" : "/opt/yarn/nm" }

]

##  hostTemplates  ##

hostTemplates = [
 { "refName" : "HostTemplate-0-from-ethon.cloudera.com",
   "cardinality" : 1,
   "roleConfigGroupsRefNames" : [ "hbase-MASTER-BASE", "hbase-REGIONSERVER-BASE", "hdfs-DATANODE-BASE", "hdfs-NAMENODE-BASE", "hdfs-SECONDARYNAMENODE-BASE", "hive-GATEWAY-BASE", "hive-HIVEMETASTORE-BASE", "hive-HIVESERVER2-BASE", "hue-HUE_LOAD_BALANCER-BASE", "hue-HUE_SERVER-BASE", "impala-CATALOGSERVER-BASE", "impala-IMPALAD-BASE", "impala-STATESTORE-BASE", "oozie-OOZIE_SERVER-BASE", "spark2_on_yarn-SPARK2_YARN_HISTORY_SERVER-BASE", "yarn-JOBHISTORY-BASE", "yarn-NODEMANAGER-BASE", "yarn-RESOURCEMANAGER-BASE", "zookeeper-SERVER-BASE","flume-AGENT-BASE" ]
  }
]


instantiator['variables'] = variables

template['instantiator'] = instantiator

template['hostTemplates'] = hostTemplates


## Service  ##

service = []


## ZOOKEEPER   ##
zookeeper_server_config = [

{ "name" : "max_log_size", "value" : "1" }

]
zookeeper_roleConfigGroups = [
   {
     "refName" : "zookeeper-SERVER-BASE",
     "roleType" : "SERVER",
     "configs" : zookeeper_server_config,
     "base": "true"
   }
]

zookeeper = {

"refName" : "zookeeper",
"serviceType" : "ZOOKEEPER",
"serviceConfigs" : [],
"roleConfigGroups" : zookeeper_roleConfigGroups


}



##  HDFS  ##

hdfs_server_config = [

{ "name" : "dfs_replication" , "value" : "3"}
 
]

### NAMENODE CONFIG ### 
hdfs_namenode_config = [

{ "name" : "dfs_name_dir_list", "variable" : "hdfs-NAMENODE-BASE-dfs_name_dir_list"  }

]

namenode_roleConfigGroups = {
     "refName" :"hdfs-NAMENODE-BASE",
     "roleType" : "NAMENODE",
     "configs" : hdfs_namenode_config,
     "base": "true"
   }


### SECONDARYNAMENODE ###

hdfs_secondarynamenode_config = [ 

{ "name": "fs_checkpoint_dir_list" , "variable": "hdfs-SECONDARYNAMENODE-BASE-fs_checkpoint_dir_list"  }

]

secondarynamenode_roleConfigGroups = {
     "refName" :"hdfs-SECONDARYNAMENODE-BASE",
     "roleType" : "SECONDARYNAMENODE",
     "configs" : hdfs_secondarynamenode_config,
     "base": "true"
   }

### DATANODE ### 

hdfs_datanode_config = [

{"name":"dfs_data_dir_list", "value" : "/opt/dfs/dn"},
{"name":"dfs_datanode_failed_volumes_tolerated" , "value":"0"}
# if two path "value" : "/xxx/xxx/xxx , /xxx/xx/xxx"
]

datanode_roleConfigGroups = {
     "refName" :"hdfs-DATANODE-BASE",
     "roleType" : "DATANODE",
     "configs" : hdfs_datanode_config,
     "base": "true"
   }

## Main HDFS config ## 

hdfs_roleConfigGroups = []
hdfs_roleConfigGroups.append(namenode_roleConfigGroups)
hdfs_roleConfigGroups.append(secondarynamenode_roleConfigGroups)
hdfs_roleConfigGroups.append(datanode_roleConfigGroups)

hdfs = {

"refName" : "hdfs",
"serviceType" : "HDFS",
"serviceConfigs" : [],
"roleConfigGroups" : hdfs_roleConfigGroups

}

### YARN Service ### 

## RESOURCEMANAGER ## 

yarn_resourcemanager_config = [

{ "name" : "yarn_scheduler_increment_allocation_mb" , "value" : "1024" }

]

resourcemanager_roleConfigGroups = {
    "refName" : "yarn-RESOURCEMANAGER-BASE" ,
    "roleType" : "RESOURCEMANAGER",
    "configs" : yarn_resourcemanager_config ,
    "base" : "true"
}

## NODEMANAGER ## 

yarn_nodemanager_config = [

{ "name" : "yarn_nodemanager_local_dirs" , "variable" : "yarn-NODEMANAGER-BASE-yarn_nodemanager_local_dirs" }

]

nodemanager_roleConfigGroups = {
    "refName" : "yarn-NODEMANAGER-BASE" ,
    "roleType" : "NODEMANAGER" , 
    "configs" : yarn_nodemanager_config ,
    "base" : "true"
}


## JOBHISTORY SERVER ## 

yarn_jobhis_config = [

#{ "name" : "xxx" , "value": "xxx"}

]

jobhis_roleConfigGroups = {
    "refName" : "yarn-JOBHISTORY-BASE" ,
    "roleType" : "JOBHISTORY" , 
    "configs" : yarn_jobhis_config ,
    "base" : "true"
}

## YARN GATEWAY  ##

yarn_gateway_config = [

{ "name" : "mapreduce_reduce_memory_mb" , "value" : "1024" },
{ "name" : "mapreduce_map_memory_mb" , "value" : "1024" }

]

yarngateway_roleConfigGroups = {
    "refName" : "yarn-GATEWAY-BASE" ,
    "roleType" : "GATEWAY" , 
    "configs" : yarn_gateway_config ,
    "base" : "true"
}


### Main YARN ### 

yarn_roleConfigGroups = []
yarn_roleConfigGroups.append(resourcemanager_roleConfigGroups)
yarn_roleConfigGroups.append(nodemanager_roleConfigGroups)
yarn_roleConfigGroups.append(jobhis_roleConfigGroups)
yarn_roleConfigGroups.append(yarngateway_roleConfigGroups)

yarn = {

"refName" : "yarn",
"serviceType" : "YARN",
"serviceConfigs" : [],
"roleConfigGroups" : yarn_roleConfigGroups

}


## Hive ## 
### HIVESERVER2 ### 

hive_hiveserver2_config = [
#{"name":""}
]
hiveserver2_roleConfigGroups = {
    "refName" : "hive-HIVESERVER2-BASE" ,
    "roleType" : "HIVESERVER2" , 
    "configs" : hive_hiveserver2_config ,
    "base" : "true"
}


### HIVEMETASTORE ### 

hive_metastore_config = [
# {"name":"", "value":""}
]

metastore_roleConfigGroups = {
    "refName" : "hive-HIVEMETASTORE-BASE" ,
    "roleType" : "HIVEMETASTORE" , 
    "configs" : hive_metastore_config ,
    "base" : "true"
}


### HIVEGATEWAY ### 

hive_gateway_config = [
# {"name":"","value":""}
]

hivegatwway_roleConfigGroups = {
    "refName" : "hive-GATEWAY-BASE" ,
    "roleType" : "GATEWAY" , 
    "configs" : hive_gateway_config ,
    "base" : "true"
}

### Main Hive Service 


hive_roleConfigGroups = []
hive_roleConfigGroups.append(metastore_roleConfigGroups)
hive_roleConfigGroups.append(hiveserver2_roleConfigGroups)
hive_roleConfigGroups.append(hivegatwway_roleConfigGroups)


hive_service_config = [
{ "name" : "hive_metastore_database_password" , "variable" : "hive-hive_metastore_database_password" },
{ "name" : "hive_metastore_database_host" , "variable" : "hive-hive_metastore_database_host" }
]


hive = {

"refName" : "hive",
"serviceType" : "HIVE",
"serviceConfigs" : hive_service_config,
"roleConfigGroups" : hive_roleConfigGroups

}



###  Impala Service  ###
#### Impala Deamon ####


impald_config = [
  {"name":"scratch_dirs", "variable":"impala-IMPALAD-BASE-scratch_dirs"}  
]

impalad_roleConfigGroups = {
    "refName" : "impala-IMPALAD-BASE" ,
    "roleType" : "IMPALAD" , 
    "configs" : impald_config ,
    "base" : "true"
}

#### Impala STATESTORE####

statestore_config = [
  
]

statestore_roleConfigGroups= {
    "refName" : "impala-STATESTORE-BASE" ,
    "roleType" : "STATESTORE" , 
    "configs" : statestore_config ,
    "base" : "true"
}

#### Impala CATALOGSERVER ####

catalogserver_config = [

]

catalogserver_roleConfigGroups = {
    "refName" : "impala-CATALOGSERVER-BASE" ,
    "roleType" : "CATALOGSERVER" , 
    "configs" : catalogserver_config ,
    "base" : "true"
}


#### Impala Main Service ####

impala_roleConfigGroups = []

impala_roleConfigGroups.append(impalad_roleConfigGroups)
impala_roleConfigGroups.append(catalogserver_roleConfigGroups)
impala_roleConfigGroups.append(statestore_roleConfigGroups)

impala_service_config = []

impala = {

"refName" : "impale",
"serviceType" : "IMPALA",
"serviceConfigs" : impala_service_config,
"roleConfigGroups" : impala_roleConfigGroups

}


### OOZIE service ###
#### oozie server ####

oozie_server_config = [
 {"name":"oozie_database_user", "variable":"oozie-OOZIE_SERVER-BASE-oozie_database_user"},
 {"name":"oozie_database_host", "variable":"oozie-OOZIE_SERVER-BASE-oozie_database_host"},
 {"name":"oozie_database_type", "variable":"oozie-OOZIE_SERVER-BASE-oozie_database_type"},
 {"name":"oozie_database_password", "variable":"oozie-OOZIE_SERVER-BASE-oozie_database_password"}
]

oozie_server_roleConfigGroups = {
    "refName" : "oozie-OOZIE_SERVER-BASE" ,
    "roleType" : "OOZIE_SERVER" , 
    "configs" : oozie_server_config ,
    "base" : "true"
}

#### OOZIE Main Service #### 

oozie_roleConfigGroups = []
oozie_roleConfigGroups.append(oozie_server_roleConfigGroups)

oozie_service_config = [

]

oozie = {
"refName" : "oozie",
"serviceType" : "OOZIE",
"serviceConfigs" : oozie_service_config,
"roleConfigGroups" : oozie_roleConfigGroups
}


### HBase Service ###

#### HBase REGIONSERVER ####

regionserver_config = [

]

regionserver_roleConfigGroups = {
    "refName" : "hbase-REGIONSERVER-BASE" ,
    "roleType" : "REGIONSERVER" , 
    "configs" : regionserver_config ,
    "base" : "true"
}


#### HBase MASTER #### 

hbase_master_config = [
]

hbase_master_roleConfigGroups = {
    "refName" : "hbase-MASTER-BASE" ,
    "roleType" : "MASTER" , 
    "configs" : hbase_master_config,
    "base" : "true"
}

#### Hbase Main Service ####

hbase_roleConfigGroups = []
hbase_roleConfigGroups.append(regionserver_roleConfigGroups)
hbase_roleConfigGroups.append(hbase_master_roleConfigGroups)

hbase_service_config = []

hbase = {
"refName" : "hbase",
"serviceType" : "HBASE",
"serviceConfigs" : hbase_service_config,
"roleConfigGroups" : hbase_roleConfigGroups
}


### Hue ### 
#### Hue Server ####

hue_server_config = [ 

]

hue_server_roleConfigGroups = {
    "refName" : "hue-HUE_SERVER-BASE" ,
    "roleType" : "HUE_SERVER" , 
    "configs" : hue_server_config ,
    "base" : "true"
}


#### HUE_LOAD_BALANCER ####

hue_loadbalancer_config = []

loadblancer_roleConfigGroups = {
    "refName" : "hue-HUE_LOAD_BALANCER-BASE" ,
    "roleType" : "HUE_LOAD_BALANCER" , 
    "configs" : hue_loadbalancer_config ,
    "base" : "true"
}

#### Hue Main Service ####

hue_roleConfigGroups = []
hue_roleConfigGroups.append(hue_server_roleConfigGroups)
hue_roleConfigGroups.append(loadblancer_roleConfigGroups)

hue_service_config = [
        { "name":"database_password", "variable": "hue-database_password"},
        { "name":"database_type", "variable":"hue-database_type"},
        { "name":"database_host", "variable":"hue-database_host" }
]

hue = {
"refName" : "hue",
"serviceType" : "HUE",
"serviceConfigs" : hue_service_config,
"roleConfigGroups" : hue_roleConfigGroups
}

### SPARK2 ###


#### SPARK2 HISTORY SERVER ####

spark2_hissrv_config = []

spark2_hissrv_roleConfigGroups = {
    "refName" : "spark2_on_yarn-SPARK2_YARN_HISTORY_SERVER-BASE" ,
    "roleType" : "SPARK2_YARN_HISTORY_SERVER" , 
    "configs" : spark2_hissrv_config ,
    "base" : "true"
}

#### SPARK2 GATEWAY ####

#### Not get config XD


#### Spark2 Main Service ####


spark2_roleConfigGroups = []

spark2_roleConfigGroups.append(spark2_hissrv_roleConfigGroups)


spark2_service_config = [
        {"name":"yarn_service" ,"value": "yarn"},
        {"name":"hive_service", "value": "Hive"}
]

spark2 = {
"refName" : "spark2_on_yarn",
"serviceType" : "SPARK2_ON_YARN",
"serviceConfigs" : spark2_service_config,
"roleConfigGroups" : spark2_roleConfigGroups
}



###  Flume Service ###

#### Flume agent ####

flume_agent_config = [] 

flume_agent_roleConfigGroups = {
    "refName" : "flume-AGENT-BASE" ,
    "roleType" : "AGENT" , 
    "configs" : flume_agent_config ,
    "base" : "true"

}


### Flume Main Service ###


flume_service_roleConfigGroups = []
flume_service_roleConfigGroups.append(flume_agent_roleConfigGroups)


flume_config = [
        {"name": "hdfs_service","value" :"hdfs"}
        ]


flume = {
"refName" : "flume",
"serviceType" : "FLUME",
"serviceConfigs" : flume_config,
"roleConfigGroups" : flume_service_roleConfigGroups
}













service.append(zookeeper)
service.append(hdfs)
service.append(yarn)
service.append(hive)
service.append(impala)
service.append(oozie)
service.append(hbase)
service.append(hue)
service.append(spark2)
service.append(flume)

template['services'] = service

output = json.dumps(template, ensure_ascii=False)
print output
