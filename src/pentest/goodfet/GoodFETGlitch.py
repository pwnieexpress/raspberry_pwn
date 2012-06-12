#!/usr/bin/env python
# GoodFET Client Library
# 
# (C) 2009 Travis Goodspeed <travis at radiantmachines.com>
#
# This code is being rewritten and refactored.  You've been warned!

import sys, time, string, cStringIO, struct, glob, serial, os, random;
import sqlite3;

from GoodFET import *;


# After four million points, this kills 32-bit gnuplot.
# Dumping to a bitmap might be preferable.
script_timevcc="""
plot "< sqlite3 glitch.db 'select time,vcc,glitchcount from glitches where count=0;'" \
with dots \
title "Scanned", \
"< sqlite3 glitch.db 'select time,vcc,count from glitches where count>0;'" \
with dots \
title "Success", \
"< sqlite3 glitch.db 'select time,vcc,count from glitches where count>0 and lock>0;'" \
with dots \
title "Exploited"
""";
script_timevccrange="""
plot "< sqlite3 glitch.db 'select time,vcc,glitchcount from glitches where count=0;'" \
with dots \
title "Scanned", \
"< sqlite3 glitch.db 'select time,vcc,count from glitches where count>0;'" \
with dots \
title "Success", \
"< sqlite3 glitch.db 'select time,max(vcc),count from glitches where count=0 group by time ;'" with lines title "Max", \
"< sqlite3 glitch.db 'select time,min(vcc),count from glitches where count>0 group by time ;'" with lines title "Min"
""";

