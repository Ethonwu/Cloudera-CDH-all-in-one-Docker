from cm_api.api_client import ApiResource
from cm_api.endpoints.clusters import ApiCluster
from cm_api.endpoints.clusters import create_cluster
from cm_api.endpoints.parcels import ApiParcel
from cm_api.endpoints.parcels import get_parcel
from cm_api.endpoints.cms import ClouderaManager
from cm_api.endpoints.services import ApiService, ApiServiceSetupInfo
from cm_api.endpoints.services import create_service
from cm_api.endpoints.types import ApiCommand, ApiRoleConfigGroupRef
from cm_api.endpoints.role_config_groups import get_role_config_group
from cm_api.endpoints.role_config_groups import ApiRoleConfigGroup
from cm_api.endpoints.roles import ApiRole
import time
import re
import os
import sys
import pprint

CMD_TIMEOUT = 180
cm_host = "localhost"
cm_username = "admin"
cm_port= 7180
cm_password = "admin"
cm_service_name = "mgmt"
host_username = "root"
host_password = "cloudera"
host_list = ['ethon.cloudera.com']
cluster_name = "Cluster 1"
cdh_version = "CDH5" # also valid: "CDH4"
cdh_version_number = "5" # also valid: 4
cm_username = "admin"
cm_password = "admin"
cm_service_name = "mgmt"
host_username = "root"
host_password = "cloudera"
PRETTY_PRINT = pprint.PrettyPrinter(indent=4)
cm_repo_url =  "https://archive.cloudera.com/cm5/redhat/7/x86_64/cm/5/"
api_num = os.popen("""curl -s -X GET -u "admin:admin"  http://localhost:7180/api/version""").read().replace("v","")
PARCELS = [
    { 'name' : "CDH", 'version' : "5.16.2-1.cdh5.16.2.p0.8" }
    #{ 'name' : "ACCUMULO", 'version' : "1.4.3-cdh4.3.0-beta-3"}
]
HADOOP_DATA_DIR_PREFIX = "/opt"
FIREHOSE_DATABASE_PASSWORD = "cloudera"
HEADLAMP_DATABASE_PASSWORD = "cloudera"
NAVIGATOR_DATABASE_PASSWORD = "cloudera"
HIVE_METASTORE_PASSWORD = "cloudera"
MGMT_SERVICENAME = "MGMT"
MGMT_SERVICE_CONFIG = {
    'zookeeper_datadir_autocreate': 'true',
}
MGMT_ROLE_CONFIG = {
    'quorumPort': 2888,
}
AMON_ROLENAME = "ACTIVITYMONITOR"
AMON_ROLE_CONFIG = {
    'firehose_database_host': cm_host + ":7432",
    'firehose_database_user': 'amon',
    'firehose_database_password': FIREHOSE_DATABASE_PASSWORD,
    'firehose_database_type': 'mysql',
    'firehose_database_name': 'amon',
    'firehose_heapsize': '1000000000',
    'max_log_backup_index':'1',
    'max_log_size' : '1'
}
APUB_ROLENAME = "ALERTPUBLISHER"
APUB_ROLE_CONFIG = { }
ESERV_ROLENAME = "EVENTSERVER"
ESERV_ROLE_CONFIG = {
    'event_server_heapsize': '1000000000',
    'max_log_backup_index' :'1',
    'max_log_size' : '1'
}
HMON_ROLENAME = "HOSTMONITOR"
HMON_ROLE_CONFIG = { 
     'max_log_backup_index' :'1',
     'max_log_size' : '1'

          }
SMON_ROLENAME = "SERVICEMONITOR"
SMON_ROLE_CONFIG = { 
    'max_log_backup_index' :'1',
    'max_log_size' : '1'
          }
NAV_ROLENAME = "NAVIGATOR"
NAV_ROLE_CONFIG = {
    'navigator_database_host': cm_host + ":7432",
    'navigator_database_user': 'nav',
    'navigator_database_password': NAVIGATOR_DATABASE_PASSWORD,
    'navigator_database_type': 'mysql',
    'navigator_database_name': 'nav',
    'navigator_heapsize': '1000000000',
}
NAVMS_ROLENAME = "NAVIGATORMETADATASERVER"
NAVMS_ROLE_CONFIG = {
}
RMAN_ROLENAME = "REPORTMANAGER"
RMAN_ROLE_CONFIG = {
    'headlamp_database_host': cm_host + ":7432",
    'headlamp_database_user': 'rman',
    'headlamp_database_password': HEADLAMP_DATABASE_PASSWORD,
    'headlamp_database_type': 'mysql',
    'headlamp_database_name': 'rman',
    'headlamp_heapsize': '1000000000',
    }

