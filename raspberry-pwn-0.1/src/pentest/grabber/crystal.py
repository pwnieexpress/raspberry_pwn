#!/usr/bin/env python
"""
	Crystal Module for Grabber v0.1
	Copyright (C) 2006 - Romain Gaucher - http://rgaucher.info
"""
import sys,os,re, string, shutil
from xml.sax import *   # Need PyXML [http://pyxml.sourceforge.net/]
from grabber import getContent_POST, getContentDirectURL_POST
from grabber import getContent_GET , getContentDirectURL_GET
from grabber import single_urlencode, partially_in, unescape
from grabber import investigate, setDatabase
from spider  import flatten, htmlencode, dict_add
from spider  import database


vulnToDescritiveNames = {
	'xss' : 'Cross-Site Scripting',
	'sql' : 'SQL Injection',
	'bsql': 'Specific Blind Injection...',
	'include' : 'PHP Include Vulnerability'
}


"""
	Crystal Module Cooking Book
	---------------------------

	Make-ahead Tip: Prepare lots of coffee before starting...
	Preparation: 24 hours
	Ingredients:
		A: PHP-Sat
		B: Grabber Modules lambda
	Tools:
		A: Context editor
		B: Python 2.4
		C: Nice music (Opera is not needed but you should listen this)

	Directions:
		0) Read the configuration file (with boolean operator in patterns)
		1) Scan the PHP sources with PHP-Sat handler (which copy everything in the
		'/local/crystal/' directory).
		2) Make a kind of diff then:
			If the diff results, check for the patterns (given in the configuration file)
				Parse the PHP line under the end of the pattern
				Try to get a variable value
				<after>
					If no direct variable... backtrack sequentially or in the AST
				</after>
		3) Generate the XML report of "the crystal-static-analysis" module
		4) Build a database of:
			>>> transformed_into_URL(hypothetical flawed files) : {list of "flawed" params}
		5) Run the classical tools
"""

# Crystal Configuration variables
crystalFiles      = None
crystalUrl        = None
crystalExtension  = None

crystalAnalyzerBin= None
crystalAnalyzerInputParam = None
crystalAnalyzerOutputParam = None

crystalCheckStart = None
crystalCheckEnd   = None
# example: {'xss' : ['pattern_1 __AND__ pattern_3','pattern_2'], 'sql' : ['pattern_3'], 'bsql' : ['pattern_3']}
crystalPatterns   = {}
# example: {'xss' : [{'var-position' : reg1}], 'sql' : [{'var-position' : reg2}]}
crystalRegExpPatterns = {}
crystalStorage    = []
crystalDatabase   = {}
crystalFinalStorage = {}


def normalize_whitespace(text):
	return ' '.join(text.split())

def clear_whitespace(text):
	return text.replace(' ','')

