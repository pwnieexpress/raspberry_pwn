#!/usr/bin/env python
# GoodFET Client Library
# 
# (C) 2009 Travis Goodspeed <travis at radiantmachines.com>
#
# This code is being rewritten and refactored.  You've been warned!

import sys, time, string, cStringIO, struct, glob, serial, os;
import sqlite3;

fmt = ("B", "<H", None, "<L")

def getClient(name="GoodFET"):
    import GoodFET, GoodFETCC, GoodFETAVR, GoodFETSPI, GoodFETMSP430, GoodFETNRF;
    if(name=="GoodFET" or name=="monitor"): return GoodFET.GoodFET();
    elif name=="cc" or name=="chipcon": return GoodFETCC.GoodFETCC();
    elif name=="avr": return GoodFETAVR.GoodFETAVR();
    elif name=="spi": return GoodFETSPI.GoodFETSPI();
    elif name=="msp430": return GoodFETMSP430.GoodFETMSP430();
    elif name=="nrf": return GoodFETNRF.GoodFETNRF();
    
    print "Unsupported target: %s" % name;
    sys.exit(0);

class SymbolTable:
    """GoodFET Symbol Table"""
    db=sqlite3.connect(":memory:");
    
    def __init__(self, *args, **kargs):
        self.db.execute("create table if not exists symbols(adr,name,memory,size,comment);");
    def get(self,name):
        self.db.commit();
        c=self.db.cursor();
        try:
            c.execute("select adr,memory from symbols where name=?",(name,));
            for row in c:
                #print "Found it.";
                sys.stdout.flush();
                return row[0];
            #print "No dice.";
        except:# sqlite3.OperationalError:
            #print "SQL error.";
            return eval(name);
        return eval(name);
    def define(self,adr,name,comment="",memory="vn",size=16):
        self.db.execute("insert into symbols(adr,name,memory,size,comment)"
                        "values(?,?,?,?,?);", (
                adr,name,memory,size,comment));
        #print "Set %s=%s." % (name,adr);