### ZooKeeper ###
# ZK quorum will be the first three hosts
ZOOKEEPER_HOSTS = host_list
ZOOKEEPER_SERVICE_NAME = "Zookeeper"
ZOOKEEPER_SERVICE_CONFIG = {
    'zookeeper_datadir_autocreate': 'true',
}
ZOOKEEPER_ROLE_CONFIG = {
     'quorumPort': 2888,
     'electionPort': 3888,
     'dataLogDir': '/var/lib/zookeeper',
     'dataDir': '/var/lib/zookeeper',
     'maxClientCnxns': '1024',
    'max_log_backup_index' :'1',
    'max_log_size' : '1'
}


### HDFS ###
HDFS_SERVICE_NAME = "HDFS"
HDFS_SERVICE_CONFIG = {
  'dfs_replication': 1,
  'dfs_permissions': 'false',
  #'dfs_permissions': 'true',
  'dfs_block_local_path_access_user': 'impala,hbase,mapred,spark',
  'zookeeper_service': ZOOKEEPER_SERVICE_NAME,
}
HDFS_NAMENODE_SERVICE_NAME = "nn"
HDFS_NAMENODE_HOST = host_list[0]
HDFS_NAMENODE_CONFIG = {
  #'dfs_name_dir_list': '/data01/hadoop/namenode',
  'dfs_name_dir_list': HADOOP_DATA_DIR_PREFIX + '/namenode',
  'dfs_namenode_handler_count': 30, #int(ln(len(DATANODES))*20),
    'max_log_backup_index' :'1',
    'max_log_size' : '1'
}
HDFS_SECONDARY_NAMENODE_HOST = host_list[0]
HDFS_SECONDARY_NAMENODE_CONFIG = {
  #'fs_checkpoint_dir_list': '/data01/hadoop/namesecondary',
  'fs_checkpoint_dir_list': HADOOP_DATA_DIR_PREFIX + '/namesecondary',
    'max_log_backup_index' :'1',
    'max_log_size' : '1'
}
HDFS_DATANODE_HOSTS = host_list
#dfs_datanode_du_reserved must be smaller than the amount of free space across the data dirs
#Ideally each data directory will have at least 1TB capacity; they need at least 100GB at a minimum
#dfs_datanode_failed_volumes_tolerated must be less than the number of different data dirs (ie volumes) in dfs_data_dir_list
HDFS_DATANODE_CONFIG = {
  #'dfs_data_dir_list': '/data01/hadoop/datanode,/data02/hadoop/datanode,/data03/hadoop/datanode,/data04/hadoop/datanode,/data05/hadoop/datanode,/data06/hadoop/datanode,/data07/hadoop/datanode,/data08/hadoop/datanode',
  'dfs_data_dir_list': HADOOP_DATA_DIR_PREFIX + '/datanode',
  'dfs_datanode_handler_count': 30,
  #'dfs_datanode_du_reserved': 42949672960,
  'dfs_datanode_du_reserved': 1073741824,
  'dfs_datanode_failed_volumes_tolerated': 0,
  'dfs_datanode_data_dir_perm': 755,
    'max_log_backup_index' :'1',
    'max_log_size' : '1'
}
HDFS_GATEWAY_HOSTS = host_list
#HDFS_GATEWAY_HOSTS.append(host_list)
HDFS_GATEWAY_CONFIG = {
  'dfs_client_use_trash' : 'true'
}


### YARN ###
YARN_SERVICE_NAME = "YARN"
YARN_SERVICE_CONFIG = {
  'hdfs_service': HDFS_SERVICE_NAME,
  'zookeeper_service': ZOOKEEPER_SERVICE_NAME,
}
YARN_RM_HOST = host_list[0]
YARN_RM_CONFIG = { 
    'max_log_backup_index' :'1',
    'max_log_size' : '1'
        }

YARN_JHS_HOST = host_list[0]
YARN_JHS_CONFIG = { 
    'max_log_backup_index' :'1',
    'max_log_size' : '1'
        }
