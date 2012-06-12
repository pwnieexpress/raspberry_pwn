#!/usr/bin/env python
"""
	Session Analyzer Module for Grabber v0.1
	Copyright (C) 2006 - Romain Gaucher - http://rgaucher.info
"""
import sys,re,time,datetime
from grabber import getContentDirectURL_GET
sessions = {}


def normalize_whitespace(text):
	return ' '.join(text.split())


def getDirectSessionID(currentURL, sid):
	k = currentURL.find(sid)
	if k > 0:
		return currentURL[k+10:]
	return None

def stripNoneASCII(output):
	# should be somepthing to do that.. :/
	newOutput = ""
	for s in output:
		try:
			s = s.encode()
			newOutput += s
		except UnicodeDecodeError:
			continue
	return newOutput

regDate = re.compile(r'^Date: (.*)$', re.I)

def lookAtSessionID(url, sidName, regSession):
	global sessions
	handle = getContentDirectURL_GET(url,"")
	if handle != None:
		output = handle.read()
		header = str(handle.info()).split('\n')
		for h in header:
			# extract date header information
			if regDate.match(h):
				out = regDate.search(h)
				date = out.group(1)
				# convert this date into the good GMT number
				# ie time in seconds since 01/01/1970 00:00:00
				gi = time.strptime(normalize_whitespace(date.replace('GMT','')), "%a, %d %b %Y %H:%M:%S")
				gi = time.mktime(gi) - time.mktime(time.gmtime(0))

		output = output.replace('\n','')
		output = output.replace('\t','')
		# print output[790:821]
		output = stripNoneASCII(output)
		if output.find(sidName) > 0:
			if regSession.match(output):
				out = regSession.search(output)
				ssn = out.group(2)
				if ssn != None:
					if gi != None:
						sessions[ssn] = gi
					else:
						sessions[ssn] = ''

def process(url, database, sidName):
	regString  = "(.*)" + sidName + "=([a-z|A-Z|0-9]+)(.*)"
	regSession = re.compile(regString,re.I)
	print url, sidName, regString
	for k in range(0,1000):
		lookAtSessionID(url, sidName, regSession)
	o = open('results/sessions.txt','w')
	for s in sessions:
		o.write("%s, %s\n" % (s, sessions[s]))
	o.close()
