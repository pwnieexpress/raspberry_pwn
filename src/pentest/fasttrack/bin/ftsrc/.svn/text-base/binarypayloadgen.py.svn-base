#!/usr/bin/env python
import os
import sys
import time
import subprocess

definepath=os.getcwd()
sys.path.append("%s/bin/ftsrc/" % (definepath))
import include
include.print_banner()

try:
   import psyco
   psyco.full()
except ImportError:
   pass
try:
   define=sys.argv[3]
except IndexError:
   print """Binary to Hex Generator v0.1
   
    This menu will convert an exe to a hex file which you just need
    to copy and paste the output to a windows command prompt, it will
    then generate an executable based on your payload

    **Note** Based on Windows restrictions the file cannot be over 64kb
    
    <ctrl>-c to Cancel
"""
   define=raw_input("    Enter the path to the file to convert to hex: ") 
output="binarypayload.txt"
from sys import exit, stdout
throwerror=300
filesize = lambda x,n: stdout.write(x+'\n') or throwerror#(n)#exit(n)
try: fileopen,writefile = open(define,'rb'),open(output,'w')
except: print "    Something went wrong...."
FOOTER  = ''.join(map(lambda x:"echo "+x+">>T\n",
["RCX","%X ","N T.BIN","WDS:0","Q"])) 
FOOTER += 'DEBUG<T 1>NUL\nMOVE T.BIN binary.exe 1>NUL 2>NUL'
FC,CX = 0, fileopen.seek(0,2) or fileopen.tell()
if (CX > 0xFFFF): 
  fileopen.close(); writefile.close()
  filesize('[!] filesize exceeds 64kb, quitting.',1);
fileopen.seek(0,0)
writefile.write('DEL T 1>NUL 2>NUL\n')
try:
   for chunk in xrange(0x1000):
     finalwrite = fileopen.read(16) or writefile.write(FOOTER%CX) or filesize("",0)
     if finalwrite.count('\0')==0x10: FC += 1
     else:
       if FC > 0:
         writefile.write('echo FDS:%X L %X 00>>T\n'%((chunk-FC)*0x10,FC*0x10))
         FC = 0
       writefile.write('echo EDS:%X '%(chunk*0x10))
       writefile.write(' '.join(map(lambda x:"%02X"%ord(x),finalwrite))+'>>T\n')
except Exception:
       print "Finished..."
       print "Check out the file 'binarypayload.txt' in the Fast-Track directory."
# Removed old call for os.system, no longer supported
#kateopen=os.system(r"kwrite %s 2> /dev/null &" % (output))
#kateopen=subprocess.Popen(r"kwrite %s 1> /dev/null 2> /dev/null &" % (output), shell=True)
