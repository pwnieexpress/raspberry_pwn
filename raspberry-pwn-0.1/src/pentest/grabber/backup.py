#!/usr/bin/env python
"""
	Backup Files Module for Grabber v0.1
	Copyright (C) 2006 - Romain Gaucher - http://rgaucher.info
"""
import sys
from grabber import getContentDirectURL_GET
from spider  import allowed

# list of possible add-in extension
ext = [".bak",".old",".",".txt",".inc",".zip",".tar"]

def generateOutput(url):
	astr = "\n\t<backup>%s"  % (url)
	astr += "</backup>"
	return astr

def allowed_inUrl(u):
	for a in allowed:
		if u.count('.'+a) > 0:
			return True
	return False

def process(url, database, attack_list):
	plop = open('results/backup_GrabberAttacks.xml','w')
	plop.write("<backupFiles>\n")
	for u in database.keys():
		if allowed_inUrl(u):
			for e in ext:
				url1 = u + e
				url2 = u + e.upper()
				try:
					if len(getContentDirectURL_GET(url1,'').read()) > 0:
						plop.write(generateOutput(url1))
					if len(getContentDirectURL_GET(url2,'').read()) > 0:
						plop.write(generateOutput(url2))
				except AttributeError:
					continue
	plop.write("\n</backupFiles>")
	plop.close()
	return ""
