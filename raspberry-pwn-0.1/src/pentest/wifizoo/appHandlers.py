# wifizoo
# app handlers
# complains to Hernan Ochoa (hernan@gmail.com)

import curses.ascii
from scapy import *
import wifiglobals
import datetime

# big TODO: create class hierarchy, the same code is repeated 10 times

def msnHandler(pkt):
	wifiglobals.Info.incrementCounter('1863/tcp')
	raw = pkt['Raw']
	ippkt = pkt['IP']
	tpkt = pkt['TCP']
	dot11 = pkt.getlayer(Dot11)
	f = open(wifiglobals.Info.logDir()+"msn.log", "ab")
	f.write( "WHEN: " + str(datetime.datetime.now()) + "\n" )
	pktChannel = 0
	if wifiglobals.Info.hasPrismHeaders() == 1:
		pktChannel = pkt.channel
	f.write("SRC: channel " + str(pktChannel) + "\n")
	(src,dst,bssid) = wifiglobals.Info.getSrcDstBssid(pkt)
	ssid = wifiglobals.Info.getSSID(bssid)
	f.write("SRC: bssid=" + bssid + " (" + ssid + ")" + " src=" + src +  " dst=" + dst  + "\n")
 	f.write("TCP: " + str(ippkt.src) + "." + str(tpkt.sport) + ' -> ' + str(ippkt.dst) + "." + str(tpkt.dport) + '\n')
	for c in str(raw):
            if wifiglobals.Info.isAlpha(c):
            	f.write(c)
	f.write('\n')
	f.close()
	return

def httpHandler(pkt):
	wifiglobals.Info.incrementCounter('80/tcp')
	raw = pkt['Raw']
	dot11 = pkt.getlayer(Dot11)
	ippkt = pkt['IP']
	tpkt = pkt['TCP']
	f = open(wifiglobals.Info.logDir()+"http.log", "ab")
	cf = open(wifiglobals.Info.logDir()+"cookies.log", "ab")
	cf2 = open(wifiglobals.Info.logDir()+"httpauth.log", "ab")
	when =  "WHEN: " + str(datetime.datetime.now()) + "\n" 
	f.write(when)
	pktChannel = 0
	if wifiglobals.Info.hasPrismHeaders() == 1:
		pktChannel = pkt.channel
	src = "SRC: channel " + str(pktChannel) + "\n"
	f.write(src)
	(src,dst,bssid) = wifiglobals.Info.getSrcDstBssid(pkt)
	ssid = wifiglobals.Info.getSSID(bssid)
	airdata = "SRC: bssid=" + bssid + " (" + ssid + ")" + " src=" + src +  " dst=" + dst  + "\n"
	f.write(airdata)
 	tcpdata = "TCP: " + str(ippkt.src) + "." + str(tpkt.sport) + ' -> ' + str(ippkt.dst) + "." + str(tpkt.dport) + '\n'
	f.write(tcpdata)
	data = ''
	for c in str(raw):
            if wifiglobals.Info.isAlpha(c):
            	data = data + c
	f.write(data)
	lines = data.split('\n')
	post = ''
	get = ''
	hosth = ''
	for line in lines:
		if line.find("POST ") != -1 or line.find("post ") != -1:
			post = line
		if line.find("GET ") != -1 or line.find("get ") != -1:
			get = line
		if line.find("Host:") != -1 or line.find("host:") != -1:
			hosth = line
		if line.find("Set-Cookie:") != -1 or line.find("Cookie:") != -1:
			cf.write("-"*80+"\n")
			cf.write(when)
			cf.write(airdata)
			cf.write(tcpdata)
			if post != '':
				cf.write(post + "\n")
			if get != '':
				cf.write(get + "\n")
			if hosth != '':
				cf.write(hosth + "\n")
			cf.write("COOKIE: " + line + "\n")
			cf.write("-"*80+"\n")
		if line.find("Authorization:") != -1 or line.find("WWW-Authenticate") != -1:
			cf2.write("-"*80+"\n")
			cf2.write(when)
			cf2.write(airdata)
			cf2.write(tcpdata)
			if post != '':
				cf2.write(post + "\n")
			if get != '':
				cf2.write(get + "\n")
			if hosth != '':
				cf2.write(hosth + "\n")
			cf2.write("AUTH:"  + line + "\n")
			cf.write("-"*80+"\n")
	f.write('\n')
	f.close()
	cf.close()

	
	return


