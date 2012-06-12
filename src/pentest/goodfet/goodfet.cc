#!/usr/bin/env python
# GoodFET Chipcon Example
# 
# (C) 2009 Travis Goodspeed <travis at radiantmachines.com>
#
# This code is being rewritten and refactored.  You've been warned!

import sys;
import binascii;

from GoodFETCC import GoodFETCC;
from GoodFETConsole import GoodFETConsole;
from intelhex import IntelHex;

if(len(sys.argv)==1):
    print "Usage: %s verb [objects]\n" % sys.argv[0];
    print "%s test" % sys.argv[0];
    print "%s term" % sys.argv[0];
    print "%s info" % sys.argv[0];
    print "%s radioinfo" % sys.argv[0];
    print "%s dumpcode $foo.hex [0x$start 0x$stop]" % sys.argv[0];
    print "%s dumpdata $foo.hex [0x$start 0x$stop]" % sys.argv[0];
    print "%s erase" % sys.argv[0];
    print "%s writedata $foo.hex [0x$start 0x$stop]" % sys.argv[0];
    print "%s verify $foo.hex [0x$start 0x$stop]" % sys.argv[0];
    print "%s peekdata 0x$start [0x$stop]" % sys.argv[0];
    print "%s pokedata 0x$adr 0x$val" % sys.argv[0];
    print "%s peek 0x$iram" % sys.argv[0];
    print "%s poke 0x$iram 0x$val" % sys.argv[0];
    print "%s peekcode 0x$start [0x$stop]" % sys.argv[0];
    sys.exit();

#Initailize FET and set baud rate
#client=GoodFET.GoodFETCC.GoodFETCC();
client=GoodFETCC();
client.serInit()

#Connect to target
client.setup();
client.start();


if(sys.argv[1]=="explore"):
    print "Exploring undefined commands."
    print "Status: %s" %client.status();
    
    cmd=0x04; #read status
    for foo in range(0,0x5):
        client.CCcmd([(0x0F<<3)|(0x00)|0x03,0x09<<3]);
        print "Status %02x: %s" % (foo,client.status());
    for foo in range(0,3):
        print "PC: %04x" % client.CCgetPC();
if(sys.argv[1]=="term"):
    GoodFETConsole(client).run();
if(sys.argv[1]=="test"):
    client.test();
if(sys.argv[1]=="deadtest"):
    for i in range(1,10):
        print "IDENT as %s" % client.CCidentstr();
if(sys.argv[1]=="dumpcode"):
    f = sys.argv[2];
    start=0x0000;
    stop=0xFFFF;
    if(len(sys.argv)>3):
        start=int(sys.argv[3],16);
    if(len(sys.argv)>4):
        stop=int(sys.argv[4],16);
    
    print "Dumping code from %04x to %04x as %s." % (start,stop,f);
    h = IntelHex(None);
    i=start;
    while i<=stop:
        h[i]=client.CCpeekcodebyte(i);
        if(i%0x100==0):
            print "Dumped %04x."%i;
        i+=1;
    h.write_hex_file(f);
if(sys.argv[1]=="dumpdata"):
    f = sys.argv[2];
    start=0xE000;
    stop=0xFFFF;
    if(len(sys.argv)>3):
        start=int(sys.argv[3],16);
    if(len(sys.argv)>4):
        stop=int(sys.argv[4],16);
    
    print "Dumping data from %04x to %04x as %s." % (start,stop,f);
    h = IntelHex(None);
    i=start;
    while i<=stop:
        h[i]=client.CCpeekdatabyte(i);
        if(i%0x100==0):
            print "Dumped %04x."%i;
        i+=1;
    h.write_hex_file(f);
if(sys.argv[1]=="status"):
    print "Status: %s" %client.status();
if(sys.argv[1]=="info"):
    print "%s" % client.CCidentstr();
if(sys.argv[1]=="radioinfo"):
    client.CMDrs();
if(sys.argv[1]=="erase"):
    print "Status: %s" % client.status();
    client.CCchiperase();
    print "Status: %s" %client.status();

if(sys.argv[1]=="peekinfo"):
    print "Select info flash."
    client.CCwr_config(1);
    print "Config is %02x" % client.CCrd_config();
    
    start=0x0000;
    if(len(sys.argv)>2):
        start=int(sys.argv[2],16);
    stop=start;
    if(len(sys.argv)>3):
        stop=int(sys.argv[3],16);
    print "Peeking from %04x to %04x." % (start,stop);
    while start<=stop:
        print "%04x: %02x" % (start,client.CCpeekcodebyte(start));
        start=start+1;
if(sys.argv[1]=="poke"):
    client.CCpokeirambyte(int(sys.argv[2],16),
                          int(sys.argv[3],16));
