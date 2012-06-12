#!/usr/bin/env python
import os
import sys
import time
import subprocess
import re

def get_basepath():
    basepath = os.getcwd()
    return basepath

definepath=get_basepath()

try:
 if sys.argv[1]=='install':
   print """
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~        *** Fast-Track Setup ***               ~
~  *** Install Fast-Track dependencies ***      ~
~  ***           Version 2.1           ***      ~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fast-Track initial setup menu, you should use this if you are updating 
Fast-Track at all due to added dependancies when writing new application
modules into Fast-Track. 

Some things to note before running Fast-Track, you must install the following:

Metasploit (for autopwn, and mass client attack) 
SQLite3 (for autopwn)

There are other requirements however, Fast-Track will check for them and if
your missing it, Fast-Track will install it for you.

NOTE: Some changes, pymssql is currently compiled at a lower level, higher levels
completely break Fast-Track at this point. Working on a solution to fix the overall
issues. 
   """
# Check if we're root
   if os.geteuid() != 0:
      print "\nFast-Track v4 - A new beginning...\n\n"
      print "Fast-Track Setup is not running under root. Please re-run the tool under root...\n"
      sys.exit(1)
   #print "Metasploit directory example: /pentest/exploits/framework3/"
   #print "\nMake sure you do /folder/ with the / at the end or it'll\njack some stuff up."
   try:
      print "[*] Ensure that you configure the Metasploit path in bin/config/config\n"
      #metasploitpath=raw_input("\nEnter the path to the metasploit directory\nHit enter for default (/pentest/exploits/framework3/): ")
      #if metasploitpath=='':
      #   metasploitpath="/pentest/exploits/framework3/"
      #if os.path.isfile("%smsfconsole" % (metasploitpath)): print "Metasploit files detected, moving on..."
      #if not os.path.isfile("%smsfconsole" % (metasploitpath)): print "Metasploit not detected in path specified. You should re-run setup and specify the correct path."         
      #writefile=file("%s/bin/setup/metasploitconfig.file" % (definepath),'w')
      #writefile.write("%s" % (metasploitpath))
      #writefile.close()
      #print "*** Metasploit directory set..... ***\n"
      print "No guarantee this will successfully install all dependancies correctly\nyou may need to install some manually..\n\nDifferent Linux OS require different things to work.\n"
      installstuff=raw_input("Would you like to attempt all dependancies, yes or no: ")
      # Thanks to swc|666 for the help below
      if installstuff=='yes':
        print '[-] Installing requirements needed for Fast-Track.. [-]'
        print '\n[-] Detecting Linux version... [-]'
      	time.sleep(2)
        if os.path.isfile("/etc/apt/sources.list"):
        	### Not every sources.list file presence indicates Ubuntu (this works on all flavors of Ubuntu, Debian and Sidux @least)  
           if os.path.isfile("/etc/lsb-release"):
        		pat=re.compile("=|\"",re.M|re.DOTALL)
        		distro=open("/etc/lsb-release").read()
        		distro=pat.sub("",distro).split("\n")
        		distro=[i.strip() for i in distro if i.strip() != ''  ]
        		for n,items in enumerate(distro):
        			  if "DISTRIB_DESCRIPTION" in items:
              				d1 = distro[n+0]
         			        d2 = d1.strip("DISTRIB_DESCRIPTION")
          			        d3 = "\n[-] " "%s " "Detected  [-]\n" % (d2)
              				#print d3
			                print "[-] Installing requirements to run on " "%s" "! [-]" % (d2)
