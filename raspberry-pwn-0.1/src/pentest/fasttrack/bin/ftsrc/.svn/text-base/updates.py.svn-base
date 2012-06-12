#!/usr/bin/env python

import time
import os
import sys
import subprocess
import re

try:
   import psyco
   psyco.full()
except ImportError:
   pass
definepath=os.getcwd()
print "\nNote this DOES NOT install prereqs, please go to the installation menu for that.\nUpdating Fast-Track, Metasploit, Aircrack-NG, Nikto, W3AF, Kismet-NewCore and SQL Map"
time.sleep(3)
sys.path.append("%s/bin/ftsrc/" % (definepath))
import updateft
counter=0
print """**** Updating Metasploit v3 ****"""
definepath=os.getcwd()

# define metasploit path
meta_path=file("%s/config/fasttrack_config" % (definepath),"r").readlines()
for line in meta_path:
    line=line.rstrip()
    match=re.search("METASPLOIT_PATH",line)
    if match:
       line=line.replace("METASPLOIT_PATH=","")
       metapath=line

try: 
   updatingmetasploit=subprocess.Popen("svn update %s" % (metapath), shell=True).wait()
   print """\n**** Updating AirCrack-NG ****""" 
   updatesaircrack=subprocess.Popen("svn co http://trac.aircrack-ng.org/svn/trunk /pentest/wireless/aircrack-ng;cd /pentest/wireless/aircrack-ng;make sqlite=true && make sqlite=true install", shell=True).wait()
   print "\nUpdating Nikto..." 
   niktoupdate=subprocess.Popen("cd /pentest/scanners/nikto/;./nikto.pl -update", shell=True).wait()
   print "\nUpdating the Web Application Attack and Audit Framework (W3AF)"
   w3afupdates=subprocess.Popen("svn co https://w3af.svn.sourceforge.net/svnroot/w3af/ /pentest/web/w3af", shell=True)
   w3afupdates=subprocess.Popen("cd /pentest/web/w3af;svn update", shell=True).wait()
   print "\nUpdating SQLMap..."

   # CHECK FOR NEW SQLMAP
   fileopen=file("bin/config/sqlmap_config", "r").readlines()
   for line in fileopen:
       line=line.rstrip()
       if line == 'SQLMAP=0':
          #fileopen.close()
          filewrite=file("bin/config/sqlmap_config", "w")
          filewrite.write("SQLMAP=1")
          filewrite.close()
          subprocess.Popen("rm -rf /pentest/database/sqlmap", shell=True).wait()
          subprocess.Popen("svn co https://svn.sqlmap.org/sqlmap/trunk/sqlmap /pentest/database/sqlmap/", shell=True).wait()
       if line == 'SQLMAP=1':
		sqlmapupdate=subprocess.Popen("svn co https://svn.sqlmap.org/sqlmap/trunk/sqlmap /pentest/database/sqlmap", shell=True).wait()
   print "\nUpdating Offsec Exploit-DB exploits..."
   subprocess.Popen("cd /pentest/exploits/;svn co svn://devel.offensive-security.com/exploitdb exploitdb", shell=True).wait()
   subprocess.Popen("cd /pentest/exploits/exploitdb;svn update", shell=True).wait()
   print "Updating Kismet-NewCore..."
   if not os.path.isfile("/pentest/wireless/kismet-newcore"):
      createdir=subprocess.Popen("mkdir /pentest/ 2> /dev/null", shell=True)
      createdir=subprocess.Popen("mkdir /pentest/wireless/ 2> /dev/null" , shell=True)
   rmold=subprocess.Popen("rm /pentest/wireless/kismet-newcore 2> /dev/null", shell=True)
   conew=subprocess.Popen("svn co https://www.kismetwireless.net/code/svn/trunk /pentest/wireless/kismet-newcore;cd /pentest/wireless/kismet-newcore;./configure;make;make install", shell=True).wait()
   print "Updating Gerix Wifi Cracker NG"
   subprocess.Popen("cd /usr/share;svn co svn://devel.offensive-security.com/gerix-ng", shell=True).wait()
   subprocess.Popen("cd /usr/share;svn update", shell=True).wait()
   print "Updating the Social-Engineer Toolkit"
   subprocess.Popen("cd /pentest/exploits/;svn co http://svn.secmaniac.com/social_engineering_toolkit SET/", shell=True).wait()
   subprocess.Popen("cd /pentest/exploits/SET;svn update", shell=True).wait()
   
   print "\nFinished updating...."
except KeyboardInterrupt:
   print "\n\nControl-C detected, exiting Fast-Track...\n\n"
   sys.exit()
except Exception, e: 
   print "Error occured, printing error message: "+e
