#!/usr/bin/python
# coding: utf-8

# UAtester
#
# Chris John Riley
# blog.c22.cc
# contact [AT] c22 [DOT] cc
# 26/09/2010
# Version: 1.06 BETA
#
# Changelog
# 0.1 --> Initial version
# 0.2 --> Improved redirect handling
# 0.3 --> ASCII-ART for the WIN! 
# 0.4 --> Output formatting (Still not happy with this)
# 0.5 --> Released for limited Alpha testing
# 0.6 --> Changed handling of default UA strings (no need for -d), added verbose output, single mode -s, handler for URL without HTTP://
# 0.7 --> Added Android default UA string, altered -h to reflect changes to usage
# 0.8 --> Expanded on user feedback to avoid confusion of results, added feedback to clarify results, expanded default user agent strings (categorized)
# 0.81 --> Added TRY to handle ctrl-c quits
# 0.84 --> Redo response header comparison to cover full return headers, [[35;40m+[0m] Added Headers, [[35;40m-[0m] Removed Headers, [[35;40m![0m] Altered Headers
# 0.9 --> Added Set-Cookie comparison, Full headers
# 0.93 --> Added ability to select type of default UAstrings to use -d/--default --> BETA
# 0.94 --> Bug fixes and code consilidation. Increase Verbose feedback. Correct issues raised in BETA testing
# 0.95 --> Cookie comparison
# 0.98 --> Completed Secure and HTTPonly Cookie checks, added new browser UAstrings and Dangerous UA strings -d X
#      --> Added formatting changes to correct line wraps on long UA Strings, URLS, etc...
#      --> Updated positioning and minor tweaks to remove unused debug code
# 1.00 --> BruCON release... Codename Purple Pimp
# 1.01 --> Minor display bug-fix (verbose mode only)
# 1.02 --> Corrected TextWrap configuration to make Python 2.5.x compatible (removed break_on_hyphens)
# 1.03 --> Altered path to interpreter, corrected --help
# 1.04 --> Added file output CSV format - Simple output, requires manual sorting to match removed, added headers
# 1.05 --> Corrected minor display issues with blank UA strings
# 1.06 --> Minor file handling correction....
	   
import httplib
import hashlib
import urllib
import urllib2
import getopt
import sys
import re
import time
import socket
import csv
import string
import os
from textwrap import *

socket.setdefaulttimeout(15)
rechecktime = 2 # Alter this value to increase of decrease the delay between initial stability checks (default:2)
rechecks = 3 # Alter this value to decrease the number of stable checks (default/max:3)
debug = 0
err = 0
err_2 = 0
uafilepresent = False
csvfilepresent = False
single = False
verbose = False
uafile = False
csvfile = False
default = False
default_options = False
default_opts = 0
cookie_names_ref = []
cookie_names_ua = []
cookie_full_ref = []
cookie_full_ua = []

logo = '''

         _/    _/  _/_/_/_/       _/_/_/_/ _/_/_/_/ _/_/_/_/ _/_/_/_/ _/_/_/_/ _/_/_/_/
        _/    _/  _/    _/          _/    _/       _/          _/    _/       _/    _/
       _/    _/  _/_/_/_/  _/_/_/  _/    _/_/_/   _/_/_/_/    _/    _/_/_/   _/_/_/_
      _/    _/  _/    _/          _/    _/             _/    _/    _/       _/    _/
     _/_/_/_/  _/    _/          _/    _/_/_/_/ _/_/_/_/    _/    _/_/_/_/ _/      _/ [\x1B[35;40mv1.06\x1B[0m]

                                                                 _/ User-Agent Tester \x1B[35;40m↵\x1B[0m
                                                                  _/ AKA: \x1B[35;40mPurple Pimp\x1B[0m ↵
                                                                    _/ ChrisJohnRiley \x1B[35;40m↵\x1B[0m
                                                                       _/ blog.c22.cc \x1B[35;40m↵\x1B[0m\n'''

