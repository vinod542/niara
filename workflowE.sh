#!/bin/bash
echo "create view jointly as select workflow.batch_id, workflow.name, workflow.start_time, workflow.end_time, workflow.end_time-workflow.start_time as duration, workflow.status, workflow.message, workflow.data_status, active_events.source_instance, active_events.reported_time, active_events.cleared_time, active_events.source_module, active_events.is_alarm from workflow inner join active_events on workflow.name = active_events.source_instance where workflow.message != 'success' and active_events.reported_time > current_date - interval '15 days' and source_module = 'wfe' order by start_time;" | psql -d niara
echo "select distinct on (name) name from jointly;" | psql -d niara | sed '1,2d' | head -n -2 > failedWF.txt
while read wflows
        do
        echo "select name, batch_id from jointly where name = '$wflows' order by batch_id desc limit 7;" | psql -d niara | sed '1,2d' | awk '{print $1,$3}' | head -n -2 >> failedbatches.txt;
        done < failedWF.txt
python workflow.py failedbatches.txt
echo "DROP view IF EXISTS jointly;" | psql -d niara
