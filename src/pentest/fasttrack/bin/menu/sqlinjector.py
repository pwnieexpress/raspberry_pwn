#!/usr/bin/env python
import os,sys,time
definepath=os.getcwd()
sys.path.append("%s/bin/ftsrc/" % (definepath))
import include
while 1==1:
   include.print_banner()
   menu=raw_input("""
Enter which SQL Injector you want to use:

    1. SQL Injector - Query String Parameter Attack
    2. SQL Injector - POST Parameter Attack
    3. SQL Injector - GET FTP Payload Attack
    4. SQL Injector - GET Manual Setup Binary Payload Attack

    (q)uit

    Enter your choice: """)
   if menu == 'quit' or menu == 'q': break
   # Start query string attack
   if menu == '1':
      try:
         reload(sqlbinarypayload)
      except Exception:
         pass
      import sqlbinarypayload
   # POST ATTACK
   if menu == '2':
      try:
         reload(sqlbinarypayloadpost)
      except Exception:
         pass
      import sqlbinarypayloadpost

   # Reverse FTP
   if menu == '3':
      try:
         reload(sqlftppayload)
      except Exception:
         pass
      import sqlftppayload
   # manual setup
   if menu == '4':
      try:
         reload(sqlmanual)
      except Exception:
         pass
      import sqlmanual