usage = '''

  This tool is designed to automatically check a given URL using a list of standard and non-
  standard User Agent strings provided by the user (1 per line).
  
  The results of these checks are then reported to the user for further manual analysis where 
  required. Gathered data includes Response Codes, resulting URL in the case of a 30x response,
  MD5 and length of response body, and select Server headers.

  Results: When in non-verbose mode, only values that do not match the initial reference connection
  are reported to the user. If no results are shown for a specific useragent then all results match
  the initial reference connection. If you require a full output of all checks regardless of matches
  to the reference, please use the verbose setting.
  
     Output:  [\x1B[35;40m+\x1B[0m] Added Headers, [\x1B[35;40m-\x1B[0m] Removed Headers, [\x1B[35;40m!\x1B[0m] Altered Headers, [ ] No Change 

  Usage .:
            -u / --url Complete URL
            -f / --file <Path to User Agent file> / If no file is provided, -d options must be present
            -s / --single provide single user-agent string (may need to be contained within quotes)
            -d / --default Select the UA String type(s) to check. Select 1 or more of the following \x1B[35;40m↵\x1B[0m
            	           catagories. (\x1B[31;40mM\x1B[0m)obile, (\x1B[31;40mD\x1B[0m)esktop, mis(\x1B[31;40mC\x1B[0m), (\x1B[31;40mT\x1B[0m)ools, (\x1B[31;40mB\x1B[0m)ots, e(\x1B[31;40mX\x1B[0m)treme [\x1B[35;40m!\x1B[0m])
			
	    -o / --output <Path to output file> CSV formated output (FILE WILL BE OVERWRITTEN[\x1B[31;40m!\x1B[0m])
	    -v / --verbose results (Displays full headers for each check) >> Recommended
            --debug See debug messages (This isn't the switch you're looking for)\n

  Example .:

	    ./UATester.py -u www.example.com -f ./useragentlist.txt -v
	    ./UATester.py -u https://www.wordpress.com
	    ./UATester.py -u http://www.defaultserver.com -v --debug
	    ./UATester.py -u facebook.com -v -d MDBX
	    ./UATester.py -u https://www.google.com -s "MySpecialUserAgent"
	    ./UATester.py -u blog.c22.cc -d MC -o ./output.csv\n'''

