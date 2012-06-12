#!/usr/bin/env python
"""
	Grabber Core v0.1
	Copyright (C) 2006 - Romain Gaucher - http://rgaucher.info
"""
from BeautifulSoup import BeautifulSoup
from xml.sax import *   # Need PyXML [http://pyxml.sourceforge.net/]
from optparse import OptionParser
from urllib2 import URLError, HTTPError
import urllib
import time
import re,sys,os

# Personal libraries
from spider import database, database_css, database_js
from spider import spider, cj, allowedExtensions

COOKIEFILE = 'cookies.lwp'          # the path and filename that you want to use to save your cookies in
import os.path
txdata = None
refererUrl = "http://google.com/?q=grabber"
txheaders = {'User-agent' : 'Grabber/0.1 (X11; U; Linux i686; en-US; rv:1.7)', 'Referer' : refererUrl}

import cookielib
import urllib2
urlopen = urllib2.urlopen
Request = urllib2.Request

def normalize_whitespace(text):
	return ' '.join(text.split())

def clear_whitespace(text):
	return text.replace(' ','')

# Configuration variables
confFile = False
confUrl  = ""
confSpider = False
confActions = []
confInfos   = {}

# Handle the XML file with a SAX Parser
class ConfHandler(ContentHandler):
	def __init__(self):
		global confFile
		confFile = True
		self.inSite    = False
		self.inScan    = False
		self.inSpider  = False
		self.inUrl     = False
		self.inAction  = False
		self.string = ""
		self.listActions = ["crystal", "sql","bsql","xss","include","backup","javascript", "session"]
	def startElement(self, name, attrs):
		global confUrl,confInfos
		self.string = ""
		if name == 'site':
			self.inSite = True
		if name == 'spider' and self.inSite:
			self.inSpider = True
		if name == 'scan' and self.inSite:
			self.inScan = True
		elif self.inSite and name == 'url':
			self.inUrl = True
			confUrl = ""
		elif self.inScan and name in self.listActions:
			self.inAction = True
			if 'info' in attrs.keys():
				confInfos[name] = attrs.getValue('info')
	def characters(self, ch):
		if self.inSite:
			self.string = self.string + ch
	def endElement(self, name):
		global confUrl,confActions,confSpider
		if name == 'url' and self.inUrl:
			self.inUrl = False
			confUrl = normalize_whitespace(self.string)
		if name == 'spider' and self.inSpider:
			self.inSpider = False
			confSpider = clear_whitespace(self.string)
		if name in self.listActions and self.inScan and not name in confActions:
			confActions.append(name)
		if name == 'site' and self.inSite:
			self.inSite = False

attack_list = { }

# Handle the XML file with a SAX Parser
class AttackHandler(ContentHandler):
	def __init__(self):
		global attack_list
		attack_list = {}
		self.inElmt = False
		self.inCode = False
		self.inName = False
		self.sName   = ""
		self.code   = ""
	def startElement(self, name, attrs):
		if name == 'attack':
			self.inElmt = True
		elif name == 'code':
			self.inCode = True
			self.code = ""
		elif name == "name":
			self.inName = True
			self.sName = ""
	def characters(self, ch):
		if self.inCode:
			self.code = self.code + ch
		elif self.inName:
			self.sName = self.sName + ch
	def endElement(self, name):
		global attack_list
		if name == 'code':
			self.inCode = False
			self.code = normalize_whitespace(self.code)
		if name == 'name':
			self.inName = False
			self.sName = normalize_whitespace(self.sName)
		if name == 'attack':
			self.inElmt = False
			# send the plop in the dictionnary
			if not (self.sName in attack_list.keys()):
				attack_list[self.sName] = []
			attack_list[self.sName].append(self.code)

class LogHandler:
	def __init__(self, fileName):
		self.stream = None
		try:
			self.stream = open(fileName, 'w')
		except IOError:
			print "Error during the construction of the log system"
			return
		self.stream.write("# Log from Grabber.py\n")
	def __le__(self, string):
		self.stream.write(string + '\n')
		self.stream.flush()
	def __del__(self):
		self.stream.close()

