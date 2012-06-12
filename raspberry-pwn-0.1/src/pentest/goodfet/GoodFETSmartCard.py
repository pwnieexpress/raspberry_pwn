#!/usr/bin/env python
# GoodFET SPI and SPIFlash Client Library
# 
# (C) 2009 Travis Goodspeed <travis at radiantmachines.com>
#
# This code is being rewritten and refactored.  You've been warned!

import sys, time, string, cStringIO, struct, glob, serial, os;

from GoodFET import GoodFET;

class GoodFETSmartCard(GoodFET):
    SMARTCARDAPP=0x73;
    APP=SMARTCARDAPP;
    
    def setup(self):
        """Move the FET into the SmartCard application."""
        self.writecmd(self.APP,0x10,0,self.data);
    def start(self):
        """Start the connection, reat ATR."""
        self.writecmd(self.APP,0x20,0,None);
