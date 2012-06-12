# WifiZoo
# complains to Hernan Ochoa (hernan@gmail.com)
import curses.ascii
from scapy import *
import datetime
import WifiZooEntities
import os

class WifiGlobals: 
	def __init__(self):
		self.APdict = {}
		self.AccessPointsList = []
		self.ProbeRequestsListBySSID = []
		self.ProbeRequestsListBySRC = []
		self._hasPrismHeaders = 1
		self._logdir = "./logs/"
		self._Cookie = None
		self._CookiesList = []
		self._pktCounters = {}
		self._OUIList = ''

	def incrementCounter(self, proto):
		if self._pktCounters.has_key(proto):
				n = self._pktCounters[proto]
				self._pktCounters[proto] = n+1
		else:
			self._pktCounters[proto] = 1
		
	def getCounter(self, proto):
		return self._pktCounters[proto]

	def getAllCounters(self):
		return self._pktCounters		

	def getMACVendor(self, aMAC):
		if len(aMAC) < 8:
			return 'Unknown'
		if self._OUIList == '':
			f = open("oui_list.txt", "rb")
			self._OUIList = f.read()
			f.close()

		lines = self._OUIList.split('\n')
		myMAC = aMAC[0:8]
		myMAC = myMAC.lower()
		for line in lines:
			if len(line) > 8:
				vendorname = line.split('\t')[2]	
				vendormac = line[0:8].replace('-',':').lower()
				if vendormac == myMAC:
					return vendorname
		return 'Unknown'
			
	def addCookie(self, aCookie):
		self._CookiesList.append(aCookie)
		return

	def getCookiesList(self):
		return self._CookiesList


	def setCookie(self, aCookie):
		self._Cookie = aCookie

	def getCookie(self):
		return self._Cookie

	def setHasPrismHeaders(self, aBoolean):
		self._hasPrismHeaders = aBoolean
	def hasPrismHeaders(self):
		return self._hasPrismHeaders
	def getClients(self):
		return self.APdict

	def logDir(self):
		if not os.path.isdir( self._logdir ):
				os.mkdir( self._logdir )
		return "./logs/"

	def getProbeRequestsBySSID(self):
		return self.ProbeRequestsListBySSID

	def addProbeRequest(self, aProbeRequest):
		# add ProbeRequest by SSID
		found = 0
		if len(aProbeRequest.getSSID()) > 0:
			for pr in self.ProbeRequestsListBySSID:
				if pr.getSSID() == aProbeRequest.getSSID():
					# TODO: change the LASTSEEN thing
					found = 1
		# if SSID was not seen before, add it to the list
		if len(aProbeRequest.getSSID()) > 0 and found == 0:
			self.ProbeRequestsListBySSID.append( aProbeRequest )

		#add ProbeRequest by SRC
		if len(aProbeRequest.getSSID()) == 0:
				for pr in self.ProbeRequestsListBySRC:
					if aProbeRequest.getSRC() == pr.getSRC() and pr.getSSID() == "<Empty>":
						return

				aProbeRequest.setSSID( "<Empty>" )
				self.ProbeRequestsListBySRC.append( aProbeRequest )	
				return
		else:
			for pr in self.ProbeRequestsListBySRC:
				if pr.getSRC() == aProbeRequest.getSRC() and pr.getSSID() == aProbeRequest.getSSID():
					return


		# add proberequests with different src or ssid
		self.ProbeRequestsListBySRC.append( aProbeRequest )		
		

	def dumpProbeRequests(self):
		if len(self.ProbeRequestsListBySSID) >= 1:
			prf = open( self.logDir() + "probereqsuniqssid.log", "wb"  )
			for pr in self.ProbeRequestsListBySSID:
				prf.write("ssid=" + pr.getSSID() + " dst=" + pr.getDST() + " src=" + pr.getSRC() + " bssid=" + pr.getBSSID() + " (ch: " + str(pr.getChannel()) + ")" + "\n")
			prf.close()

		if len(self.ProbeRequestsListBySRC) >= 1:
			prf = open( self.logDir() + "probereqbysrc.log", "wb" )
                        setup = """
digraph ProbeReqGraph {
        compound=true;
        ranksep=1.25;
	rankdir="LR";
        label="Probe Requests by SRC and SSID";

        node [shape=ellipse, fontsize=12];

        bgcolor=white;
        edge[arrowsize=1, color=black];

                        """
			prf.write(setup + "\n\n")
			for pr in self.ProbeRequestsListBySRC:
				prf.write( "\"" + pr.getSSID() + "\""  + " -> " + "\"" + pr.getSRC() + "\"" +  "\r\n" )
		
			prf.write("}\n\n")
			prf.close()

	
	def getAPList(self):
		return self.AccessPointsList

	def getAPbyBSSID(self, aBSSID):
		for ap in self.AccessPointsList:
			if ap.getBSSID() == aBSSID:
				return ap
		return None
	
	def addAccessPoint(self, bssid, ssid, channel, isprotected):
		apFound = 0
		for ap in self.AccessPointsList:
			if ap.getBSSID() == bssid:
				apFound = 1

		# could modify this to 'update' SSID of bssid, but mmm
		if apFound == 1: 
				return 0

		anAP = WifiZooEntities.AccessPoint()
		anAP.setBSSID( bssid )
		anAP.setSSID( ssid )
		anAP.setChannel( channel )
		anAP.setProtected( isprotected )
		# I assume it was found NOW, right before this function was called
		anAP.setFoundWhen( datetime.datetime.now() )
		self.AccessPointsList.append(anAP)
		return 1

	def dumpAccessPointsList(self, outfile='ssids.log'):
		if len(self.AccessPointsList) < 1: 
			return
		sf = open( self.logDir() + outfile , "wb" )

		# first dump OPEN networks
		for ap in self.AccessPointsList:
				if not ap.isProtected():
                        		sf.write( str(ap.getBSSID()) + " -> " + str(ap.getSSID()) + " (ch:" + str(ap.getChannel()) + ")" + " (Encryption:Open)" + " (when: " + str(ap.getFoundWhenString()) + ")" + "\n"  )

		# now protected networks
		for ap in self.AccessPointsList:
				if ap.isProtected():
                        		sf.write( str(ap.getBSSID()) + " -> " + str(ap.getSSID()) + " (ch:" + str(ap.getChannel()) + ")" + " (Encryption:YES)" + " (when: " + str(ap.getFoundWhenString()) + ")" + "\n"  )

                sf.close()
		return

	def addClients(self, src, dst, bssid):
		bssidfound = 0
		dump = 0
		for x in self.APdict.keys():
			if x == bssid:
				bssidfound = 1
				clientList = self.APdict[ x ]
				srcFound = 0
				dstFound = 0
				for client in clientList:
					if client == src:
						srcFound = 1
					if client == dst:
						dstFound = 1
				if srcFound == 0:
					if src != "ff:ff:ff:ff:ff:ff" and src != bssid:
						dump = 1
						clientList.append(src)
				if dstFound == 0:
					if dst != "ff:ff:ff:ff:ff:ff" and dst != bssid:
						dump = 1
						clientList.append(dst)
				self.APdict[ x ] = clientList
		
		if bssidfound == 0:			
			alist = []
			if src != 'ff:ff:ff:ff:ff:ff' and src != bssid:
				dump = 1
				alist.append( src )
			if dst != 'ff:ff:ff:ff:ff:ff' and src != dst and dst != bssid:
				dump = 1
				alist.append( dst )
			self.APdict[ bssid ] = alist
			# add this 'nameless' bssid also to the list of access points
			#self.addAccessPoint(bssid, '<addedbyClient>', 0, 0)
			

		if dump == 1:
			fdump = open(self.logDir()+"clients.log", "wb")
			#fdump.write("--DUMP-----" + "-"*30 + "\n")
			fdump.write("digraph APgraph {\n\n")
			setup = """
			
	compound=true;
       	ranksep=1.25;
	rankdir="LR";
       	label="802.11 bssids->clients";

        node [shape=ellipse, fontsize=12];

        bgcolor=white;
        edge[arrowsize=1, color=black];

			"""
			fdump.write(setup + "\n\n")

			for apmac in self.APdict.keys():
				clientList = self.APdict[ apmac ]
				for client in clientList:
					#fdump.write("\"" + apmac + "\" -> \"" + client + "\"\n") 
					ssid = self.getSSID(apmac)
					fdump.write("\"" + apmac + " (" + ssid + ")\" -> \"" + client + "\"\n") 
			fdump.write("\n }\n")
			#fdump.write("-----------" + "-"*30  +  "\n")
			fdump.close()	
			
	def getSSID(self, bssid):
		aSsid = 'Unknown'
		for ap in self.AccessPointsList:
			if ap.getBSSID() == bssid:
				aSsid = ap.getSSID()
		return aSsid

	# my weird version
 	def isAlpha(self, c):
		if c != '\x0A' and c != '\x0D':
			if curses.ascii.isctrl(c):
				return 0
        	return 1

	def getSrcDstBssid(self, pkt):
		bssid = ''
		src = ''
		dst = ''
		#0 = mgmt, 1=control, 2=data
		p = pkt.getlayer(Dot11)
		# is it a DATA packet?
		t = p.type
		if t == 2:
			# if packet FROMDS then dst,bssid,src
			# if packet TODS then bssid,src,dst
			# toDS
			if p.FCfield & 1:
				#print "toDS"
				bssid = str(p.addr1)
				src = str(p.addr2)
				dst = str(p.addr3)
			# fromDS
			elif p.FCfield & 2:
				#print "fromDS"
				dst = str(p.addr1)
				bssid = str(p.addr2)
				src = str(p.addr3)
			# if bits are 0 & 0, thn ad-hoc network
			# if bits are 1 & 1, then WDS system
			# TODO
		return (src,dst,bssid)

Info =  WifiGlobals()