# Handle the XML file with a SAX Parser
class CrystalConfHandler(ContentHandler):
	def __init__(self):
		self.inAnalyzer  = False
		self.inPatterns  = False
		self.inPattern   = False
		self.isRegExp    = False
		self.curretVarPos= None
		self.currentKeys = []
		self.string     = ""
	def startElement(self, name, attrs):
		global crystalAnalyzerInputParam, crystalAnalyzerOutputParam, crystalPatterns, crystalCheckStart, crystalCheckEnd
		self.string = ""
		self.currentKeys = []
		if name == 'analyzer':
			self.inAnalyzer = True
		elif name == 'path' and self.inAnalyzer:
			# store the attributes input and output
			if 'input' in attrs.keys() and 'output' in attrs.keys():
				crystalAnalyzerInputParam  = attrs.getValue('input')
				crystalAnalyzerOutputParam = attrs.getValue('output')
			else:
				raise KeyError("CrystalXMLConf: <path> needs 'input' and 'output' attributes")
		elif name == 'patterns' and self.inAnalyzer:
			self.inPatterns = True
			if 'start' in attrs.keys() and 'end' in attrs.keys():
				crystalCheckStart = attrs.getValue('start')
				crystalCheckEnd   = attrs.getValue('end')
			else:
				raise KeyError("CrystalXMLConf: <patterns> needs 'start' and 'end' attributes")
			if 'name' in attrs.keys():
				if attrs.getValue('name').lower() == 'regexp':
					self.isRegExp = True

		elif self.inPatterns and name == 'pattern':
			self.inPattern = True
			if 'module' in attrs.keys():
				modules = attrs.getValue('module')
				modules.replace(' ','')
				self.currentKeys = modules.split(',')
				if self.isRegExp:
					if 'varposition' in attrs.keys():
						curretVarPos = attrs.getValue('varposition')
			else:
				raise KeyError("CrystalXMLConf: <pattern > needs 'varposition' attribute")

	def characters(self, ch):
		self.string = self.string + ch

	def endElement(self, name):
		global crystalFiles, crystalUrl, crystalExtension, crystalAnalyzerBin, crystalPatterns, crystalRegExpPatterns
		if name == 'files':
			crystalFiles = normalize_whitespace(self.string)
		elif name == 'url':
			crystalUrl = normalize_whitespace(self.string)
		elif name == 'extension' and self.inAnalyzer:
			crystalExtension = normalize_whitespace(self.string)
		elif name == 'path' and self.inAnalyzer:
			crystalAnalyzerBin = normalize_whitespace(self.string)
		elif not self.isRegExp and name == 'pattern' and self.inPattern:
			tempList = self.string.split('__OR__')
			for a in self.currentKeys:
				if a not in crystalPatterns:
					crystalPatterns[a] = []
				l = crystalPatterns[a]
				for t in tempList:
					l.append(normalize_whitespace(t))
		elif self.isRegExp and name == 'pattern' and self.inPattern:
			"""
			tempList = self.string.split('__OR__')
			for a in self.currentKeys:
				if a not in crystalPatterns:
					crystalRegExpPatterns[a] = []
				l = crystalRegExpPatterns[a]
				# build the compiled regexp
				plop = normalize_whitespace(l)
				plop = re.compile(plop, re.I)
				l.append({currentVarPos : plop})
			"""
		elif name == "patterns" and self.inPatterns:
			self.inPatterns = False
			if self.isRegExp:
				self.isRegExp = False
		elif name == "analyzer" and self.inAnalyzer:
			self.inAnalyzer = False

def copySubTree(src, dst, regFilter):
	global crystalStorage
	names = os.listdir(src)
	try:
		os.mkdir(dst)
	except OSError:
		a = 0
	try:
		os.mkdir(dst.replace('crystal/current', 'crystal/analyzed'))
	except OSError:
		a = 0
	for name in names:
		srcname = os.path.join(src, name)
		dstname = os.path.join(dst, name)
		try:
			if os.path.islink(srcname):
				linkto = os.readlink(srcname)
				os.symlink(linkto, dstname)
			elif os.path.isdir(srcname):
				copySubTree(srcname, dstname, regFilter)
			elif regFilter.match(srcname):
				shutil.copy2(srcname, dstname)
				crystalStorage.append(dstname)
		except (IOError, os.error), why:
			continue

def execCmd(program, args):
	p = os.popen(program + " " + args)
	p.close()


def generateListOfFiles():
	"""
		Create a ghost in ./local/crystal/current and /local/crystal/analyzed
		And run the SwA tool
	"""
	regScripts = re.compile(r'(.*).' + crystalExtension + '$', re.I)
	copySubTree(crystalFiles, 'local/crystal/current', regScripts)
	print "Running the static analysis tool..."
	for file in crystalStorage:
		fileIn  = os.path.abspath(os.path.join('./', file))
		fileOut = os.path.abspath(os.path.join('./', file.replace('current', 'analyzed')))
		cmdLine = crystalAnalyzerInputParam + " " + fileIn + " " + crystalAnalyzerOutputParam + " " + fileOut
		# execCmd(crystalAnalyzerBin, cmdLine)
		print crystalAnalyzerBin,cmdLine
		os.system(crystalAnalyzerBin +" "+ cmdLine)

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

