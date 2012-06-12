#!/usr/bin/env ipython
import sys, struct, binascii
from GoodFETARM import *
from intelhex import IntelHex


data = []

client=GoodFETARM();
def init():
    #Initailize FET and set baud rate
    client.serInit()
    #
    #Connect to target
    client.setup()
    client.start()
    print "STARTUP: "+repr(client.data)
    #

def test1():
    global data
    print "\n\nTesting JTAG for ARM\n"
    client.writecmd(0x33,0xd0,4,[0x40,0x40,0x40,0x40]); print "loopback:   \t %s"%repr(client.data)                  # loopback
    data.append(client.data)
    client.writecmd(0x33,0xd1,2,[1,0]); print "scanchain1:\t %s"%repr(client.data)               # set scan chain
    data.append(client.data)
    client.writecmd(0x33,0xd2,0,[]); print "debug state:\t %s"%repr(client.data)                  # get dbg state
    data.append(client.data)
    client.writecmd(0x33,0xd3,0,[0,0,0xa0,0xe1]); print "exec_nop: \t %s"%repr(client.data)     # execute instruction
    data.append(client.data)
    client.writecmd(0x33,0xd3,0,[0,0,0x8e,0xe5]); print "exec_stuff: \t %s"%repr(client.data)     # execute instruction
    data.append(client.data)
    client.writecmd(0x33,0xd3,0,[0,0,0xa0,0xe1]); print "exec_nop: \t %s"%repr(client.data)     # execute instruction
    data.append(client.data)
    client.writecmd(0x33,0xd3,0,[0,0,0xa0,0xe1]); print "exec_nop: \t %s"%repr(client.data)     # execute instruction
    data.append(client.data)
    client.writecmd(0x33,0xd3,0,[0,0,0xa0,0xe1]); print "exec_nop: \t %s"%repr(client.data)     # execute instruction
    data.append(client.data)
    client.writecmd(0x33,0xd6,0,[]); print "shift_dr_32: \t %s"%repr(client.data)                  # dr_shift32
    data.append(client.data)
    client.writecmd(0x33,0xd5,8,[3, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40, 0x40]); print "set_register:\t %s"%repr(client.data)                  # set register
    data.append(client.data)
    client.writecmd(0x33,0xd4,1,[3]); print "get_register:\t %s"%repr(client.data)                  # get register
    data.append(client.data)
    client.writecmd(0x33,0xd7,0,[]); print "chain1:      \t %s"%repr(client.data)                  # chain1
    data.append(client.data)
    client.writecmd(0x33,0xd8,0,[]); print "read_chain2: \t %s"%repr(client.data)                  # read chain2
    data.append(client.data)
    client.writecmd(0x33,0xd9,0,[]); print "idcode:      \t %s"%repr(client.data)                  # read idcode
    data.append(client.data)
    client.writecmd(0x33,0xf0,2,[4,4,1,1]); print "f0:       \t %s"%repr(client.data)   # read idcode
    data.append(client.data)
    client.writecmd(0x33,0xdb,8,[0x0,4,4,4,4,4,4,4]); print "verb(0):     \t %s"%repr(client.data)
    data.append(client.data)
    client.writecmd(0x33,0xdb,8,[0x2,4,4,4,4,4,4,4]); print "verb(2):     \t %s"%repr(client.data)
    data.append(client.data)
    client.writecmd(0x33,0xdb,8,[0x3,4,4,4,4,4,4,4]); print "verb(3):     \t %s"%repr(client.data)
    data.append(client.data)
    client.writecmd(0x33,0xdb,8,[0x4,4,4,4,4,4,4,4]); print "verb(4):     \t %s"%repr(client.data)
    data.append(client.data)
    client.writecmd(0x33,0xdb,8,[0x5,4,4,4,4,4,4,4]); print "verb(5):     \t %s"%repr(client.data)
    data.append(client.data)
    client.writecmd(0x33,0xdb,8,[0x7,4,4,4,4,4,4,4]); print "verb(7):     \t %s"%repr(client.data)
    data.append(client.data)
    client.writecmd(0x33,0xdb,8,[0x9,4,4,4,4,4,4,4]); print "verb(9):     \t %s"%repr(client.data)
    data.append(client.data)
    client.writecmd(0x33,0xdb,8,[0xc,4,4,4,4,4,4,4]); print "verb(c):     \t %s"%repr(client.data)
    data.append(client.data)
    client.writecmd(0x33,0xdb,8,[0xe,0,0,0,0,0,0xa0,0xe1]); print "verb(e):     \t %s"%repr(client.data)
    data.append(client.data)
    client.writecmd(0x33,0xdb,8,[0xf,4,4,4,4,4,4,4]); print "verb(f):     \t %s"%repr(client.data)
    data.append(client.data)

