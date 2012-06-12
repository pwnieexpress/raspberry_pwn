#!/usr/bin/env python
'''Created on Sep 18, 2010
@author: Joey Furr (j0fer)'''

import os
from bin.include import print_banner
from time import sleep

# For NSE integration
def runnse(command):
    print_banner()
    os.system(command)
    raw_input("\nPress <enter> to return...\n")


def get_target(counter,self_banner):
    
    """ get user input, check for valid input, and 
        loop back through if invalid input is entered. """
    
    tries = counter
    target_input = raw_input("""
    NOTE: A single host or a network/block can be specified for testing.
          examples:   192.168.1.21
                      192.168.1.0/24
    
    Enter the host or range to be checked: """)
    if counter == 3:
        print_banner()
        print self_banner
        sleep(1)
        print "    Just so you know...I can go on like this all day...."
        sleep(1)
        tries = 0
        get_target(tries,self_banner)

    if target_input == "" or len(target_input.split(".")) != 4:
        print_banner()
        print self_banner
        print "    *** YOU MUST ENTER A VALID HOST OR RANGE TO CHECK **"
        tries+=1
        get_target(tries,self_banner)
    else:
        return(target_input)
