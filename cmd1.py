from datetime import datetime

from niara.analyzer_sched import AnalyzerSchedLogger


logger = AnalyzerSchedLogger.getLogger('eflow_backlog')


def append_completed_folder(input_path, status, time_delta):
    with open("processed.txt", "a") as afile:
        afile.write('{} \t {} \t {}\n'.format(input_path, status, time_delta))


def load_one_batch(run_id, input_path):

    cmd = "/opt/spark/bin/spark-submit --class com.niara.dataloader.BulkDataLoader --executor-cores 1 --queue default --master yarn-client --conf spark.executorEnv.ANALYZER_KERBEROS_REALM=CLUSTER-INTERNAL --conf spark.executorEnv.ANALYZER_COLUMNAR_FORMAT=parquet --conf spark.rdd.compress=true --conf spark.executorEnv.PYTHONPATH=. --conf spark.executor.extraClassPath=/usr/hdp/2.4.2.0-258/hbase/lib/hbase-server-1.1.2.2.4.2.0-258.jar:/usr/hdp/2.4.2.0-258/hbase/lib/metrics-core-2.2.0.jar:/usr/hdp/2.4.2.0-258/hbase/lib/htrace-core-3.1.0-incubating.jar:/usr/hdp/2.4.2.0-258/zookeeper/zookeeper-3.4.6.2.4.2.0-258.jar:/usr/hdp/2.4.2.0-258/hbase/lib/hbase-common-1.1.2.2.4.2.0-258.jar:/usr/hdp/2.4.2.0-258/hbase/lib/hbase-protocol-1.1.2.2.4.2.0-258.jar:/usr/hdp/2.4.2.0-258/hbase/lib/netty-all-4.0.23.Final.jar:/usr/hdp/2.4.2.0-258/hbase/lib/hbase-client-1.1.2.2.4.2.0-258.jar:/usr/hdp/2.4.2.0-258/hbase/lib/hbase-hadoop-compat-1.1.2.2.4.2.0-258.jar:/usr/hdp/2.4.2.0-258/hbase/lib/protobuf-java-2.5.0.jar:/usr/hdp/2.4.2.0-258/hbase/lib/guava-12.0.1.jar --conf spark.executorEnv.ANALYZER_PRINCIPAL=niara --conf spark.dynamicAllocation.enabled=False --conf spark.storage.memoryFraction=0.5 --conf spark.shuffle.manager=SORT --conf spark.executorEnv.NIARA_PLATFORM=an-hadoop --conf spark.yarn.executor.memoryOverhead=1024 --conf spark.executorEnv.ANALYZER_KEYTAB_FILE=/etc/security/keytabs/niara.keytab --conf spark.executorEnv.NIARA_PATH=analyzer --conf spark.serializer=org.apache.spark.serializer.KryoSerializer --conf spark.executorEnv.ANALYZER_HDFS_PREFIX=/user/niara --conf spark.driver.extraClassPath=/usr/hdp/2.4.2.0-258/hbase/lib/hbase-server-1.1.2.2.4.2.0-258.jar:/usr/hdp/2.4.2.0-258/hbase/lib/metrics-core-2.2.0.jar:/usr/hdp/2.4.2.0-258/hbase/lib/htrace-core-3.1.0-incubating.jar:/usr/hdp/2.4.2.0-258/zookeeper/zookeeper-3.4.6.2.4.2.0-258.jar:/usr/hdp/2.4.2.0-258/hbase/lib/hbase-common-1.1.2.2.4.2.0-258.jar:/usr/hdp/2.4.2.0-258/hbase/lib/hbase-protocol-1.1.2.2.4.2.0-258.jar:/usr/hdp/2.4.2.0-258/hbase/lib/netty-all-4.0.23.Final.jar:/usr/hdp/2.4.2.0-258/hbase/lib/hbase-client-1.1.2.2.4.2.0-258.jar:/usr/hdp/2.4.2.0-258/hbase/lib/hbase-hadoop-compat-1.1.2.2.4.2.0-258.jar:/usr/hdp/2.4.2.0-258/hbase/lib/protobuf-java-2.5.0.jar:/usr/hdp/2.4.2.0-258/hbase/lib/guava-12.0.1.jar:/opt/niara/analyzer/lib/classes/hbase-bulk-load-1.0.0.jar --conf spark.executorEnv.ANALYZER_USER_GROUP=niara --conf spark.executorEnv.PYENCHANT_LIBRARY_PATH=lib/libenchant.so.1 --conf spark.executorEnv.NIARA_ENCHANT_OVERRIDE=lib/enchant --conf spark.scheduler.mode=FAIR --driver-memory 1g --driver-cores 3 /opt/niara/analyzer/lib/classes/bulk-loader-1.0.0.jar"

    cmd_args = cmd.split(" ")
    cmd_args.extend(["--num-executors", "8"])
    cmd_args.extend(["--executor-memory", "2048m"])
    cmd_args.extend(["--name", "Eflow_CatchUp_{}".format(run_id)])
    cmd_args.extend(['--input-file', input_path])
    cmd_args.extend(["--cur-batch", str(run_id)])
    cmd_args.extend(["--datasource", "eflow"])
    cmd_args.extend(["--stores", "hbase,es"])
    cmd_args.extend(["--config-file", "backlog_bulk_loader.yml"])

    job_env = dict(os.environ)
    start_time = datetime.utcnow()
    job = subprocess.Popen(cmd_args, env=job_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)

    stdout, stderr = job.communicate()
    end_time = datetime.utcnow()
    if job.returncode != 0:
        # the loader job has error
        logger.warning('Failed in bulk loading (run_id: {}, path: {})\n{}\n{}'
                           .format(run_id, input_path, stderr, stdout))
        append_completed_folder(input_path, 'error', end_time - start_time)
    else:
        # the loader job finished one batch successfully
        # move the input_path to the backup folder
        # append the input_path into processed.dat file
        logger.warning('Successfully completed bulk loading (run_id: {}, path: {})\n{}\n{}'
                           .format(run_id, input_path, stderr, stdout))
        append_completed_folder(input_path, 'success', end_time - start_time)

if __name__ == "__main__":
    run_id = 1000
    input_path =
    load_one_batch(run_id, input_path)
