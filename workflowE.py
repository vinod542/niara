#!/usr/bin/python
#-*- coding: utf-8 -*-
import os, sys
import subprocess
from fnmatch import fnmatch

def flocation(pattern, s2, startwf):
    path='/var/log/analyzer_sched'
    for path, subdirs, files in os.walk(path):
        for filename in files:
            if fnmatch(filename, pattern):
                route = path+'/'+filename
                try:
                    with open(route , "r|*") as logfile, open(s2 + ".txt", "w") as file1:
                        for logline in logfile:
                            part="Start workflow "+startwf
                            if part in logline:
                                end="Start workflow "
                                cmd = ["sed", "-n", "/"+part+"/,/"+end+"/p", route]
                                subprocess.call(cmd, stdout=file1)
                                #file1.writelines(str(subprocess.call("sed -n "+"'/"+part+"/,/"+end+"/p' "+route + "\n", shell=True)))
                except IOERROR as (errno, strerror):
                    print "IO ERROR".format(errno, strerror)

if __name__ == '__main__':
    workflows= ['BatchDataBackupPipeLine', 'CefFeyeCorrPipeLine', 'EntityScoring', 'EventAggregator', 'FeedPipeLine', 'FilePurger', 'LogIngestionPipeLine' 'ObjectPipeLine', 'RetentionPurgerPipeLine',
                'ThreatCentralUploader', 'UserTimeline', 'WatchlistPurger', 'GenericUBA', 'EflowCorrelation', 'CorrelationBulkLoader', 'EntityAuthProfiler', 'RuleEnginePipeLine', 'EventGenerator',
                'CacheTransform']
    with open (sys.argv[1], 'r') as inputf:
         for line in inputf:
              if any(word in line for word in workflows):
                   s1 = line.split(' ')[0]
                   if s1 == 'EflowCorrelation':
                        pattern = 'eflow_corr.l*'
                        startwf = line
                        s2 = line.split(' ')[0]
                        flocation(pattern, s2, startwf)
                   elif s1 == 'GenericUBA':
                        pattern = 'generic_uba.l*'
                        s2 = line.split(' ')[0]
                        startwf = line
                        flocation(pattern, s2, startwf)
                   elif s1 == 'CacheTransform':
                        pattern = 'cache_transform.l*'
                        s2 = "CacheTransformWorkflows"
                        startwf = s2+" "+line.split(' ')[1]
                        flocation(pattern, s2, startwf)
                   elif s1 == 'CefFeyeCorrPipeLine':
                        pattern = 'cef_feye_corr.l*'
                        s2 = "CefFeyeDataProcessor"
                        startwf = s2+" "+line.split(' ')[1]
                        flocation(pattern, s2, startwf)
                   elif s1 == 'CorrelationBulkLoader':
                        pattern = 'corr_bulkloader.l*'
                        s2 = "CorrelateWorkflow"
                        startwf = s2+" "+line.split(' ')[1]
                        flocation(pattern, s2, startwf)
                   elif s1 == 'EntityAuthProfiler':
                        pattern = 'entity_auth_profiling.l*'
                        s2 = "EntityAuthProfiling"
                        startwf = s2+" "+line.split(' ')[1]
                        flocation(pattern, s2, startwf)
                   elif s1 == 'EntityScoring':
                        pattern = 'entity_scoring.l*'
                        s2 = "EntityScoringWorkflow"
                        startwf = s2+" "+line.split(' ')[1]
                        flocation(pattern, s2, startwf)
                   elif s1 == 'EventAggregator':
                        pattern = 'event_aggregator.l*'
                        s2 = "EventAggregation"
                        startwf = s2+" "+line.split(' ')[1]
                        flocation(pattern, s2, startwf)
                   elif s1 == 'ThreatCentralUploader':
                        pattern = 'threat_central_uploader.l*'
                        startwf = line
                        s2 = line.split(' ')[0]
                        flocation(pattern, s2, startwf)
                   elif s1 == 'UserTimeline':
                        pattern = 'user_timeline.l*'
                        startwf = line
                        s2 = line.split(' ')[0]
                        flocation(pattern, s1, startwf)
                   elif s1 == 'WatchlistPurger':
                        pattern = 'watchlist_purger.l*'
                        s2 = line.split(' ')[0]
                        startwf = line
                        flocation(pattern, s2, startwf)
                   elif s1 == 'BatchDataBackupPipeLine':
                        pattern = 'batch_data_backup.l*'
                        s2 = "BatchDataBackupWorkflow"
                        startwf = s2+" "+line.split(' ')[1]
                        flocation(pattern, s2, startwf)
                   elif s1 == 'FeedPipeLine':
                        pattern = 'feed.l*'
                        s2 = "Feed"
                        startwf = s2+" "+line.split(' ')[1]
                        flocation(pattern, s2, startwf)
                   elif s1 == 'FilePurger':
                        pattern = 'fs_purger.l*'
                        s2 = "FSPurgeWorkflow"
                        startwf = s2+" "+line.split(' ')[1]
                        flocation(pattern, s2, startwf)
                   elif s1 == 'LogIngestionPipeLine':
                        pattern = 'log_workflow.l*'
                        s2 = "LogEtlWorkflow"
                        startwf = s2+" "+line.split(' ')[1]
                        flocation(pattern, s2, startwf)
                   elif s1 == 'RuleEnginePipeLine':
                        pattern = 'rule_engine.l*'
                        s2 = "RuleEngineDriver"
                        startwf = s2+" "+line.split(' ')[1]
                        flocation(pattern, s2, startwf)
                   elif s1 == 'EventGenerator':
                        pattern = 'analyzer_event.l*'
                        s2 = "AnalyzerEvent"
                        startwf = s2+" "+line.split(' ')[1]
                        flocation(pattern, s2, startwf)
                   elif s1 == 'ObjectPipeLine':
                        pattern = 'object_workflow.l*'
                        s2 = "ObjectWorkflow"
                        startwf = s2+" "+line.split(' ')[1]
                        flocation(pattern, s2, startwf)
                   elif s1 == 'RetentionPurgerPipeLine':
                        pattern = 'retention_purger.lo*'
                        s2 = "RetentionPurgeWorkflow"
                        startwf = s2+" "+line.split(' ')[1]
                        flocation(pattern, s2. startwf)
                   else:
                        print "Couldn't find"
                    
pass
