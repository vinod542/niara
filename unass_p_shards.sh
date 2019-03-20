#!/bin/bash
echo "Assigning the primary Unassigned shards to available nodes"
curl cdh-2:9200/_cat/health?v
curl -s -XGET cdh-3:9200/_cat/shards?h=index,shard,prirep,state,unassigned.reason | egrep -i 'p UNASSIGNED CLUSTER_RECOVERED\| p UNASSIGNED ALLOCATION_FAILED' | awk '{print $1,$2}' > unassignedshards.txt
curl cdh-2:9200/_cat/nodes?v | awk '{print $NF}' | sed 1d > nodes
while read lines
   do
        word=lines | awk '{print $1}'
        number=lines | awk '{print $1}'
        node=$(sort --random-sort nodes | head -n 1)
        curl -XPOST 'cdh-1:9200/_cluster/reroute?pretty' -H 'Content-Type: application/json' -d'{"commands" : [{"allocate_stale_primary" : {"index" : "$word", "shard" : $number,"node" : "$node","accept_data_loss" : true}}]}'
   done < unassignedshards.txt
   rm -f nodes
   rm -f unassignedshards.txt
curl cdh-2:9200/_cat/health?v
curl -s -XGET cdh-3:9200/_cat/shards?h=index,shard,prirep,state,unassigned.reason | egrep -i 'p UNASSIGNED'
echo "DONE"
