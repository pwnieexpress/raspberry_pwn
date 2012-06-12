#!/usr/bin/env python
# GoodFET SPI and SPIFlash Client Library
# 
# (C) 2009 Travis Goodspeed <travis at radiantmachines.com>
#
# This code is being rewritten and refactored.  You've been warned!

import sys, time, string, cStringIO, struct, glob, serial, os;

from GoodFET import GoodFET;

class GoodFETSPI(GoodFET):
    def SPIsetup(self):
        """Move the FET into the SPI application."""
        self.writecmd(0x01,0x10,0,self.data); #SPI/SETUP
        
    def SPItrans8(self,byte):
        """Read and write 8 bits by SPI."""
        data=self.SPItrans([byte]);
        return ord(data[0]);
    
    def SPItrans(self,data):
        """Exchange data by SPI."""
        self.data=data;
        self.writecmd(0x01,0x00,len(data),data);
        return self.data;

class GoodFETSPIFlash(GoodFETSPI):
    JEDECmanufacturers={0xFF: "MISSING",
                        0xEF: "Winbond",
                        0xC2: "MXIC",
                        0x20: "Numonyx/ST",
                        0x1F: "Atmel",
                        0x01: "AMD/Spansion"
                        };

    JEDECdevices={0xFFFFFF: "MISSING",
                  0xEF3015: "W25X16L",
                  0xEF3014: "W25X80L",
                  0xEF3013: "W25X40L",
                  0xEF3012: "W25X20L",
                  0xEF3011: "W25X10L",
                  0xC22017: "MX25L6405D",
                  0xC22016: "MX25L3205D",
                  0xC22015: "MX25L1605D",
                  0xC22014: "MX25L8005",
                  0xC22013: "MX25L4005",
                  0x204011: "M45PE10"
                  };
    
    JEDECsizes={0x17: 0x800000,
                0x16: 0x400000,
                0x15: 0x200000,
                0x14: 0x100000,
                0x13: 0x080000,
                0x12: 0x040000,
                0x11: 0x020000
                };
    
    JEDECsize=0;

    def SPIjedec(self):
        """Grab an SPI Flash ROM's JEDEC bytes."""
        data=[0x9f, 0, 0, 0];
        data=self.SPItrans(data);
        
        self.JEDECmanufacturer=ord(data[1]);
        self.JEDECtype=ord(data[2]);
        self.JEDECcapacity=ord(data[3]);
        self.JEDECsize=self.JEDECsizes.get(self.JEDECcapacity);
        if self.JEDECsize==None:
            self.JEDECsize=0;
        self.JEDECdevice=(ord(data[1])<<16)+(ord(data[2])<<8)+ord(data[3]);
        return data;
    def SPIpeek(self,adr):
        """Grab a byte from an SPI Flash ROM."""
        data=[0x03,
              (adr&0xFF0000)>>16,
              (adr&0xFF00)>>8,
              adr&0xFF,
              0];
        self.SPItrans(data);
        return ord(self.data[4]);
    def SPIpeekblock(self,adr):
        """Grab a few block from an SPI Flash ROM.  Block size is unknown"""
        data=[(adr&0xFF0000)>>16,
              (adr&0xFF00)>>8,
              adr&0xFF];
        
        self.writecmd(0x01,0x02,3,data);
        return self.data;
    
    def SPIpokebyte(self,adr,val):
        self.SPIpokebytes(adr,[val]);
    def SPIpokebytes(self,adr,data):
        #Used to be 24 bits, BE, not 32 bits, LE.
        adranddata=[adr&0xFF,
                    (adr&0xFF00)>>8,
                    (adr&0xFF0000)>>16,
                    0, #MSB
                    ]+data;
        #print "%06x: poking %i bytes" % (adr,len(data));
        self.writecmd(0x01,0x03,
                      len(adranddata),adranddata);
        
    def SPIchiperase(self):
        """Mass erase an SPI Flash ROM."""
        self.writecmd(0x01,0x81);
    def SPIwriteenable(self):
        """SPI Flash Write Enable"""
        data=[0x06];
        self.SPItrans(data);
        
    def SPIjedecmanstr(self):
        """Grab the JEDEC manufacturer string.  Call after SPIjedec()."""
        man=self.JEDECmanufacturers.get(self.JEDECmanufacturer)
        if man==0:
            man="UNKNOWN";
        return man;
    
    def SPIjedecstr(self):
        """Grab the JEDEC manufacturer string.  Call after SPIjedec()."""
        man=self.JEDECmanufacturers.get(self.JEDECmanufacturer);
        if man==0:
            man="UNKNOWN";
        device=self.JEDECdevices.get(self.JEDECdevice);
        if device==0:
            device="???"
        return "%s %s" % (man,device);

