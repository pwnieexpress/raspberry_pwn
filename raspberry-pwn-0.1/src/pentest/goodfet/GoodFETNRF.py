#!/usr/bin/env python
# GoodFET Nordic RF Radio Client
# 
# (C) 2009 Travis Goodspeed <travis at radiantmachines.com>
#
# This code is being rewritten and refactored.  You've been warned!

import sys, time, string, cStringIO, struct, glob, serial, os;

from GoodFET import GoodFET;

class GoodFETNRF(GoodFET):
    NRFAPP=0x50;
    def NRFsetup(self):
        """Move the FET into the NRF application."""
        self.writecmd(self.NRFAPP,0x10,0,self.data); #NRF/SETUP
        
    def NRFtrans8(self,byte):
        """Read and write 8 bits by NRF."""
        data=self.NRFtrans([byte]);
        return ord(data[0]);
    
    def NRFtrans(self,data):
        """Exchange data by NRF."""
        self.data=data;
        self.writecmd(self.NRFAPP,0x00,len(data),data);
        return self.data;
    
    def peek(self,reg,bytes=-1):
        """Read an NRF Register.  For long regs, result is flipped."""
        data=[reg,0,0,0,0,0];
        
        #Automatically calibrate the len.
        if bytes==-1:
            bytes=1;
            if reg==0x0a or reg==0x0b or reg==0x10: bytes=5;
        
        self.writecmd(self.NRFAPP,0x02,len(data),data);
        toret=0;
        for i in range(0,bytes):
            toret=toret|(ord(self.data[i+1])<<(8*i));
        return toret;
    def poke(self,reg,val,bytes=-1):
        """Write an NRF Register."""
        data=[reg];
        
        #Automatically calibrate the len.
        if bytes==-1:
            bytes=1;
            if reg==0x0a or reg==0x0b or reg==0x10: bytes=5;
        
        for i in range(0,bytes):
            data=data+[(val>>(8*i))&0xFF];
        self.writecmd(self.NRFAPP,0x03,len(data),data);
        if self.peek(reg,bytes)!=val and reg!=0x07:
            print "Warning, failed to set r%02x=%02x, got %02x." %(reg,
                                                                 val,
                                                                 self.peek(reg,bytes));
        return;
    
    def status(self):
        """Read the status byte."""
        status=self.peek(0x07);
        print "Status=%02x" % status;
    
    #Radio stuff begins here.
    def RF_setenc(self,code="GFSK"):
        """Set the encoding type."""
        if code!=GFSK:
            return "%s not supported by the NRF24L01.  Try GFSK."
        return;
    def RF_getenc(self):
        """Get the encoding type."""
        return "GFSK";
    def RF_getrate(self):
        rate=self.peek(0x06)&0x28;
        if rate==0x28:
            rate=250*10**3; #256kbps
        elif rate==0x08:
            rate=2*10**6;  #2Mbps
        elif rate==0x00: 
            rate=1*10**6;  #1Mbps
        return rate;
    def RF_setrate(self,rate=2*10**6):
        r6=self.peek(0x06); #RF_SETUP register
        r6=r6&(~0x28);   #Clear rate fields.
        if rate==2*10**6:
            r6=r6|0x08;
        elif rate==1*10**6:
            r6=r6;
        elif rate==250*10**3:
            r6=r6|0x20;
        print "Setting r6=%02x." % r6;
        self.poke(0x06,r6); #Write new setting.
    def RF_setfreq(self,frequency):
        """Set the frequency in Hz."""
        
        #On the NRF24L01+, register 0x05 is the offset in
        #MHz above 2400.
        
        chan=frequency/1000000-2400;
        self.poke(0x05,chan);
    def RF_getfreq(self):
        """Get the frequency in Hz."""
        
        #On the NRF24L01+, register 0x05 is the offset in
        #MHz above 2400.
        
        return (2400+self.peek(0x05))*10**6
        self.poke(0x05,chan);
    def RF_getsmac(self):
        """Return the source MAC address."""
        
        #Register 0A is RX_ADDR_P0, five bytes.
        mac=self.peek(0x0A, 5);
        return mac;
    def RF_setsmac(self,mac):
        """Set the source MAC address."""
        
        #Register 0A is RX_ADDR_P0, five bytes.
        self.poke(0x0A, mac, 5);
        return mac;
    def RF_gettmac(self):
        """Return the target MAC address."""
        
        #Register 0x10 is TX_ADDR, five bytes.
        mac=self.peek(0x10, 5);
        return mac;
    def RF_settmac(self,mac):
        """Set the target MAC address."""
        
        #Register 0x10 is TX_ADDR, five bytes.
        self.poke(0x10, mac, 5);
        return mac;

    def RF_rxpacket(self):
        """Get a packet from the radio.  Returns None if none is waiting."""
        if self.peek(0x07) & 0x40:
            #Packet has arrived.
            self.writecmd(self.NRFAPP,0x80,0,None); #RX Packet
            data=self.data;
            self.poke(0x07,0x40);#clear bit.
            return data;
        elif self.peek(0x07)==0:
            self.writecmd(self.NRFAPP,0x82,0,None); #Flush
            self.poke(0x07,0x40);#clear bit.
        return None;
    def RF_carrier(self):
        """Hold a carrier wave on the present frequency."""
        # Set CONT_WAVE, PLL_LOCK, and 0dBm in RF_SETUP            
        self.poke(0x06,8+10+4+2); 
        
    packetlen=16;
    def RF_setpacketlen(self,len=16):
        """Set the number of bytes in the expected payload."""
        self.poke(0x11,len);
        self.packetlen=len;
    def RF_getpacketlen(self):
        """Set the number of bytes in the expected payload."""
        len=self.peek(0x11);
        self.packetlen=len;
        return len;
    maclen=5;
    def RF_getmaclen(self):
        """Get the number of bytes in the MAC address."""
        choices=[0, 3, 4, 5];
        choice=self.peek(0x03)&3;
        self.maclen=choices[choice];
        return self.maclen;
    def RF_setmaclen(self,len):
        """Set the number of bytes in the MAC address."""
        choices=["illegal", "illegal", "illegal", 
                 1, 2, 3];
        choice=choices[len];
        self.poke(0x03,choice);
        self.maclen=len;
