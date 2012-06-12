#!/usr/bin/env python
# Author: sickness
# Hope you like it
# For any bugs/suggestions contact sick.n3ss416@gmail.com
import sys,subprocess,time,os,signal,socket,getopt,urllib2
from time import sleep,localtime,strftime
#-------------------------------------------------------------------------------
spike = ""
fpath = ""
script = ""
ip = ""
port = ""
iface = ""
log = ""
#-------------------------------------------------------------------------------
def help_screen():
	print "                    __             ___                           "
	print "         __        /\ \          /'___\                          "
	print "     ____/\_\    ___\ \ \/'\     /\ \__/  __  __  ____    ____    "
	print "   /',__\/\ \  /'___\ \ , <     \ \ ,__\/\ \/\ \/\_ ,`\ /\_ ,`\  "
	print "  /\__, `\ \ \/\ \__/\ \ \\`\    \ \ \_/\ \ \_\ \/_/  /_\/_/  /_ "
	print "  \/\____/\ \_\ \____\\ \_\ \_\   \ \_\  \ \____/ /\____\ /\____\ "
	print "   \/___/  \/_/\/____/ \/_/\/_/    \/_/   \/___/  \/____/ \/____/\n\n"
	print "  Welcome to sickfuzz version 0.3"
	print "  Codename: 'Have you g0tmi1k!?'"
	print "  Author: sickness"
	print "  Bug reports or suggestions at: sick.n3ss416@gmail.com\n"
	print "  Usage example:"
	print "  ./sickfuzz.py --spike /pentest/fuzzers/spike/ --fpath /root/sickfuzz/ --script all --ip 192.168.1.64 --port 80 --iface wlan0 --log /root/"+"\n"
	print "  IMPORTANT: DO NOT USE THE pcap_logs DIRECTORY TO SAVE LOGS from --log !!!\n"
	print "	-h/--help  - prints this help menu."
	print "	-s/--spike <path to spike folder>"
	print "	-f/--fpath <path to the fuzzer>"
	print "	-c/--script <[all]/[number]>    use --script-show to view available scripts"
	print "	-t/--ip <target ip>"
	print "	-p/--port <target port>"
	print "	-i/--iface <network interface>"
	print "	-l/--log <path where .pcap log files will be saved> (Other then 'pcap_logs' directory.)\n"
	sys.exit()

def script_show():
	print "  [1/12] Fuzzing: AAAA"
	print "  [2/12] Fuzzing: GET /"
	print "  [3/12] Fuzzing: HEAD /"
	print "  [4/12] Fuzzing: POST /"
	print "  [5/12] Fuzzing: GET / HTTP/1.1"
	print "  [6/11] Fuzzing: HEAD / HTTP/1.1"
	print "  [7/12] Fuzzing: POST / HTTP/1.1"
	print "  [8/12] Fuzzing: Authorization:"
	print "  [9/12] Fuzzing: Content-Length:"
	print "  [10/12] Fuzzing: If-Modified-Since:"
	print "  [11/12] Fuzzing: Connection:"
	print "  [12/12] Fuzzing: X-a:"
	sys.exit()

if len(sys.argv) == 1:
	help_screen()
elif sys.argv[1] == ("--script-show" or "-c-show"):
	script_show()
elif sys.argv[1] == ("-?" or "-h" or "--help"):
	help_screen()

	
def openport():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		s.connect((ip,int(port)))
		s.shutdown(2)
		return True
	except:
		return False
	

