#!/usr/bin/env python
# GoodFET Client Library
# 
#
# Good luck with alpha / beta code.
# Contributions and bug reports welcome.
#

import sys, binascii, struct
import atlasutils.smartprint as asp

#Global Commands
READ  = 0x00
WRITE = 0x01
PEEK  = 0x02
POKE  = 0x03
SETUP = 0x10
START = 0x20
STOP  = 0x21
CALL  = 0x30
EXEC  = 0x31
NOK   = 0x7E
OK    = 0x7F

# ARM7TDMI JTAG commands
GET_DEBUG_CTRL      = 0x80
SET_DEBUG_CTRL      = 0x81
GET_PC              = 0x82
SET_PC              = 0x83
GET_CHIP_ID         = 0x84
GET_DEBUG_STATE     = 0x85
GET_WATCHPOINT      = 0x86
SET_WATCHPOINT      = 0x87
GET_REGISTER        = 0x88
SET_REGISTER        = 0x89
GET_REGISTERS       = 0x8a
SET_REGISTERS       = 0x8b
HALTCPU             = 0x8c
RESUMECPU           = 0x8d
DEBUG_INSTR         = 0x8e      #
STEP_INSTR          = 0x8f      #
STEP_REPLACE        = 0x90      #
READ_CODE_MEMORY    = 0x91      # ??
WRITE_FLASH_PAGE    = 0x92      # ??
READ_FLASH_PAGE     = 0x93      # ??
MASS_ERASE_FLASH    = 0x94      # ??
PROGRAM_FLASH       = 0x95
LOCKCHIP            = 0x96      # ??
CHIP_ERASE          = 0x97      # can do?
# Really ARM specific stuff
GET_CPSR            = 0x98
SET_CPSR            = 0x99
GET_SPSR            = 0x9a
SET_SPSR            = 0x9b
SET_MODE_THUMB      = 0x9c
SET_MODE_ARM        = 0x9d

from GoodFET import GoodFET
from intelhex import IntelHex