def main():
	
	try:
		global err
		global err_2
		global default
		global verbose
		global TextWrapper
		
		# Setup Text Wrappers to make output uniformed
		
		REFWRAP = TextWrapper(replace_whitespace=False, width=110, initial_indent="    [ ] ", subsequent_indent="	            ")
		TXTWRAP = TextWrapper(replace_whitespace=False, width=110, subsequent_indent="	             ")
		PLUSWRAP = TextWrapper(replace_whitespace=False, width=110, initial_indent="    [[35;40m+[0m] ", subsequent_indent="	            ")
		MINUSWRAP = TextWrapper(replace_whitespace=False, width=110, initial_indent="    [[35;40m-[0m] ", subsequent_indent="	            ")
		UAWRAP = TextWrapper(replace_whitespace=False, width=110, initial_indent="\n\n [>] User-Agent String : ", subsequent_indent="                         ")
		
		if verbose == True: print " [[31;40m*[0m] Running in Verbose mode\n"
		if debug == 1: print " [[31;40m*[0m] Running in Debug mode.... God help you!\n" 
		
		#uastring = 'Nokia7650/1.0 Symbian-QP/6.1 Nokia/2.1' # UAstring used for testing configuration
		uastring = 'Mozilla/5.0' # UAstring used for initial checks
		
		print " [>] Performing initial request and confirming stability\n",
		print " [>] Using User-Agent string", uastring, '\n'
		
		if csvfilepresent == True:
		
			if os.path.exists(csvfile): 
				print " [[31;40m![0m] Output file already exists!\n"
				exit()
					
			try:
				csvoutputfile_handle = open(csvfile, 'w') # Set output CSV file
				csvoutputfile = csv.writer(csvoutputfile_handle, dialect='excel')

			except:
				print"\n [[35;40m![0m] Failed to open/create the output file specified. ", err
				print"\n [!| Thanks for coming.. bye!"
				exit() 
	
		opener = urllib2.build_opener(SmartRedirectHandler()) 
		req = urllib2.Request(url)
		req.add_header('User-agent', uastring)
	
		try: resp = opener.open(req)
		except socket.timeout, err:
			print " [[31;40m*[0m] Socket Timeout: ", err
		except socket.error,err_2:
			print " [[31;40m*[0m] Socket Error: ", err
		except urllib2.HTTPError, err:
			print " [[31;40m*[0m] HTTPError: ", err
		except urllib2.URLError, err:
				print " [[31;40m*[0m] URLError: ", err
		except ValueError, err:
			print " [[31;40m*[0m] ValueError: ", err, "\n"
		if err: exit();

 		try: ref_resp_statuscode = resp.status
 		except AttributeError, err:
 			ref_resp_statuscode = resp.code, resp.msg
	 
		print '    [ ] URL (ENTERED):', url
		ref_url = resp.geturl()	
		if url != resp.geturl(): 
			print '    [[35;40m![0m] URL (FINAL):',
			for line in TXTWRAP.wrap(resp.geturl()): print line
		if url != resp.geturl(): print '    [[35;40m![0m] Response Code:', ref_resp_statuscode[0], ref_resp_statuscode[1]
		else: print '    [ ] Response Code:', ref_resp_statuscode[0], ref_resp_statuscode[1]
		
		ref_headers = resp.info()
		ref_headers_len = len(str(ref_headers).split('\n')) -1
		ref_data = resp.read()
		ref_md5 = hashlib.md5(ref_data)
		
		if csvfilepresent == True:
			csvform = map(string.strip, ref_headers.headers)
			csvform.insert(0, ref_resp_statuscode)
			csvform.insert(0, resp.geturl())
			csvform.insert(0, uastring)
			csvform.append(ref_md5.hexdigest())
			csvoutputfile.writerow(csvform)
		
		if debug == 1: print resp.info()
		
		i = 0
		while i < ref_headers_len:
		
			for line in REFWRAP.wrap(ref_headers.headers[i]): print line
			i=i+1

		print '    [ ] Data (MD5):', ref_md5.hexdigest(), "\n"
	
		i = 0
		stable = 1
		while i < rechecks: 
			time.sleep(rechecktime) # wait X second and recheck server - See rechecktime variable
			req2 = req
			
			try:resp_2 = opener.open(req2)
			except socket.timeout, err_2:
				print " [[31;40m*[0m] Socket Timeout: ", err_2
			except socket.error,err_2:
				print " [[31;40m*[0m] Socket Error: ", err_2
			except urllib2.HTTPError, err_2:
				print " [[31;40m*[0m] HTTPError: ", err_2
			except urllib2.URLError, err_2:
				print " [[31;40m*[0m] URLError: ", err_2
			except ValueError, err_2:
				print " [[31;40m*[0m] ValueError: ", err_2, "\n"
			if err_2: print ' [[31;40m*[0m] ERR ', err_2; exit();
			
			try: ref_resp_2_statuscode = resp.status
			except AttributeError, err:
				ref_resp_2_statuscode = resp.code, resp.msg
			
			if debug == 1: print "\n        [Debug RESP2] :", ref_resp_2_statuscode[0], ref_resp_2_statuscode[1]
			
			if debug == 1: print "\n	[Debug URL] :", resp_2.geturl(); print "	[Debug URL] :", resp.geturl();
			if resp_2.geturl() != ref_url:
				print "\n [[35;40m![0m] URL Value doesn't appear stable" 
				print '    [[35;40m![0m] URL (FINAL):',
				for line in TXTWRAP.wrap(resp_2.geturl()): print line
				
				stable = 0
				url_stable = 0
			else:	
				print " [\x1B[31;40m"+ str(i+1) +"\x1B[0m] Pass"
			
			stable_check_headers = resp_2.info()
			stable_check_headers_len = len(str(stable_check_headers).split('\n')) -1
			stable_check_data = resp_2.read()
			stable_check_md5 = hashlib.md5(stable_check_data)
			
			if debug == 1: print resp_2.info()

			j = 0
			exclude = 0
			while j < stable_check_headers_len:
				if re.search(r'expires|vtag|etag|date|time|set-cookie|x-transaction|X-Cache|Age' , stable_check_headers.headers[j], re.IGNORECASE): # Ignore commonly changing headers
					exclude = 1
			
				if exclude == 0:
					if debug == 1: print "\n	[Debug] :", stable_check_headers.headers[j],; print "	[Debug] :", ref_headers.headers[j],;
					if stable_check_headers.headers[j] != ref_headers.headers[j]:
						print '	[[35;40m![0m] Instability Detected'
						stable = 0
						print '		[[35;40m![0m]', ref_headers.headers[j],
						print '		[[35;40m![0m]', stable_check_headers.headers[j],
						
				if i == 2 and re.search(r'set-cookie' , stable_check_headers.headers[j], re.IGNORECASE): # On last Stable check, gather cookie info for later comparison
					ref_cookie_temp = ref_headers.headers[j].split(':',1)
					ref_cookie_temp_2 = ref_headers.headers[j].split(';')
					ref_cookie_temp = ref_cookie_temp[1].split('=',1)
					if ref_cookie_temp[0] not in cookie_names_ref:
						cookie_names_ref.append(ref_cookie_temp[0])
						cookie_full_ref.append(stable_check_headers.headers[j])
						
				if stable != 1: break; # If the responses are not stable, break while loop - No point in checking 3 times if once will do
				
				j=j+1
			
			i = i+1	
			
			if debug == 1: print 'Cookies', cookie_names_ref
	
		if stable != 1:
			print "\n [[35;40m![0m] The URL given doesn't appear to give stable responses"
			print " [[35;40m![0m] Results may vary, and should be manually confirmed\n"
		else:
			print "\n [>] URL appears stable. Beginning test"