def spike_fuzz( x ):
	if x == 0: print " [>] [1/12] Fuzzing: AAAA"
	elif x == 1: print " [>] [2/12] Fuzzing: GET /"
	elif x == 2: print " [>] [3/12] Fuzzing: HEAD /"
	elif x == 3: print " [>] [4/12] Fuzzing: POST /"
	elif x == 4: print " [>] [5/12] Fuzzing: GET / HTTP/1.1"
	elif x == 5: print " [>] [6/12] Fuzzing: HEAD / HTTP/1.1"
	elif x == 6: print " [>] [7/12] Fuzzing: POST / HTTP/1.1"
	elif x == 7: print " [>] [8/12] Fuzzing: Authorization:"
	elif x == 8: print " [>] [9/12] Fuzzing: Content-Length:"
	elif x == 9: print " [>] [10/12] Fuzzing: If-Modified-Since:"
	elif x == 10: print " [>] [11/12] Fuzzing: Connection:"
	elif x == 11: print " [>] [12/12] Fuzzing: X-a:"
	try:
		subprocess.Popen("export LD_LIBRARY_PATH=. && cd "+spike+"&&"+fuzzer+" "+ip+" "+port+" "+fpath+scripts[x]+" "+skipv+" > "+fpath+"spike_log.txt",shell=True).wait()
	except KeyboardInterrupt:
		print " [>] Press CTRL+C again to stop fuzzing and start the clear-up process!\n"
		sleep(1000000)
	if openport() == True:
		try:
			print "\n [>] Finished, moving to next script ..."
			print " [>] Press CTRL+C again to stop fuzzing!\n"
		except KeyboardInterrupt:
			log = log.rstrip("/")+"/"
			clean_up()
			sys.exit()
	elif openport() == False:
		print " [>] We have a crash!"
		log = log.rstrip("/")+"/"
		clean_up()
		sys.exit()
		
def clean_up():
	print " [>] Stopping fuzzing and tshark ..."
	os.kill(tshark.pid,signal.SIGTERM)
	print " [>] Starting clean-up process"
	print " [>] Splitting .pcap files"
	subprocess.Popen("editcap -c 10000 "+fpath+"pcap_logs/fuzzing_log.pcap"+" "+fpath+"pcap_logs/logs.pcap",shell=True).wait()
	subprocess.Popen("mv -f "+fpath+"pcap_logs/*"+" "+log,shell=True).wait()
	subprocess.Popen("rm -rf "+fpath+"pcap_logs/*",shell=True).wait()
	subprocess.Popen("mv -f "+fpath+"spike_log.txt"+" "+log,shell=True).wait()
	print " [>] Done!"
	print " [>] Go to the 'pcap_logs' directory and delete anything from there.(DONT DO rm -rf pcap_logs/*)"
	print " [>] For more details about the fuzzing strings open 'spike_log.txt' from your log directory.\n"
	
time_start = time.time()
print "\n [>] Fuzzing starting at "+strftime("%a, %d %b %Y %H:%M:%S", localtime())+" ..."
sleep(2)

try:
    opts, args = getopt.getopt(sys.argv[1:], "s:f:c:t:p:i:l:h?", ["spike=","fpath=","script=","ip=","port=","iface=", "log=","help"])
except getopt.GetoptError, err:
	help_screen()
	sys.exit()
for o, a in opts:
	if o in ("-s", "--spike"):
		spike = a
	if o in ("-f", "--fpath"):
	        fpath = a
	if o in ("-c", "--script"):
		script = a
	if o in ("-t", "--ip"):
		ip = a
	if o in ("-p", "--port"):
		port = a
	if o in ("-i", "--iface"):
		iface = a
	if o in ("-l", "--log"):
		log = a
		
