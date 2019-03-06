import sys
import re
from datetime import datetime
import os
import pickle
import difflib

file1 = sys.argv[1]
file2 = sys.argv[2]

with open(file1) as text1:
    with open(file2) as text2:
        d = difflib.Differ()
        diff = list(d.compare(text1.readlines(), text2.readlines()))
        with open('diff.txt', 'w') as diff_file:
            _diff = ''.join(diff)
            diff_file.write(_diff)