class GoodFET:
    """GoodFET Client Library"""

    besilent=0;
    app=0;
    verb=0;
    count=0;
    data="";
    verbose=False
    
    GLITCHAPP=0x71;
    MONITORAPP=0x00;
    symbols=SymbolTable();
    
    def __init__(self, *args, **kargs):
        self.data=[0];
    def getConsole(self):
        from GoodFETConsole import GoodFETConsole;
        return GoodFETConsole(self);
    def name2adr(self,name):
        return self.symbols.get(name);
    def timeout(self):
        print "timeout\n";
    def serInit(self, port=None, timeout=2):
        """Open the serial port"""
        # Make timeout None to wait forever, 0 for non-blocking mode.
        
        if port is None and os.environ.get("GOODFET")!=None:
            glob_list = glob.glob(os.environ.get("GOODFET"));
            if len(glob_list) > 0:
                port = glob_list[0];
            else:
                port = os.environ.get("GOODFET");
        if port is None:
            glob_list = glob.glob("/dev/tty.usbserial*");
            if len(glob_list) > 0:
                port = glob_list[0];
        if port is None:
            glob_list = glob.glob("/dev/ttyUSB*");
            if len(glob_list) > 0:
                port = glob_list[0];
        if os.name=='nt':
            from scanwin32 import winScan;
            scan=winScan();
            for order,comport,desc,hwid in sorted(scan.comports()):
                if hwid.index('FTDI')==0:
                    port=comport;
                    #print "Using FTDI port %s" % port
                    
        
        self.serialport = serial.Serial(
            port,
            #9600,
            115200,
            parity = serial.PARITY_NONE,
            timeout=timeout
            )
        
        self.verb=0;
        attempts=0;
        connected=0;
        while connected==0:
            while self.verb!=0x7F or self.data!="http://goodfet.sf.net/":
                #print "Resyncing.";
                self.serialport.flushInput()
                self.serialport.flushOutput()
                #Explicitly set RTS and DTR to halt board.
                self.serialport.setRTS(1);
                self.serialport.setDTR(1);
                #Drop DTR, which is !RST, low to begin the app.
                self.serialport.setDTR(0);
                self.serialport.flushInput()
                self.serialport.flushOutput()
                #time.sleep(60);
                attempts=attempts+1;
                self.readcmd(); #Read the first command.
            #Here we have a connection, but maybe not a good one.
            connected=1;
            olds=self.infostring();
            clocking=self.monitorclocking();
            for foo in range(1,30):
                if not self.monitorecho():
                    if self.verbose: print "Comm error on %i try, resyncing out of %s." % (foo,
                                                  clocking);
                    connected=0;
                    break;
        if self.verbose: print "Connected after %02i attempts." % attempts;
        self.mon_connected();
        
    def getbuffer(self,size=0x1c00):
        writecmd(0,0xC2,[size&0xFF,(size>>16)&0xFF]);
        print "Got %02x%02x buffer size." % (self.data[1],self.data[0]);
    def writecmd(self, app, verb, count=0, data=[]):
        """Write a command and some data to the GoodFET."""
        self.serialport.write(chr(app));
        self.serialport.write(chr(verb));
        
        #if data!=None:
        #    count=len(data); #Initial count ignored.
        
        #print "TX %02x %02x %04x" % (app,verb,count);
        
        #little endian 16-bit length
        self.serialport.write(chr(count&0xFF));
        self.serialport.write(chr(count>>8));

        if self.verbose:
            print "Tx: ( 0x%02x, 0x%02x, 0x%04x )" % ( app, verb, count )
        
        #print "count=%02x, len(data)=%04x" % (count,len(data));
        
        if count!=0:
            if(isinstance(data,list)):
                for i in range(0,count):
                #print "Converting %02x at %i" % (data[i],i)
                    data[i]=chr(data[i]);
            #print type(data);
            outstr=''.join(data);
            self.serialport.write(outstr);
        if not self.besilent:
            return self.readcmd()
        else:
            return []

    def readcmd(self):
        """Read a reply from the GoodFET."""
        while 1:#self.serialport.inWaiting(): # Loop while input data is available
            try:
                #print "Reading...";
                self.app=ord(self.serialport.read(1));
                #print "APP=%2x" % self.app;
                self.verb=ord(self.serialport.read(1));
                #print "VERB=%02x" % self.verb;
                self.count=(
                    ord(self.serialport.read(1))
                    +(ord(self.serialport.read(1))<<8)
                    );

                if self.verbose:
                    print "Rx: ( 0x%02x, 0x%02x, 0x%04x )" % ( self.app, self.verb, self.count )
            
                #Debugging string; print, but wait.
                if self.app==0xFF:
                    if self.verb==0xFF:
                        print "# DEBUG %s" % self.serialport.read(self.count)
               	    elif self.verb==0xFE:
                        print "# DEBUG 0x%x" % struct.unpack(fmt[self.count-1], self.serialport.read(self.count))[0]
                    sys.stdout.flush();
                else:
                    self.data=self.serialport.read(self.count);
                    return self.data;
            except TypeError:
                if self.connected:
                    print "Error: waiting for serial read timed out (most likely).";
                    print "This shouldn't happen after syncing.  Exiting for safety.";
                    sys.exit(-1)
                return self.data;
    #Glitching stuff.
    def glitchApp(self,app):
        """Glitch into a device by its application."""
        self.data=[app&0xff];
        self.writecmd(self.GLITCHAPP,0x80,1,self.data);
        #return ord(self.data[0]);
    def glitchVerb(self,app,verb,data):
        """Glitch during a transaction."""
        if data==None: data=[];
        self.data=[app&0xff, verb&0xFF]+data;
        self.writecmd(self.GLITCHAPP,0x81,len(self.data),self.data);
        #return ord(self.data[0]);
    def glitchstart(self):
        """Glitch into the AVR application."""
        self.glitchVerb(self.APP,0x20,None);
    def glitchstarttime(self):
        """Measure the timer of the START verb."""
        return self.glitchTime(self.APP,0x20,None);
    def glitchTime(self,app,verb,data):
        """Time the execution of a verb."""
        if data==None: data=[];
        self.data=[app&0xff, verb&0xFF]+data;
        self.writecmd(self.GLITCHAPP,0x82,len(self.data),self.data);
        return ord(self.data[0])+(ord(self.data[1])<<8);
    def glitchVoltages(self,low=0x0880, high=0x0fff):
        """Set glitching voltages. (0x0fff is max.)"""
        self.data=[low&0xff, (low>>8)&0xff,
                   high&0xff, (high>>8)&0xff];
        self.writecmd(self.GLITCHAPP,0x90,4,self.data);
        #return ord(self.data[0]);
    def glitchRate(self,count=0x0800):
        """Set glitching count period."""
        self.data=[count&0xff, (count>>8)&0xff];
        self.writecmd(self.GLITCHAPP,0x91,2,
                      self.data);
        #return ord(self.data[0]);
    
    
    #Monitor stuff
    def silent(self,s=0):
        """Transmissions halted when 1."""
        self.besilent=s;
        print "besilent is %i" % self.besilent;
        self.writecmd(0,0xB0,1,[s]);
    connected=0;
    def mon_connected(self):
        """Announce to the monitor that the connection is good."""
        self.connected=1;
        self.writecmd(0,0xB1,0,[]);
    def out(self,byte):
        """Write a byte to P5OUT."""
        self.writecmd(0,0xA1,1,[byte]);
    def dir(self,byte):
        """Write a byte to P5DIR."""
        self.writecmd(0,0xA0,1,[byte]);
    def call(self,adr):
        """Call to an address."""
        self.writecmd(0,0x30,2,
                      [adr&0xFF,(adr>>8)&0xFF]);
    def execute(self,code):
        """Execute supplied code."""
        self.writecmd(0,0x31,2,#len(code),
                      code);
    def peekbyte(self,address):
        """Read a byte of memory from the monitor."""
        self.data=[address&0xff,address>>8];
        self.writecmd(0,0x02,2,self.data);
        #self.readcmd();
        return ord(self.data[0]);
    def peekword(self,address):
        """Read a word of memory from the monitor."""
        return self.peekbyte(address)+(self.peekbyte(address+1)<<8);
    def peek(self,address):
        """Read a word of memory from the monitor."""
        return self.peekbyte(address)+(self.peekbyte(address+1)<<8);
    def pokebyte(self,address,value):
        """Set a byte of memory by the monitor."""
        self.data=[address&0xff,address>>8,value];
        self.writecmd(0,0x03,3,self.data);
        return ord(self.data[0]);
    def dumpmem(self,begin,end):
        i=begin;
        while i<end:
            print "%04x %04x" % (i, self.peekword(i));
            i+=2;
    def monitor_ram_pattern(self):
        """Overwrite all of RAM with 0xBEEF."""
        self.writecmd(0,0x90,0,self.data);
        return;
    def monitor_ram_depth(self):
        """Determine how many bytes of RAM are unused by looking for 0xBEEF.."""
        self.writecmd(0,0x91,0,self.data);
        return ord(self.data[0])+(ord(self.data[1])<<8);
    
    #Baud rates.
    baudrates=[115200, 
               9600,
               19200,
               38400,
               57600,
               115200];
    def setBaud(self,baud):
        """Change the baud rate.  TODO fix this."""
        rates=self.baudrates;
        self.data=[baud];
        print "Changing FET baud."
        self.serialport.write(chr(0x00));
        self.serialport.write(chr(0x80));
        self.serialport.write(chr(1));
        self.serialport.write(chr(baud));
        
        print "Changed host baud."
        self.serialport.setBaudrate(rates[baud]);
        time.sleep(1);
        self.serialport.flushInput()
        self.serialport.flushOutput()
        
        print "Baud is now %i." % rates[baud];
        return;
    def readbyte(self):
        return ord(self.serialport.read(1));
    def findbaud(self):
        for r in self.baudrates:
            print "\nTrying %i" % r;
            self.serialport.setBaudrate(r);
            #time.sleep(1);
            self.serialport.flushInput()
            self.serialport.flushOutput()
            
            for i in range(1,10):
                self.readbyte();
            
            print "Read %02x %02x %02x %02x" % (
                self.readbyte(),self.readbyte(),self.readbyte(),self.readbyte());
    def monitortest(self):
        """Self-test several functions through the monitor."""
        print "Performing monitor self-test.";
        self.monitorclocking();
        for f in range(0,3000):
            a=self.peekword(0x0c00);
            b=self.peekword(0x0c02);
            if a!=0x0c04 and a!=0x0c06:
                print "ERROR Fetched %04x, %04x" % (a,b);
            self.pokebyte(0x0021,0); #Drop LED
            if self.peekbyte(0x0021)!=0:
                print "ERROR, P1OUT not cleared.";
            self.pokebyte(0x0021,1); #Light LED
            if not self.monitorecho():
                print "Echo test failed.";
        print "Self-test complete.";
        self.monitorclocking();
    def monitorecho(self):
        data="The quick brown fox jumped over the lazy dog.";
        self.writecmd(self.MONITORAPP,0x81,len(data),data);
        if self.data!=data:
            if self.verbose: print "Comm error recognized by monitorecho().";
            return 0;
        return 1;
    def monitorclocking(self):
        DCOCTL=self.peekbyte(0x0056);
        BCSCTL1=self.peekbyte(0x0057);
        return "0x%02x, 0x%02x" % (DCOCTL, BCSCTL1);

    # The following functions ought to be implemented in
    # every client.

    def infostring(self):
        a=self.peekbyte(0xff0);
        b=self.peekbyte(0xff1);
        return "%02x%02x" % (a,b);
    def lock(self):
        print "Locking Unsupported.";
    def erase(self):
        print "Erasure Unsupported.";
    def setup(self):
        return;
    def start(self):
        return;
    def test(self):
        print "Unimplemented.";
        return;
    def status(self):
        print "Unimplemented.";
        return;
    def halt(self):
        print "Unimplemented.";
        return;
    def resume(self):
        print "Unimplemented.";
        return;
    def getpc(self):
        print "Unimplemented.";
        return 0xdead;
    def flash(self,file):
        """Flash an intel hex file to code memory."""
        print "Flash not implemented.";
    def dump(self,file,start=0,stop=0xffff):
        """Dump an intel hex file from code memory."""
        print "Dump not implemented.";
    def peek32(self,address, memory="vn"):
        return (self.peek16(address,memory)+
                (self.peek16(address+2,memory)<<16));
    def peek16(self,address, memory="vn"):
        return (self.peek8(address,memory)+
                (self.peek8(address+1,memory)<<8));
    def peek8(self,address, memory="vn"):
        return self.peekbyte(address); #monitor
    def peekword(self,address, memory="vn"):
        return self.peek(address); #monitor
    
    def loadsymbols(self):
        return;
