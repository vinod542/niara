#!/bin/bash
echo "Assigning the primary Unassigned shards to available nodes"
curl cdh-2:9200/_cat/health?v
curl -s -XGET cdh-3:9200/_cat/shards?h=index,shard,prirep,state,unassigned.reason | egrep -i 'p UNASSIGNED CLUSTER_RECOVERED\| p UNASSIGNED ALLOCATION_FAILED' | awk '{print $NF}' > unassignedshards
count=$(grep -c $ unassignedshards)
if [$count -gt 0]; then
   curl cdh-2:9200/_cat/nodes?v | awk '{print $NF}' > nodes
   sed 1d nodes > nodelist
   rm -f nodes
   #count=$(grep -c $ unassignedshards)
   for (( i=0; i<= $count;i++ ))
   do
        read word _ < unassignedshards
        number=(awk ' {print $2; exit} ' unassignedshards)
        node=$(sort --random-sort nodelist | head -n 1)
        curl -XPOST 'cdh-1:9200/_cluster/reroute?pretty' -H 'Content-Type: application/json' -d'{"commands" : [{"allocate_stale_primary" : {"index" : "$word", "shard" : $number,"node" : "$node","accept_data_loss" : true}}]}'
        sed 1d unassignedshards
   done
   rm -f nodelist
   rm -f unassignedshards
else
   curl cdh-2:9200/_cat/health?v
   curl -s -XGET cdh-3:9200/_cat/shards?h=index,shard,prirep,state,unassigned.reason | egrep -i 'p UNASSIGNED'
   echo "DONE"
fi






#NOTES:
#script to assign a undassigned Primary shards
#analyzer-manager -x | egrep -i red
#curl cdh-2:9200/_cat/health?v
#[root@an-node ~]# curl cdh-2:9200/_cat/nodes?v
#curl -s -XGET cdh-3:9200/_cat/shards?h=index,shard,prirep,state,unassigned.reason | egrep -i 'p UNASSIGNED CLUSTER_RECOVERED\| p UNASSIGNED ALLOCATION_FAILED' 
#curl -XPOST 'cdh-1:9200/_cluster/reroute?pretty' -H 'Content-Type: application/json' -d'{"commands" : [{"allocate_stale_primary" : {"index" : "$1", "shard" : $2,"node" : "$3","accept_data_loss" : true}}]}'