log = LogHandler('grabber.log')

def unescape(s):
	"""
		Unescaping the HTML special characters
	"""
	s = s.replace("&lt;", "<")
	s = s.replace("&gt;", ">")
	s = s.replace("&quot;", "\"")
	s = s.replace("&apos;","'")
	s = s.replace("&amp;", "&")
	return s


def single_urlencode(text):
   """single URL-encode a given 'text'.  Do not return the 'variablename=' portion."""
   blah = urllib.urlencode({'blahblahblah':text})
   #we know the length of the 'blahblahblah=' is equal to 13.  This lets us avoid any messy string matches
   blah = blah[13:]
   blah = blah.replace('%5C0','%00')
   return blah

def getContent_GET(url,param,injection):
	global log
	"""
		Get the content of the url by GET method
	"""
	newUrl = url
	ret = None
	if url.find('?') < 0:
		if url[len(url)-1] != '/' and not allowedExtensions(url):
			url += '/'
		newUrl = url + '?' + param + '=' + single_urlencode(str(injection))
	else:
		newUrl = url + '&' + param + '=' + single_urlencode(str(injection))
	try:
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		urllib2.install_opener(opener)
		log <= ( newUrl)
		req = Request(newUrl, None, txheaders) # create a request object
		ret = urlopen(req)                     # and open it to return a handle on the url
		ret = urlopen(req)                     # and open it to return a handle on the url
	except HTTPError, e:
		log <= ( 'The server couldn\'t fulfill the request.')
		log <= ( 'Error code: %s' % e.code)
		return None
	except URLError, e:
		log <= ( 'We failed to reach a server.')
		log <= ( 'Reason: %s' % e.reason)
		return None
	except IOError:
		log <= ( "Cannot open: %s" % url)
		return None
	return ret


def getContentDirectURL_GET(url, string):
	global log
	"""
		Get the content of the url by GET method
	"""
	ret = ""
	try:
		if len(string) > 0:
			if url[len(url)-1] != '/' and url.find('?') < 0  and not allowedExtensions(url):
				url += '/'
			url = url + "?" + (string)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		urllib2.install_opener(opener)
		log <= ( url)
		req = Request(url, None, txheaders) # create a request object
		ret = urlopen(req)                     # and open it to return a handle on the url
	except HTTPError, e:
		log <= ( 'The server couldn\'t fulfill the request.')
		log <= ( 'Error code: %s' % e.code)
		return None
	except URLError, e:
		log <= ( 'We failed to reach a server.')
		log <= ( 'Reason: %s' % e.reason)
		return None
	except IOError:
		log <= ( "Cannot open: %s" % url)
		return None
	return ret


def getContent_POST(url,param,injection):
	global log
	"""
		Get the content of the url by POST method
	"""
	txdata = urllib.urlencode({param: injection})
	ret = None
	try:
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		urllib2.install_opener(opener)
		log <= ( url)
		log <= ( txdata)
		req = Request(url, txdata, txheaders)  # create a request object
		ret = urlopen(req)                     # and open it to return a handle on the url
		ret = urlopen(req)                     # and open it to return a handle on the url
	except HTTPError, e:
		log <= ( 'The server couldn\'t fulfill the request.')
		log <= ( 'Error code: %s' % e.code)
		return None
	except URLError, e:
		log <= ( 'We failed to reach a server.')
		log <= ( 'Reason: %s' % e.reason)
		return None
	except IOError:
		log <= ( "Cannot open: %s" % url)
		return None
	return ret


