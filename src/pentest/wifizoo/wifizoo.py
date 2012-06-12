# wifizoo
# complains to Hernan Ochoa (hernan@gmail.com)
import sys
import curses.ascii
from scapy import *
import scapy
import wifiglobals
import appHandlers
import datetime
import getopt
from scapy.all import *

import WifiZooEntities
import wifizoowebgui
import wifizooproxy

# tcp port numbers
HTTP_PORT = 80
POP3_PORT = 110
FTP_PORT = 21
TELNET_PORT = 23
MSN_PORT = 1863
SMTP_PORT = 25

# udp port numbers
NETBIOS_NS_UDP		=	137
NETBIOS_DGM_UDP		=	138

# dictionary of portnumber->handler
tcpHandlers = {}
udpHandlers = {}


# add your handlers here
# tcpHandlers
tcpHandlers[ HTTP_PORT ] = appHandlers.httpHandler
tcpHandlers[ POP3_PORT ] = appHandlers.pop3Handler
tcpHandlers[ FTP_PORT  ] = appHandlers.ftpHandler
tcpHandlers[ TELNET_PORT ] = appHandlers.telnetHandler
tcpHandlers[ MSN_PORT ] = appHandlers.msnHandler
tcpHandlers[ SMTP_PORT ] = appHandlers.smtpHandler

# udpHandlers
udpHandlers[ NETBIOS_NS_UDP ] = appHandlers.netbiosnsHandler
udpHandlers[ NETBIOS_DGM_UDP ] = appHandlers.netbiosdgmHandler

#config
conf.verb=0
# interface where to listen for traffic
# tested with a rt2570 chipset
conf.iface = 'rausb0'


def showBanner():
	print "WifiZoo v1.3 -complaints to Hernan Ochoa (hernan@gmail.com)"
	print "options:"
	print "\t-i <interface>"
	print "\t-c <pcap_file>\n"


### MAIN ###

if len(sys.argv) < 2:
	showBanner()
	sys.exit(0)

# parameters
iface_name = 'None'
pcap_filename = 'None'

pcap_opt = 0
iface_opt = 0

try:
	opts, args = getopt.getopt(sys.argv[1:], 'i:c:')

except getopt.GetoptError, e:
	print e
	sys.exit(0)

for o, a in opts:
	if o == '-i':
		iface_name = a
		iface_opt = 1
	elif o == '-c':
		pcap_filename = a
		pcap_opt = 1

if pcap_opt == 1 and iface_opt == 1:
	showBanner()
	print "You cannot use -i and -c together!."
	sys.exit(0)

if pcap_opt == 0 and iface_opt == 0:
	showBanner()
	sys.exit(0)

if iface_opt == 1:	
	conf.iface = iface_name


print "WifiZoo v1.3, complains to Hernan Ochoa (hernan@gmail.com)"
if iface_opt == 1:
	print "using interface %s" % iface_name
elif pcap_opt == 1:
	print "using capture file %s" % pcap_filename

webgui = wifizoowebgui.WifiZooWebGui()
webgui.start()
webproxy = wifizooproxy.WifiZooProxy()
webproxy.start()
print "Waiting..."

# if pcap file specified, read packets from file
if pcap_opt == 1:
	pcapr = PcapReader(pcap_filename)

	
