#!/usr/bin/env python

import sys,os
definepath=os.getcwd()
sys.path.append("%s/bin/ftsrc/" % (definepath))
import include

# method to display the tutorial text
def show_tutorial(tutorial_file):
   include.print_banner()
   print '\n'
   display = open(tutorial_file, 'r')
   try:
      for line in display:
         sys.stdout.write(line)
   finally:
      display.close()
      pause=raw_input("\nPress enter to return to menu")

while 1==1:
   include.print_banner()
   tutmenu1=raw_input('''\nFast-Track Tutorials Menu:

    1.  General Functionality and Movement in Fast-Track
    2.  How to update Fast-Track
    3.  MetaSploit AutoPwn
    4.  SQL 1433 Hacking
    5.  SQL Injection HOWTO
    6.  FTP Brute Forcer
    7.  Spawning a Shell
    8.  Exploits
    9.  Mass Client-Side Attacks
    10. Binary to Hex Payload Generator
    
    (q)uit

    Enter number: ''')

####################################################################

   if tutmenu1 == '1':
      tutorial_file="bin/ftsrc/tutorials/general_functionality.txt"
      show_tutorial(tutorial_file)

   if tutmenu1 == '2':
      tutorial_file="bin/ftsrc/tutorials/updating_fasttrack.txt"
      show_tutorial(tutorial_file)

   if tutmenu1 == '3':
      tutorial_file="bin/ftsrc/tutorials/metasploit_autopwn.txt"
      show_tutorial(tutorial_file)

   if tutmenu1 == '4':
      tutorial_file="bin/ftsrc/tutorials/sql_1433_hacking.txt"
      show_tutorial(tutorial_file)

   if tutmenu1 == '5':
      tutorial_file="bin/ftsrc/tutorials/sql_injection_howto.txt"
      show_tutorial(tutorial_file)

   if tutmenu1 == '6':
      tutorial_file="bin/ftsrc/tutorials/ftp_brute_forcer.txt"
      show_tutorial(tutorial_file)

   if tutmenu1 == '7':
      tutorial_file="bin/ftsrc/tutorials/spawn_command_shell.txt"
      show_tutorial(tutorial_file)

   if tutmenu1 == '8':
      tutorial_file="bin/ftsrc/tutorials/exploits_menu.txt"
      show_tutorial(tutorial_file)

   if tutmenu1 == '9':
      tutorial_file="bin/ftsrc/tutorials/mass_clientside_attack.txt"
      show_tutorial(tutorial_file)

   if tutmenu1 == '10':
      tutorial_file="bin/ftsrc/tutorials/binary_hex_payload.txt"
      show_tutorial(tutorial_file)

   if tutmenu1 == 'q':
      print '\n\nReturning to main menu...\n'
      break
      