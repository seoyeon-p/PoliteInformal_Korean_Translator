#!/usr/bin/env python
# coding = utf-8

'''
This script extracts the English Sentences and Korean Sentences, from the orginal English-Korean paired corpus and
saves it into two seperate files  
'''

from os import listdir
from os.path import isfile, join
import re
mypath='./'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles.pop()
foutput1 = open(mypath+'eng.txt','w')
foutput2 = open(mypath+'korean.txt','w')
for f in onlyfiles:
    files = open(mypath+f,'r',encoding = 'utf-8')
    while True:
        line1 = files.readline()
        if line1:
            line1 = line1.strip()
            if line1 == '':
                continue
            if not line1[0].isdigit():
                continue
            line2 = files.readline().strip()
            line3 = files.readline().strip()
            if line2 == '' or line3 == '' or line1 == '':
                continue
            try:
                line2.encode('ascii')
            except UnicodeEncodeError:
                continue
            else:
                if line2.startswith('#'):
                    foutput1.write(line2[1:]+'\n')
                else:
                    foutput1.write(line2+'\n')
                if line3.startswith('#'):
                    foutput2.write(line3[1:]+'\n')
                else:
                    foutput2.write(line3+'\n')
        else:
            break
foutput1.close()
foutput2.close()


