#!/usr/bin/env python

import os
import re

try:
   import psyco
   psyco.full()
except ImportError:
   pass
definepath=os.getcwd()

# define metasploit path
meta_path=file("%s/config/fasttrack_config" % (definepath),"r").readlines()
for line in meta_path:
    line=line.rstrip()
    match=re.search("METASPLOIT_PATH",line)
    if match:
       line=line.replace("METASPLOIT_PATH=","")
       metapath=line

print "    Updating Metasploit...."
metaupdate=os.system("svn update %s" % (metapath))
