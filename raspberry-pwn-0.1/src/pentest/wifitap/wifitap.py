#! /usr/bin/env python

########################################
#
# wifitap.py --- WiFi injection tool through tun/tap device
#
# Copyright (C) 2005 Cedric Blancher <sid@rstack.org>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation; version 2.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
#########################################

import os,sys,getopt,struct,re,string,logging

# Import Psyco if available to speed up execution
try:
	import psyco
	psyco.full()
except ImportError:
	print "Psyco optimizer not installed, running anyway..."

from socket import *
from fcntl  import ioctl
from select import select

logging.getLogger("scapy").setLevel(1)
from scapy  import Raw,Ether,PrismHeader,Dot11,Dot11WEP,LLC,SNAP,sendp,conf

TUNSETIFF = 0x400454ca
IFF_TAP   = 0x0002
TUNMODE   = IFF_TAP

IN_IFACE  = "ath0"
OUT_IFACE = "ath0"
HAS_SMAC  = 0
SMAC      = ""
WEP       = 0
KEYID     = 0
DEBUG     = 0
VERB      = 0
BSSID     = ""
WEPKEY    = ""


def usage(status=0):
    print "Usage: wifitap -b <BSSID> [-o <iface>] [-i <iface>] [-s <SMAC>]"
    print "                          [-w <WEP key> [-k <key id>]] [-d [-v]] [-h]"
    print "     -b <BSSID>    specify BSSID for injection"
    print "     -o <iface>    specify interface for injection (default: ath0)"
    print "     -i <iface>    specify interface for listening (default: ath0)"
    print "     -s <SMAC>     specify source MAC address for injected frames"
    print "     -w <key>      WEP mode and key"
    print "     -k <key id>   WEP key id (default: 0)"
    print "     -d            activate debug"
    print "     -v            verbose debugging"
    print "     -h            this so helpful output"
    sys.exit(status)

opts = getopt.getopt(sys.argv[1:],"b:o:i:s:w:k:dvh")

for opt,optarg in opts[0]:
    if opt == "-b":
	BSSID = optarg
    elif opt == "-o":
	OUT_IFACE = optarg
    elif opt == "-i":
	IN_IFACE = optarg
    elif opt == "-s":
	HAS_SMAC += 1
	SMAC = optarg
    elif opt == "-w":
	WEP += 1
	WEPKEY = optarg
    elif opt == "-k":
	KEYID = int(optarg)
    elif opt == "-d":
	DEBUG += 1
    elif opt == "-v":
	VERB += 1
    elif opt == "-h":
	usage()

if not BSSID:
    print "\nError: BSSID not defined\n"
    usage()

# Match and parse BSSID
if re.match('^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$', BSSID):
    BSSID = BSSID.lower()
else:
    print "\nError: Wrong format for BSSID\n"
    usage ()

# Support for source MAC spoofing for adhoc support
if HAS_SMAC:
    if not SMAC:
	print "\nError: SMAC not defined\n"
	usage()
    # Match and parse SMAC
    elif re.match('^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$', SMAC):
	SMAC = SMAC.lower()
    else:
	print "\nError: Wrong format for SMAC\n"
	usage()

print "IN_IFACE:   %s" % IN_IFACE
print "OUT_IFACE:  %s" % OUT_IFACE
print "BSSID:      %s" % BSSID
if HAS_SMAC:
    print "SMAC:       %s" % SMAC

if WEP:
    # Match and parse WEP key
    tmp_key = ""
    if re.match('^([0-9a-fA-F]{2}){5}$', WEPKEY) or re.match ('^([0-9a-fA-F]{2}){13}$', WEPKEY):
	tmp_key = WEPKEY
    elif re.match('^([0-9a-fA-F]{2}[:]){4}[0-9a-fA-F]{2}$', WEPKEY) or re.match('^([0-9a-fA-F]{2}[:]){12}[0-9a-fA-F]{2}$', WEPKEY):
	tmp_key = re.sub(':', '', WEPKEY)
    elif re.match ('^([0-9a-fA-F]{4}[-]){2}[0-9a-fA-F]{2}$', WEPKEY) or re.match ('^([0-9a-fA-F]{4}[-]){6}[0-9a-fA-F]{2}$', WEPKEY):
	tmp_key = re.sub('-', '', WEPKEY)
    else:
	print "\nError : Wrong format for WEP key\n"
	usage()
    g = lambda x: chr(int(tmp_key[::2][x],16)*16+int(tmp_key[1::2][x],16))
    for i in range(len(tmp_key)/2):
	conf.wepkey += g(i)
    print "WEP key:    %s (%dbits)" % (WEPKEY, len(tmp_key)*4)
    if KEYID > 3 or KEYID < 0:
	print "Key id:     %s (defaulted to 0 due to wrong -k argument)" % KEYID
	KEYID = 0
    else:
	print "Key id:     %s" % KEYID
else:
    if KEYID != 0:
	print "WEP not activated, key id ignored"

