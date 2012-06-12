#!/usr/bin/env python
import time,re,os,sys,subprocess
try:
   import psyco
   psyco.full()
except ImportError:
   pass
definepath=os.getcwd()
sys.path.append("%s/bin/ftsrc/" % (definepath))
import include

sys.path.append("%s/bin/setup/" % (definepath))
import depend

updateconfig=""

# Main Menu to choose
readversion=file("bin/version/version","r")
for line in readversion:
    version=line.rstrip()

try:
   while 1==1:
      include.print_banner()
      mainmenu=raw_input('''
   Fast-Track Main Menu:

    1.  Fast-Track Updates
    2.  Autopwn Automation
    3.  Nmap Scripting Engine
    4.  Microsoft SQL Tools
    5.  Mass Client-Side Attack
    6.  Exploits
    7.  Binary to Hex Payload Converter
    8.  Payload Generator
    9.  Fast-Track Tutorials
    10. Fast-Track Changelog
    11. Fast-Track Credits
    12. Exit Fast-Track

   Enter the number: ''')

      if mainmenu == '1':
         try:
            # DEBUGGING
            # Check OS - show or hide updates
            configfile=file("bin/config/config", "r").readlines()
            for line in configfile:
               search=re.search("SHOWUPDATES=",line)
               if search:
                  line=line.rstrip()
                  updateconfig=line.split("=")
                  updateconfig=updateconfig[1]

            if updateconfig == "":
            #Suggest running setup and show restricted menu
               try:
                  reload(updatemenu)
               except Exception:
                  pass
               import updatemenu     
         
            if updateconfig == "YES":
            # Is not BackTrack, show all updates
               try:
                  reload(updatemenu)
               except Exception:
                  pass
               import updatemenu     
        
            if updateconfig == "NO":
            # Is BackTrack, update fast-track only
               try:
                  reload(updateftonlymenu)
               except Exception:
                  pass
               import updateftonlymenu     
         except KeyboardInterrupt :
            print '\n\n   Returning to previous menu...'
            time.sleep(2)  
    
 # Start Metasploit Autopwn
      if mainmenu == '2':
         try:
            sys.path.append("%s/bin/ftsrc/" % (definepath))
            try:
               reload(autopwn)
            except Exception:
               pass
            import autopwn
         except KeyboardInterrupt :
            print '\n\n   Returning to previous menu...'
            time.sleep(2)

# Nmap Scripting Engine 
      if mainmenu == '3' :
         try:
            try: 
               reload(nsemenu)
            except Exception: 
               pass
            import nsemenu
         except KeyboardInterrupt :
            print '\n\n   Returning to previous menu...'
            time.sleep(2)

# MSSQL Attacks
      if mainmenu == '4' :
         try:
            try:
               reload(mssqlattacks)
            except Exception:
               pass
            import mssqlattacks
         except KeyboardInterrupt :
            print '\n\n   Returning to previous menu...'
            time.sleep(2)

 # Start Mass Client Attack
      if mainmenu == '5':
         try:
            sys.path.append("%s/bin/ftsrc/clientattack/" % (definepath))
            try:
               reload(massclient)
            except Exception:
               pass
            import massclient
         except KeyboardInterrupt :
            print '\n\n   Returning to previous menu...'
            time.sleep(2)

 # Exploit menu start
      if mainmenu == '6':
         try:
            try:
               reload(exploitmenu)
            except Exception:
               import exploitmenu
         except KeyboardInterrupt: 
            print '\n\n   Returning to previous menu...'
            time.sleep(2)

      if mainmenu == '7':
      
 #Start Binary to Hex Generator
         try:
            sys.path.append("%s/bin/ftsrc/" % (definepath))
            try:
               reload(binarypayloadgen)
            except Exception:
               pass
            import binarypayloadgen
         except KeyboardInterrupt :
            print '\n   Returning to previous menu...'
            time.sleep(2)
 
 # Start Option 7 Payload Generator
      if mainmenu == '8':
         try:
            sys.path.append("%s/bin/ftsrc/" % (definepath))
            try:
               reload(payloadgen)
            except Exception:
               pass
            import payloadgen
         except KeyboardInterrupt :
            print '\n   Returning to previous menu...'
            time.sleep(2)

# Start Option 8 Tutorials
      if mainmenu == '9' :
         try:
            try:
               reload(tutorialsmenu)
            except Exception:
               pass
            import tutorialsmenu
         except KeyboardInterrupt :
            print '\n   Returning to previous menu...'
            time.sleep(2)

# Start Option 9 ChangeLog
      if mainmenu == '10' :
         try:
            sys.path.append("%s/bin/ftsrc/" % (definepath))
            try:
               reload(changelog)
            except Exception:
               pass
            import changelog
         except KeyboardInterrupt :
            print '\n\n   Returning to previous menu...\n'
            time.sleep(2)

   # Start Option 10 credits
      if mainmenu == '11' :
         try:
            sys.path.append("%s/bin/ftsrc/" % (definepath))
            try:
               reload(credits)
            except Exception:
               pass
            import credits
         except KeyboardInterrupt :
            print '\n\n   Returning to previous menu...\n'
            time.sleep(2)      

 # Exit Fast-Track
      if mainmenu == '12':
         print """\n\n  Exiting Fast-Track...\n\n """
         cleanup=subprocess.Popen("rm sqlpassword 2> /dev/null;rm SqlScan.txt 2> /dev/null;rm sqlopen.txt 2> /dev/null;rm pentest 2> /dev/null;rm parse2.txt 2> /dev/null;rm parse.txt 2> /dev/null;rm binarypayload.txt 2> /dev/null;portscan.txt 2> /dev/null", shell=True)

         sys.exit()

 # Error handling
except KeyboardInterrupt :
   print """\n\n  Exiting Fast-Track...\n"""
   cleanup=subprocess.Popen("rm sqlpassword 2> /dev/null;rm SqlScan.txt 2> /dev/null;rm sqlopen.txt 2> /dev/null;rm pentest 2> /dev/null;rm parse2.txt 2> /dev/null;rm parse.txt 2> /dev/null;rm binarypayload.txt 2> /dev/null;rm portscan.txt 2> /dev/null", shell=True)