def test2():
    global data
    print "\n\nTesting JTAG for ARM\n"
    print "IDCODE:      %x"%client.ARMident()
    print "Debug State: %x"%client.ARMget_dbgstate ()
    print "Debug State: %x"%client.ARMget_dbgstate ()
    print "Debug State: %x"%client.ARMget_dbgstate ()
    print "Debug CTRL:  %x"%client.ARMget_dbgctrl()
    client.writecmd(0x33,0xda,0,[])
    print "TEST CHAIN0: %s"%repr(client.data)
    print "Debug State: %x"%client.ARMget_dbgstate ()
    print "IDCODE:      %x"%client.ARMident()
    print "Debug State: %x"%client.ARMget_dbgstate ()
    client.writecmd(0x33,0xd0,4,[0xf7,0xf7,0xf7,0xf7])
    print "Loopback:   \t %s"%repr(client.data)                  # loopback
    print "Debug State: %x"%client.ARMget_dbgstate ()
    print "IDCODE:      %x"%client.ARMident()
    print "GetPC: %x"%client.ARMgetPC()
    print "IDCODE:      %x"%client.ARMident()
    print "Debug State: %x"%client.ARMget_dbgstate ()
    print "IDCODE:      %x"%client.ARMident()
    print "set_register(3,0x41414141):  %x"%client.ARMset_register(3,0x41414141)
    print "IDCODE:      %x"%client.ARMident()
    print "Debug State: %x"%client.ARMget_dbgstate ()
    print "IDCODE:      %x"%client.ARMident()
    print "get_register(3):             %x"%client.ARMget_register(3)
    print "IDCODE:      %x"%client.ARMident()
    print "Debug State: %x"%client.ARMget_dbgstate ()
    print "IDCODE:      %x"%client.ARMident()

def test3():
    print "IDCODE:      %x"%client.ARMident()
    print "Debug State: %x"%client.ARMget_dbgstate ()
    client.writecmd(0x33,0xd0,4,[0xf7,0xf7,0xf7,0xf7])
    print "Loopback:   \t %s"%repr(client.data)                  # loopback
    client.writecmd(0x33,0xd5,8,[0,0,0,0,0xf7,0xf7,0xf7,0xf7])
    print "test_set_reg:   \t %s"%repr(client.data)            
    client.writecmd(0x33,0xd4,1,[0])
    print "test_get_reg:   \t %s"%repr(client.data)           
    print "set_register(3,0x41414141):  %x"%client.ARMset_register(3,0x41414141)
    print "get_register(3):             %x"%client.ARMget_register(3)
    client.writecmd(0x33,0xd4,1,[0])
    print "test_get_reg:   \t %s"%repr(client.data)           

init()
print "Don't forget to 'client.stop()' if you want to exit cleanly"



"""
  case 0xD0: // loopback test
    cmddatalong[0] = 0x12345678;
  case 0xD1: // Set Scan Chain
    cmddatalong[0] = jtagarm7tdmi_scan_n(cmddataword[0]);
  case 0xD2: //
    cmddatalong[0] = jtagarm7tdmi_get_dbgstate();
  case 0xD3:
    cmddatalong[0] = jtagarm7tdmi_exec(cmddatalong[0]);
  case 0xD4:
    cmddatalong[0] = jtagarm7tdmi_get_register(cmddata[0]);
  case 0xD5:
    cmddatalong[0] = jtagarm7tdmi_set_register(cmddata[0], cmddatalong[1]);
  case 0xD6:
    cmddatalong[0] = jtagarm7tdmi_dr_shift32(cmddatalong[0]);
  case 0xD7:
    cmddatalong[0] = jtagarm7tdmi_chain1(cmddatalong[0], 0);
  case 0xD8:
    cmddatalong[0] = jtagarm7tdmi_chain2_read(cmddata[0], 32);
"""

"""
if(sys.argv[1]=="test"):
    client.CCtest();
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
    print "Status: %s" %client.CCstatusstr();
if(sys.argv[1]=="erase"):
    print "Status: %s" % client.CCstatusstr();
    client.CCchiperase();
    print "Status: %s" %client.CCstatusstr();

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
   
     h = IntelHex(f);
     page = 0x0000;
     pagelen = 2048; #2kB pages in 32-bit words
     bcount = 0;
     
     print "Wiping Flash."
     #Wipe all of flash.
     #client.CCchiperase();
     #Wipe the RAM buffer for the next flash page.
     #client.CCeraseflashbuffer();
     for i in h._buf.keys():
         while(i>page+pagelen):
             if bcount>0:
                 client.CCflashpage(page);
                 #client.CCeraseflashbuffer();
                 bcount=0;
                 print "Flashed page at %06x" % page
             page+=pagelen;
             
         #Place byte into buffer.
         client.CCpokedatabyte(0xF000+i-page,
                               h[i]);
         bcount+=1;
         if(i%0x100==0):
                print "Buffering %04x toward %06x" % (i,page);
     #last page
     client.CCflashpage(page);
     print "Flashed final page at %06x" % page;
     
if(sys.argv[1]=="lock"):
    print "Status: %s" %client.CCstatusstr();
    client.CClockchip();
    print "Status: %s" %client.CCstatusstr();
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
"""
