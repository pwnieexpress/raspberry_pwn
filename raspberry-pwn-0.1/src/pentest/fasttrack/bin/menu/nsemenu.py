#!/usr/bin/env python
import os,sys,time,subprocess
definepath=os.getcwd()
sys.path.append("%s/bin/ftsrc/" % (definepath))
sys.path.append("%s/bin/scanners/" % (definepath))
import include

try:
   import psyco
   psyco.full()
except ImportError:
   pass

while 1==1:
   try:       
      include.print_banner()
      exploit1=raw_input("""
    The Nmap Scripting Engine is a powerful addition to Nmap, allowing for
    custom scripts which can fingerprint, scan, and even exploit hosts!
    
    Select your script:

    1.  Scan For SMB Vulnerabilities
    
    <ctrl>-c or (q)uit
 
    Enter number: """)

      if exploit1 == '1' :
         try:
            reload(nmapsmbcheckvulns)
         except Exception: pass
         import nmapsmbcheckvulns

#      if exploit1 == '2' :
#         try: reload(ibmcad)
#         except Exception: pass
#         import ibmcad
    
      if exploit1 == 'q' :
         print "\nReturning to previous menu...\n"
         break
   except Exception, e:
      print "\n\n    The system may not be vulnerable. Printing Error: "+str(e)+"\n"
      print e