if not DEBUG:
    if VERB:
	print "DEBUG not activated, verbosity ignored"
else:
    print "DEBUG activated"
    if VERB:
	print "Verbose debugging"

conf.iface = OUT_IFACE

# Here we put a BPF filter so only 802.11 Data/to-DS frames are captured
s = conf.L2listen(iface = IN_IFACE,
    filter = "link[0]&0xc == 8 and link[1]&0xf == 1")

# Open /dev/net/tun in TAP (ether) mode
f = os.open("/dev/net/tun", os.O_RDWR)
ifs = ioctl(f, TUNSETIFF, struct.pack("16sH", "wj%d", TUNMODE))
ifname = ifs[:16].strip("\x00")
print "Interface %s created. Configure it and use it" % ifname

# Speed optimization si Scapy does not have to parse payloads
Ether.payload_guess=[]
SNAP.payload_guess=[]

try:
    while 1:
        r = select([f,s],[],[])[0]

	# frame from /dev/net/tun
	if f in r:

	    # tuntap frame max. size is 1522 (ethernet, see RFC3580) + 4
	    buf = os.read(f,1526)
            eth_rcvd_frame=Ether(buf[4:])

	    if DEBUG:
	        os.write(1,"Received from %s\n" % ifname)
		if VERB:
		    os.write(1,"%s\n" % eth_rcvd_frame.summary())
	    
	# Prepare Dot11 frame for injection
	    dot11_sent_frame = Dot11(
		type = "Data",
		FCfield = "from-DS",
		addr1 = eth_rcvd_frame.getlayer(Ether).dst,
		addr2 = BSSID)
	# It doesn't seem possible to set tuntap interface MAC address
	# when we create it, so we set source MAC here
	    if not HAS_SMAC:
	        dot11_sent_frame.addr3 = eth_rcvd_frame.getlayer(Ether).src
	    else:
		dot11_sent_frame.addr3 = SMAC
	    if WEP:
		dot11_sent_frame.FCfield |= 0x40
		dot11_sent_frame /= Dot11WEP(
		    iv = "111",
		    keyid = KEYID)
	    dot11_sent_frame /= LLC(ctrl = 3)/SNAP(code=eth_rcvd_frame.getlayer(Ether).type)/eth_rcvd_frame.getlayer(Ether).payload

	    if DEBUG:
	        os.write(1,"Sending from-DS to %s\n" % OUT_IFACE)
		if VERB:
		    os.write(1,"%s\n" % dot11_sent_frame.summary())
	
	# Frame injection :
	    sendp(dot11_sent_frame,verbose=0) # Send from-DS frame

	# Frame from WiFi network
	if s in r:

	    # 802.11 maximum frame size is 2346 bytes (cf. RFC3580)
	    # However, WiFi interfaces are always MTUed to 1500
	    dot11_rcvd_frame = s.recv(2346)

	# WEP handling is automagicly done by Scapy if conf.wepkey is set
	# Nothing to do to decrypt (although not yet tested)
	# WEP frames have Dot11WEP layer, others don't

	    if DEBUG:
		if dot11_rcvd_frame.haslayer(Dot11WEP): # WEP frame
		    os.write(1,"Received WEP from %s\n" % IN_IFACE)
		else: # Cleartext frame
		    os.write(1,"Received from %s\n" % IN_IFACE)
		if VERB:
		    os.write(1,"%s\n" % dot11_rcvd_frame.summary())

	#    if dot11_frame.getlayer(Dot11).FCfield & 1: # Frame is to-DS
	# For now, we only take care of to-DS frames...

	    if dot11_rcvd_frame.getlayer(Dot11).addr1 != BSSID:
		continue

	# One day, we'll try to take care of AP to DS trafic (cf. TODO)
	#    else: # Frame is from-DS
	#        if dot11_frame.getlayer(Dot11).addr2 != BSSID:
	#            continue
	#	eth_frame = Ether(dst=dot11_frame.getlayer(Dot11).addr1,
	#           src=dot11_frame.getlayer(Dot11).addr3)
	    
	    if dot11_rcvd_frame.haslayer(SNAP):
		eth_sent_frame = Ether(
		    dst=dot11_rcvd_frame.getlayer(Dot11).addr3,
		    src=dot11_rcvd_frame.getlayer(Dot11).addr2,
		    type=dot11_rcvd_frame.getlayer(SNAP).code)
		eth_sent_frame.payload = dot11_rcvd_frame.getlayer(SNAP).payload

		if DEBUG:
		    os.write(1, "Sending to %s\n" % ifname)
		    if VERB:
			os.write(1, "%s\n" % eth_sent_frame.summary())

	# Add Tun/Tap header to frame, convert to string and send
		buf = "\x00\x00" + struct.pack("!H",eth_sent_frame.type) + str(eth_sent_frame)
		os.write(f, buf)

# Program killed
except KeyboardInterrupt:
    print "Stopped by user."

s.close()
os.close(f)

sys.exit()