#YARN_NM_HOSTS = list(CLUSTER_HOSTS)
YARN_NM_HOSTS = host_list
YARN_NM_CONFIG = {
  #'yarn_nodemanager_local_dirs': '/data01/hadoop/yarn/nm',
  'yarn_nodemanager_local_dirs': HADOOP_DATA_DIR_PREFIX + '/yarn/nm',
    'max_log_backup_index' :'1',
    'max_log_size' : '1'
}
YARN_GW_HOSTS = host_list
YARN_GW_CONFIG = {
  'mapred_submit_replication': min(3, len(YARN_GW_HOSTS))
}


### HBase ###
HBASE_SERVICE_NAME = "HBase"
HBASE_SERVICE_CONFIG = {
  'hdfs_service': HDFS_SERVICE_NAME,
  'zookeeper_service': ZOOKEEPER_SERVICE_NAME,
}
HBASE_HM_HOST = host_list[0]
HBASE_HM_CONFIG = { 
    'max_log_backup_index' :'1',
    'max_log_size' : '1'
        }
HBASE_RS_HOSTS = host_list
HBASE_RS_CONFIG = {
  'hbase_hregion_memstore_flush_size': 1024000000,
  'hbase_regionserver_handler_count': 10,
  'hbase_regionserver_java_heapsize': 2048000000,
  'hbase_regionserver_java_opts': '',
    'max_log_backup_index' :'1',
    'max_log_size' : '1'
}
#HBASE_THRIFTSERVER_SERVICE_NAME = "HBASETHRIFTSERVER"
#HBASE_THRIFTSERVER_HOST = CLUSTER_HOSTS[0]
#HBASE_THRIFTSERVER_CONFIG = { }
HBASE_GW_HOSTS = host_list
HBASE_GW_CONFIG = { }


### Hive ###
HIVE_SERVICE_NAME = "Hiveeeeeee"
HIVE_SERVICE_CONFIG = {
  'hive_metastore_database_host':host_list[0] ,
  'hive_metastore_database_name': 'metastore',
  'hive_metastore_database_password': HIVE_METASTORE_PASSWORD,
  'hive_metastore_database_port': 3306,
  'hive_metastore_database_type': 'mysql',
  #'mapreduce_yarn_service': MAPRED_SERVICE_NAME,
  'zookeeper_service': ZOOKEEPER_SERVICE_NAME,
  'mapreduce_yarn_service': YARN_SERVICE_NAME,
}
HIVE_HMS_HOST = host_list[0]
HIVE_HMS_CONFIG = {
  'hive_metastore_java_heapsize': 85306784,
    'max_log_backup_index' :'1',
    'max_log_size' : '1'
}
HIVE_HS2_HOST = host_list[0]
HIVE_HS2_CONFIG = { 
    'max_log_backup_index' :'1',
    'max_log_size' : '1'
        }
#HIVE_WHC_HOST = host_list[0]
#HIVE_WHC_CONFIG = { 
        #}
HIVE_GW_HOSTS = host_list
HIVE_GW_CONFIG = { }


### Impala ###
IMPALA_SERVICE_NAME = "Impalalalalalalalal"
IMPALA_SERVICE_CONFIG = {
  'hdfs_service': HDFS_SERVICE_NAME,
  'hbase_service': HBASE_SERVICE_NAME,
  'hive_service': HIVE_SERVICE_NAME,
}
IMPALA_SS_HOST = host_list[0]
IMPALA_SS_CONFIG = { }
IMPALA_CS_HOST = host_list[0]
IMPALA_CS_CONFIG = { }
IMPALA_ID_HOSTS = host_list
IMPALA_ID_CONFIG = { }

