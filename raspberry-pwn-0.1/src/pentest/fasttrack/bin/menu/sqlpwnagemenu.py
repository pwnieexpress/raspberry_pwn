#!/usr/bin/env python
import os,sys,time
try:
   import psyco
   psyco.full()
except ImportError:
   pass
definepath=os.getcwd()
sys.path.append("%s/bin/ftsrc/sqlpwnage/" % (definepath))
try:
       try:
           reload(sqlpwnage)
       except Exception: pass  
       import sqlpwnage
except Exception,e:
       print e
     
