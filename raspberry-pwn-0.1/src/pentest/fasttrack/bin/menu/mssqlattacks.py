#!/usr/bin/env python
import os,sys,time
definepath=os.getcwd()
sys.path.append("%s/bin/ftsrc/" % (definepath))
import include

try:
   import psyco
   psyco.full()
except ImportError:
   pass
definepath=os.getcwd()
while 1==1:
  include.print_banner()
  menu=raw_input("""
Microsoft SQL Attack Tools

    1. MSSQL Injector
    2. MSSQL Bruter
    3. SQLPwnage

    (q)uit

    Enter your choice : """)
  if menu == 'q': break

# MSSQL Injector Start
  if menu == '1':
    sys.path.append("%s/bin/ftsrc/" % (definepath))
    try:
        try:
           reload(sqlinjector)
        except Exception: pass
        import sqlinjector
    except Exception,e:
           print e

# Start SQL Bruter
  if menu == '2':
   sys.path.append("%s/bin/ftsrc/" % (definepath))
   try:
       try:
          reload(sqlbrute)
       except Exception: pass
       import sqlbrute
   except Exception,e:
          print e


#SQLPwnage Start
  if menu == '3':
     sys.path.append("%s/bin/ftsrc/sqlpwnage/" % (definepath))
     try:
         try:
            reload(sqlpwnage)
         except Exception: pass  
         import sqlpwnage
     except Exception,e:
            print e
# Cancel
  if menu == '4':
     break