def deploy_management(manager, mgmt_servicename, mgmt_service_conf, mgmt_role_conf, amon_role_name, amon_role_conf, apub_role_name, apub_role_conf, eserv_role_name, eserv_role_conf, hmon_role_name, hmon_role_conf, smon_role_name, smon_role_conf, nav_role_name, nav_role_conf, navms_role_name, navms_role_conf, rman_role_name, rman_role_conf):
    mgmt = manager.create_mgmt_service(ApiServiceSetupInfo())
    
    # create roles. Note that host id may be different from host name (especially in CM 5). Look it it up in /api/v5/hosts
    mgmt.create_role(amon_role_name + "-1", "ACTIVITYMONITOR", host_list[0])
    mgmt.create_role(apub_role_name + "-1", "ALERTPUBLISHER", host_list[0])
    mgmt.create_role(eserv_role_name + "-1", "EVENTSERVER", host_list[0])
    mgmt.create_role(hmon_role_name + "-1", "HOSTMONITOR", host_list[0])
    mgmt.create_role(smon_role_name + "-1", "SERVICEMONITOR", host_list[0])
    #mgmt.create_role(nav_role_name + "-1", "NAVIGATOR", cm_host)
    #mgmt.create_role(navms_role_name + "-1", "NAVIGATORMETADATASERVER", cm_host)
    #mgmt.create_role(rman_role_name + "-1", "REPORTSMANAGER", cm_host)
    
    # now configure each role    
    for group in mgmt.get_all_role_config_groups():
         if group.roleType == "ACTIVITYMONITOR":
              group.update_config(amon_role_conf)
         elif group.roleType == "ALERTPUBLISHER":
              group.update_config(apub_role_conf)
         elif group.roleType == "EVENTSERVER":
              group.update_config(eserv_role_conf)
         elif group.roleType == "HOSTMONITOR":
              group.update_config(hmon_role_conf)
         elif group.roleType == "SERVICEMONITOR":
              group.update_config(smon_role_conf)
     #    elif group.roleType == "NAVIGATOR":
     #         group.update_config(nav_role_conf)
     #    elif group.roleType == "NAVIGATORMETADATASERVER":
     #         group.update_config(navms_role_conf)
     #    elif group.roleType == "REPORTSMANAGER":
     #         group.update_config(rman_role_conf)
    
    # now start the management service
    mgmt.start().wait()
    print "Deploy CM service is successful"
    mgmt.stop().wait()
         
# Downloads and distributes parcels
def deploy_parcels(cluster, parcels):
    for parcel in parcels:
        p = cluster.get_parcel(parcel['name'], parcel['version'])
        p.start_download()
        while True:
            p = cluster.get_parcel(parcel['name'], parcel['version'])
            if p.stage == "DOWNLOADED":
                break
            if p.state.errors:
                raise Exception(str(p.state.errors))
            print "Downloading %s: %s / %s" % (parcel['name'], p.state.progress, p.state.totalProgress)
            time.sleep(15)
        print "Downloaded %s" % (parcel['name'])
        p.start_distribution()
        while True:
            p = cluster.get_parcel(parcel['name'], parcel['version'])
            if p.stage == "DISTRIBUTED":
                break
            if p.state.errors:
                raise Exception(str(p.state.errors))
            print "Distributing %s: %s / %s" % (parcel['name'], p.state.progress, p.state.totalProgress)
            time.sleep(15)
        print "Distributed %s" % (parcel['name'])
        p.activate()
def init_cluster(api, cluster_name, cdh_version, hosts, cm_host):
    cluster = api.create_cluster(cluster_name, cdh_version)
    # Add the CM host to the list of hosts to add in the cluster so it can run the management services
    all_hosts = list(hosts)
    #all_hosts = []
    #all_hosts.append(cm_host)
    #cluster.add_hosts(all_hosts)
    cluster.add_hosts(cm_host)
    return cluster
def deploy_zookeeper(cluster, zk_name, zk_hosts, zk_service_conf, zk_role_conf):
    zk = cluster.create_service(zk_name, "ZOOKEEPER")
    zk.update_config(zk_service_conf)

    zk_id = 0
    for zk_host in zk_hosts:
        zk_id += 1
        print  zk_id , " as " , zk_host
        zk_role_conf['serverId'] = zk_id

        role = zk.create_role(zk_name + "-" + str(zk_id), "SERVER", zk_host)

        role.update_config(zk_role_conf)
    #zk_id = 1
    #zk_role_conf['serverId'] = zk_id
    #role = zk.create_role(zk_name + "-" + str(zk_id), "SERVER", zk_hosts[0])
    #role.update_config(zk_role_conf)
    zk.init_zookeeper() 

    return zk