#           else:
                	### A sources.list and not a lsb-release file? >.<
        		print '\n[-] Debian-Based OS Detected [-]\n' 
        		print '[-] Installing requirements! [-]'
           print "Installing Subversion, Build-Essential, Python-ClientForm, FreeTds-Dev, PExpect, and Python2.5-Dev, PYMILLS, through Apt, please wait.."
           subprocess.Popen("apt-get --force-yes -y install subversion build-essential vncviewer nmap python-clientform python2.6-dev python-pexpect python-setuptools", shell=True).wait()
           subprocess.Popen("wget http://ibiblio.org/pub/Linux/ALPHA/freetds/stable/freetds-stable.tgz", shell=True).wait()
           subprocess.Popen("wget http://downloads.sourceforge.net/pymssql/pymssql-0.8.0.tar.gz", shell=True).wait()
           subprocess.Popen("tar -zxvf freetds-stable.tgz;tar -zxvf pymssql-0.8.0.tar.gz;cd freetds-0.*;./configure --enable-msdblib --with-tdsver=8.0 && make && make install; cd ..;cd pymssql-0.8.0;ln -s /usr/local/lib/libsysbdb.so.5 /usr/lib;python setup.py install;cd ..;rm -rf freetds*;rm -rf pymssql*", shell=True).wait()
           print '[-] Running ldconfig.... [-]'
           subprocess.Popen("ldconfig", shell=True).wait()
           subprocess.Popen("wget http://downloads.sourceforge.net/pymssql/pymssql-0.8.0.tar.gz", shell=True).wait()
           subprocess.Popen("tar -zxvf pymssql-0.8.0.tar.gz;cd pymssql-0.8.0;ln -s /usr/local/lib/libsysbdb.so.5 /usr/lib;python setup.py install;cd ..;rm -rf pymssql*", shell=True).wait()
           subprocess.Popen('wget http://pypi.inqbus.de/pymills/pymills-3.4.tar.gz#md5=5741d4a5c30aaed5def2f4b4f86e92a9;tar -zxvf pymills-3.4.tar.gz;mv pymills-3.4 pymills;cd pymills/; python setup.py install', shell=True).wait()
           subprocess.Popen('rm -rf pymills; rm -rf pymills-3.4.tar.gz', shell=True).wait()
           print "Installing BeautifulSoup Python Module"
           subprocess.Popen("wget http://www.crummy.com/software/BeautifulSoup/download/BeautifulSoup.tar.gz;tar -zxvf BeautifulSoup.tar.gz;cd BeautifulSoup*;python setup.py install;cd ..;rm -rf BeautifulSoup*", shell=True).wait()
           print "BeautifulSoup Installed."
           # Taken from http://wiredbytes.com/node/5
           metasploitinstall=raw_input("\nWould you like Fast-Track to install Metasploit 3 for you (experimental)? yes or no: ")
           if metasploitinstall == 'yes':
              subprocess.Popen("apt-get install build-essential ruby libruby rdoc libyaml-ruby libzlib-ruby libopenssl-ruby libdl-ruby libreadline-ruby libiconv-ruby libgtk2-ruby libglade2-ruby subversion sqlite3 libsqlite3-ruby irb", shell=True).wait()
              subprocess.Popen("wget -c http://rubyforge.org/frs/download.php/70696/rubygems-1.3.7.tgz;tar -xvzf rubygems-1.3.7.tgz -C /tmp/;cd /tmp/rubygems-1.3.7/;ruby setup.rb", shell=True).wait()
              subprocess.Popen("/usr/bin/gem1.8 install rails", shell=True).wait()
              subprocess.Popen("rm rubygems-1.3.7.tgz", shell=True).wait()
              subprocess.Popen("mkdir /pentest/exploits/framework3;cd /pentest/exploits/framework/;svn co http://metasploit.com/svn/framework3/trunk/ ." , shell=True).wait()
           print "Metasploit should have been installed..running ldconfig"
           ldconfig=subprocess.Popen("ldconfig").wait()
        else:
            print "[-] Generic Linux OS detected! [-] \n[-] Installing vanilla installation for dependancies [-]"    
            print '[-] Installing FreeTDS and PYMMSQL [-]'
            subprocess.Popen("wget http://ibiblio.org/pub/Linux/ALPHA/freetds/stable/freetds-stable.tgz", shell=True).wait()
            subprocess.Popen("wget http://downloads.sourceforge.net/pymssql/pymssql-0.8.0.tar.gz", shell=True).wait()
            subprocess.Popen("tar -zxvf freetds-stable.tgz;tar -zxvf pymssql-0.8.0.tar.gz;cd freetds-0.*;./configure --enable-msdblib --with-tdsver=8.0 && make && make install; cd ..;cd pymssql-0.8.0;ln -s /usr/local/lib/libsysbdb.so.5 /usr/lib;python setup.py install;cd ..;rm -rf freetds*;rm -rf pymssql*", shell=True).wait()
            print '[-] Running ldconfig.... [-]'
            subprocess.Popen("ldconfig", shell=True).wait()
            print '[-] Finished..moving on.. [-]'
            time.sleep(2)
            print 'Installing Module for Python Called "PExpect"'
            subprocess.Popen('wget http://downloads.sourceforge.net/pexpect/pexpect-2.3.tar.gz;tar -zxvf pexpect-2.3.tar.gz;cd pexpect-2.3;python setup.py install;cd ..;rm -rf pexpect-2.3;rm pexpect-2.3.tar.gz', shell=True).wait() 
            print 'Installed! Moving on...'
            print 'Installing SQLite3'
            subprocess.Popen('cd /usr/local/bin/;ln -s tclsh8.4 tclsh', shell=True).wait()
            subprocess.Popen('wget http://www.sqlite.org/sqlite-3.7.0.1.tar.gz;tar -zxvf sqlite-3.7.0.1;cd sqlite-3.7.0.1;./configure --prefix=/usr/local && make && make install;cd ..;rm sqlite-3.7.0.1.tar.gz;rm -rf sqlite-3.7.0.1', shell=True).wait()
            subprocess.Popen('wget http://rubyforge.org/frs/download.php/2820/sqlite-ruby-2.2.3.tar.gz;tar -zxvf sqlite3-ruby-2.2.3.tar.gz;cd sqlite3-ruby-2.2.3;ruby setup.rb config;ruby setup.rb setup;ruby setup.rb install;cd ..;rm  sqlite3-ruby-2.2.3.tar.gz;rm -rf sqlite3-ruby-2.2.3', shell=True).wait() 
            print 'SQLite3 installed..Moving on...'
            print "Installing ClientForm Python Module"
            subprocess.Popen("svn co http://codespeak.net/svn/wwwsearch/ClientForm/trunk ClientForm;cd ClientForm;python setup.py install;cd ..;rm -rf ClientForm", shell=True).wait()
            print "ClientForm Installed, moving on.."
            print "Installing PROFTPD"
            subprocess.Popen("""wget ftp://ftp.proftpd.org/distrib/source/proftpd-1.3.3a.tar.gz;tar -zxvf proftpd-1.3.3a.tar.gz;cd proftpd-1.3.*/;./configure && make && make install;cd ..;rm -rf proftpd*;echo "UseReverseDNS off" >> /usr/local/etc/proftpd.conf;echo "IdentLookups off" >> /usr/local/etc/proftpd.conf;killall proftpd""", shell=True).wait()
            print "PROFRPD installed..Moving on..."
            print "Installing PyMills"
            subprocess.Popen('python setuptools.py;wget http://pypi.inqbus.de/pymills/pymills-3.4.tar.gz;tar -zxvf pymills-3.4.tar.gz;mv pymills-3.4 pymills;cd pymills/;python setup.py install;cd ..;rm -rf pymills*', shell=True).wait()
            print "PyMills installed..Moving on..."
            print "Installing BeautifulSoup..."
            subprocess.Popen("wget http://www.crummy.com/software/BeautifulSoup/download/BeautifulSoup.tar.gz;tar -zxvf BeautifulSoup.tar.gz;cd BeautifulSoup*;python setup.py install;cd ..;rm -rf BeautifulSoup*", shell=True).wait()
            print "BeautifulSoup installed..Moving on..."
            print "Finished with installations..."
            print "Running ldconfig to wrap up everything..."
            subprocess.Popen("ldconfig", shell=True).wait()
            print "\n[-] Finished with setup [-]\n[-] Try running Fast-Track now. [-]\n[-] If unsucessful, manually compile from source the deps. [-]"
            print "[-] Re-checking dependencies... [-]"
      try:
         sys.path.append("%s/bin/setup/" % (definepath))
         import depend
         print "\n"
         print "Finished..running ldconfig to wrap everything up...\n"
         ldconfig=subprocess.Popen("ldconfig", shell=True)
         print "Fast-Track setup exiting...\n"
      except ImportError:
         print "Error importing dependancy checker."
   except KeyboardInterrupt:
      print "\n\nExiting Fast-Track setup...\n"
except IndexError:
     print """
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~                                           ~
~      Fast-Track Setup and Installation    ~
~                                           ~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This script will allow you to install the required
dependencies needed for Fast-Track to function
correctly. Note this does not install Metasploit for
you. If you want to use the automated autopwn
functionality within Metasploit, you will need to
install that yourself.

Usage: python setup.py install
    """