while 1:
	# mm, would be better to use callback perhaps. TODO
	if iface_opt == 1:
		p = sniff(filter=None, iface=conf.iface, count=1)
		pkt = p[0]
	elif pcap_opt == 1:
		try:
			pkt = pcapr.next()
		except:
			continue


	if not pkt.haslayer(Dot11):
		# this is not a 802.11 packet
		continue

	if pkt.haslayer(Dot11):
		if not pkt.haslayer(PrismHeader):
			# I assume now the card does not output prism headers
			wifiglobals.Info.setHasPrismHeaders(0)
		else:
			wifiglobals.Info.setHasPrismHeaders(1)

	#if not pkt.haslayer(PrismHeader) or not pkt.haslayer(Dot11):
	#		continue

	# try to add to AP & clients list
	#0 = mgmt, 1=control, 2=data
	d = pkt.getlayer(Dot11)
	t= pkt.getlayer(Dot11).type
	if t == 2:
		# if packet FROMDS then dst,bssid,src
		# if packet TODS then bssid,src,dst
		# toDS
		#print d.mysummary()
		#print d.FCfield
		if d.FCfield & 1:
			#print "toDS"
			bssid = str(d.addr1)
			src = str(d.addr2)
			dst = str(d.addr3)
			wifiglobals.Info.addClients(src,dst,bssid)
			#try to add the bssid to our list of APs
			# this is hardcore :)
			isprotected = 0
                	if pkt.sprintf("%Dot11ProbeResp.cap%").find("privacy") != -1:
                                isprotected = 1
                	else:
                                isprotected = 0
                	pktChannel = 0
                	if wifiglobals.Info.hasPrismHeaders() == 1:
                        	pktChannel = pkt.channel
                	if wifiglobals.Info.addAccessPoint( bssid, '', pktChannel, isprotected ) == 1:
				wifiglobals.Info.dumpAccessPointsList()
                   	 

		# fromDS
		elif d.FCfield & 2:
			#print "fromDS"
			dst = str(d.addr1)
			bssid = str(d.addr2)
			src = str(d.addr3)
			wifiglobals.Info.addClients(src,dst,bssid)
			#try to add the bssid to our list of APs
			# this is hardcore :)
                        isprotected = 0
                        if pkt.sprintf("%Dot11ProbeResp.cap%").find("privacy") != -1:
                                isprotected = 1
                        else:
                                isprotected = 0
                        pktChannel = 0
                        if wifiglobals.Info.hasPrismHeaders() == 1:
                                pktChannel = pkt.channel
                        if wifiglobals.Info.addAccessPoint( bssid, '', pktChannel, isprotected ) == 1:
				wifiglobals.Info.dumpAccessPointsList()



		# if bits are 0 & 0, thn ad-hoc network
		# if bits are 1 & 1, then WDS system
		#print wifiglobals.Info.getClients()
		# is the packet encrypted?
		#if d.FCfield & 0x40 == 0:
		#		print "UNENCRYPTED"
		#else:
		#		print "ENCRYPTED"


	# is it a probe request?
	if pkt.haslayer(Dot11ProbeReq):
		aProbeRequest = WifiZooEntities.ProbeRequest()
		aProbeRequest.setPKT(pkt)
		aProbeRequest.setDST( str(pkt.getlayer(Dot11).addr1) )
		aProbeRequest.setSRC( str(pkt.getlayer(Dot11).addr2) )
		aProbeRequest.setBSSID( str(pkt.getlayer(Dot11).addr3) )
		if wifiglobals.Info.hasPrismHeaders() == 1:
			aProbeRequest.setChannel( pkt.channel )
		else:
			aProbeRequest.setChannel( 0 )

		thetime = datetime.datetime.now()
		aProbeRequest.setFirstSeen( thetime )
		aProbeRequest.setLastSeen( thetime )
		# let's check if the ssid is 'printable'
		assid = pkt.sprintf("%Dot11ProbeReq.info%")
		#print len(assid)
		#for x in assid:
		#	print hex(ord(x))
		#print "===FIN==="
		isPrintable = 1
		for x in assid:
			if not wifiglobals.Info.isAlpha(x):
				isPrintable = 0
				break

		if isPrintable == 0:
			temp = assid
			assid = ''
			for x in temp:
				assid = assid + str(hex(ord(x)))
			
		aProbeRequest.setSSID( assid )
		wifiglobals.Info.addProbeRequest( aProbeRequest )
		wifiglobals.Info.dumpProbeRequests()

	if pkt.haslayer(Dot11ProbeResp):
		#dst,src,bssid
		src = str(pkt.getlayer(Dot11).addr2)
		ssid = pkt.sprintf("%Dot11ProbeResp.info%")
		# this is hardcore :)
		if pkt.sprintf("%Dot11ProbeResp.cap%").find("privacy") != -1:
				isprotected = 1
		else:
				isprotected = 0
		pktChannel = 0
		if wifiglobals.Info.hasPrismHeaders() == 1:
			pktChannel = pkt.channel
		if wifiglobals.Info.addAccessPoint( src, ssid, pktChannel, isprotected ) == 1:
			wifiglobals.Info.dumpAccessPointsList()

	# is it a beacon?
	# if it is, get SSID
	if pkt.haslayer(Dot11Beacon):
		# bssid
		j = pkt.getlayer(Dot11).addr3
		# ssid
		s = pkt.getlayer(Dot11Beacon).getlayer(Dot11Elt).info
		# this is hardcore :)
		if pkt.sprintf("%Dot11Beacon.cap%").find("privacy") != -1:
				isprotected = 1
		else:
				isprotected = 0
		pktChannel = 0
		if wifiglobals.Info.hasPrismHeaders() == 1:
			pktChannel = pkt.channel
		if wifiglobals.Info.addAccessPoint( j, s, pktChannel, isprotected) == 1:
			wifiglobals.Info.dumpAccessPointsList()



	if pkt.getlayer(IP) == 0 or pkt.getlayer(UDP) == 0 or pkt.getlayer(TCP) == 0:
		continue
		
	dot11 = pkt.getlayer(Dot11)
	raw = pkt['Raw']
	ippkt = pkt['IP']
	tpkt = None
	isUDP = 0
	isTCP = 0
	#isUDP = isTCP = 0
	try:
		tpkt = pkt['UDP']
		if tpkt != None:
			isUDP = 1
	except e: 
		print "error in udp"
		isUDP = 0

	if isUDP == 0:	
		try:
			tpkt = pkt['TCP']
			if tpkt != None:
				isTCP = 1
		except ex:
			print "error in tcp"
			isTCP = 0


	if isTCP == 1:
		try:
			if wifiglobals.Info.hasPrismHeaders() == 1:
				print "Channel: " + str(pkt.channel)
			else:
				print "Channel: Unavailable (No PrismHeaders)."
		except Exception, e:
			print e
		(src,dst,bssid) = wifiglobals.Info.getSrcDstBssid(pkt)
		print "bssid=" + bssid + " src=" + src + " dst=" + dst
		print "TCP: " + str(ippkt.src) + "." + str(tpkt.sport) + ' -> ' + str(ippkt.dst) + "." + str(tpkt.dport)

	if isUDP == 1:
		if wifiglobals.Info.hasPrismHeaders() == 1:
			print "Channel: " + str(pkt.channel)
		else:
			print "Channel: Unavailable (No PrismHeaders)."

		(src,dst,bssid) = wifiglobals.Info.getSrcDstBssid(pkt)
		print "bssid=" + bssid + " src=" + src + " dst=" + dst
		print "UDP: " + str(ippkt.src) + "." + str(tpkt.sport) + ' -> ' + str(ippkt.dst) + "." + str(tpkt.dport)


	if raw != None:
		if isTCP:
			for port in tcpHandlers.keys():
				if tpkt.dport == port or tpkt.sport == port:
					tcpHandlers[ port ](pkt)
				
	
		if isUDP:
			for port in udpHandlers.keys():
				if tpkt.dport == port or tpkt.sport == port:
					udpHandlers[ port ](pkt)