# Deploys HDFS - NN, DNs, SNN, gateways.
# This does not yet support HA yet.
def deploy_hdfs(cluster, hdfs_service_name, hdfs_config, hdfs_nn_service_name, hdfs_nn_host, hdfs_nn_config, hdfs_snn_host, hdfs_snn_config, hdfs_dn_hosts, hdfs_dn_config, hdfs_gw_hosts, hdfs_gw_config):
    hdfs_service = cluster.create_service(hdfs_service_name, "HDFS")
    hdfs_service.update_config(hdfs_config)

    nn_role_group = hdfs_service.get_role_config_group("{0}-NAMENODE-BASE".format(hdfs_service_name))
    nn_role_group.update_config(hdfs_nn_config)
    nn_service_pattern = "{0}-" + hdfs_nn_service_name
    hdfs_service.create_role(nn_service_pattern.format(hdfs_service_name), "NAMENODE", hdfs_nn_host)

    snn_role_group = hdfs_service.get_role_config_group("{0}-SECONDARYNAMENODE-BASE".format(hdfs_service_name))
    snn_role_group.update_config(hdfs_snn_config)
    hdfs_service.create_role("{0}-snn".format(hdfs_service_name), "SECONDARYNAMENODE", hdfs_snn_host)

    dn_role_group = hdfs_service.get_role_config_group("{0}-DATANODE-BASE".format(hdfs_service_name))
    dn_role_group.update_config(hdfs_dn_config)

    gw_role_group = hdfs_service.get_role_config_group("{0}-GATEWAY-BASE".format(hdfs_service_name))
    gw_role_group.update_config(hdfs_gw_config)

    datanode = 0
    for host in hdfs_dn_hosts:
        datanode += 1
        hdfs_service.create_role("{0}-dn-".format(hdfs_service_name) + str(datanode), "DATANODE", host)

    gateway = 0
    for host in hdfs_gw_hosts:
        gateway += 1
        hdfs_service.create_role("{0}-gw-".format(hdfs_service_name) + str(gateway), "GATEWAY", host)

    return hdfs_service

# Initializes HDFS - format the file system
def init_hdfs(hdfs_service, hdfs_name, timeout):
    cmd = hdfs_service.format_hdfs("{0}-nn".format(hdfs_name))[0]
    if not cmd.wait(timeout).success:
        print "WARNING: Failed to format HDFS, attempting to continue with the setup"
def deploy_yarn(cluster, yarn_service_name, yarn_service_config, yarn_rm_host, yarn_rm_config, yarn_jhs_host, yarn_jhs_config, yarn_nm_hosts, yarn_nm_config, yarn_gw_hosts, yarn_gw_config):
    yarn_service = cluster.create_service(yarn_service_name, "YARN")
    yarn_service.update_config(yarn_service_config)
       
    rm = yarn_service.get_role_config_group("{0}-RESOURCEMANAGER-BASE".format(yarn_service_name))
    rm.update_config(yarn_rm_config)
    yarn_service.create_role("{0}-rm".format(yarn_service_name), "RESOURCEMANAGER", yarn_rm_host)
       
    jhs = yarn_service.get_role_config_group("{0}-JOBHISTORY-BASE".format(yarn_service_name))
    jhs.update_config(yarn_jhs_config)
    yarn_service.create_role("{0}-jhs".format(yarn_service_name), "JOBHISTORY", yarn_jhs_host)
    
    nm = yarn_service.get_role_config_group("{0}-NODEMANAGER-BASE".format(yarn_service_name))
    nm.update_config(yarn_nm_config)
    
    nodemanager = 0
    for host in yarn_nm_hosts:
       nodemanager += 1
       yarn_service.create_role("{0}-nm-".format(yarn_service_name) + str(nodemanager), "NODEMANAGER", host)
    
    gw = yarn_service.get_role_config_group("{0}-GATEWAY-BASE".format(yarn_service_name))
    gw.update_config(yarn_gw_config)
    
    gateway = 0
    for host in yarn_gw_hosts:
       gateway += 1
       yarn_service.create_role("{0}-gw-".format(yarn_service_name) + str(gateway), "GATEWAY", host)
    
    #TODO need api version 6 for these, but I think they are done automatically?
    #yarn_service.create_yarn_job_history_dir()
    #yarn_service.create_yarn_node_manager_remote_app_log_dir()
    
    return yarn_service