if(sys.argv[1]=="randtest"):
    #Seed RNG
    client.CCpokeirambyte(0xBD,0x01); #RNDH=0x01
    client.CCpokeirambyte(0xB4,0x04); #ADCCON1=0x04
    client.CCpokeirambyte(0xBD,0x01); #RNDH=0x01
    client.CCpokeirambyte(0xB4,0x04); #ADCCON1=0x04
    
    #Dump values
    for foo in range(1,10):
        print "%02x" % client.CCpeekirambyte(0xBD); #RNDH
        client.CCpokeirambyte(0xB4,0x04); #ADCCON1=0x04
        client.CCreleasecpu();
        client.CChaltcpu();
    print "%02x" % client.CCpeekdatabyte(0xDF61); #CHIP ID
if(sys.argv[1]=="adctest"):
    # ADCTest 0xDF3A 0xDF3B
    print "ADC TEST %02x%02x" % (
        client.CCpeekdatabyte(0xDF3A),
        client.CCpeekdatabyte(0xDF3B));
if(sys.argv[1]=="config"):
    print "Config is %02x" % client.CCrd_config();

if(sys.argv[1]=="flash"):
     f=sys.argv[2];
     start=0;
     stop=0xFFFF;
     if(len(sys.argv)>3):
         start=int(sys.argv[3],16);
     if(len(sys.argv)>4):
         stop=int(sys.argv[4],16);
   
     client.flash(f);
if(sys.argv[1]=="lock"):
    print "Status: %s" %client.status();
    client.CClockchip();
    print "Status: %s" %client.status();
if(sys.argv[1]=="flashpage"):
    target=0;
    if(len(sys.argv)>2):
        target=int(sys.argv[2],16);
    print "Writing a page of flash from 0xF000 in XDATA"
    client.CCflashpage(target);
if(sys.argv[1]=="erasebuffer"):
    print "Erasing flash buffer.";
    client.CCeraseflashbuffer();

if(sys.argv[1]=="writedata"):
    f=sys.argv[2];
    start=0;
    stop=0xFFFF;
    if(len(sys.argv)>3):
        start=int(sys.argv[3],16);
    if(len(sys.argv)>4):
        stop=int(sys.argv[4],16);
    
    h = IntelHex(f);
    
    for i in h._buf.keys():
        if(i>=start and i<=stop):
            client.CCpokedatabyte(i,h[i]);
            if(i%0x100==0):
                print "%04x" % i;
#if(sys.argv[1]=="flashtest"):
#    client.CCflashtest();
if(sys.argv[1]=="peekdata"):
    start=0x0000;
    if(len(sys.argv)>2):
        start=int(sys.argv[2],16);
    stop=start;
    if(len(sys.argv)>3):
        stop=int(sys.argv[3],16);
    print "Peeking from %04x to %04x." % (start,stop);
    while start<=stop:
        print "%04x: %02x" % (start,client.CCpeekdatabyte(start));
        start=start+1;
if(sys.argv[1]=="peek"):
    start=0x0000;
    if(len(sys.argv)>2):
        start=int(sys.argv[2],16);
    stop=start;
    if(len(sys.argv)>3):
        stop=int(sys.argv[3],16);
    print "Peeking from %04x to %04x." % (start,stop);
    while start<=stop:
        print "%04x: %02x" % (start,client.CCpeekirambyte(start));
        start=start+1;
if(sys.argv[1]=="verify"):
    f=sys.argv[2];
    start=0;
    stop=0xFFFF;
    if(len(sys.argv)>3):
        start=int(sys.argv[3],16);
    if(len(sys.argv)>4):
        stop=int(sys.argv[4],16);
    
    h = IntelHex(f);
    for i in h._buf.keys():
        if(i>=start and i<stop):
            peek=client.CCpeekcodebyte(i)
            if(h[i]!=peek):
                print "ERROR at %04x, found %02x not %02x"%(i,peek,h[i]);
            if(i%0x100==0):
                print "%04x" % i;
if(sys.argv[1]=="peekcode"):
    start=0x0000;
    if(len(sys.argv)>2):
        start=int(sys.argv[2],16);
    stop=start;
    if(len(sys.argv)>3):
        stop=int(sys.argv[3],16);
    print "Peeking from %04x to %04x." % (start,stop);
    while start<=stop:
        print "%04x: %02x" % (start,client.CCpeekcodebyte(start));
        start=start+1;
if(sys.argv[1]=="pokedata"):
    start=0x0000;
    val=0x00;
    if(len(sys.argv)>2):
        start=int(sys.argv[2],16);
    if(len(sys.argv)>3):
        val=int(sys.argv[3],16);
    print "Poking %04x to become %02x." % (start,val);
    client.CCpokedatabyte(start,val);

client.stop();