def smtpHandler(pkt):
	wifiglobals.Info.incrementCounter('25/tcp')
	raw = pkt['Raw']
	ippkt = pkt['IP']
	tpkt = pkt['TCP']
	dot11 = pkt.getlayer(Dot11)
	f = open(wifiglobals.Info.logDir()+"smtp.log", "ab")
	f.write( "WHEN: " + str(datetime.datetime.now()) + "\n" )
	pktChannel = 0
	if wifiglobals.Info.hasPrismHeaders() == 1:
		pktChannel = pkt.channel
	f.write("SRC: channel " + str(pktChannel) + "\n")
	(src,dst,bssid) = wifiglobals.Info.getSrcDstBssid(pkt)
	ssid = wifiglobals.Info.getSSID(bssid)
	airdata = "SRC: bssid=" + bssid + " (" + ssid + ")" + " src=" + src +  " dst=" + dst  + "\n"
	f.write(airdata)
 	f.write("TCP: " + str(ippkt.src) + "." + str(tpkt.sport) + ' -> ' + str(ippkt.dst) + "." + str(tpkt.dport) + '\n')
	for c in str(raw):
            if wifiglobals.Info.isAlpha(c):
            	f.write(c)
	f.write('\n')
	f.close()
	return

	
def pop3Handler(pkt):
	wifiglobals.Info.incrementCounter('110/tcp')
	raw = pkt['Raw']
	ippkt = pkt['IP']
	tpkt = pkt['TCP']
	dot11 = pkt.getlayer(Dot11)
	f = open(wifiglobals.Info.logDir()+"pop3.log", "ab")
	when = "WHEN: " + str(datetime.datetime.now()) + "\n" 
	f.write(when)
	pktChannel = 0
	if wifiglobals.Info.hasPrismHeaders() == 1:
		pktChannel = pkt.channel
	f.write("SRC: channel " + str(pktChannel) + "\n")
	(src,dst,bssid) = wifiglobals.Info.getSrcDstBssid(pkt)
	ssid = wifiglobals.Info.getSSID(bssid)
	airdata = "SRC: bssid=" + bssid + " (" + ssid + ")" + " src=" + src +  " dst=" + dst  + "\n"
	f.write(airdata)
 	tcpdata = "TCP: " + str(ippkt.src) + "." + str(tpkt.sport) + ' -> ' + str(ippkt.dst) + "." + str(tpkt.dport) + '\n'
	f.write(tcpdata)
	data = ''
	for c in str(raw):
            if wifiglobals.Info.isAlpha(c):
		data =  data + c
        f.write(data)
	f.write('\n')
	f.close()

	lines = data.split("\n")    
	uf = open(wifiglobals.Info.logDir()+"pop3_creds.log", "ab")
	for line in lines:
		if line.find("USER") != -1 or line.find("user") != -1:
			uf.write(when)
			uf.write(airdata)
			uf.write(tcpdata)
			uf.write(line + "\n")
		if line.find("PASS") != -1 or line.find("pass") != -1:
			uf.write(when)
			uf.write(airdata)
			uf.write(tcpdata)
			uf.write(line + "\n") 

	uf.close()
	return

def ftpHandler(pkt):
	wifiglobals.Info.incrementCounter('21/tcp')
	raw = pkt['Raw']
	ippkt = pkt['IP']
	tpkt = pkt['TCP']
	dot11 = pkt.getlayer(Dot11)
	f = open(wifiglobals.Info.logDir()+"ftp.log", "ab")
	f.write( "WHEN: " + str(datetime.datetime.now()) + "\n" )
	pktChannel = 0
	if wifiglobals.Info.hasPrismHeaders() == 1:
		pktChannel = pkt.channel
	f.write("SRC: channel " + str(pktChannel) + "\n")
	(src,dst,bssid) = wifiglobals.Info.getSrcDstBssid(pkt)
	ssid = wifiglobals.Info.getSSID(bssid)
	airdata = "SRC: bssid=" + bssid + " (" + ssid + ")" + " src=" + src +  " dst=" + dst  + "\n"
	f.write(airdata)
 	f.write("TCP: " + str(ippkt.src) + "." + str(tpkt.sport) + ' -> ' + str(ippkt.dst) + "." + str(tpkt.dport) + '\n')
	for c in str(raw):
            if wifiglobals.Info.isAlpha(c):
            	f.write(c)
	f.write('\n')
	f.close()
	return