def deploy_hbase(cluster, hbase_service_name, hbase_service_config, hbase_hm_host, hbase_hm_config, hbase_rs_hosts, hbase_rs_config, hbase_gw_hosts, hbase_gw_config ):
    hbase_service = cluster.create_service(hbase_service_name, "HBASE")
    hbase_service.update_config(hbase_service_config)
       
    hm = hbase_service.get_role_config_group("{0}-MASTER-BASE".format(hbase_service_name))
    hm.update_config(hbase_hm_config)
    hbase_service.create_role("{0}-hm".format(hbase_service_name), "MASTER", hbase_hm_host)
    
    rs = hbase_service.get_role_config_group("{0}-REGIONSERVER-BASE".format(hbase_service_name))
    rs.update_config(hbase_rs_config)
    
    #ts = hbase_service.get_role_config_group("{0}-HBASETHRIFTSERVER-BASE".format(hbase_service_name))
    #ts.update_config(hbase_thriftserver_config)
    #ts_name_pattern = "{0}-" + hbase_thriftserver_service_name
    #hbase_service.create_role(ts_name_pattern.format(hbase_service_name), "HBASETHRIFTSERVER", hbase_thriftserver_host)
    
    gw = hbase_service.get_role_config_group("{0}-GATEWAY-BASE".format(hbase_service_name))
    gw.update_config(hbase_gw_config)
    
    regionserver = 0
    for host in hbase_rs_hosts:
       regionserver += 1
       hbase_service.create_role("{0}-rs-".format(hbase_service_name) + str(regionserver), "REGIONSERVER", host)
    
    gateway = 0
    for host in hbase_gw_hosts:
       gateway += 1
       hbase_service.create_role("{0}-gw-".format(hbase_service_name) + str(gateway), "GATEWAY", host)
    
    hbase_service.create_hbase_root()
    
    return hbase_service

# Deploys Hive - hive metastore, hiveserver2, webhcat, gateways
def deploy_hive(cluster, hive_service_name, hive_service_config, hive_hms_host, hive_hms_config, hive_hs2_host, hive_hs2_config, hive_gw_hosts, hive_gw_config):
    hive_service = cluster.create_service(hive_service_name, "HIVE")
    hive_service.update_config(hive_service_config)
    
    hms = hive_service.get_role_config_group("{0}-HIVEMETASTORE-BASE".format(hive_service_name))
    hms.update_config(hive_hms_config)
    hive_service.create_role("{0}-hms".format(hive_service_name), "HIVEMETASTORE", hive_hms_host)
    
    hs2 = hive_service.get_role_config_group("{0}-HIVESERVER2-BASE".format(hive_service_name))
    hs2.update_config(hive_hs2_config)
    hive_service.create_role("{0}-hs2".format(hive_service_name), "HIVESERVER2", hive_hs2_host)
    
    #whc = hive_service.get_role_config_group("{0}-WEBHCAT-BASE".format(hive_service_name))
    #whc.update_config(hive_whc_config)
    #hive_service.create_role("{0}-whc".format(hive_service_name), "WEBHCAT", hive_whc_host)
    
    gw = hive_service.get_role_config_group("{0}-GATEWAY-BASE".format(hive_service_name))
    gw.update_config(hive_gw_config)
    
    gateway = 0
    for host in hive_gw_hosts:
       gateway += 1
       hive_service.create_role("{0}-gw-".format(hive_service_name) + str(gateway), "GATEWAY", host)
    
    return hive_service


# Initialized hive
def init_hive(hive_service):
    hive_service.create_hive_metastore_database()
    hive_service.create_hive_metastore_tables()
    hive_service.create_hive_warehouse()

# Deploys Impala - statestore, catalogserver, impalads
def deploy_impala(cluster, impala_service_name, impala_service_config, impala_ss_host, impala_ss_config, impala_cs_host, impala_cs_config, impala_id_hosts, impala_id_config):
    impala_service = cluster.create_service(impala_service_name, "IMPALA")
    impala_service.update_config(impala_service_config)
    
    ss = impala_service.get_role_config_group("{0}-STATESTORE-BASE".format(impala_service_name))
    ss.update_config(impala_ss_config)
    impala_service.create_role("{0}-ss".format(impala_service_name), "STATESTORE", impala_ss_host)
    
    cs = impala_service.get_role_config_group("{0}-CATALOGSERVER-BASE".format(impala_service_name))
    cs.update_config(impala_cs_config)
    impala_service.create_role("{0}-cs".format(impala_service_name), "CATALOGSERVER", impala_cs_host)
    
    id = impala_service.get_role_config_group("{0}-IMPALAD-BASE".format(impala_service_name))
    id.update_config(impala_id_config)
    
    impalad = 0
    for host in impala_id_hosts:
       impalad += 1
       impala_service.create_role("{0}-id-".format(impala_service_name) + str(impalad), "IMPALAD", host)

    # Don't think we need these at the end:
    #impala_service.create_impala_catalog_database()
    #impala_service.create_impala_catalog_database_tables()
    #impala_service.create_impala_user_dir()
    
    return impala_service

