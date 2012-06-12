#!/usr/bin/env python

import os
import re
import time

# Compile a regex for faster searching
re_distrofile = re.compile ('BackTrack.+')


def get_version():
    readversion=file("bin/version/version","r")
    for line in readversion:
        version=line.rstrip()
    return version
#
# Class for colors
#
class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

    def disable(self):
        self.PURPLE = ''
        self.BLUE = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.RED = ''
        self.ENDC = ''

def print_banner():
        time.sleep(1)
        os.system("clear")
        print bcolors.BLUE + """
  [---]                                                  [---]
  [---]          Fast Track: A new beginning             [---]
  [---]        Written by:""" + bcolors.RED+""" David Kennedy """+bcolors.BLUE+"""("""+bcolors.YELLOW+"""ReL1K"""+bcolors.BLUE+""")         [---]
  [---]        Lead Developer:""" + bcolors.RED+""" Joey Furr """+bcolors.BLUE+"""("""+bcolors.YELLOW+"""j0fer"""+bcolors.BLUE+""")         [---]
  [---]                 Version: """ + bcolors.RED + """4.0.1""" + bcolors.BLUE +"""                   [---]
  [---]        Homepage: """ + bcolors.YELLOW + """http://www.secmaniac.com""" + bcolors.BLUE + """        [---]
  [---]                                                  [---]
  """ + bcolors.ENDC


### OLD CODE
#def print_banner():
#    os.system("clear")
#    print ''' *****************************************************************
# **                                                             **
# **  Fast-Track - A new beginning...                            **
# **  Version: 4.0.2                                             **
# **  Written by: David Kennedy (ReL1K)                          **
# **  Lead Developer: Joey Furr (j0fer)                          **
# **  http://www.secmaniac.com                                   **
# **                                                             **
# *****************************************************************'''
 