def telnetHandler(pkt):
	wifiglobals.Info.incrementCounter('23/tcp')
	raw = pkt['Raw']
	ippkt = pkt['IP']
	tpkt = pkt['TCP']
	dot11 = pkt.getlayer(Dot11)
	f = open(wifiglobals.Info.logDir()+"telnet.log", "ab")
	f.write( "WHEN: " + str(datetime.datetime.now()) + "\n" )
	pktChannel = 0
	if wifiglobals.Info.hasPrismHeaders() == 1:
		pktChannel = pkt.channel
	f.write("SRC: channel " + str(pktChannel) + "\n")
	(src,dst,bssid) = wifiglobals.Info.getSrcDstBssid(pkt)
	ssid = wifiglobals.Info.getSSID(bssid)
	airdata = "SRC: bssid=" + bssid + " (" + ssid + ")" + " src=" + src +  " dst=" + dst  + "\n"
	f.write(airdata)
 	f.write("TCP: " + str(ippkt.src) + "." + str(tpkt.sport) + ' -> ' + str(ippkt.dst) + "." + str(tpkt.dport) + '\n')
	for c in str(raw):
            if wifiglobals.Info.isAlpha(c):
            	f.write(c)
	f.write('\n')
	f.close()
	return

def netbiosnsHandler(pkt):
	wifiglobals.Info.incrementCounter('137/udp')
	raw = pkt['Raw']
	ippkt = pkt['IP']
	tpkt = pkt['UDP']
	dot11 = pkt.getlayer(Dot11)
	f = open(wifiglobals.Info.logDir()+"nbtns.log", "ab")
	f.write( "WHEN: " + str(datetime.datetime.now()) + "\n" )
	pktChannel = 0
	if wifiglobals.Info.hasPrismHeaders() == 1:
		pktChannel = pkt.channel
	f.write("SRC: channel " + str(pktChannel) + "\n")
	(src,dst,bssid) = wifiglobals.Info.getSrcDstBssid(pkt)
	ssid = wifiglobals.Info.getSSID(bssid)
	airdata = "SRC: bssid=" + bssid + " (" + ssid + ")" + " src=" + src +  " dst=" + dst  + "\n"
	f.write(airdata)
 	f.write("UDP: " + str(ippkt.src) + "." + str(tpkt.sport) + ' -> ' + str(ippkt.dst) + "." + str(tpkt.dport) + '\n')

	for c in str(raw):
		 if wifiglobals.Info.isAlpha(c):
			f.write(c)


	
#	if tpkt.haslayer(NBNSRequest):
#			h = tpkt.getlayer(NBNSRequest)
#	if tpkt.haslayer(NBNSQueryRequest):
#			h = tpkt.getlayer(NBNSQueryRequest)
#	if tpkt.haslayer(NBNSQueryResponse):
#			h = tpkt.getlayer(NBNSQueryResponse)
#	if tpkt.haslayer(NBNSQueryResponseNegative):
#			h = tpkt.getlayer(NBNSQueryResponseNegative)
#	if tpkt.haslayer(NBNSNodeStatusResponse):
#			h = tpkt.getlayer(NBNSNodeStatusResponse)
#	if tpkt.haslayer(NBNSNodeStatusResponseService):
#			h = tpkt.getlayer(NBNSNodeStatusResponseService)
#	if tpkt.haslayer(NBNSNodeStatusResponseEnd):
#			h = tpkt.getlayer(NBNSNodeStatusResponseEnd)
#	if tpkt.haslayer(NBNSWackResponse):
#			h = tpkt.getlayer(NBNSWackResponse)
#	
#	f.write( str(h) )
	f.write('\n')
	f.close()
	return

def netbiosdgmHandler(pkt):
	wifiglobals.Info.incrementCounter('138/udp')
	raw = pkt['Raw']
	ippkt = pkt['IP']
	tpkt = pkt['UDP']
	dot11 = pkt.getlayer(Dot11)
	f = open(wifiglobals.Info.logDir()+"nbtdgm.log", "ab")
	f.write( "WHEN: " + str(datetime.datetime.now()) + "\n" )
	pktChannel = 0
	if wifiglobals.Info.hasPrismHeaders() == 1:
		pktChannel = pkt.channel
	f.write("SRC: channel " + str(pktChannel) + "\n")
	(src,dst,bssid) = wifiglobals.Info.getSrcDstBssid(pkt)
	ssid = wifiglobals.Info.getSSID(bssid)
	airdata = "SRC: bssid=" + bssid + " (" + ssid + ")" + " src=" + src +  " dst=" + dst  + "\n"
	f.write(airdata)
 	f.write("UDP: " + str(ippkt.src) + "." + str(tpkt.sport) + ' -> ' + str(ippkt.dst) + "." + str(tpkt.dport) + '\n')
	for c in str(raw):
		if wifiglobals.Info.isAlpha(c):
       		     	f.write(c)
#	if tpkt.haslayer(NBTDatagram):
#		h = tpkt.getlayer(NBTDatagram)
#		f.write( str(h) )
	f.write('\n')
	f.close()
	return

