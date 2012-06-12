#!/usr/bin/env python
"""
	Simple JavaScript Checker Module for Grabber v0.1
	Copyright (C) 2006 - Romain Gaucher - http://rgaucher.info
	
	- Look at the JavaScript Source... 

"""
import sys, re, os
from spider  import htmlencode
from xml.sax import *   # Need PyXML [http://pyxml.sourceforge.net/]

# JavaScript Configuration variables
jsAnalyzerBin= None
jsAnalyzerInputParam = None
jsAnalyzerOutputParam = None
jsAnalyzerConfParam = None
jsAnalyzerConfFile= None
jsAnalyzerExtension = None
jsAnalyzerPattern = None

# { 'FILENAME' : { 'line' : ['error 1', 'error 2']  } }
jsDatabase = {}

"""
<?xml version="1.0"?>
<!-- JavaScript Source Code Analyzer configuration file -->
<javascript version="0.1">
	<!--
		Analyzer information, here JavaScript Lint by Matthias Miller
		http://www.JavaScriptLint.com
	-->
	<analyzer>
		<path input="-process" output="">C:\server\jsl-0.3.0\jsl.exe</path>
		<configuration param="-conf">C:\server\jsl-0.3.0\jsl.grabber.conf</configuration>
		<extension>js</extension>
	</analyzer>
</javascript>
"""

def normalize_whitespace(text):
	return ' '.join(text.split())

def clear_whitespace(text):
	return text.replace(' ','')

# Handle the XML file with a SAX Parser
class JavaScriptConfHandler(ContentHandler):
	def __init__(self):
		self.inAnalyzer  = False
		self.string      = ""

	def startElement(self, name, attrs):
		global jsAnalyzerInputParam, jsAnalyzerOutputParam, jsAnalyzerConfParam
		self.string = ""
		self.currentKeys = []
		if name == 'analyzer':
			self.inAnalyzer = True
		elif name == 'path' and self.inAnalyzer:
			# store the attributes input and output
			if 'input' in attrs.keys() and 'output' in attrs.keys():
				jsAnalyzerInputParam  = attrs.getValue('input')
				jsAnalyzerOutputParam = attrs.getValue('output')
			else:
				raise KeyError("JavaScriptXMLConf: <path> needs 'input' and 'output' attributes")
		elif name == 'configuration' and self.inAnalyzer:
			# store the attribute 'param'
			if 'param' in attrs.keys():
				jsAnalyzerConfParam  = attrs.getValue('param')
			else:
				raise KeyError("JavaScriptXMLConf: <configuration> needs 'param' attribute")

	def characters(self, ch):
		self.string = self.string + ch

	def endElement(self, name):
		global jsAnalyzerBin, jsAnalyzerConfFile, jsAnalyzerExtension,jsAnalyzerPattern
		if name == 'configuration':
			jsAnalyzerConfFile = normalize_whitespace(self.string)
		elif name == 'extension' and self.inAnalyzer:
			jsAnalyzerExtension = normalize_whitespace(self.string)
		elif name == 'path' and self.inAnalyzer:
			jsAnalyzerBin = normalize_whitespace(self.string)
		elif name == "analyzer":
			self.inAnalyzer = False
		elif name == "pattern":
			jsAnalyzerPattern = normalize_whitespace(self.string)

def execCmd(program, args):
	buff = []
	p = os.popen(program + " " + args)
	buff = p.readlines()
	p.close()
	return buff


def generateListOfFiles(localDB, urlGlobal):
	global jsDatabase
	"""
		Create a ghost in ./local/crystal/current and /local/crystal/analyzed
		And run the SwA tool
	"""
	regScripts = re.compile(r'(.*).' + jsAnalyzerExtension + '$', re.I)
	# escape () and []
	localRegOutput = jsAnalyzerPattern
	localRegOutput = localRegOutput.replace('(', '\(')
	localRegOutput = localRegOutput.replace(')', '\)')
	localRegOutput = localRegOutput.replace('[', '\[')
	localRegOutput = localRegOutput.replace(']', '\]')
	localRegOutput = localRegOutput.replace(':', '\:')
	localRegOutput = localRegOutput.replace('__LINE__', '(\d+)')
	localRegOutput = localRegOutput.replace('__FILENAME__', '(.+)')
	localRegOutput = localRegOutput.replace('__ERROR__', '(.+)')
	regOutput = re.compile('^'+localRegOutput+'$', re.I)
	
	print "Running the static analysis tool..."
	for file in localDB:
		print file
		file = file.replace(urlGlobal + '/', '')
		fileIn  = os.path.abspath(os.path.join('./local', file))
		cmdLine = jsAnalyzerConfParam + " " +jsAnalyzerConfFile + " " + jsAnalyzerInputParam + " " + fileIn
		if jsAnalyzerOutputParam != "":
			cmdLine += " " + jsAnalyzerOutputParam + " " + fileIn+'.jslint'
		output  = execCmd(jsAnalyzerBin, cmdLine)
		# Analyze the output
		for o in output:
			lO = o.replace('\n','')
			if regOutput.match(lO):
				out = regOutput.search(lO)
				if file not in jsDatabase:
					jsDatabase[file] = {}
				line = clear_whitespace(out.group(2))
				if line not in jsDatabase[file]:
					jsDatabase[file][line] = []
				jsDatabase[file][line].append(normalize_whitespace(out.group(3)))
	# sort the dictionary
	# + file
	#   + lines


def process(urlGlobal, localDB, attack_list):
	"""
		Crystal Module entry point
	"""
	print "JavaScript Module Start"
	try:
		f = open("javascript.conf.xml", 'r')
		f.close()
	except IOError:
		print "The javascript module needs the 'javascript.conf.xml' configuration file."
		sys.exit(1)
	parser = make_parser()
	js_handler = JavaScriptConfHandler()
	# Tell the parser to use our handler
	parser.setContentHandler(js_handler)
	try:
		parser.parse("javascript.conf.xml")
	except KeyError, e:
		print e
		sys.exit(1)

	# only a white box testing...
	generateListOfFiles(localDB,urlGlobal)
	# create the report
	plop = open('results/javascript_Grabber.xml','w')
	plop.write("<javascript>\n")
	plop.write("<site>\n")
	for file in jsDatabase:
		plop.write("\t<file name='%s'>\n" % file)
		for line in jsDatabase[file]:
			if len(jsDatabase[file][line]) > 1:
				plop.write("\t\t<line number='%s'>\n" % line)
				for error in jsDatabase[file][line]:
					plop.write("\t\t\t<error>%s</error>\n" % htmlencode(error))
				plop.write("\t\t</line>\n")
			else:
				plop.write("\t\t<line number='%s'>%s</line>\n" % (line, htmlencode(jsDatabase[file][line][0])))
		plop.write("\t</file>\n")
	plop.write("</site>\n")
	plop.write("</javascript>\n")
	plop.close()