def getContentDirectURL_POST(url,allParams):
	global log
	"""
		Get the content of the url by POST method
	"""
	txdata = urllib.urlencode(allParams)
	ret = None
	try:
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		urllib2.install_opener(opener)
		log <= ( url)
		log <= ( txdata)
		req = Request(url, txdata, txheaders)  # create a request object
		ret = urlopen(req)                     # and open it to return a handle on the url
		ret = urlopen(req)                     # and open it to return a handle on the url
	except HTTPError, e:
		log <= ( 'The server couldn\'t fulfill the request.')
		log <= ( 'Error code: %s' % e.code)
		return None
	except URLError, e:
		log <= ( 'We failed to reach a server.')
		log <= ( 'Reason: %s' % e.reason)
		return None
	except IOError:
		log <= ( "Cannot open: %s" % url)
		return None
	return ret

# Levenstein distance
def ld(a, b): # stolen from m.l. hetland
	n, m = len(a), len(b)
	if n > m:
		# Make sure n <= m, to use O(min(n,m)) space
		a,b = b,a
		n,m = m,n
	current = xrange(n+1)
	for i in xrange(1,m+1):
		previous, current = current, [i]+[0] * m
		for j in xrange(1, n+1):
			add, delete = previous[j] + 1, current[j-1] + 1
			change = previous[j-1]
			if a[j-1] != b[i-1]:
				change +=1
			current[j] = min(add, delete, change)
	return current[n]


def partially_in(object, container, url = "IMPOSSIBLE_GRABBER_URL", two_long = False):
	"""
		Crappy decision function
			Is an object partially in a text ?
	"""
	try:
		if object in container and url not in container:
			return True
	except TypeError:
		return False
	if not two_long:
		# load the big engine...
		dist = ld(object, container)
		# espilon ~ len(object) / 4
		b1 = int(len(object) - len(object) / 4)
		b2 = int(len(object) + len(object) / 4)
		# diff of the original text and the given text
		length = abs(len(container)- dist)
		if b1 < length and length < b2:
			return True
	else:
		# load the big engine...
		dist = ld(object, container)
		# espilon ~ len(object) / (len(object) + 1)
		b1 = int(len(object) - len(object) / (len(object) + 1))
		b2 = int(len(object) + len(object) / (len(object) + 1))
		# diff of the original text and the given text
		length = abs(len(container)- dist)
		if b1 < length and length < b2:
			return True
	return False


def load_definition(fileName):
	"""
		Load the XML of definition
	"""
	global attack_list
	attack_list = {}
	parser = make_parser()
	xss_handler = AttackHandler()
	# Tell the parser to use our handler
	parser.setContentHandler(xss_handler)
	parser.parse(fileName)


def	setDatabase(localDatabase):
	global database
	database = {}
	database = localDatabase


def investigate(url, what = "xss"):
	global attack_list
	"""
		Cross-Site Scripting Checking
		Injection
		Blind Injection
	"""
	localDB = None
	if what == "xss":
		from xss import process
		load_definition('xssAttacks.xml')
		localDB = database
	elif what == "sql":
		from sql import process
		load_definition('sqlAttacks.xml')
		localDB = database
	elif what == "bsql":
		from bsql import process
		load_definition('bsqlAttacks.xml')
		localDB = database
	elif what == "backup":
		from backup import process
		localDB = database
	elif what == "include":
		from files import process
		load_definition('filesAttacks.xml')
		localDB = database
	elif what == "javascript":
		from javascript import process
		localDB = database_js
	elif what == "crystal":
		from crystal import process
		localDB = database
	elif what == "session":
		if 'session' in confInfos:
			attack_list = confInfos['session']
			localDB = None
			from session import process
		else:
			raise AtrributeError("You need to give the session id storage key e.g. PHPSESSID, sid etc. ")

	process(url, localDB, attack_list)

	# look at teh cookies returned
	for index, cookie in enumerate(cj):
		print '[Cookie]\t', index, '\t:\t', cookie
	cj.save(COOKIEFILE)

# put a link
def active_link(s):
	pos = s.find('http://')
	if pos < 1:
		return s
	else:
		print pos, len(s), s[pos:len(s)]
		url = s[pos:len(s)]
		newStr = s[0:pos-1] + "<a href='" +url + "'>" + urllib.unquote(url) + "</a>"
		return newStr
	return s