def isPatternInFile(fileName):
	global crystalDatabase
	file = None
	try:
		file = open(fileName, 'r')
	except IOError:
		print "Crystal: Cannot open the file [%s]" % fileName
		return False
	inZone, inLined = False, False
	detectPattern = False
	lineNumber = 0
	shortName  = fileName[fileName.rfind('analyzed') + 9 : ]
	vulnName = ""
	for l in file.readlines():
		lineNumber += 1
		l = l.replace('\n','')
		try:
			"""
				Check for the regular expression patterns
			if len(crystalRegExpPatterns) > 0:
				for modules in crystalRegExpPatterns:
					for regexp in crystalRegExpPatterns[modules]:
						if regexp.match()
			"""
			if len(vulnName) > 0 and (detectPattern and not inZone or inLined):
				# creating the nice structure
				# { 'index.php' : {'xss' : {'12', 'echo $_GET["plop"]'}}}
				if shortName not in crystalDatabase:
					crystalDatabase[shortName] = {}
				if vulnName not in crystalDatabase[shortName]:
					crystalDatabase[shortName][vulnName] = {}
				if str(lineNumber) not in crystalDatabase[shortName][vulnName]:
					crystalDatabase[shortName][vulnName][str(lineNumber)] = l
				detectPattern = False
				inLined = False
				vulnName = ""
	
			if l.count(crystalCheckStart) > 0 and not inZone:
				b1 = l.find(crystalCheckStart)
				inZone = True
				# same line for start and end ?
				if l.count(crystalCheckEnd) > 0:
					b2 = l.find(crystalCheckStart)
					if b1 < b2:
						inZone = False
						position = l.lower().find(pattern.lower())
						if b1 < position and position < b2:
							detectPattern = True
							inLined = True
			elif inZone:
				# is there any pattern around the corner ?
				for modules in crystalPatterns:
					for p in crystalPatterns[modules]:
						p = p.lower()
						l = l.lower()
						# The folowing code is stupid!
						# I have to change the algorithm for the __AND__ parsing...
						if '__AND__' in p:
							listPatterns = p.split('__AND__')
							isIn = True
							for patton in listPatterns:
								if patton not in l:
									isIn = isIn and False
							if isIn:
								detectPattern = True
								vulnName = modules
							a=0
						else:
							# test if the simple pattern is in the line
							if p in l:
								detectPattern = True
								vulnName = modules
				if l.count(crystalCheckEnd) > 0:
					inZone = False
		except UnicodeDecodeError:
			continue
	return True

def buildDatabase():
	"""
		Read the analzed files (indirectly with the crystalStorage.replace('current','analyzed') )
		And look for the patterns
	"""
	listOut = []
	for file in crystalStorage:
		fileOut = os.path.abspath(os.path.join('./', file.replace('current', 'analyzed')))
		if not isPatternInFile(fileOut):
			print "Error with the file [%s]" % file

def createStructure():
	"""
		Create the structure in the ./local directory
	"""
	try:
		os.mkdir("local/crystal/")
	except OSError,e :
		a=0
	try:
		os.mkdir("local/crystal/current")
	except OSError,e :
		a=0
	try:
		os.mkdir("local/crystal/analyzed")
	except OSError,e :
		a=0

"""
def realLineNumberReverse(fileName, codeStr):
	print fileName, codeStr
	try:
		fN = os.path.abspath(os.path.join('./local/crystal/current/', fileName))
		file = open(fN, 'r')
		lineNumber = 0
		for a in file.readlines():
			lineNumber += 1
			if codeStr in a:
				print a
				file.close()
				return lineNumber
		file.close()
	except IOError,e:
		print e
		return 0
	return 0
"""

def generateReport_1():
	"""
		Create a first report like:

		* Developer report:
			# using XSLT...
			<site>
				<file name="index.php">
					<vulnerability line="9">xss</vulnerability>
					<vulnerability line="25">sql</vulnerability>
				</file>
				...
			</site>
		
		* Security report:
			<site>
				<vulnerability name="xss">
					<file name="index.php" line="9" />
					...
				</vulnerabilty>
				<vulnerability name="sql">
					<file name="index.php" line="25" />
				</vulnerabilty>
			</site>
	"""
	plop = open('results/crystal_SecurityReport_Grabber.xml','w')
	plop.write("<crystal>\n")
	plop.write("<site>\n")
	plop.write("<!-- The line numbers are from the files in the 'analyzed' directory -->\n")
	for file in crystalDatabase:
		plop.write("\t<file name='%s'>\n" % file)
		for vuln in crystalDatabase[file]:
			for line in crystalDatabase[file][vuln]:
				# lineNumber = realLineNumberReverse(file,crystalDatabase[file][vuln][line])
				localVuln = vuln
				if localVuln in vulnToDescritiveNames:
					localVuln = vulnToDescritiveNames[localVuln]
				plop.write("\t\t<vulnerability name='%s' line='%s' >%s</vulnerability>\n" % (localVuln, line, htmlencode(crystalDatabase[file][vuln][line])))
		plop.write("\t</file>\n")
	plop.write("</site>\n")
	plop.write("</crystal>\n")
	plop.close()