#
# (BUILT-IN) UA STRINGS
#
		
		def_uastrings_desktop = [
	
		# Default Browsers
		
		"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
		"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)",
		"Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)",
		"Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
		"Mozilla/4.0 (compatible;MSIE 5.5; Windows 98)",
		"Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)",
		"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100922 Firefox/4.0.1",
		"Mozilla/5.0 (Windows; U; Windows NT 5.2; rv:1.9.2) Gecko/20100101 Firefox/3.6",
		"Mozilla/5.0 (X11; U; SunOS sun4v; en-US; rv:1.8.1.3) Gecko/20070321 Firefox/2.0.0.3",
		"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
		"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
		"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
		"Opera/9.99 (Windows NT 5.1; U; pl) Presto/9.9.9",
		]
	
		def_uastrings_bots = [
	
		# Spidering bots (Goolge, MSN, etc..)
		
		"Googlebot/2.1 (+http://www.google.com/bot.html)",
		"Googlebot-Image/1.0",
		"Mediapartners-Google",
		"Mozilla/2.0 (compatible; Ask Jeeves)",
		"msnbot-Products/1.0 (+http://search.msn.com/msnbot.htm)",
		"mmcrawler",
		]
	
		def_uastrings_crazy = [
		
		# Crazy WTF stuff (TrackBack is the local Apache uastring)
		
		"Windows-Media-Player/9.00.00.4503",
		"Mozilla/5.0 (PLAYSTATION 3; 2.00)",
		"TrackBack/1.02",
		"wispr",
		"",
		]
		
		def_uastrings_dangerous = [
		
		# Possible dangerous strings, use at own risk! Not run unless selected through -d X
		
		"<script>alert('UATester')</script>",
		"'",
		"' or 22=22'--",
		"%0d%0a",
		"../../../../../../etc/passwd",
		"../../../../../boot.ini",
		"VUF0ZXN0ZXIgdGhlIHBydXBsZSBwaW1wIGVkaXRpb24=", # Base64 encoded string "UAtester the pruple pimp edition"
		]
	
		def_uastrings_tools = [
	
		# Commonly used tools. Additions from the Mod_Security ruleset
		
		"Mozilla/4.75 (Nikto/2.01)",
		"curl/7.7.2 (powerpc-apple-darwin6.0) libcurl 7.7.2 (OpenSSL 0.9.6b)",
		"w3af.sourceforge.net",
		"HTTrack",
		"Wget 1.9cvs-stable",
		"Lynx (textmode)",
		".nasl",
		"paros",
		"webinspect",
		"brutus",
		"java",
		]
	
		def_uastrings_mobile = [
		
		# Mobile devices
		
		"Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3",
		"Mozilla/5.0 (iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10",
		"Mozilla/5.0 (Linux; U; Android 2.1-update1; en-at; HTC Hero Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
		"jBrowser-WAP",
		"Nokia7650/1.0 Symbian-QP/6.1 Nokia/2.1"
		]

