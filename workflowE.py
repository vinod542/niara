#!/usr/bin/python
#-*- coding: utf-8 -*-
import os, sys
import subprocess
from fnmatch import fnmatch

def flocation(pattern, s1, workflow):
     path='/var/log/analyzer_sched/'
     for path, subdirs, files in os.walk(path):
          for filename in files:
               if fnmatch(filename, pattern):
                    route = path+'/'+filename
                    with open(route , 'r|') as logfile, open(s1 + ".txt", 'w|') as file1:
                         for logline in logfile:
                              if any(part in line for part in "Start workflow "+s1):
                                   begin="Start workflow "+workflow
                                   end="Finish workflow "+s1
                                   file1.write(subprocess.call(['sed', 's/begin/end/g',route]))
                    
if __name__ == '__main__':
    workflows= ['BatchDataBackupPipeLine', 'CefFeyeCorrPipeLine', 'EntityScoring', 'EventAggregator', 'FeedPipeLine', 'FilePurger', 'LogIngestionPipeLine' 'ObjectPipeLine', 'RetentionPurgerPipeLine',
                'ThreatCentralUploader', 'UserTimeline', 'WatchlistPurger', 'GenericUBA', 'EflowCorrelation', 'CorrelationBulkLoader', 'EntityAuthProfiler', 'RuleEnginePipeLine', 'EventGenerator',
                'CacheTransform']
    with open (sys.argv[1], 'r') as inputf:
         for line in inputf:
              if any(word in line for word in workflows):
                   s1 = line.split(' ')[0]
                   workflow = line
                   if s1 == 'EflowCorrelation':
                        pattern = 'eflow_corr.l*'
                        flocation(pattern, s1, workflow)
                   elif s1 == 'GenericUBA':
                        pattern = 'generic_uba.l*'
                        flocation(pattern, s1, workflow)
                   elif s1 == 'CacheTransform':
                        pattern = 'cache_transform.l*'
                        flocation(pattern, s1, workflow)
                   elif s1 == 'CefFeyeCorrPipeLine':
                        pattern = 'cef_feye_corr.l*'
                        flocation(pattern, s1, workflow)
                   elif s1 == 'CorrelationBulkLoader':
                        pattern = 'corr_bulkloader.l*'
                        flocation(pattern, s1, workflow)
                   elif s1 == 'EntityAuthProfiler':
                        pattern = 'entity_auth_profiling.l*'
                        flocation(pattern, s1, workflow)
                   elif s1 == 'EntityScoring':
                        pattern = 'entity_scoring.l*'
                        flocation(pattern, s1, workflow)
                   elif s1 == 'EventAggregator':
                        pattern = 'event_aggregator.l*'
                        flocation(pattern, s1, workflow)
                   elif s1 == 'ThreatCentralUploader':
                        pattern = 'threat_central_uploader.l*'
                        flocation(pattern, s1, workflow)
                   elif s1 == 'UserTimeline':
                        pattern = 'user_timeline.l*'
                        flocation(pattern, s1, workflow)
                   elif s1 == 'WatchlistPurger':
                        pattern = 'watchlist_purger.l*'
                        flocation(pattern, s1, workflow)
                   else:
                   print "Done"
                    
pass
