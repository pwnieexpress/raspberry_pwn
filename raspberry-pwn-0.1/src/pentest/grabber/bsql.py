#!/usr/bin/env python
"""
	Blind SQL Module for Grabber v0.1
	Copyright (C) 2006 - Romain Gaucher - http://rgaucher.info
"""
import sys
from grabber import getContent_POST, getContent_GET
from grabber import getContentDirectURL_GET, getContentDirectURL_POST
from grabber import single_urlencode

# order of the Blind SQL operations
orderBSQL = {'AND' : 'TEST', 'TEST' : ['OR','COMMENT','ESCAPE','EVASION']}


overflowStr = "" 
for k in range(0,512):
	overflowStr += '9'

def detect_sql(output, ):
	listWords = ["SQL","MySQL","sql","mysql"]
	for wrd in listWords:
		if output.count(wrd) > 0:
			return True
	return False

def equal(h1,h2):
	if h1 == h2:
		return True
	return False

def generateOutput(url, gParam, instance,method,type):
	astr = "<bsql>\n\t<method>%s</method>\n\t<url>%s</url>\n\t<parameter name='%s'>%s</parameter>\n\t<type name='Blind SQL Injection Type'>%s</type>"  % (method,url,gParam,str(instance),type)
	if method in ("get","GET"):
		# print the real URL
		p = (url+"?"+gParam+"="+single_urlencode(str(instance)))
		astr += "\n\t<result>%s</result>" % p
	astr += "\n</bsql>\n"
	return astr

def generateOutputLong(url, urlString ,method,type, allParams = {}):
	astr = "<bsql>\n\t<method>%s</method>\n\t<url>%s</url>\n\t<type name='Blind SQL Injection Type'>%s</type>"  % (method,url,type)
	if method in ("get","GET"):
		# print the real URL
		p = (url+"?"+urlString)
		astr += "\n\t<result>%s</result>" % (p)
	else:
		astr += "\n\t<parameters>"
		for k in allParams:
			astr += "\n\t\t<parameter name='%s'>%s</parameter>" % (k, allParams[k])
		astr += "\n\t</parameters>"
	astr += "\n</bsql>\n"
	return astr

def permutations(L):
	if len(L) == 1:
		yield [L[0]]
	elif len(L) >= 2:
		(a, b) = (L[0:1], L[1:])
		for p in permutations(b):
			for i in range(len(p)+1):
				yield b[:i] + a + b[i:]


def process(url, database, attack_list):
	plop = open('results/bsql_GrabberAttacks.xml','w')
	plop.write("<bsqlAttacks>\n")

	for u in database.keys():
		if len(database[u]['GET']):
			print "Method = GET ", u
			# single parameter testing
			for gParam in database[u]['GET']:
				defaultValue = database[u]['GET'][gParam]
				defaultReturn = getContent_GET(u,gParam,defaultValue)
				if defaultReturn == None:
					continue
				# get the AND statments
				for andSQL in attack_list['AND']:
					tmpError = getContent_GET(u,gParam,andSQL)
					if tmpError == None:
						continue
					if equal(defaultReturn.read(), tmpError.read()):
						# dive here :)
						basicError  = getContent_GET(u,gParam,'')
						overflowErS = getContent_GET(u,gParam,overflowStr)
						if basicError == None or overflowErS == None:
							continue
						if equal(basicError.read(), overflowErS.read()):
							for key in orderBSQL[orderBSQL['AND']]:
								for instance in attack_list[key]:
									tmpError  = getContent_GET(u,gParam,instance)
									if tmpError == None:
										continue
									if equal(basicError.read(), tmpError.read()):
										# should be an error
										# print u,gParam,instance
										plop.write(generateOutput(u,gParam,instance,"GET",key))
						else:
							# report a overflow possible error
							#print u,gParam, "overflow"
							plop.write(generateOutput(u,gParam,"99999...99999","GET","Overflow"))
			"""
			# see the permutations
			if len(database[u]['GET'].keys()) > 1:
				for typeOfInjection in attack_list:
					for instance in attack_list[typeOfInjection]:
						url = ""
						for gParam in database[u]['GET']:
							url += ("%s=%s&" % (gParam, single_urlencode(str(instance))))
						handle = getContentDirectURL_GET(u,url)
						if handle != None:
							output = handle.read()
							if detect_sql(output):
								# generate the info...
								plop.write(generateOutputLong(u,url,"GET",typeOfInjection))
			"""
		if len(database[u]['POST']):
			print "Method = POST ", u
			# single parameter testing
			for gParam in database[u]['POST']:
				defaultValue = database[u]['POST'][gParam]
				defaultReturn = getContent_POST(u,gParam,defaultValue)
				if defaultReturn == None:
					continue
				# get the AND statments
				for andSQL in attack_list['AND']:
					tmpError = getContent_POST(u,gParam,andSQL)
					if tmpError == None:
						continue
					if equal(defaultReturn.read(), tmpError.read()):
						# dive here :)
						basicError  = getContent_POST(u,gParam,'')
						overflowErS = getContent_POST(u,gParam,overflowStr)
						if basicError == None or overflowErS == None:
							continue
						if equal(basicError.read(), overflowErS.read()):
							for key in orderBSQL[orderBSQL['AND']]:
								for instance in attack_list[key]:
									tmpError  = getContent_POST(u,gParam,instance)
									if tmpError == None:
										continue
									if equal(basicError.read(), tmpError.read()):
										# should be an error
										plop.write(generateOutput(u,gParam,instance,"POST",key))
						else:
							# report a overflow possible error
							plop.write(generateOutput(u,gParam,"99999...99999","POST","Overflow"))
	plop.write("\n</bsqlAttacks>\n")
	plop.close()
	return ""
