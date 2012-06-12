# wifizoo
# web gui
# complains to Hernan Ochoa (hernan@gmail.com)

import BaseHTTPServer
import SimpleHTTPServer
import urlparse
import SocketServer
import wifiglobals
from threading import Thread
import os
import cgi
import urllib
import urlparse
import socket
import WifiZooEntities

class WebHandler (SimpleHTTPServer.SimpleHTTPRequestHandler):
    __base = SimpleHTTPServer.SimpleHTTPRequestHandler
    __base_handle = __base.handle

    def __init__(self, *args, **kargs):
		self._CommandsHandlers = {}
		self._initCmdHandlers()
		SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, *args, **kargs)

    def _initCmdHandlers(self):
		#self._CommandsHandlers = {}
		self._CommandsHandlers['/showssids'] = self._Handle_showssids
		self._CommandsHandlers['/showcookies'] = self._Handle_showcookies
		self._CommandsHandlers['/showapsgraph'] = self._Handle_apsgraph
		self._CommandsHandlers['/showprobesgraph'] = self._Handle_showprobesgraph
		self._CommandsHandlers['/showpop3creds'] = self._Handle_showpop3creds
		self._CommandsHandlers['/showprobessid'] = self._Handle_showprobessid
		self._CommandsHandlers['/setcookie'] = self._Handle_setcookie
		self._CommandsHandlers['/showcounters'] = self._Handle_showcounters
		self._CommandsHandlers['/showftpdata'] = self._Handle_showftpdata
		self._CommandsHandlers['/showsmtpdata'] = self._Handle_showsmtpdata
		self._CommandsHandlers['/showmsndata'] = self._Handle_showmsndata
		self._CommandsHandlers['/listapclients'] = self._Handle_listapclients

    def log_message(self, format, *args):
		return
   
    def _Handle_showcounters(self):
			self.send_response(200, 'OK')
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write('<HTML>\n')
			self.wfile.write('<HEAD><meta http-equiv="refresh" content="5"></HEAD>')

                        self.wfile.write('<TITLE>WifiZoo - Statistics</TITLE>\n')
			counters = wifiglobals.Info.getAllCounters()
			if len(counters) == 0:
				self.wfile.write('No data collected yet.<p>')
				self.wfile.write('<hr><a href="javascript:window.close()">Close</a>')
				return
			self.wfile.write('<TABLE><TR>\n')
			for k in counters.keys():
				self.wfile.write('<TD>' + k + ': ' + str(counters[k]) + '</TD><TR>')
			self.wfile.write('<TR></TABLE>')
			self.wfile.write('<hr><a href="javascript:window.close()">Close</a>')
			self.wfile.write('</HTML>')
			return

 
    def _Handle_setcookie(self):
			self.send_response(200, 'OK')
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write('<HTML>\n')
                        self.wfile.write('<TITLE>WifiZoo - Set Cookie in proxy</TITLE>\n')
			thePath = self.path[ self.path.find('?')+1: ]
			params = thePath.split('&')
			params_dict = {}
			for s in params:
					(param_name, param_value) = s.split('=')
					params_dict[ param_name ] = urllib.unquote(param_value)
			aCookie = WifiZooEntities.Cookie()
			aCookie.setData( params_dict[ 'cookie'] )
			wifiglobals.Info.setCookie( aCookie )
			self.wfile.write('Cookie Set!<p>')
			self.wfile.write('<a href="http://%s">Jump to %s</a><p>' % (params_dict['host'], params_dict['host']))
			self.wfile.write('<a href="/showcookies"/>Back</a><p>')
			#self.wfile.write("<form method=get action=/setcookie2>")
			#self.wfile.write('Cookie:<p>')
			#self.wfile.write('<textarea name=cookie width=70%>')
			#self.wfile.write( cgi.escape( params_dict['cookie'] ) )
			#self.wfile.write('</textarea><p>')
			#self.wfile.write('Host:<p>')
			#self.wfile.write('<textarea name=host width=70%>')
			#self.wfile.write( cgi.escape( params_dict['host'] ) )
			#self.wfile.write('</textarea>')
			#self.wfile.write('<input type=submit>')
			#self.wfile.write('</form>')
			#self.wfile.write( params_dict )
			self.wfile.write('\n</HTML>\n')
                        return

    def _Handle_listapclients(self):
			self.send_response(200, 'OK')
			self.send_header('Content-tye', 'text/html')
			self.end_headers()
			self.wfile.write('<HTML>\n')
			self.wfile.write('<TITLE>WifiZoo - AP clients</TITLE>\n')

			# obtain parameters
			thePath = self.path[ self.path.find('?')+1: ]
                        params = thePath.split('&')
                        params_dict = {}
                        for s in params:
                                        (param_name, param_value) = s.split('=')
                                        params_dict[ param_name ] = urllib.unquote(param_value)

			try:
				APbssid = params_dict['bssid']
			except KeyError, e:
				self.wfile.write('No clients were seen so far.')
				self.wfile.write('</HTML>\n')
				return
				
			theAP = wifiglobals.Info.getAPbyBSSID( APbssid )
			apSSID = theAP.getSSID()
			apChannel = theAP.getChannel()
			theVendor = wifiglobals.Info.getMACVendor( APbssid )
			self.wfile.write('<H2> ' + cgi.escape(APbssid) + '(' + cgi.escape(apSSID) + ') (ch:' + str(apChannel) + ')'+ '(Vendor: ' + theVendor + ') clients</H2>\n')
			

			try:
				clientsList = wifiglobals.Info.APdict[ APbssid ] 
			except KeyError, e:
				self.wfile.write('No clients were seen so far.')
				self.wfile.write('</HTML>\n')
				return
				
			for client in clientsList:
				self.wfile.write('<FONT SIZE=4>')
				clientVendor = wifiglobals.Info.getMACVendor(client)
				self.wfile.write( cgi.escape(client) + ' (' + cgi.escape(clientVendor) + ') <br>')
				self.wfile.write('</FONT>')

			self.wfile.write('</HTML>\n')
			return

    def _Handle_showmsndata(self):
                        self.send_response(200, 'OK')
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write('<HTML>\n')
                        self.wfile.write('<TITLE>WifiZoo - MSN Data</TITLE>\n')
                        if not os.path.isfile( wifiglobals.Info.logDir() + "msn.log" ):
                                        self.wfile.write('No information was captured yet.<p><a href="/index.html">Back</a><hr><p></HTML>')
                                        return
                        data = open(wifiglobals.Info.logDir()+"msn.log", "rb").read()
                        msndata = data.split('\n')
                        for aline in msndata:
                                if len(aline) > 3:
                                        if aline.find('TCP:') == 0 or aline.find('SRC:') == 0 or aline.find('WHEN:') == 0:
                                                self.wfile.write( '<FONT SIZE=2>' + cgi.escape(aline) + '<br>\n' + '</FONT>')
                                        else:
                                                self.wfile.write( '<b>' + cgi.escape(aline) + '</b><br>\n')
                        self.wfile.write('</HTML>\n')
                        return

    def _Handle_showprobessid(self):
			self.send_response(200, 'OK')
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<HTML>\n')
                        self.wfile.write('<TITLE>WifiZoo - SSIDS obtained from probes</TITLE>\n')
			ProbesList = wifiglobals.Info.getProbeRequestsBySSID()
			if len(ProbesList) == 0:
					self.wfile.write('No information was captured yet.<p><a href="/index.html">Back</a><hr><p></HTML>')
					return

			self.wfile.write('<table><tr>')
			self.wfile.write('<td><b>SSID</b></TD><td><b>DST</b></td><td><b>SRC</b></td></td><td><b>BSSID</b></td></td><td><b>Ch</b></td>')	

			for probe in ProbesList:
					iSSID = str(probe.getSSID())
					iDST = str(probe.getDST())
					iSRC = str(probe.getSRC())
					iBSSID = str(probe.getBSSID())
					iCh = str(probe.getChannel())
					self.wfile.write('<tr><td>%s</TD><td>%s</td><td>%s</td></td><td>%s</td></td><td>%s</td>' % (cgi.escape(iSSID), cgi.escape(iDST), cgi.escape(iSRC), cgi.escape(iBSSID), cgi.escape(iCh)))	
					

			self.wfile.write('</table>')
                        self.wfile.write('\n</HTML>\n')
			return

    def _Handle_showprobesgraph(self):
			self.send_response(200, 'OK')
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
			if not os.path.isfile( wifiglobals.Info.logDir() + "probereqbysrc.log" ):
					self.wfile.write('No information was captured yet.<p><a href="/index.html">Back</a><hr><p></HTML>')
					return
                        os.system('dot -Tpng -o./webgui/probes.png ./'+wifiglobals.Info.logDir()+'/probereqbysrc.log')
                        self.wfile.write('<HTML>\n<IMG alt=\"sthg went wrong. this feature needs graphviz\" SRC=\"probes.png\"></HTML>')
                        return


    def _Handle_apsgraph(self):
			self.send_response(200, 'OK')
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			if not os.path.isfile( wifiglobals.Info.logDir() + "clients.log" ):
					self.wfile.write('No information was captured yet.<p><a href="/index.html">Back</a><hr><p></HTML>')
					return
			os.system('dot -Tpng -o./webgui/clients.png ./'+wifiglobals.Info.logDir()+'/clients.log')
			self.wfile.write('<HTML>\n<IMG alt=\"sthg went wrong. this feature needs graphviz\" SRC=\"clients.png\"></HTML>')
			return

    def _Handle_showsmtpdata(self):
			self.send_response(200, 'OK')
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<HTML>\n')
			self.wfile.write('<TITLE>WifiZoo - SMTP Data</TITLE>\n')
			if not os.path.isfile( wifiglobals.Info.logDir() + "smtp.log" ):
                                        self.wfile.write('No information was captured yet.<p><a href="/index.html">Back</a><hr><p></HTML>')
                                        return
                        data = open(wifiglobals.Info.logDir()+"smtp.log", "rb").read()
                        smtpdata = data.split('\n')
			for aline in smtpdata:
				if len(aline) > 3:
					if aline.find('WHEN:') == 0 or aline.find('SRC:') == 0 or aline.find('TCP:') == 0:
						self.wfile.write('<FONT SIZE=2>' + cgi.escape(aline) + '<br>\n')
					else:
						self.wfile.write('<b>' +  cgi.escape(aline) + '</b><br>\n')
			self.wfile.write('</HTML>\n')
			return

	
    def _Handle_showftpdata(self):
			self.send_response(200, 'OK')
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<HTML>\n')
			self.wfile.write('<TITLE>WifiZoo - FTP Data</TITLE>\n')
			if not os.path.isfile( wifiglobals.Info.logDir() + "ftp.log" ):
                                        self.wfile.write('No information was captured yet.<p><a href="/index.html">Back</a><hr><p></HTML>')
                                        return
                        data = open(wifiglobals.Info.logDir()+"ftp.log", "rb").read()
                        ftpdata = data.split('\n')
			for aline in ftpdata:
				if len(aline) > 3:
					if aline.find('TCP:') == 0 or aline.find('SRC:') == 0 or aline.find('WHEN:') == 0:
						self.wfile.write( '<FONT SIZE=2>' + cgi.escape(aline) + '<br>\n' + '</FONT>')
					else:
						self.wfile.write( '<b>' + cgi.escape(aline) + '</b><br>\n')
			self.wfile.write('</HTML>\n')
			return

					
    def _Handle_showpop3creds(self):
			self.send_response(200, 'OK')
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
			self.wfile.write('<HTML>\n')
			self.wfile.write('<TITLE>WifiZoo - POP3 Credentials</TITLE>\n')
			if not os.path.isfile( wifiglobals.Info.logDir() + "pop3_creds.log" ):
					self.wfile.write('No information was captured yet.<p><a href="/index.html">Back</a><hr><p></HTML>')
					return
                        data = open(wifiglobals.Info.logDir()+"pop3_creds.log", "rb").read()
                        pop3creds = data.split('\n')
                        for aline in pop3creds:
                                if len(aline) > 3:
					if aline.find('WHEN') == 0 or aline.find('SRC:') == 0 or aline.find('TCP:') == 0:
						self.wfile.write('<font size=2>' + cgi.escape(aline) + '</font><br>\n')
					elif aline.find('USER') != -1 or aline.find('PASS') != -1:
						self.wfile.write('<font color=red>')
                                        	self.wfile.write( '<b>'+cgi.escape(aline) + '</font></b><br>' + '\n')
					else:		
                                        	self.wfile.write('<b>'+cgi.escape(aline) + '</b><br>' + '\n')
			self.wfile.write('\n</HTML>\n')
                        return


    def _Handle_showcookies(self):
			self.send_response(200, 'OK')
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<HTML>\n')
			self.wfile.write('<TITLE>WifiZoo - Cookies</TITLE>\n')
			if not os.path.isfile( wifiglobals.Info.logDir() + "cookies.log" ):
					self.wfile.write('No information was captured yet.<p><a href="/index.html">Back</a><hr><p></HTML>')
					return
			self.wfile.write('<a href="/index.html">Back</a><br><hr><p>')
			data = open(wifiglobals.Info.logDir()+"cookies.log", "rb").read()
			cookies = data.split('\n')
			tcp_data = ''

			for aline in cookies:
				if len(aline) > 3 and aline.find('--------------') != 0:
					# get TCP ip addresses
					if aline.find('TCP:') == 0 or aline.find('WHEN:') == 0 or aline.find('SRC:') == 0:
						if aline.find('TCP: ') == 0:
								tcp_data = aline
						self.wfile.write('<FONT SIZE=2>' + cgi.escape(aline) + '</FONT><br>' + '\n')
					elif aline.find('COOKIE:') == 0:
						self.wfile.write('<FONT COLOR=RED><b>')
						# the cookie is from web server to client
						if aline.find('Set-Cookie:') != -1:
							ndx = aline.find('Set-Cookie:')
							hdrlen = len('Set-Cookie:')
							cookieline = aline[ ndx+hdrlen :]
							cookie_pos_end = cookieline.find(';')
							cookie = cookieline[ 0:cookie_pos_end ]
							cookie_data = cookieline[ cookie_pos_end:]
							ipport = tcp_data.split(' ')[1]
							ipparts = ipport.split('.')
							ip = ipparts[0] + '.' + ipparts[1] + '.' + ipparts[2] + '.' + ipparts[3]
							self.wfile.write( cgi.escape ( aline[0:ndx+hdrlen] ) )	
							self.wfile.write( '<a href="/setcookie?cookie=' + urllib.quote(cookie) +  '&host=' + urllib.quote(ip) + '" target="_blank">' + cgi.escape(cookie+cookie_data) + '</a><br>')
							self.wfile.write('</b></FONT>')
						# the cookie is from client to web server
						if aline.find('Cookie:') != -1 and aline.find('Set-Cookie:') == -1:
							ndx = aline.find('Cookie:')
							hdrlen = len('Cookie:')
							cookie = aline[ ndx+len('Cookie:'):]
							ipport = tcp_data.split(' ')[3]
							ipparts = ipport.split('.')
							ip = ipparts[0] + '.' + ipparts[1] + '.' + ipparts[2] + '.' + ipparts[3]
						
							self.wfile.write( cgi.escape ( aline[0:ndx+hdrlen] ) )	
							self.wfile.write( '<a href="/setcookie?cookie=' + urllib.quote(cookie) +  '&host=' + urllib.quote(ip) + '" target="_blank">' + cgi.escape(cookie) + '</a>i<br>')
							self.wfile.write('</b></FONT>')
							
				
					else:
						self.wfile.write('<B>' + cgi.escape(aline) + '</B><br>' + '\n')

			self.wfile.write('\n</HTML>\n')
			return

    def _Handle_showssids(self):
			self.send_response(200, 'OK')
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			# get 'autorefresh' option
			autorefresh = 'off'

			# obtain parameters
			if self.path.find('?') != -1:
                        	thePath = self.path[ self.path.find('?')+1: ]
                        	params = thePath.split('&')
                        	params_dict = {}

				if len(params) >= 1:
                			for s in params:
                        	                (param_name, param_value) = s.split('=')
                                	        params_dict[ param_name ] = urllib.unquote(param_value)
			
					try:
                       	  	      		autorefresh = params_dict['autorefresh']
                       			except KeyError, e:
						autorefresh = 'off'

			if autorefresh != 'off' and autorefresh != 'on':
				autorefresh = 'off'
	

			if autorefresh == 'on':
				self.wfile.write('<HEAD><meta http-equiv="refresh" content="5"></HEAD>')

			if autorefresh == 'on':
				self.wfile.write("<font size=1><a href=\"/showssids?autorefresh=off\">[turn autorefresh off]</a></font><p>")
			else:
				self.wfile.write("<font size=1><a href=\"/showssids?autorefresh=on\">[turn autorefresh on]</a></font><p>")


			APList = wifiglobals.Info.getAPList()
			if len(APList) == 0:
					self.wfile.write('No information was captured yet.<p><a href="/index.html">Back</a><hr><p></HTML>')
					return
			
			self.wfile.write('<HTML>\n')
			self.wfile.write('<TITLE>WifiZoo - SSIDS (AP) List</TITLE>\n')
			self.wfile.write('<table>\n')
			self.wfile.write('<tr><td><b>BSSID</b></td><td><b>SSID<b></td><td><b>Ch</b></td><td><b>Enc</b></td><td><b>#clients</td><td><b>Vendor</b></td><td><b>First Seen</b></td><tr>\n')

			# first dump OPEN networks
                	for ap in APList:
                                if not ap.isProtected():
					iBSSID = str(ap.getBSSID())
					iSSID = str(ap.getSSID())
					iEnc = 'Open'
					iWhen = str(ap.getFoundWhenString()).split('.')[0]
					iCh = str(ap.getChannel())
					iClientsNum = 0
					try:
						clients = wifiglobals.Info.APdict[ iBSSID ]
						iClientsNum = len(clients)
					except:
						iClientsNum = 0
					
					apVendor = wifiglobals.Info.getMACVendor( iBSSID )	
					self.wfile.write('<tr><td><font size=2>%s</font></td><td><font size=2>%s</td><td><font size=2>%s</td><td><font size=2>%s</td><td><font size=2>%s</td><td><font size=2>%s</td><td><font size=2>%s</td>' % ('<a href="/listapclients?bssid=' + urllib.quote(iBSSID) + '\" target=\"_blank\" onclick=\"window.open(this.href,this.target);return false;\">' + cgi.escape(iBSSID) + '</a>',cgi.escape(iSSID),cgi.escape(iCh),cgi.escape(iEnc),iClientsNum,cgi.escape(apVendor),cgi.escape(iWhen)) )
					self.wfile.write('\n')

               		# now protected networks
                	for ap in APList:
                                if ap.isProtected():
					iBSSID = str(ap.getBSSID())     
                                        iSSID = str(ap.getSSID())
                                        iEnc = 'Enc'
                                        iWhen = str(ap.getFoundWhenString()).split('.')[0]
                                        iCh = str(ap.getChannel())
					iClientsNum = 0
					try:
						clients = wifiglobals.Info.APdict[ iBSSID ]
						iClientsNum = len(clients)
					except:
						iClientsNum = 0

					apVendor = wifiglobals.Info.getMACVendor( iBSSID )
					self.wfile.write('<tr><td><font size=2>%s</td><td><font size=2>%s</td><td><font size=2>%s</td><td><font size=2>%s</td><td><font size=2>%s</td><td><font size=2>%s</td><td><font size=2>%s</td>' % ('<a href=\"/listapclients?bssid=' + urllib.quote(iBSSID) + '\" target=\"_blank\" onclick=\"window.open(this.href,this.target);return false;\">' + cgi.escape(iBSSID) + '</a>',cgi.escape(iSSID),cgi.escape(iCh),cgi.escape(iEnc),iClientsNum,cgi.escape(apVendor),cgi.escape(iWhen)) )

			self.wfile.write('\n')
			self.wfile.write('</TABLE>')
			self.wfile.write('</HTML>\n')
			return
	
    def do_GET(self):
	## horrible, but works
	#self._initCmdHandlers()
	cmdFound = 0
	thePath = ''
	if self.path.find('?') != -1:
		thePath = self.path[ 0:self.path.find('?') ]
	else:
		thePath = self.path
	for cmd in self._CommandsHandlers.keys():
			if thePath == cmd:
				self._CommandsHandlers[cmd]()
				cmdFound = 1

	if cmdFound == 1:
			return	

	self.path = "/webgui/" + self.path
	SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
	#(scheme, netloc, path, params, query, fragment) = urlparse.urlparse( self.path )
	#self.wfile.write(self.path)
	#self.wfile.write(params)
	#self.wfile.write(query)


class ThreadingHTTPServer (SocketServer.ThreadingMixIn,
                           BaseHTTPServer.HTTPServer): pass

def dummy_log():
		return
	
class WifiZooWebGui(Thread):
        def __init__(self):
                Thread.__init__(self)
        def run(self):
                print "Launching Web Interface.."
                #SimpleHTTPServer.test(WebHandler, ThreadingHTTPServer)
		HandlerClass = WebHandler
		ServerClass = ThreadingHTTPServer
		protocol = 'HTTP/1.0'
		port = 8000
    		server_address = ('127.0.0.1', port)
    		HandlerClass.protocol_version = protocol
   		httpd = ServerClass(server_address, HandlerClass)
		httpd.log_message = dummy_log
    		sa = httpd.socket.getsockname()
   		print "WifiZoo Web GUI Serving HTTP on", sa[0], "port", sa[1], "..."
    		httpd.serve_forever()

                         
