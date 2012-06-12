#!/usr/bin/env python
import os,sys

definepath=os.getcwd()
sys.path.append("%s/bin/ftsrc/" % (definepath))
import include

try:
   import psyco
   psyco.full()
except ImportError:
   pass
while 1 == 1 :
   include.print_banner()
   menuz=raw_input('''
Fast-Track Update Menu (BackTrack):

    1.  Update Fast-Track

    (q)uit

    Enter number: ''')

   if menuz == '1':
      try:
         reload(updateft)
      except Exception:
         pass
      import updateft

   if menuz == 'q': break
     
# End Updates Menu     