# NEW CHECK SECTION
		
		global default
		default = True
		uastrings = [] # Create empty list for UAstrings
		
		if uafilepresent == True:
			print"\n [>] Reading User-Agents from: ", uafile
			default = False # prevent default strigns from running
			
			try:
				uastrings_file = open (uafile) # Set uastrings to file contents

			except:
				print"\n [[35;40m![0m] Failed to read the User-Agents from the file specified"
				print"\n [!| Thanks for coming.. bye!"
				exit(1)

			uastrings = uastrings_file.readlines() # Add all file contents into list

			try:
				uastrings_file.close() # Close file
			except:
				print 'Unable to close file handle... sorry'
				exit(1)
	
		if single == True:
			print"\n [>] Using SINGLE User-Agent String specified in commandline"
			print" [[35;40m![0m] Verbose mode activated for SINGLE mode testing"
			verbose = True
			
			default = False # prevent default strigns from running
			uastrings.append(single_uastring) # Set uastrings to Single
	
		if default == True:
			print"\n [>] Using DEFAULT User-Agent Strings"
				
			if default_options == True:
					
				if 'M' in default_opts.upper():
					print"\n [>] Using Mobile User-Agent Strings",
					uastrings.extend(def_uastrings_mobile)
				if 'D' in default_opts.upper():
					print"\n [>] Using Desktop User-Agent Strings",
					uastrings.extend(def_uastrings_desktop)
				if 'C' in default_opts.upper():
					print"\n [>] Using Crazy User-Agent Strings",
					uastrings.extend(def_uastrings_crazy)
				if 'T' in default_opts.upper():
					print"\n [>] Using Tool User-Agent Strings",
					uastrings.extend(def_uastrings_tools)
				if 'B' in default_opts.upper():
					print"\n [>] Using Bot User-Agent Strings",
					uastrings.extend(def_uastrings_bots)
				if 'X' in default_opts.upper():
					print"\n [>] Using Dangerous User-Agent Strings\n [>] Contine at your own risk"
					answer = raw_input("\n    [>] Press Y to accept >> ")
					if answer.upper() != 'Y':
						print"\n [>] Bam... pimp slap!\n"
						exit();
					else: print"\n [>] 00OOooh Who da' man! Well don't say you didn't ask for it!"
					uastrings.extend(def_uastrings_dangerous)
			
			else: uastrings.extend(def_uastrings_mobile);uastrings.extend(def_uastrings_desktop);uastrings.extend(def_uastrings_crazy);uastrings.extend(def_uastrings_tools);uastrings.extend(def_uastrings_bots)
		
		print "\n\n [>] Output: [[35;40m+[0m] Added Headers, [[35;40m-[0m] Removed Headers, [[35;40m![0m] Altered Headers, [ ] No Change"
		
		header_printed_global = False
		
		for ualine in uastrings:
			err = 0		
			current = ualine
			header_printed = False

			req = urllib2.Request(url)
			req.add_header('User-agent', ualine)
			
			try: resp2 = opener.open(req)
			except socket.timeout, err:
				print " [[31;40m*[0m] Socket Timeout: ", err
			except socket.error,err_2:
				print " [[31;40m*[0m] Socket Error: ", err
			except urllib2.HTTPError, err:
				print " [[31;40m*[0m] HTTPError: ", err
			except urllib2.URLError, err:
				print " [[31;40m*[0m] URLError: ", err
			except ValueError, err:
				print " [[31;40m*[0m] ValueError: ", err, "\n"
			if err: exit();
			
			if ualine == "": ualine = "EMPTY USER-AGENT STRING\x1B[31;40m!\x1B[0m" # Set to inform user of empty string
	
			ua_check_headers = resp2.info()
			ua_check_headers_len = len(str(ua_check_headers).split('\n')) -1
			ua_check_data = resp2.read()
			ua_check_md5 = hashlib.md5(ua_check_data)
			
			try: statuscode = resp2.status
			except AttributeError, err:
				statuscode = resp2.code, resp2.msg
			
			if csvfilepresent == True:
				csvform = []
				csvform = map(string.strip, ua_check_headers.headers)
				csvform.insert(0, statuscode)
				csvform.insert(0, resp2.geturl())
				csvform.insert(0, ualine)
				csvform.append(ua_check_md5.hexdigest())
				csvoutputfile.writerow(csvform)
			
			if debug == 1: print resp2.info()
				
			if ref_url != resp2.geturl() or verbose == True:
				icon = ' '
				if ref_url != resp2.geturl(): icon = '\x1B[35;40m!\x1B[0m'
				for line in UAWRAP.wrap(ualine): print line
				print '\n'
				print '    [' + icon + '] URL (FINAL):',
				for line in TXTWRAP.wrap(resp2.geturl()): print line
				header_printed = True
				header_printed_global = True
				
			ua_check_statuscode = statuscode
			
			if ref_resp_statuscode[0] != ua_check_statuscode[0] or verbose == True:
				if header_printed == False: 
					for line in UAWRAP.wrap(ualine): print line
					print '\n'
				icon = ' '
				if ref_resp_statuscode[0] != ua_check_statuscode[0]: icon = '\x1B[35;40m!\x1B[0m'
				print '    [' + icon + '] Response Code:', ua_check_statuscode[0],ua_check_statuscode[1]; match = True
				header_printed = True
				header_printed_global = True
				
			j = 0
			exclude = 0
	
			while j < ua_check_headers_len:
				
				if verbose == False and re.search(r'expires|vtag|date|time|x-transaction|Set-Cookie|X-Cache|Age' , ua_check_headers.headers[j], re.IGNORECASE): # Ignore commonly changing headers
					exclude = 1
		
				if exclude == 0:
					ua_check_headers_match = ua_check_headers.headers[j].split(':',1)
					if debug == 1:
						if header_printed == False: 
							for line in UAWRAP.wrap(ualine): print line
							print '\n'
						header_printed = True
						header_printed_global = True

					k = 0
					while k < ref_headers_len:
						ref_headers_match = ref_headers.headers[k].split(':',1)
						if debug == 1:
							if header_printed == False:
								for line in UAWRAP.wrap(ualine): print line
								print '\n'
							header_printed = True
							header_printed_global = True
						
						if ua_check_headers_match[0] == ref_headers_match[0]:
							header_match = 1
							if ua_check_headers_match[1] == ref_headers_match[1]:
								value_match = 1
								if verbose == True:
									if header_printed == False:
										for line in UAWRAP.wrap(ualine): print line
										print '\n'
									header_printed = True
									header_printed_global = True
									for line in REFWRAP.wrap(ua_check_headers.headers[j]): print line
									#print '    [ ]', ua_check_headers.headers[j],
								break;
							else:
								if header_printed == False:
									for line in UAWRAP.wrap(ualine): print line
									print '\n'
								header_printed = True
								header_printed_global = True
								if re.search(r'Set-Cookie' , ua_check_headers.headers[j], re.IGNORECASE): 
									break;
								else: 
									print '    [[35;40m![0m]', ua_check_headers.headers[j],
								break;
						k=k+1
						
					if k == ref_headers_len and header_match == 0:
						print '    [[35;40m+[0m]', ua_check_headers.headers[j],
				
				if re.search(r'set-cookie' , ua_check_headers.headers[j], re.IGNORECASE):
					ua_cookie_temp = ua_check_headers.headers[j].split(':',1)
					ua_cookie_temp = ua_cookie_temp[1].split('=',1)
					if ua_cookie_temp[0] not in cookie_names_ua:
						cookie_names_ua.append(ua_cookie_temp[0])
						cookie_full_ua.append(ua_check_headers.headers[j])
				
				j=j+1
				
				if j == ua_check_headers_len:
					if debug == 1:print ' ua and ref cookies =', cookie_names_ua, cookie_names_ref
					
					l = 0
					k = 0

					while l < len(cookie_names_ua):		
						
						cookie_name = str(cookie_names_ua[l])
						try: ref_match = cookie_names_ref.index(cookie_name)
						except: ref_match = False
						
						if cookie_names_ua[l] not in cookie_names_ref:
							if header_printed == False: 
								for line in UAWRAP.wrap(ualine): print line
								print '\n'
								header_printed = True
								header_printed_global = True
								
							for line in PLUSWRAP.wrap(cookie_full_ua[l]): print line
						else:
						
							httponly = False
							httponly_ref = False
							httponly_ua = False
							secure = False
							secure_ref = False
							secure_ua = False # Reset results for next Cookie
							
							if re.search(r'httponly', cookie_full_ua[l] , re.IGNORECASE) or re.search(r'httponly', cookie_full_ref[ref_match] , re.IGNORECASE):
								httponly = True # Mark httponly flag found
								if re.search(r'httponly', cookie_full_ref[ref_match] , re.IGNORECASE): httponly_ref = True
								if re.search(r'httponly', cookie_full_ua[l] , re.IGNORECASE): httponly_ua = True
							
							if re.search(r'secure', cookie_full_ua[l] , re.IGNORECASE) or re.search(r'secure', cookie_full_ref[ref_match] , re.IGNORECASE):
								secure = True # Mark secure flag found
								if re.search(r'secure', cookie_full_ref[ref_match] , re.IGNORECASE): secure_ref = True
								if re.search(r'secure', cookie_full_ua[l] , re.IGNORECASE): secure_ua = True
							
							if httponly_ref != httponly_ua:
								print '    [[35;40m![0m]', cookie_full_ua[l],
								if httponly_ref == False: print '        [[35;40m+[0m] HTTPonly flag set'
								else: print '        [[35;40m-[0m] HTTPonly flag removed'
							if secure_ref != secure_ua:
								print '    [[35;40m![0m]', cookie_full_ua[l],
								if secure_ref == False: print '        [[35;40m+[0m] Secure flag set'
								else: print '        [[35;40m-[0m] Secure flag removed'
							
							if httponly == False and secure == False:
								if cookie_names_ua[l] in cookie_names_ref and verbose == True:
									for line in REFWRAP.wrap(cookie_full_ua[l]): print line
							
							
						l=l+1
					while k < len(cookie_names_ref):
						if cookie_names_ref[k] not in cookie_names_ua:
							if header_printed == False: 
								for line in UAWRAP.wrap(ualine): print line
								print '\n'
								header_printed = True
								header_printed_global = True
								
							for line in MINUSWRAP.wrap(cookie_full_ref[k]): print line
						k=k+1
	
				exclude = 0
				header_match = 0
				value_match = 0
	
			j = 0 # Reset counter for missing header check
			exclude = 0
			while j < ref_headers_len:
				ref_headers_match = ref_headers.headers[j].split(':',1)
				k = 0
				while k < ua_check_headers_len:
					ua_check_headers_match = ua_check_headers.headers[k].split(':',1)
					if ref_headers_match[0] == ua_check_headers_match[0]:
						header_match = 1
						break;
	
					k=k+1
					
				if k == ua_check_headers_len and header_match != 1:
					if header_printed == False: 
						for line in UAWRAP.wrap(ualine): print line
						print '\n'
						header_printed = True
						header_printed_global = True
					for line in MINUSWRAP.wrap(ref_headers.headers[j]): print line
							
				j=j+1
				exclude = 0
				header_match = 0
				value_match = 0
	
			if ref_md5.hexdigest() != ua_check_md5.hexdigest():
				if header_printed == False:
					for line in UAWRAP.wrap(ualine): print line
					print '\n'
					print '    [[35;40m![0m] Data (MD5):', ua_check_md5.hexdigest()
			elif verbose == True:
				if header_printed == False: 
					for line in UAWRAP.wrap(ualine): print line
					print '\n'
					header_printed = True
					header_printed_global = True
				print '    [ ] Data (MD5):', ua_check_md5.hexdigest();
			
		print "\n"
		if header_printed_global == False: print " [>] Checks completed... try enabling VERBOSE mode for more detailed output\n"	
		if csvfilepresent == True:
			try:
				csvoutputfile_handle.close() # Close file
			except:
				print 'Unable to close output file handle... sorry', err
				exit(1)
		
		print " [>] That's all folks... Fo' Shizzle!"
		print "\n"
		
	except KeyboardInterrupt: print '\n\n [[31;40m*[0m] Error: ctrlc_caught'; print ' [[31;40m*[0m] Thanks for coming... keep on pimpin!\n'; exit()	
			
