#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
from fnmatch import fnmatch
import subprocess
import sys

def sedprocess(pattern, startwf, s2):
    path="/var/log/analyzer_sched"
    for path, subdirs, files in os.walk(path):
        for filename in files:
            if fnmatch(filename, pattern):
                route=os.path.join(path, filename)
                try:
                    with open(route, 'r|*') as logfile:
                        for logline in logfile:
                            begin = "Start workflow "+startwf
                            end = "Start workflow "+s2
                            if begin in logline:
                                file1 = open(s2+".txt", 'w|*')
                                cmd = ["sed", "-n", "/"+begin+"/,/"+end+"/p", route]
                                subprocess.call(cmd, stdout=file1)
                                file1.close()
                except IOError as (errno, strerr):
                    return "IOError".format(errno, strerr)

def __main__():
    with open(sys.argv[1], 'r|') as inputf:
        for line in inputf:
            batchID = line.split(' ')[1].strip()
            IS_WF = {
            "BatchDataBackupPipeLine":["batch_data_backup*", "BatchDataBackupWorkflow "+batchID, "BatchDataBackupWorkflow"],
            "CacheTransform":["cache_transform*", "CacheTransformWorkflows "+batchID, "CacheTransformWorkflows"],
            "CefFeyeCorrPipeLine":["cef_feye_corr*", "CefFeyeDataProcessor "+batchID, "CefFeyeDataProcessor"],
            "CorrelationBulkLoader":["corr_bulkloader*", "CorrelateWorkflow "+batchID, "CorrelateWorkflow"],
            "EflowCorrelation": ["eflow_corr*", line.strip(), "EflowCorrelation"],
            "EntityAuthProfiler":["entity_auth_profiling*", "EntityAuthProfiling "+batchID, "EntityAuthProfiling"],
            "EntityScoring":["entity_scoring*", "EntityScoringWorkflow "+batchID, "EntityScoringWorkflow"],
            "EventAggregator":["event_aggregator*", "EventAggregation "+batchID, "EventAggregation"],
            "EventGenerator":["analyzer_event*", "AnalyzerEvent "+batchID, "AnalyzerEvent"],
            "FeedPipeLine":["feed*", "Feed "+batchID, "Feed"],
            "FilePurger":["fs_purger*", "FSPurgeWorkflow "+batchID, "FSPurgeWorkflow" ],
            "GenericUBA":["generic_uba*", line.strip(), "GenericUBA"],
            "LogIngestionPipeLine":["log_workflow*", "LogEtlWorkflow "+batchID, "LogEtlWorkflow"],
            "ObjectPipeLine":["object_workflow*", "ObjectWorkflow "+batchID, "ObjectWorkflow"],
            "RetentionPurgerPipeLine":["retention_purger*", "RetentionPurgeWorkflow "+batchID, "RetentionPurgeWorkflow"],
            "RuleEnginePipeLine":["rule_engine*", "RuleEngineDriver "+batchID, "RuleEngineDriver"],
            "ThreatCentralUploader":["threat_central_uploader*", line.strip(), "ThreatCentralUploader"],
            "UserTimeline":["user_timeline*", line.strip(), "UserTimeline"],
            "WatchlistPurger":["watchlist_purger*", line.strip(), "WatchlistPurger"]
            };
            for (k,v) in IS_WF.items():
                if k in line:
                    pattern = IS_WF[k][0]
                    startwf = IS_WF[k][1]
                    s2 =  IS_WF[k][2]
                    sedprocess(pattern, startwf, s2)
      
if __name__ == '__main__':
    __main__()
