#!/bin/bash
echo "Assigning the primary Unassigned shards to available nodes"
curl cdh-2:9200/_cat/health?v
curl -s -XGET cdh-3:9200/_cat/shards | egrep -i "p UNASSIGNED"
while read lines
   do
        read -a fields <<<"$lines"
        curl -XPOST 'cdh-2:9200/_cluster/reroute?pretty' -H 'Content-Type: application/json' -d'{"commands" : [{"allocate_stale_primary" : {"index" : "'${fields[0]}'", "shard" : ${fields[1]},"node" : "'${fields[7]}'","accept_data_loss" : true}}]}'
   done
curl cdh-2:9200/_cat/health?v
curl -s -XGET cdh-3:9200/_cat/shards | egrep -i "p UNASSIGNED"
echo "DONE"