#def post_startup(cluster, hdfs_service, oozie_service):
def post_startup(cluster, hdfs_service):
    # Create HDFS temp dir
    hdfs_service.create_hdfs_tmp()
    
    # Create hive warehouse dir
    shell_command = ['curl -i -H "Content-Type: application/json" -X POST -u "' + ADMIN_USER + ':' + ADMIN_PASS + '" -d "serviceName=' + HIVE_SERVICE_NAME + ';clusterName=' + CLUSTER_NAME + '" http://' + CM_HOST + ':7180/api/v5/clusters/' + CLUSTER_NAME + '/services/' + HIVE_SERVICE_NAME + '/commands/hiveCreateHiveWarehouse']
    create_hive_warehouse_output = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read()
    
    # Create oozie database
    #oozie_service.stop().wait()
    #shell_command = ['curl -i -H "Content-Type: application/json" -X POST -u "' + ADMIN_USER + ':' + ADMIN_PASS + '" -d "serviceName=' + OOZIE_SERVICE_NAME + ';clusterName=' + CLUSTER_NAME + '" http://' + CM_HOST + ':7180/api/v5/clusters/' + CLUSTER_NAME + '/services/' + OOZIE_SERVICE_NAME + '/commands/createOozieDb']
    #create_oozie_db_output = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read()
    ## give the create db command time to complete
    #time.sleep(30)
    #oozie_service.start().wait()
    
    # Deploy client configs to all necessary hosts
    cmd = cluster.deploy_client_config()
    if not cmd.wait(CMD_TIMEOUT).success:
       print "Failed to deploy client configs for {0}".format(cluster.name)
    
    # Noe change permissions on the /user dir so YARN will work
    shell_command = ['sudo -u hdfs hadoop fs -chmod 775 /user']
    user_chmod_output = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read()