class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
	
    def http_error_301(self, req, fp, code, msg, headers):  
        result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)              
        try: result.status = code, msg
        except: result.status = 'No Status Code in Return Header'       
        return result 
	
    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers) 
        try: result.status = code, msg
        except: result.status = 'No Status Code in Return Header'
	return result
   
    def http_error_303(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)
        try: result.status = code, msg
        except: result.status = 'No Status Code in Return Header'
        return result

    def http_error_307(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)
        try: result.status = code, msg
        except: result.status = 'No Status Code in Return Header'
        return result
		
try:
	opts, args = getopt.getopt(sys.argv[1:], "u:f:s:d:o:vh", ["url=", "file=", "single", "default=", "output=", "verbose", "help", "debug"])
except getopt.GetoptError:
	print (logo)
	print (usage)
	sys.exit(2)
if len(sys.argv) < 3:
        print (logo)
        print (usage)
	sys.exit(2)
for opt, arg in opts:
	if opt in ("-h", "--help"):
		print (logo)
		print (usage)
		sys.exit()
	elif opt in ("-u", "--url"):
		url = arg.lower()
		if url.startswith("http"): url = arg
		else: url = "http://" +arg 
	elif opt in ("-f", "--file"):
		uafile = arg
		uafilepresent = True
        elif opt in ("-s", "--single"):
                single_uastring = arg
                single = True
       	elif opt in ("-d", "--default"):
        		if arg == ' ': arg = 'MDCTB'
        		default_opts = arg
        		default_options = True
	elif opt in ("-o", "--output"):
		csvfile = arg
		csvfilepresent = True
	elif opt in ("-v", "--verbose"):
		verbose = True
	elif opt in ("--debug"):
		debug = 1

if __name__== '__main__':  
   print (logo)
   main()  
