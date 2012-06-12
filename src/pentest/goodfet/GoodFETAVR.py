#!/usr/bin/env python
# GoodFET SPI and SPIFlash Client Library
# 
# (C) 2009 Travis Goodspeed <travis at radiantmachines.com>
#
# This code is being rewritten and refactored.  You've been warned!

import sys, time, string, cStringIO, struct, glob, serial, os;

from GoodFET import GoodFET;

class GoodFETAVR(GoodFET):
    AVRAPP=0x32;
    APP=AVRAPP;
    AVRVendors={0x1E: "Atmel",
                0x00: "Locked",
                };
    
    #List imported from http://avr.fenceline.de/device_data.html
    AVRDevices={
        0x9003: "ATtiny10",
        0x9004: "ATtiny11",
        0x9005: "ATtiny12",
        0x9007: "ATtiny13",
        0x9006: "ATtiny15",
        0x9106: "ATtiny22",
        0x910A: "ATtiny2313",
        0x9108: "ATtiny25",
        0x9109: "ATtiny26",
        0x9107: "ATtiny28",
        0x9206: "ATtiny45",
        0x930B: "ATtiny85",
        0x9304: "AT90C8534",
        0x9001: "AT90S1200",
        0x9101: "AT90S2313",
        0x9102: "AT90S2323",
        0x9105: "AT90S2333",
        0x9103: "AT90S2343",
        0x9201: "AT90S4414",
        0x9203: "AT90S4433",
        0x9202: "AT90S4434",
        0x9301: "AT90S8515",
        0x9303: "AT90S8535",
        0x9381: "AT90PWM2",
        0x9381: "AT90PWM3",
        0x9781: "AT90CAN128",
        0x9205: "ATmega48",
        0x9306: "ATmega8515",
        0x9308: "ATmega8535",
        0x9307: "ATmega8",
        0x930A: "ATmega88",
        0x9403: "ATmega16",
        0x9401: "ATmega161",
        0x9404: "ATmega162",
        0x9402: "ATmega163",
        0x9407: "ATmega165",
        0x9406: "ATmega168",
        0x9405: "ATmega169",
        0x9502: "ATmega32",
        0x9501: "ATmega323",
        0x9503: "ATmega325",
        0x9504: "ATmega3250",
        0x9503: "ATmega329",
        0x9504: "ATmega3290",
        0x9507: "ATmega406",
        0x9602: "ATmega64",
        0x9607: "ATmega640",
        0x9603: "ATmega645",
        0x9604: "ATmega6450",
        0x9603: "ATmega649",
        0x9604: "ATmega6490",
        0x0101: "ATmega103",
        0x9701: "ATmega103",
        0x9702: "ATmega128",
        0x9703: "ATmega1280",
        0x9704: "ATmega1281",
        0x9801: "ATmega2560",
        0x9802: "ATmega2561",
        0x9002: "ATtiny19",
        0x9302: "ATmega85",
        0x9305: "ATmega83",
        0x9601: "ATmega603",
        };
    
    def setup(self):
        """Move the FET into the AVR application."""
        self.writecmd(self.AVRAPP,0x10,0,self.data); #SPI/SETUP
    
    def trans(self,data):
        """Exchange data by AVR.
        Input should probably be 4 bytes."""
        self.data=data;
        self.writecmd(self.AVRAPP,0x00,len(data),data);
        return self.data;

    def start(self):
        """Start the connection."""
        self.writecmd(self.AVRAPP,0x20,0,None);
    def forcestart(self):
        """Forcibly start a connection."""
        
        for i in range(0x880,0xfff):
            #self.glitchVoltages(0x880, i);
            self.start();
            bits=self.lockbits();
            print "At %04x, Lockbits: %02x" % (i,bits);
            if(bits==0xFF): return;
    def erase(self):
        """Erase the target chip."""
        self.writecmd(self.AVRAPP,0xF0,0,None);
    def lockbits(self):
        """Read the target's lockbits."""
        self.writecmd(self.AVRAPP,0x82,0,None);
        return ord(self.data[0]);
    def setlockbits(self,bits=0x00):
        """Read the target's lockbits."""
        self.writecmd(self.AVRAPP,0x92,1,[bits]);
        return self.lockbits();
    def lock(self):
        self.setlockbits(0xFC);
    def eeprompeek(self, adr):
        """Read a byte of the target's EEPROM."""
        self.writecmd(self.AVRAPP,0x81 ,2,
                      [ (adr&0xFF), (adr>>8)]
                      );#little-endian address
        return ord(self.data[0]);
    def flashpeek(self, adr):
        """Read a byte of the target's Flash memory."""
        self.writecmd(self.AVRAPP,0x02 ,2,
                      [ (adr&0xFF), (adr>>8)]
                      );#little-endian address
        return ord(self.data[0]);
    def flashpeekblock(self, adr):
        """Read a byte of the target's Flash memory."""
        self.writecmd(self.AVRAPP,0x02 ,4,
                      [ (adr&0xFF), (adr>>8) &0xFF, 0x80, 0x00]
                      );
        return self.data;
    
    def eeprompoke(self, adr, val):
        """Write a byte of the target's EEPROM."""
        self.writecmd(self.AVRAPP,0x91 ,3,
                      [ (adr&0xFF), (adr>>8), val]
                      );#little-endian address
        return ord(self.data[0]);
    
    def identstr(self):
        """Return an identifying string."""
        self.writecmd(self.AVRAPP,0x83,0, None);
        vendor=self.AVRVendors.get(ord(self.data[0]));
        deviceid=(ord(self.data[1])<<8)+ord(self.data[2]);
        device=self.AVRDevices.get(deviceid);
        
        #Return hex if device is unknown.
        #They are similar enough that it needn't be known.
        if device==None:
            device=("0x%04x" % deviceid);
        
        return "%s %s" % (vendor,device);