def main():
    api = ApiResource(cm_host, cm_port, cm_username, cm_password, version=api_num)
    cm = ClouderaManager(api)
    #cm.host_install(host_username, host_list, password=host_password, cm_repo_url=cm_repo_url)
    MANAGER = api.get_cloudera_manager()
    #MANAGER.update_config)
    print "Connected to CM host on " + cm_host + " and updated CM configuration"

    CLUSTER = init_cluster(api, cluster_name , cdh_version, host_list ,host_list)

    deploy_management(MANAGER, MGMT_SERVICENAME, MGMT_SERVICE_CONFIG, MGMT_ROLE_CONFIG, AMON_ROLENAME, AMON_ROLE_CONFIG, APUB_ROLENAME, APUB_ROLE_CONFIG, ESERV_ROLENAME, ESERV_ROLE_CONFIG, HMON_ROLENAME, HMON_ROLE_CONFIG, SMON_ROLENAME, SMON_ROLE_CONFIG, NAV_ROLENAME, NAV_ROLE_CONFIG, NAVMS_ROLENAME, NAVMS_ROLE_CONFIG, RMAN_ROLENAME, RMAN_ROLE_CONFIG)

    print "Deployed CM management service " + MGMT_SERVICENAME + " to run on " + cm_host + "now service is stop!"


    deploy_parcels(CLUSTER, PARCELS)
    print "Downloaded and distributed parcels: "
    PRETTY_PRINT.pprint(PARCELS)
    
    zookeeper_service = deploy_zookeeper(CLUSTER, ZOOKEEPER_SERVICE_NAME, ZOOKEEPER_HOSTS, ZOOKEEPER_SERVICE_CONFIG, ZOOKEEPER_ROLE_CONFIG)
    print "Deployed ZooKeeper " + ZOOKEEPER_SERVICE_NAME + " to run on: "
    PRETTY_PRINT.pprint(ZOOKEEPER_HOSTS)

    
    
    hdfs_service = deploy_hdfs(CLUSTER, HDFS_SERVICE_NAME, HDFS_SERVICE_CONFIG, HDFS_NAMENODE_SERVICE_NAME, HDFS_NAMENODE_HOST, HDFS_NAMENODE_CONFIG, HDFS_SECONDARY_NAMENODE_HOST, HDFS_SECONDARY_NAMENODE_CONFIG, HDFS_DATANODE_HOSTS, HDFS_DATANODE_CONFIG, HDFS_GATEWAY_HOSTS, HDFS_GATEWAY_CONFIG)
    print "Deployed HDFS service " + HDFS_SERVICE_NAME + " using NameNode on " + HDFS_NAMENODE_HOST + ", SecondaryNameNode on " + HDFS_SECONDARY_NAMENODE_HOST + ", and DataNodes running on: "
    PRETTY_PRINT.pprint(HDFS_DATANODE_HOSTS)
    init_hdfs(hdfs_service, HDFS_SERVICE_NAME, 600)
    # Test move last method to here orginal is from post_startup function
    #hdfs_service.create_hdfs_tmp()
    print "Initialized HDFS service"

    
    yarn_service = deploy_yarn(CLUSTER, YARN_SERVICE_NAME, YARN_SERVICE_CONFIG, YARN_RM_HOST, YARN_RM_CONFIG, YARN_JHS_HOST, YARN_JHS_CONFIG, YARN_NM_HOSTS, YARN_NM_CONFIG, YARN_GW_HOSTS, YARN_GW_CONFIG)
    print "Deployed YARN service " + YARN_SERVICE_NAME + " using ResourceManager on " + YARN_RM_HOST + ", JobHistoryServer on " + YARN_JHS_HOST + ", and NodeManagers on "
    PRETTY_PRINT.pprint(YARN_NM_HOSTS)


    #deploy_hbase(CLUSTER, HBASE_SERVICE_NAME, HBASE_SERVICE_CONFIG, HBASE_HM_HOST, HBASE_HM_CONFIG, HBASE_RS_HOSTS, HBASE_RS_CONFIG, HBASE_THRIFTSERVER_SERVICE_NAME, HBASE_THRIFTSERVER_HOST, HBASE_THRIFTSERVER_CONFIG, HBASE_GW_HOSTS, HBASE_GW_CONFIG)
    deploy_hbase(CLUSTER, HBASE_SERVICE_NAME, HBASE_SERVICE_CONFIG, HBASE_HM_HOST, HBASE_HM_CONFIG, HBASE_RS_HOSTS, HBASE_RS_CONFIG, HBASE_GW_HOSTS, HBASE_GW_CONFIG)
    print "Deployed HBase service " + HBASE_SERVICE_NAME + " using HMaster on " + HBASE_HM_HOST + " and RegionServers on "
    PRETTY_PRINT.pprint(HBASE_RS_HOSTS)

    
    hive_service = deploy_hive(CLUSTER, HIVE_SERVICE_NAME, HIVE_SERVICE_CONFIG, HIVE_HMS_HOST, HIVE_HMS_CONFIG, HIVE_HS2_HOST, HIVE_HS2_CONFIG, HIVE_GW_HOSTS, HIVE_GW_CONFIG)
    print "Depoyed Hive service " + HIVE_SERVICE_NAME + " using HiveMetastoreServer on " + HIVE_HMS_HOST + " and HiveServer2 on " + HIVE_HS2_HOST
    init_hive(hive_service)
    print "Initialized Hive service"

    impala_service = deploy_impala(CLUSTER, IMPALA_SERVICE_NAME, IMPALA_SERVICE_CONFIG, IMPALA_SS_HOST, IMPALA_SS_CONFIG, IMPALA_CS_HOST, IMPALA_CS_CONFIG, IMPALA_ID_HOSTS, IMPALA_ID_CONFIG)
    print "Deployed Impala service " + IMPALA_SERVICE_NAME + " using StateStore on " + IMPALA_SS_HOST + ", CatalogServer on " + IMPALA_CS_HOST + ", and ImpalaDaemons on "
    PRETTY_PRINT.pprint(IMPALA_ID_HOSTS)
    
    CLUSTER.stop().wait()
    CLUSTER.start().wait()
    #post_startup(CLUSTER, hdfs_service, oozie_service)
    post_startup(CLUSTER, hdfs_service)
 
if __name__ == "__main__":
     main()
     