try:
	fuzzer = "./generic_web_server_fuzz2"
	scripts = ["HTTP/web00.spk","HTTP/web01.spk","HTTP/web02.spk","HTTP/web03.spk","HTTP/web04.spk","HTTP/web05.spk","HTTP/web06.spk","HTTP/web07.spk","HTTP/web08.spk","HTTP/web09.spk","HTTP/web10.spk","HTTP/web11.spk"]
	skipv = "0 0"
	
	if spike == "" :
		print "Missing \"--spike/-s\", check --help for more info.\n"
		sys.exit()
	if fpath == "" :
		print "Missing \"--fpath/-f\", check --help for more info.\n"
		sys.exit()
	if script == "" :
		print "Missing \"--script/-c\", check --help for more info.\n"
		sys.exit()
	if ip == "" :
		print "Missing \"--ip/-t\", check --help for more info.\n"
		sys.exit()
	if port == "" :
		print "Missing \"--port/-p\", check --help for more info.\n"
		sys.exit()
	if iface == "" :
		print "Missing \"--iface/-i\", check --help for more info.\n"
		sys.exit()
	if log == "" :
		print "Missing \"--log/-l\", check --help for more info.\n"
		sys.exit()

	print " [>] Starting: sickfuzz v0.3"
	if openport() == True:
		pass
	else:
		print " [>] Could not connect, check if the port is opened!"
		sys.exit()
	print " [>] Launching packet capture, please wait ..."
	try:
		fpath = fpath.rstrip("/")+"/"
		tshark = subprocess.Popen("tshark -i "+iface+" -d tcp.port=="+port+",http -w "+fpath+"pcap_logs/fuzzing_log.pcap -q",shell=True)
		sleep(2)
		print " [>] Capturing packets, now starting the fuzzer ...!\n"
		sleep(1)
	except KeyboardInterrupt:
		print " [>] Something went wrong!"
		print " [>] Exiting ..."
		sys.exit()
	
	if script == "all":
		script_numbers = range(0,12) # Scripts from 1 to 12.
		for i in script_numbers:
			if openport() == True:
				spike = spike.rstrip("/")+"/"
				fpath = fpath.rstrip("/")+"/"
				spike_fuzz( i )

			else:
				log = log.rstrip("/")+"/"
				clean_up()
				sys.exit()
	else:
		if script == "1":
			spike = spike.rstrip("/")+"/"
			fpath = fpath.rstrip("/")+"/"
			spike_fuzz( 0 )
		elif script == "2":
			spike = spike.rstrip("/")+"/"
			fpath = fpath.rstrip("/")+"/"
			spike_fuzz( 1 )
		elif script == "3":
			spike = spike.rstrip("/")+"/"
			fpath = fpath.rstrip("/")+"/"
			spike_fuzz( 2 )
		elif script == "4":
			spike = spike.rstrip("/")+"/"
			fpath = fpath.rstrip("/")+"/"
			spike_fuzz( 3 )
		elif script == "5":
			spike = spike.rstrip("/")+"/"
			fpath = fpath.rstrip("/")+"/"
			spike_fuzz( 4 )
		elif script == "6":
			spike = spike.rstrip("/")+"/"
			fpath = fpath.rstrip("/")+"/"
			spike_fuzz( 5 )
		elif script == "7":
			spike = spike.rstrip("/")+"/"
			fpath = fpath.rstrip("/")+"/"
			spike_fuzz( 6 )
		elif script == "8":
			spike = spike.rstrip("/")+"/"
			fpath = fpath.rstrip("/")+"/"
			spike_fuzz( 7 )
		elif script == "9":
			spike = spike.rstrip("/")+"/"
			fpath = fpath.rstrip("/")+"/"
			spike_fuzz( 8 )
		elif script == "10":
			spike = spike.rstrip("/")+"/"
			fpath = fpath.rstrip("/")+"/"
			spike_fuzz( 9 )
		elif script == "11":
			spike = spike.rstrip("/")+"/"
			fpath = fpath.rstrip("/")+"/"
			spike_fuzz( 10 )
		elif script == "12":
			spike = spike.rstrip("/")+"/"
			fpath = fpath.rstrip("/")+"/"
			spike_fuzz( 11 )
		else:
			print " [-] You have picked an invalid script."
			print " [-] Use the -c-show/--script-show flags to see available scripts."
		print "\n"
#-------------------------------------------------------------------------------
except KeyboardInterrupt:
	print "\r"
	print " [>] Fuzzing process ended at: "+strftime("%a, %d %b %Y %H:%M:%S", localtime())
	print " [>] Elapsed time: %.2f minutes" % ((time.time() - time_start)/60)
	print "\r"
	log = log.rstrip("/")+"/"
	clean_up()
	sys.exit()