class GoodFETARM(GoodFET):
    """A GoodFET variant for use with ARM7TDMI microprocessor."""
    def ARMhaltcpu(self):
        """Halt the CPU."""
        self.writecmd(0x33,HALTCPU,0,self.data)
    def ARMreleasecpu(self):
        """Resume the CPU."""
        self.writecmd(0x33,RESUMECPU,0,self.data)
    def ARMsetModeArm(self):
        self.writecmd(0x33,SET_MODE_ARM,0,self.data)
    def ARMtest(self):
        self.ARMreleasecpu()
        self.ARMhaltcpu()
        print "Status: %s" % self.ARMstatusstr()
        
        #Grab ident three times, should be equal.
        ident1=self.ARMident()
        ident2=self.ARMident()
        ident3=self.ARMident()
        if(ident1!=ident2 or ident2!=ident3):
            print "Error, repeated ident attempts unequal."
            print "%04x, %04x, %04x" % (ident1, ident2, ident3)
        
        #Set and Check Registers
        regs = [1024+x for x in range(1,15)]
        regr = []
        for x in range(len(regs)):
            self.ARMset_register(x, regs[x])

        for x in range(len(regs)):
            regr.append(self.ARMget_register(x))
        
        for x in range(len(regs)):
            if regs[x] != regr[x]:
                print "Error, R%d fail: %x != %x"%(x,regs[x],regr[x])

        return




        #Single step, printing PC.
        print "Tracing execution at startup."
        for i in range(15):
            pc=self.ARMgetPC()
            byte=self.ARMpeekcodebyte(i)
            #print "PC=%04x, %02x" % (pc, byte)
            self.ARMstep_instr()
        
        print "Verifying that debugging a NOP doesn't affect the PC."
        for i in range(1,15):
            pc=self.ARMgetPC()
            self.ARMdebuginstr([NOP])
            if(pc!=self.ARMgetPC()):
                print "ERROR: PC changed during ARMdebuginstr([NOP])!"
        
        print "Checking pokes to XRAM."
        for i in range(0xf000,0xf020):
            self.ARMpokedatabyte(i,0xde)
            if(self.ARMpeekdatabyte(i)!=0xde):
                print "Error in DATA at 0x%04x" % i
        
        #print "Status: %s." % self.ARMstatusstr()
        #Exit debugger
        self.stop()
        print "Done."

    def setup(self):
        """Move the FET into the JTAG ARM application."""
        #print "Initializing ARM."
        self.writecmd(0x33,SETUP,0,self.data)
    def ARMget_dbgstate(self):
        """Read the config register of an ARM."""
        retval = struct.unpack("<L", self.data[:4])[0]
        return retval
    def ARMget_dbgctrl(self):
        """Read the config register of an ARM."""
        self.writecmd(0x33,GET_DEBUG_CTRL,0,self.data)
        retval = struct.unpack("B", self.data)[0]
        return retval
    def ARMset_dbgctrl(self,config):
        """Write the config register of an ARM."""
        self.writecmd(0x33,SET_DEBUG_CTRL,1,[config&7])
    def ARMlockchip(self):
        """Set the flash lock bit in info mem."""
        self.writecmd(0x33, LOCKCHIP, 0, [])
    

    def ARMidentstr(self):
        ident=self.ARMident()
        ver     = ident >> 28
        partno  = (ident >> 12) & 0x10
        mfgid   = ident & 0xfff
        return "mfg: %x\npartno: %x\nver: %x\n(%x)" % (ver, partno, mfgid, ident); 
    def ARMident(self):
        """Get an ARM's ID."""
        self.writecmd(0x33,GET_CHIP_ID,0,[])
        retval = struct.unpack("<L", "".join(self.data[0:4]))[0]
        return retval
    def ARMgetPC(self):
        """Get an ARM's PC."""
        self.writecmd(0x33,GET_PC,0,[])
        retval = struct.unpack("<L", "".join(self.data[0:4]))[0]
        return retval
    def ARMget_register(self, reg):
        """Get an ARM's Register"""
        self.writecmd(0x33,GET_REGISTER,1,[reg&0xff])
        retval = struct.unpack("<L", "".join(self.data[0:4]))[0]
        return retval
    def ARMset_register(self, reg, val):
        """Get an ARM's Register"""
        self.writecmd(0x33,SET_REGISTER,8,[reg,0,0,0,val&0xff, (val>>8)&0xff, (val>>16)&0xff, val>>24])
        #self.writecmd(0x33,SET_REGISTER,8,[reg,0,0,0, (val>>16)&0xff, val>>24, val&0xff, (val>>8)&0xff])
        retval = struct.unpack("<L", "".join(self.data[0:4]))[0]
        return retval
    def ARMget_registers(self):
        """Get ARM Registers"""
        self.writecmd(0x33,GET_REGISTERS,0, [])
        retval = []
        for x in range(0,len(self.data), 4):
          retval.append(struct.unpack("<L", self.data[x:x+4])[0])
        return retval
    def ARMset_registers(self, regs):
        """Set ARM Registers"""
        regarry = []
        for reg in regs:
          regarry.extend([reg&0xff, (reg>>8)&0xff, (reg>>16)&0xff, reg>>24])
        self.writecmd(0x33,SET_REGISTERS,16*4,regarry)
        retval = struct.unpack("<L", "".join(self.data[0:4]))[0]
        return retval
    def ARMcmd(self,phrase):
        self.writecmd(0x33,READ,len(phrase),phrase)
        val=ord(self.data[0])
        print "Got %02x" % val
        return val
    def ARMdebuginstr(self,instr):
        if type (instr) == int:
            instr = struct.pack("<L", instr)
        self.writecmd(0x33,DEBUG_INSTR,len(instr),instr)
        return (self.data[0])
    def ARMpeekcodebyte(self,adr):
        """Read the contents of code memory at an address."""
        self.data=[adr&0xff, (adr&0xff00)>>8]
        self.writecmd(0x33,PEEK,2,self.data)
        retval = struct.unpack("<L", "".join(self.data[0:4]))[0]
        return retval
    def ARMpeekdatabyte(self,adr):
        """Read the contents of data memory at an address."""
        self.data=[adr&0xff, (adr&0xff00)>>8]
        self.writecmd(0x33, PEEK, 2, self.data)
        retval = struct.unpack("<L", "".join(self.data[0:4]))[0]
        return retval
    def ARMpokedatabyte(self,adr,val):
        """Write a byte to data memory."""
        self.data=[adr&0xff, (adr&0xff00)>>8, val]
        self.writecmd(0x33, POKE, 3, self.data)
        retval = struct.unpack("<L", "".join(self.data[0:4]))[0]
        return retval
    def ARMchiperase(self):
        """Erase all of the target's memory."""
        self.writecmd(0x33,CHIP_ERASE,0,[])
    def ARMstatus(self):
        """Check the status."""
        self.writecmd(0x33,GET_DEBUG_STATE,0,[])
        return ord(self.data[0])
    ARMstatusbits={
                  0x10 : "TBIT",
                  0x08 : "cgenL",
                  0x04 : "Interrupts Enabled (or not?)",
                  0x02 : "DBGRQ",
                  0x01 : "DGBACK"
                  }
    ARMctrlbits={
                  0x04 : "disable interrupts",
                  0x02 : "force dbgrq",
                  0x01 : "force dbgack"
                  }
                  
    def ARMstatusstr(self):
        """Check the status as a string."""
        status=self.ARMstatus()
        str=""
        i=1
        while i<0x100:
            if(status&i):
                str="%s %s" %(self.ARMstatusbits[i],str)
            i*=2
        return str
    def start(self):
        """Start debugging."""
        self.writecmd(0x33,START,0,self.data)
        #ident=self.ARMidentstr()
        #print "Target identifies as %s." % ident
        #print "Status: %s." % self.ARMstatusstr()
        #self.ARMreleasecpu()
        #self.ARMhaltcpu()
        #print "Status: %s." % self.ARMstatusstr()
        
    def stop(self):
        """Stop debugging."""
        self.writecmd(0x33,STOP,0,self.data)
    def ARMstep_instr(self):
        """Step one instruction."""
        self.writecmd(0x33,STEP_INSTR,0,self.data)
    def ARMflashpage(self,adr):
        """Flash 2kB a page of flash from 0xF000 in XDATA"""
        data=[adr&0xFF,
              (adr>>8)&0xFF,
              (adr>>16)&0xFF,
              (adr>>24)&0xFF]
        print "Flashing buffer to 0x%06x" % adr
        self.writecmd(0x33,MASS_FLASH_PAGE,4,data)

    def writecmd(self, app, verb, count=0, data=[]):
        """Write a command and some data to the GoodFET."""
        self.serialport.write(chr(app))
        self.serialport.write(chr(verb))
        count = len(data)
        #if data!=None:
        #    count=len(data); #Initial count ignored.

        #print "TX %02x %02x %04x" % (app,verb,count)

        #little endian 16-bit length
        self.serialport.write(chr(count&0xFF))
        self.serialport.write(chr(count>>8))

        #print "count=%02x, len(data)=%04x" % (count,len(data))

        if count!=0:
            if(isinstance(data,list)):
                for i in range(0,count):
                    #print "Converting %02x at %i" % (data[i],i)
                    data[i]=chr(data[i])
            #print type(data)
            outstr=''.join(data)
            self.serialport.write(outstr)
        if not self.besilent:
            self.readcmd()


