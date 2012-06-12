#!/usr/bin/env python

import os
count=0

# Perform Dependency check
print "\n\n\n\n\n***********************************************\n******* Performing dependency checks... *******\n***********************************************\n"

try:
    import _mssql
    print "*** FreeTDS and PYMMSQL are installed. (Check) ***"
    count=count+1
except ImportError:
    print "!!! *ERROR* FreeTDS and PYMMSQL are NOT installed. *ERROR* !!!"
    answer1=raw_input("Would you like to install it now? yes or no: ")
    if answer1=='yes' or answer1=='y':
        print "Installing FreeTDS and PYMMSQL"
        slack1=os.system("wget http://ibiblio.org/pub/Linux/ALPHA/freetds/stable/freetds-stable.tgz")
        slack2=os.system("wget http://downloads.sourceforge.net/pymssql/pymssql-0.8.0.tar.gz")
        slack3=os.system("tar -zxvf freetds-stable.tgz;tar -zxvf pymssql-0.8.0.tar.gz;cd freetds-0.*;./configure --enable-msdblib --with-tdsver=8.0 && make && make install; cd ..;cd pymssql-0.8.0;ln -s /usr/local/lib/libsysbdb.so.5 /usr/lib;python setup.py install;cd ..;rm -rf freetds*;rm -rf pymssql*")
        print 'Running ldconfig....'
        ldconfig=os.system("ldconfig")
        print "FreeTDS and PYMMSQL Installed..."
        print "Re-checking dependency..."
        try:
            import _mssql #@UnusedImport
            print "Installed successfully...This module is now functioning."
            count=count+1
        except ImportError:
            print "Something went wrong during the installation process, try installing FreeTDS and PYMMSQL manually..."
except KeyboardInterrupt:
    print "\nExiting Fast-Track...\n\n"

try:
    import pexpect
    print "*** PExpect is installed. (Check) ***"
except ImportError:
    print "!!! *ERROR* PExpect is NOT installed. *ERROR* !!!"
    answer1=raw_input("Would you like to install it now? yes or no: ")
    if answer1=='yes' or answer1=='y':
        print 'Installing Module for Python Called "PExpect"'
        pexpect0=os.system('wget http://downloads.sourceforge.net/pexpect/pexpect-2.3.tar.gz;tar -zxvf pexpect-2.3.tar.gz;cd pexpect-2.3;python setup.py install;cd ..;rm -rf pexpect-2.3;rm pexpect-2.3.tar.gz') 
        print "PExpect Installed..."
        print "Re-checking dependency..."
        try:
            import pexpect #@UnusedImport
            print "Installed successfully...This module is now functioning."
            count=count+1
        except ImportError:
            print "Something went wrong during the installation process, try installing FreeTDS and PYMMSQL manually..."
except KeyboardInterrupt:
    print "\nExiting Fast-Track...\n\n"

try:
    import ClientForm
    print "*** ClientForm is installed. (Check) ***"
    count=count+1
except ImportError:
    print "!!! *ERROR* ClientForm is NOT installed. *ERROR* !!!"
    answer1=raw_input("Would you like to install it now? yes or no: ")
    if answer1=='yes' or answer1=='y':
        print "Installing ClientForm Python Module"
        installclientform=os.system("svn co http://codespeak.net/svn/wwwsearch/ClientForm/trunk ClientForm;cd ClientForm;python setup.py install;cd ..;rm -rf ClientForm")
        print "ClientForm Installed."
        print "Re-checking dependency"
        try:
            import ClientForm #@UnusedImport
            print "Installed successfully...This module is now functioning."
            count=count+1
        except ImportError:
            print "Something went wrong during the installation process, try installing ClientForm manually..."        
except KeyboardInterrupt:
    print "\nExiting Fast-Track...\n\n"



try:
    import psyco
    psyco.full()
    print "*** Psyco is installed. (Check) ***"
    #  count=count+1
except ImportError:
    pass

try:
    from BeautifulSoup import BeautifulSoup
    print "*** Beautiful Soup is installed. (Check) ***"
    count=count+1
except ImportError:
    print "!!! *ERROR* Beautiful Soup is NOT installed...This is needed for SQLPwnage. *ERROR* !!!"
    answer1=raw_input("Would you like to install it now? yes or no: ")
    if answer1=='yes' or answer1=='y':
        print "Installing BeautifulSoup Python Module"
        installbeatsoup=os.system("wget http://www.crummy.com/software/BeautifulSoup/download/BeautifulSoup.tar.gz;tar -zxvf BeautifulSoup.tar.gz;cd BeautifulSoup*;python setup.py install;cd ..;rm -rf BeautifulSoup*")
        print "BeautifulSoup Installed."
        print "Re-checking dependency"
        try:
            from BeautifulSoup import BeautifulSoup #@UnusedImport
            print "Installed successfully...This module is now functioning."
            count=count+1
        except ImportError:
            print "BeautifulSoup is installed but you will need to restart Fast-Track in order for it to work properly."
except KeyboardInterrupt: 
    print "\nExiting Fast-Track...\n\n"

try:
    import pymills
    print "*** PyMills is installed. (Check) ***"
    count=count+1
except ImportError:
    print "!!! *ERROR* PyMills is NOT installed...This is needed for SQLPwnage. *ERROR* !!!"
    answer1=raw_input("Would you like to install it now? yes or no: ")
    if answer1=='yes' or answer1=='y':
        print "Installing PyMills Python Module, this may take a few mins"
        grabsetuptools=os.system("svn co http://svn.python.org/projects/sandbox/branches/setuptools-0.6/ pym;cd pym;python setup.py install;cd ..;rm -rf pym")
        installpymills=os.system('wget http://pypi.inqbus.de/pymills/pymills-3.4.tar.gz;tar -zxvf pymills-3.4.tar.gz;mv pymills-3.4 pymills;cd pymills/;python setup.py install;cd ..;rm -rf pymills*')
        print "PyMills Installed.."
        print "Re-checking dependancy"
        try:
            import pymills #@UnusedImport
            print "Installed successfully...This module is now functioning."
            count=count+1
        except ImportError:
            print "PyMills is installed but you will need to restart Fast-Track in order for it to work properly."
except KeyboardInterrupt: 
    print "\nExiting Fast-Track...\n\n"

print "\nAlso ensure ProFTP, WinEXE, and SQLite3 is installed from\nthe Updates/Installation menu."

if count ==4:
    print "\nYour system has all requirements needed to run Fast-Track!"

if count !=4:
    print "*WARNING* Your system is missing some components required for Fast-Track.. *WARNING*"