def createStructure():
	try:
		os.mkdir("results")
	except OSError,e :
		a=0
	try:
		os.mkdir("local")
	except OSError,e :
		a=0
	try:
		os.mkdir("local/js")
	except OSError,e :
		a=0
	try:
		os.mkdir("local/css")
	except OSError,e :
		a=0

if __name__ == '__main__':
	option_url = ""
	option_sql = False
	option_bsql = False
	option_xss = False
	option_backup = False
	option_include = False
	option_spider = False
	option_js = False
	option_crystal = False
	option_session = False

	if len(sys.argv) > 1:
		parser = OptionParser()
		parser.add_option("-u", "--url", dest="archives_url", help="Adress to investigate")
		parser.add_option("-s", "--sql", dest="sql", action="store_true",default=False, help="Look for the SQL Injection")
		parser.add_option("-x", "--xss", dest="xss", action="store_true",default=False, help="Perform XSS attacks")
		parser.add_option("-b", "--bsql", dest="bsql", action="store_true",default=False, help="Look for blind SQL Injection")
		parser.add_option("-z", "--backup", dest="backup", action="store_true",default=False, help="Look for backup files")
		parser.add_option("-d", "--spider", dest="spider", help="Look for every files")
		parser.add_option("-i", "--include", dest="include", action="store_true",default=False, help="Perform File Insertion attacks")
		parser.add_option("-j", "--javascript", dest="javascript", action="store_true",default=False, help="Test the javascript code ?")
		parser.add_option("-c", "--crystal", dest="crystal", action="store_true",default=False, help="Simple crystal ball test.")
		parser.add_option("-e", "--session", dest="session", action="store_true",default=False, help="Session evaluations")

		(options, args) = parser.parse_args()

		option_url = options.archives_url
		option_sql = options.sql
		option_bsql = options.bsql
		option_xss = options.xss
		option_backup = options.backup
		option_include = options.include
		option_spider = options.spider
		option_js = options.javascript
		option_crystal = options.crystal
		option_session = options.session
	else:
		try:
			f = open("grabber.conf.xml", 'r')
		except IOError:
			print "No arguments ? You need to setup the XML configuration file or using the inline arguments"
			print "Look at the doc to start..."
			sys.exit(1)
		parser = make_parser()
		conf_handler = ConfHandler()
		# Tell the parser to use our handler
		parser.setContentHandler(conf_handler)
		parser.parse("grabber.conf.xml")

		option_url    = confUrl
		option_spider = confSpider
		option_sql    = "sql" in confActions
		option_bsql   = "bsql" in confActions
		option_xss    = "xss" in confActions
		option_backup = "backup" in confActions
		option_include= "include" in confActions
		option_js     = "javascript" in confActions
		option_crystal= "crystal" in confActions
		option_session= "session" in confActions

	# default to localhost ?
	archives_url = "http://localhost"
	if option_url:
		archives_url = option_url
	root = archives_url

	createStructure()
	depth = 1
	try:
		depth = int(option_spider.strip().split()[0])
	except (ValueError, IndexError,AttributeError):
		depth = 0

	try:
		try:
			spider(archives_url, depth)
		except IOError,e :
			print "Cannot open the url = %s" % archives_url
			print e.strerror
			sys.exit(1)
		if len(database.keys()) < 1:
			print "No information found!"
			sys.exit(1)
		else:
			print "Start investigation..."

		if option_sql:
			investigate(archives_url, "sql")
		if option_xss:
			investigate(archives_url)
		if option_bsql:
			investigate(archives_url,"bsql")
		if option_backup:
			investigate(archives_url, "backup")
		if option_include:
			investigate(archives_url, "include")
		if option_js:
			investigate(archives_url, "javascript")
		if option_crystal:
			investigate(archives_url, "crystal")
		if option_session:
			investigate(archives_url, "session")
	except KeyboardInterrupt:
		print "Plouf!"




