class GoodFETGlitch(GoodFET):
    
    def __init__(self, *args, **kargs):
        print "# Initializing GoodFET Glitcher."
        #Database connection w/ 30 second timeout.
        self.db=sqlite3.connect("glitch.db",30000);
        
        #Training
        self.db.execute("create table if not exists glitches(time,vcc,gnd,trials,glitchcount,count,lock);");
        self.db.execute("create index if not exists glitchvcc on glitches(vcc);");
        self.db.execute("create index if not exists glitchtime on glitches(time);");
        
        #Exploitation record, to be built from the training table.
        self.db.execute("create table if not exists exploits(time,vcc,gnd,trials,count);");
        self.db.execute("create index if not exists exploitvcc on exploits(vcc);");
        self.db.execute("create index if not exists exploittime on exploits(time);");
        
        self.client=0;
    def setup(self,arch="avr"):
        self.client=getClient(arch);
        self.client.serInit();

    def glitchvoltages(self,time):
        """Returns list of voltages to train at."""
        c=self.db.cursor();
        #c.execute("""select
        #             (select min(vcc) from glitches where time=? and count=1),
        #             (select max(vcc) from glitches where time=? and count=0);""",
        #          [time, time]);
        c.execute("select min,max from glitchrange where time=? and max-min>0;",[time]);
        rows=c.fetchall();
        for r in rows:
            min=r[0];
            max=r[1];
            if(min==None or max==None): return [];

            spread=max-min;
            return range(min,max,1);
        #If we get here, there are no points.  Return empty set.
        return [];
    def crunch(self):
        """This builds tables for glitching voltage ranges from the training set."""
        print "Precomputing glitching ranges.  This might take a long while.";
        print "Times...";
        sys.stdout.flush();
        self.db.execute("drop table if exists glitchrange;");
        self.db.execute("create table glitchrange(time integer primary key asc,max,min);");
        self.db.commit();
        print "Calculating ranges...";
        sys.stdout.flush();
        
        maxes={};
        mins={};
        
        c=self.db.cursor();
        c.execute("select time,vcc,count from glitches;"); #Limit 10000 for testing.
        progress=0;
        for r in c:
            progress=progress+1;
            if progress % 1000000==0: print "%09i rows crunched." % progress;
            t=r[0];
            v=r[1];
            count=r[2];
            if count==0:
                try: oldmax=maxes[t];
                except: oldmax=-1;
                if v>oldmax: maxes[t]=v;
            elif count==1:
                try: oldmin=mins[t];
                except: oldmin=0x10000;
                if v<oldmin: mins[t]=v;
        print "List complete.  Inserting.";
        for t in maxes:
            max=maxes[t];
            try: min=mins[t];
            except: min=0;
            self.db.execute("insert into glitchrange(time,max,min) values (?,?,?)",(t,max,min));
        self.db.commit();
        print "Done, database crunched.";
    def graphx11(self):
        try:
            import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
        except ImportError:
            print "gnuplot-py is missing.  Can't graph."
            return;
        g = Gnuplot.Gnuplot(debug=1);
        g.clear();
        
        g.title('Glitch Training Set');
        g.xlabel('Time (16MHz)');
        g.ylabel('VCC (DAC12)');
        
        g('set datafile separator "|"');
        
        g(script_timevcc);
        print "^C to exit.";
        while 1==1:
            time.sleep(30);
    def graph(self):
        import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
        g = Gnuplot.Gnuplot(debug=1);
        
        g('\nset term png');
        g.title('Glitch Training Set');
        g.xlabel('Time (16MHz)');
        g.ylabel('VCC (DAC12)');
        
        g('set datafile separator "|"');
        g('set term png');
        g('set output "timevcc.png"');
        g(script_timevcc);
    def points(self):
        c=self.db.cursor();
        c.execute("select time,vcc,gnd,glitchcount,count from glitches where lock=0 and count>0;");
        print "time vcc gnd glitchcount count";
        for r in c:
            print "%i %i %i %i %i" % r;
    def npoints(self):
        c=self.db.cursor();
        c.execute("select time,vcc,gnd,glitchcount,count from glitches where lock=0 and count=0;");
        print "time vcc gnd glitchcount count";
        for r in c:
            print "%i %i %i %i %i" % r;
    #GnuPlot sucks for large sets.  Switch to viewpoints soon.
    # sqlite3 glitch.db "select time,vcc,count from glitches where count=0" | vp -l -d "|" -I
    
    def explore(self,tstart=0,tstop=-1, trials=1):
        """Exploration phase.  Uses thresholds to find exploitable points."""
        gnd=0;
        self.scansetup(1); #Lock the chip, place key in eeprom.
        if tstop<0:
            tstop=self.client.glitchstarttime();
        times=range(tstart,tstop);
        random.shuffle(times);
        #self.crunch();
        count=0.0;
        total=1.0*len(times);
        
        c=self.db.cursor();
        c.execute("select time,min,max from glitchrange where max-min>0;");
        rows=c.fetchall();
        c.close();
        random.shuffle(rows);
        for r in rows:
            t=r[0];
            min=r[1];
            max=r[2];
            voltages=range(min,max,1);
            count=count+1.0;
            print "%02.02f Exploring %04i points in t=%04i." % (count/total,len(voltages),t);
            sys.stdout.flush();
            for vcc in voltages:
                self.scanat(1,trials,vcc,gnd,t);
    def learn(self):
        """Learning phase.  Finds thresholds at which the chip screws up."""
        trials=1;
        lock=0;  #1 locks, 0 unlocked
        vstart=0;
        vstop=1024;  #Could be as high as 0xFFF, but upper range is useless
        vstep=1;
        tstart=0;
        tstop=self.client.glitchstarttime();
        tstep=0x1; #Must be 1
        self.scan(lock,trials,range(vstart,vstop),range(tstart,tstop));
        print "Learning phase complete, beginning to expore.";
        self.explore();
        
    def scansetup(self,lock):
        client=self.client;
        client.start();
        client.erase();
        
        self.secret=0x69;
        
        while(client.eeprompeek(0)!=self.secret):
            print "-- Setting secret";
            client.start();
            
            #Flash the secret to the first two bytes of CODE memory.
            client.erase();
            client.eeprompoke(0,self.secret);
            client.eeprompoke(1,self.secret);
            sys.stdout.flush()

        #Lock chip to unlock it later.
        if lock>0:
            client.lock();
        

    def scan(self,lock,trials,voltages,times):
        """Scan many voltages and times."""
        client=self.client;
        self.scansetup(lock);
        gnd=0;
        random.shuffle(voltages);
        #random.shuffle(times);
        
        for vcc in voltages:
            if lock<0 and not self.vccexplored(vcc):
                print "Exploring vcc=%i" % vcc;
                sys.stdout.flush();
                for time in times:
                    self.scanat(lock,trials,vcc,gnd,time)
                    sys.stdout.flush()
                self.db.commit();
            else:
                print "Voltage %i already explored." % vcc;
                sys.stdout.flush();
 
 
    def vccexplored(self,vcc):
        c=self.db.cursor();
        c.execute("select vcc from glitches where vcc=? limit 1;",[vcc]);
        rows=c.fetchall();
        for a in rows:
            return True;
        c.close();
        return False; 
    def scanat(self,lock,trials,vcc,gnd,time):
        client=self.client;
        client.glitchRate(time);
        client.glitchVoltages(gnd, vcc);  #drop voltage target
        gcount=0;
        scount=0;
        #print "-- (%5i,%5i)" % (time,vcc);
        #sys.stdout.flush();
        for i in range(0,trials):
            client.glitchstart();
            
            #Try to read *0, which is secret if read works.
            a=client.eeprompeek(0x0);
            if lock>0: #locked
                if(a!=0 and a!=0xFF and a!=self.secret):
                    gcount+=1;
                if(a==self.secret):
                    print "-- %06i: %02x HELL YEAH! " % (time, a);
                    scount+=1;
            else: #unlocked
                if(a!=self.secret):
                    gcount+=1;
                if(a==self.secret):
                    scount+=1;
        #print "values (%i,%i,%i,%i,%i);" % (
        #    time,vcc,gnd,gcount,scount);
        if(lock==0):
            self.db.execute("insert into glitches(time,vcc,gnd,trials,glitchcount,count,lock)"
                   "values (%i,%i,%i,%i,%i,%i,%i);" % (
                time,vcc,gnd,trials,gcount,scount,lock));
        elif scount>0:
            print "INSERTING AN EXPLOIT point, t=%i and vcc=%i" % (time,vcc);
            self.db.execute("insert into exploits(time,vcc,gnd,trials,count)"
                   "values (%i,%i,%i,%i,%i);" % (
                time,vcc,gnd,trials,scount));
            self.db.commit(); #Don't leave a lock open.
