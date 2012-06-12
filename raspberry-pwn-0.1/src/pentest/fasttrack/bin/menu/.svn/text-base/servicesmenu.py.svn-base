#!/usr/bin/env python
import os,time,re
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
   import psyco
   psyco.full()
except ImportError:
   pass
while 1==1 :
          servmen=raw_input("""Which service do you want to start:

  1. VNC
  2. TFTP
  3. SSH
  4. Apache
  5. Metasploit Web
  6. ProFTPD
  
  (q)uit

  Enter number: """)

          if servmen == '1' :
             vnc=os.system("vncserver;netstat -ant |grep 5901")
             print "VNC Server Started..."
          if servmen == '2' :
             tftp=os.system("atftpd --daemon --port 69 /tmp/;netstat -anu |grep 69")
             print "TFTP Server Started..."
          if servmen == '3' :
             ssh=os.system("sshd-generate;/usr/sbin/sshd;netstat -ant |grep 22")
             print "SSH Server Started..."
          if servmen == '4' :
             apache=os.system("apachectl start;netstat -ant |grep 80")
             print "Apache Server Started..."
          if servmen == '5' :
             metasplt1=os.system("%s/msfweb &" % (metapath))
             time.sleep(10)
             print 'Sleeping 10 seconds...waiting for metasploit...then launching FireFox'
             metasplt2=os.system("firefox http://127.0.0.1:55555 &")
          if servmen == '6' :
             print "Make sure you installed it from the Updates Menu first!!"
             time.sleep(2)
             print 'Starting FTP Service'
             ftpstart=os.system('proftpd &')
             print 'FTP Service Started. Returning to menu.'
          if servmen == 'q' :
             print "Returning to previous menu..."
             break