def buildUrlKey(file):
	fileName = file.replace('\\','/') # on windows...
	keyUrl = crystalUrl
	if keyUrl[len(keyUrl)-1] != '/' and fileName[0] != '/':
		keyUrl += '/'
	keyUrl += fileName
	return keyUrl


reParamPOST = re.compile(r'(.*)\$_POST\[(.+)\](.*)',re.I)
reParamGET  = re.compile(r'(.*)\$_GET\[(.+)\](.*)' ,re.I)

def getSimpleParamFromCode_GET(code):
	"""
		Using the regular expression above, try to get some parameters name
	"""
	params = [] # we can have multiple params...
	code = code.replace("'",'');
	code = code.replace('"','');
	if code.lower().count('get') > 0:
		# try to match the $_GET
		if reParamGET.match(code):
			out = reParamGET.search(code)
			params.append(out.group(2))
			params.append(getSimpleParamFromCode_GET(out.group(3)))
			params = flatten(params)
	return params


def getSimpleParamFromCode_POST(code):
	"""
		Using the regular expression above, try to get some parameters name
	"""
	params = [] # we can have multiple params...
	code = code.replace("'",'');
	code = code.replace('"','');
	if code.lower().count('post') > 0:
		# try to match the $_GET
		if reParamPOST.match(code):
			out = reParamPOST.search(code)
			params.append(out.group(2))
			params.append(getSimpleParamFromCode_POST(out.group(3)))
			params = flatten(params)
	return params


def createClassicalDatabase(vulnsType, localCrystalDB):
	"""
		From the crystalDatabase, generate the same database as in Spider
		This is generated for calling the differents modules

		ClassicalDB = { url : { 'GET' : { param : value } } }
	"""
	classicalDB = {}
	for file in localCrystalDB:
		# build the URL
		keyUrl = buildUrlKey(file)
		if keyUrl not in classicalDB:
			classicalDB[keyUrl] = {'GET' : {}, 'POST' : {}}
		for vuln in localCrystalDB[file]:
			# only get the kind of vulnerability we want
			if vuln != vulnsType:
				continue
			for line in localCrystalDB[file][vuln]:
				code = localCrystalDB[file][vuln][line]
				# try to extract some data...
				params_GET  = getSimpleParamFromCode_GET (code)
				params_POST = getSimpleParamFromCode_POST(code)
				if len(params_GET) > 0:
					for p in params_GET:
						lG = classicalDB[keyUrl]['GET']
						if p not in classicalDB[keyUrl]['GET']:
							lG = dict_add(lG,{p:''})
						classicalDB[keyUrl]['GET'] = lG
				if len(params_POST) > 0:
					for p in params_POST:
						lP = classicalDB[keyUrl]['POST']
						if p not in classicalDB[keyUrl]['POST']:
							lP = dict_add(lP,{p:''})
						classicalDB[keyUrl]['POST'] = lP
	return classicalDB


def retrieveVulnList():
	vulnList = []
	for file in crystalDatabase:
		for vuln in crystalDatabase[file]:
			if vuln not in vulnList:
				vulnList.append(vuln)
	return vulnList


def process(urlGlobal, localDB, attack_list):
	"""
		Crystal Module entry point
	"""
	print "Crystal Module Start"
	try:
		f = open("crystal.conf.xml", 'r')
		f.close()
	except IOError:
		print "The crystal module needs the 'crystal.conf.xml' configuration file."
		sys.exit(1)
	parser = make_parser()
	crystal_handler = CrystalConfHandler()
	# Tell the parser to use our handler
	parser.setContentHandler(crystal_handler)
	try:
		parser.parse("crystal.conf.xml")
	except KeyError, e:
		print e
		sys.exit(1)

	#---------- White box testing
	
	createStructure()
	generateListOfFiles()

	buildDatabase()
	print "Build first report: List of vulneratilities and places in the code"
	generateReport_1()
	#---------- Start the Black Box testing

	# need to create a classical database like, so losing information
	# but for a type of vulnerability
	listVulns = retrieveVulnList()

	for vulns in listVulns:
		localDatabase = createClassicalDatabase(vulns, crystalDatabase)
		setDatabase(localDatabase)
		print "inProcess Crystal DB = ", localDatabase
		# print vulns, database
		# Call the Black Box Module
		print "Scan for ", vulns
		investigate(crystalUrl, vulns)

	print "Crystal Module Stop"

