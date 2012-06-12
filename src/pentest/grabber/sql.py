#!/usr/bin/env python
"""
	SQL Module for Grabber v0.1
	Copyright (C) 2006 - Romain Gaucher - http://rgaucher.info
"""
import sys
from grabber import getContent_POST, getContent_GET
from grabber import getContentDirectURL_GET, getContentDirectURL_POST
from grabber import single_urlencode


def detect_sql(output, url_get = "http://localhost/?param=false"):
	listWords = ["SQL syntax","valid MySQL","ODBC Microsoft Access Driver","java.sql.SQLException","XPathException","valid ldap","javax.naming.NameNotFoundException"]
	for wrd in listWords:
		if output.count(wrd) > 0:
			return True
	return False


def generateOutput(url, gParam, instance,method,type):
	astr = "<sql>\n\t<method>%s</method>\n\t<url>%s</url>\n\t<parameter name='%s'>%s</parameter>\n\t<type name='SQL Injection Type'>%s</type>"  % (method,url,gParam,str(instance),type)
	if method in ("get","GET"):
		# print the real URL
		p = (url+"?"+gParam+"="+single_urlencode(str(instance)))
		astr += "\n\t<result>%s</result>" % p
	astr += "\n</sql>\n"
	return astr


def generateOutputLong(url, urlString ,method,type, allParams = {}):
	astr = "<sql>\n\t<method>%s</method>\n\t<url>%s</url>\n\t<type name='SQL Injection Type'>%s</type>"  % (method,url,type)
	if method in ("get","GET"):
		# print the real URL
		p = (url+"?"+urlString)
		astr += "\n\t<result>%s</result>" % (p)
	else:
		astr += "\n\t<parameters>"
		for k in allParams:
			astr += "\n\t\t<parameter name='%s'>%s</parameter>" % (k, allParams[k])
		astr += "\n\t</parameters>"
	astr += "\n</sql>\n"
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
	plop = open('results/sql_GrabberAttacks.xml','w')
	plop.write("<sqlAttacks>\n")

	for u in database.keys():
		if len(database[u]['GET']):
			print "Method = GET ", u
			for gParam in database[u]['GET']:
				for typeOfInjection in attack_list:
					for instance in attack_list[typeOfInjection]:
						handle = getContent_GET(u,gParam,instance)
						if handle != None:
							output = handle.read()
							header = handle.info()
							if detect_sql(output):
								# generate the info...
								plop.write(generateOutput(u,gParam,instance,"GET",typeOfInjection))
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
		if len(database[u]['POST']):
			print "Method = POST ", u
			for gParam in database[u]['POST']:
				for typeOfInjection in attack_list:
					for instance in attack_list[typeOfInjection]:
						handle = getContent_POST(u,gParam,instance)
						if handle != None:
							output = handle.read()
							header = handle.info()
							if detect_sql(output):
								# generate the info...
								plop.write(generateOutput(u,gParam,instance,"POST",typeOfInjection))
			# see the permutations
			if len(database[u]['POST'].keys()) > 1:
				for typeOfInjection in attack_list:
					for instance in attack_list[typeOfInjection]:
						allParams = {}
						for gParam in database[u]['POST']:
							allParams[gParam] = str(instance)
						handle = getContentDirectURL_POST(u,allParams)
						if handle != None:
							output = handle.read()
							if detect_sql(output):
								# generate the info...
								plop.write(generateOutputLong(u,url,"POST",typeOfInjection, allParams))
	plop.write("\n</sqlAttacks>\n")
	plop.close()
	return ""
