#!/usr/bin/env python

import time
import os
import sys
import subprocess

definepath=os.getcwd()
sys.path.append("%s/bin/ftsrc/" % (definepath))
import include

include.print_banner()

try:
    import psyco
    psyco.full()
except ImportError:
    pass

print "\n    Updating Fast-Track, please wait...."
time.sleep(3)

try:
    print "\n    Checking for the new versions of Fast-Track..."

    if os.path.isfile("%s/.svn/entries" % (definepath)):
        print "    Previous subversion installation detection, checking SVN for new versions..."
        updatesvn=subprocess.Popen("svn update", shell=True).wait()
        print "\n\n    Fast-Track is now running the latest version...\n\n"

    if not os.path.isfile("%s/.svn/entries" % (definepath)):
        print "    Fast-Track installation is now pulling the SVN repository for installation...Wait a few moments..\n"
        rmold=subprocess.Popen("rm md5.txt 2> /dev/null", shell=True).wait()
        rmold2=subprocess.Popen("rm /active.txt 2> /dev/null", shell=True).wait()
        updatesvn=subprocess.Popen("svn co http://svn.secmaniac.com/fasttrack %s" % (definepath), shell=True).wait()
        print "\n    Fast-Track is now running the latest version...\n\n"
        print ("    NOTE: If you received an error, you will need to manually update Fast-Track. Simply type rm -rf * (from the Fast-Track directory) then type svn co http://svn.secmaniac.com/fasttrack .\n\n") 

except KeyboardInterrupt :
        print """\n\n    Exiting Fast-Track...\n"""
        time.sleep(3)

except Exception :
        print """\n    Something went wrong when trying to update...Try again??\n"""
        time.sleep(5)
