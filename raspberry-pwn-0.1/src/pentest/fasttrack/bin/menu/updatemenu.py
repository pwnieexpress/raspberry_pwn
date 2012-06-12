#!/usr/bin/env python
import os,time,sys,subprocess

# import custom methods
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
Fast-Track Update Menu:

    1.  Update Fast-Track
    2.  Metasploit 3 Update
    3.  Update Exploit-DB Exploits
    4.  Update Gerix Wifi Cracker NG
    5.  Update Social-Engineer Toolkt

    (q)uit

    Enter number: ''')

   if menuz == '1':

	# Start check update feature
	   definepath=os.getcwd()
	   sys.path.append("%s/bin/ftsrc/" % (definepath))
	   try:
	      reload(updateft)
	   except Exception:
	      pass
	   import updateft

# End check update feature

   if menuz == '2':
      definepath=os.getcwd()
      sys.path.append("%s/bin/ftsrc/" % (definepath))
      try:
         reload(updatemeta)
      except Exception:
         pass
      import updatemeta

# Install menu end
   if menuz == '3':
      print "\nUpdating the Offsec Exploit-DB .exploits..."
      if not os.path.isfile("/pentest/exploits/exploitdb"):
         subprocess.Popen("cd /pentest/exploits;svn co svn://devel.offensive-security.com/exploitdb exploitdb/", shell=True).wait()
         subprocess.Popen("cd /pentest/exploits/exploitdb;svn update", shell=True).wait() 

   if menuz == '4':
      print "Updating Gerix Wifi Cracker NG"		
      subprocess.Popen("cd /usr/share;svn co svn://devel.offensive-security.com/gerix-ng", shell=True).wait()
      subprocess.Popen("cd /usr/share/gerix-ng;svn update", shell=True).wait()

   if menuz == '5':
      print "Updating the Social-Engineer Toolkit"
 #subprocess.Popen("cd /pentest/exploits/;svn co http://svn.secmaniac.com/social_engineering_toolkit SET/", shell=True).wait()
      subprocess.Popen("cd /pentest/exploits/SET;svn update", shell=True).wait()

   if menuz == 'q': break
     
# End Updates Menu     
