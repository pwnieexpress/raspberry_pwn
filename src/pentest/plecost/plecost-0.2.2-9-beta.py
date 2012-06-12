#!/usr/bin/python
#
# Plecost: Wordpress finger printer tool.
#
# @url: http://iniqua.com/labs/
# 
# @author:Francisco J. Gomez aka ffranz (http://iniqua.com/)
# @author:Daniel Garcia Garcia aka (http://iniqua.com/ - http://securitytoolslist.com)
#
# Code is licensed under -- GPLv3, http://www.gnu.org/licenses/gpl.html -- 
#
# DISCLAIMER:
# 
# 

import urllib
import urlparse
import urllib2
import re
import sys
import getopt
import threading
import random
import time
import os
import shelve
import cPickle as pickle
from httplib import HTTPException
from urllib2 import Request, urlopen, URLError
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
from xgoogle.search import GoogleSearch, SearchError
from threading import Thread
#
# General variables
#
WPCurrent_URL = "http://wordpress.org/download/"
WPlug_URL = "http://wordpress.org/extend/plugins/browse/popular/page/"
CVE_LIST = []
MinSleepTime = 10
MaxSleepTime = 20
ttl_cvelist = 604800
NumChecks = -1
WhithCVE = False
OutPutFile = "output.txt"
InputPluginList = ""
PluginList = ""
DisplayHelp = False
TargetURL = ""
ColoredOutput = False
NumThreats = 2
CVE_file = "CVE.dat"
verbose = True
limitForSearch = 99999
help = '''
////////////////////////////////////////////
// ..................................DMI...
// .............................:MMMM......
// .........................$MMMMM:........
// .........M.....,M,=NMMMMMMMMD...........
// ........MMN...MMMMMMMMMMMM,.............
// .......MMMMMMMMMMMMMMMMM~...............
// .......MMMMMMMMMMMMMMM..................
// ....?MMMMMMMMMMMMMMMN$I.................
// .?.MMMMMMMMMMMMMMMMMMMMMM...............
// .MMMMMMMMMMMMMMN........................
// 7MMMMMMMMMMMMMON$.......................
// ZMMMMMMMMMMMMMMMMMM.......plecost.......
// .:MMMMMMMZ~7MMMMMMMMMO..................
// ....~+:.................................
//
// Plecost - Wordpress finger printer Tool (with threads support) 0.2.2-9-beta
//        
// Developed by:
//        Francisco Jesus Gomez aka (ffranz@iniqua.com)
//        Daniel Garcia Garcia (dani@iniqua.com)
// 
// Info: http://iniqua.com/labs/
// Bug report: plecost@iniqua.com
        '''
usage = '''        
Usage: %s [options] [ URL | [-l num] -G]\r\n

Google search options:
    -l num    : Limit number of results for each plugin in google.
    -G        : Google search mode
    
Options:
    -n        : Number of plugins to use (Default all - more than 7000).
    -c        : Check plugins only with CVE associated.
    -R file   : Reload plugin list. Use -n option to control the size (This take several minutes)
    -o file   : Output file. (Default "output.txt")
    -i file   : Input plugin list. (Need to start the program)
    -s time   : Min sleep time between two probes. Time in seconds. (Default 10)
    -M time   : Max sleep time between two probes. Time in seconds. (Default 20)
    -t num    : Number of threads. (Default 1)
    -h        : Display help. (More info: http://iniqua.com/labs/) 

Examples:

  * Reload first 5 plugins list:
    	plecost -R plugins.txt -n 5
  * Search vulnerable sites for first 5 plugins:
        plecost -n 5 -G -i plugins.txt
  * Search plugins with 20 threads, sleep time between 12 and 30 seconds for www.example.com:
        plecost -i plugin_list.txt -s 12 -M 30 -t 20 -o results.txt www.example.com        

        ''' % (sys.argv[0])


####################################################################################################################################################
#
#	Functions and classes
#
####################################################################################################################################################
#
# Class for search CVE
#
class CVE(object):
    '''
     CVE class to manage vulnerabiliti info.
    '''
    def __init__(self):
        '''
        Constructor
        '''

    def CVE_list(self, key_word):
        '''
         Create a object file. Content: CVE entries [Id,Description]. Search by keyword in wordpress.
        '''
        try:
		cve_file = file(CVE_file,"w")
	except IOError:
		print "No such file or directory"
	try:
		cve = urllib2.urlopen("http://cve.mitre.org/cgi-bin/cvekey.cgi?keyword="+key_word).read()
        except URLError:
		print ""
	
	cve_tree = BeautifulSoup(cve)
        count = 0
        for ana in cve_tree.findAll('a'):
                if ana.parent.name == 'td':
                        cve_link = ana["href"]
                        if cve_link.find("/cgi-bin/cvename.cgi?name=") != -1:
                                count += 1
                                try:
					page2 = urllib2.urlopen("http://cve.mitre.org" + cve_link).read()
                                except URLError:
					print ""
				soup2 = BeautifulSoup(page2)
                                for ana2 in soup2.findAll('th'):
                                        if ana2.text == "Description":
                                                CVE_LIST.append([cve_link.split('=')[1],ana2.findNext('td').text])
                                                pickle.dump([cve_link.split('=')[1],ana2.findNext('td').text],cve_file,2)
	cve_file.close()
    
    def CVE_loadlist(self):
	'''
	 Load data from CVE.dat file to CVE_list[]
	'''
	try:
		cve_file = file(CVE_file)
	except IOError:
		print "No such file or directory"
	
	while True:
		try:
			cve_entry = pickle.load(cve_file)
		except EOFError:
			break	
		CVE_LIST.append(cve_entry)
	cve_file.close()

    def CVE_search(self, plugin_name):
        '''
         Search into CVE list. Return CVE ID list
        '''
        CVE_search_list = []
        search = plugin_name
        for sublist in CVE_LIST:
                if sublist[1].lower().find(search.lower()) != -1:
                        CVE_search_list.append(sublist[0])
        return CVE_search_list

#
# Class for analyze a website
#
class Wordpress(Thread):
    '''
     Wordpress class. Handle info about plugins
    '''
    def __init__(self):
        self.all_run = []
        '''
        Constructor
        '''
    def pluginlist_generate(self):
        '''
         Create popular plugin list
        '''
        url_count = 1
        plugin_count = 0
	plugin_cve = CVE()
	if not os.path.isfile(CVE_file): 
		plugin_cve.CVE_list("wordpress")
	stats = os.stat(CVE_file)
	if int(time.time()) - int(stats[8]) > ttl_cvelist : 
		print ""
		print "- CVE file is too old. Reload now?[y/n]:",
		opt = sys.stdin.readline()
		if opt.strip() == "y":
			print ""
			print "- Really?[y/n]:",
			opt = sys.stdin.readline()
			if opt.strip() == "y":
				print ""
				print "- Reloading CVE list... by patient"
				plugin_cve.CVE_list("wordpress")
		else: 
			print "- Maybe later."
	plugin_cve.CVE_loadlist()
	try:
		wp_file = file(PluginList,"w")
	except IOError:
	        print ""
		print "[!] Error opening file: \"" + PluginList + "\""
		print ""
		sys.exit(-1)
	final_countdown = 1
	end = 0
	tmpCount = 0
        while True:
                try:
			wpage = urllib2.urlopen(WPlug_URL+"/"+str(url_count)+"/").read()
		except URLError:
                        print ""
                        print "[!] Web site of plugin is not accesible."
                        print ""
			sys.exit(-1)
		url_count += 1
                wpsoup = BeautifulSoup(wpage)
                if str(wpsoup).find('plugin-block') == -1:
			print "Wordpress plugin list end:"
			break
                for ana in wpsoup.findAll('a'):
                        plugin_url = ana["href"]
                        if plugin_url.find("wordpress.org/extend/plugins/") != -1 and plugin_url.find("popular") == -1 and plugin_url.find("tags") == -1 and plugin_url.find("google.com") == -1 and plugin_url.find(".php") == -1:
				plugin_count += 1
                                if (plugin_url.split('/')[5] != '' ):
					name = plugin_url.split('/')[5]
                                        if len(ana.findNext('li').contents) == 2: 
						version = ana.findNext('li').contents[1]
					if name != "tac":
						cves = plugin_cve.CVE_search(plugin_url.split('/')[5])
					cves_l = ""
					for l in cves:
						cve_a = l+";"
						cves_l = cves_l + cve_a
					if type(version) == unicode:
                        			version = unicode(version, errors='replace')
                    			else:
                        			pass
					u_version = version.encode('utf-8')
					try:
						wp_file.write(name+","+u_version+","+cves_l+"\n")
					except Exception:
						pass
			if int(NumChecks) != -1 and (plugin_count - 1) == int(NumChecks): 
				end = 1
				break
		if end == 1: 
			break
	
		if tmpCount == 1:
			print plugin_count,
			print " plugins stored. Last plugin processed: " + name
			sys.stdout.flush()
			tmpCount = 0
		else:
			tmpCount+=1
	wp_file.close()

    
    

    # Private call for each URL. This method hava main code to check the URL.
    def check_url(self,url):
        '''
         Check Wordpress and plugin version. 
        '''
        # try to open file output
        if OutPutFile != None:
	        try:
		        fileoutput = open(OutPutFile,"w")
	        except IOError:
	            print ""
	            print "[!] Error while open output file."
	            print ""
	            sys.exit(-1)

        readmeok = False
        
        # Check WordPress version
        try: 
	        filetmp = "\nResults for: " + url + "\n\n"
	        filetmp += "   --------   \n"

                if url.find("http://") == -1:
        	        readme = urllib2.urlopen("http://"+url+"/readme.html")                        
                else:
        	        readme = urllib2.urlopen(url+"/readme.html")

	        soupreadme = BeautifulSoup(readme)
	        version = soupreadme.find('h1')
	        location = str(version).find("Versi")
	        print ""
	        print "==> Results for: " + url + " <=="
	        print ""
	        print chr(27) + "[0;91m[i] Wordpress version found: ",
	        filetmp +=  "\nWordpress version found: "
	        if location != -1:
		        print str(version)[(location + 8):(location + 14)].split("\n")[0]
		        filetmp += str(version)[(location + 8):(location + 14)].split("\n")[0] + "\n"
	        	wpCurrentVersion = urllib2.urlopen(WPCurrent_URL)
			soupwpCurrentVersion = BeautifulSoup(wpCurrentVersion)
			versionwpCurrentVersion = soupwpCurrentVersion.find('div', attrs={'class': 'col-3'}).find('p', attrs={'class': 'download-meta'}).find('strong').contents[0].split(';')[2]
			print "[i] Wordpress last public version: "+str(versionwpCurrentVersion)
		else:
		        print "Not result"
		        filetmp += "Not result\n"
	        filetmp += "\n\n"
	        fileoutput.write(filetmp)

	        print chr(27) + "[0;0m"

        except URLError:
            print ""
            print "[!] Can't open URL especified: \"" + url + "\""
            print ""

        try:
                plugin_list = open (InputPluginList,"r")
        except IOError:
            print ""
            print "[!] Error while open the plugins list."
            print ""
            sys.exit(-1)


        # Search for each plugin
        final_countdown = 1
        print ""
        print "[*] Search for installed plugins"
        print ""
        
        
        # Lock for threads
        lock = threading.Lock()
        # Semaphore for write in order to screen
        self.screenSemaphore = threading.Semaphore(1)
        # Semaphore for write in order to screen
        self.checkSimultaneus = threading.Semaphore(int(NumThreats)-1)
        # Semaphore for write in file
        self.writeFile = threading.Semaphore(int(NumThreats)-1)        

        # hunt keyboard interrupt
        try:                          
                
                for line in plugin_list:
                        self.checkSimultaneus.acquire()                
	                cves = "-"      
	                try:
                                plugin, version, cves= line.split(",")
	                except:
		                continue        
	
                        # Create thread
                        t = threading.Thread(target=self.__siteSearch, args=(url,plugin,cves,version,fileoutput,cves,))
                        self.all_run.append(t)
                        # run thread
                        self.all_run[len(self.all_run)-1].start()

	                final_countdown += 1
	                if int(NumChecks) != -1 and final_countdown == int(NumChecks): 
		                break
		                
        except KeyboardInterrupt:
                sys.exit(-1)
                
        plugin_list.close()
        fileoutput.close()
        print "[*] Done"
        return 0        

    # Main code for search infor for each code        
    def __siteSearch(self,url,plugin,cve,version,fileoutput,cves):

	if url.find("http://") == -1:
                url_readme = "http://"+url+"/wp-content/plugins/"+plugin+"/readme.txt"
        else:
                url_readme = url+"/wp-content/plugins/"+plugin+"/readme.txt"
        

	try:
                try:
                        data = urllib.urlopen(url_readme).read()
                except IOError:
                        return


                readme_found = data.find("== Description ==")
                location = data.find("Stable tag:")
                # check if README.txt exist
                if readme_found == -1:
	        
        		if url.find("http://") == -1:
        	        	url_readme = "http://"+url+"/wp-content/plugins/"+plugin+"/README.txt"
	        	else:
                		url_readme = url+"/wp-content/plugins/"+plugin+"/README.txt"

                        try:
                                data = urllib.urlopen(url_readme).read()
                        except IOError:
                                return
                                
                readme_found = data.find("== Description ==")
                location = data.find("Stable tag:")
                printToScreen = ""


                if readme_found != -1:
                        # screen results
                        printToScreen += "\n"
                        printToScreen += chr(27)+ "[0;92m"+"[i] Plugin found: " + plugin + "\n"
                        printToScreen += chr(27)+ "[0;94m"+"    |_Latest version: " + version + "\n"
                        # File results
                        filetmp = "\n"
                        filetmp += "Plugin found: " + plugin + "\n"

                        filetmp += "|_Latest version: " + version + "\n"
                        if location != -1: 
                                printToScreen += chr(27)+"[0;91m"+"    |_ Installed version: " + data[(location + 12):(location + 17)].split("\r")[0] + "\n"
                                filetmp += "|_ Installed version: " + data[(location + 12):(location + 17)].split("\r")[0] + "\n"
                	else: 
                                printToScreen += "    |_Installed version: No results" + "\n"
                                filetmp += "|_Installed version: No results" + "\n"
                        filetmp += "\n"

                        # Write results on file
                        self.writeFile.acquire()
                        fileoutput.write(filetmp)
			fileoutput.flush()
                        self.writeFile.release()

                        if cves != None and cves != "-" and cves != "\n": 
				printToScreen += chr(27)+"[0;91m"+"    |_CVE list: \n"
				for i in cves.split(";"):
					if i!="\n":
						printToScreen += chr(27)+"[0;91m"+"    |___" + i + ": (http://cve.mitre.org/cgi-bin/cvename.cgi?name=" + i + ")\n"
			printToScreen += chr(27)+ "[0m"
                
                self.screenSemaphore.acquire() # lock screen console
                print printToScreen,
                self.screenSemaphore.release() # release screen console

                # Release for new thread
                self.checkSimultaneus.release()        
                
        except KeyboardInterrupt:                
                raise KeyboardInterrupt
                return
               
        
#
#	Class for search on google
#
class gsearch(Thread):
    # Attributes
    filename = None
    plugins = None
    file = None
    outfilename = None
    outfile = None
    sites = None
    #
    # Results array format
    #
    # [0] = Hostaname
    # [1] = Plugin
    # [2] = Latest version
    # [3] = Version instaled
    # [4] = CVE
    # [5] = Exploit (for future use)    
    results = None

    # Default constructor
    def __init__(self, filename, outfilename):
        self.filename = filename
        self.outfilename = outfilename
        self.plugins = []
        self.sites = {}
        self.results = []

    # Open input and output file
    def openFiles(self):
        list = self.plugins
        try:
            self.file = open(self.filename,"r")
        except IOError:
	    print ""
            print "[!] Error while read the plugins file."
 	    print ""
            sys.exit(-1)

        try:
            self.outfile = open(self.outfilename, "w+")
        except IOError:
	    print ""
            print "[!] Error while open output file"
	    print ""
	    sys.exit(-1)

    # Read next plugin
    def readNextPlugin(self):
        return self.file.readline()

    # Search README.txt
    def searchReadme(self,site,plugin,cap):
        # Make complete URL
	if cap == "nocap": 
	        url = "http://" + site + "/wp-content/plugins/" + plugin + "/readme.txt"
        else: 
                url = "http://" + site + "/wp-content/plugins/" + plugin + "/README.txt"
	# Open site
	res = None
        try:
            req = Request(url.encode('utf8'))
            res = urlopen(req)
            data = res.read()
        # Close conection
        except URLError:
            return ""
        except ValueError:
            return ""
	except HTTPException:
	    return ""
        return data


    # Search plugin version in text
    def getVersion(self,text):
	if text.find("== Description ==") != -1:
        	location = text.lower().find("stable tag:")
		if location != -1: return text[(location + 12):(location + 17)].split("\r")[0]
        return "Not result"

    # Write file output 
    def writeOutput(self,results):
	if results == None:
		return

        for i in results:
		tmp = ""	
		for j in i:
			rep = j.replace("\n","")
			tmp = tmp + rep + ","
		tmp=tmp + "\n"
		self.outfile.write(tmp)
		self.outfile.flush()


    # Get the google results
    def getGoogleResults(self,pluginname,latest,cve):
        try:
		gs = GoogleSearch("inurl:'wp-content/plugins/" + pluginname + "'", random_agent=True)
        	gs.results_per_page = 100
                        

		numberOfprocessed = 0	
                self.all_run = []
                
       		for i in range(int(limitForSearch)):
        		results = gs.get_results()
            		if not results:
            		        break

                        # Semaphore for write in order to screen
                        self.checkSimultaneus = threading.Semaphore(int(NumThreats))            
                        # Semaphore for write to file
                        self.writeFile = threading.Semaphore(int(NumThreats)-1)

			for res in results:
			        self.checkSimultaneus.acquire()
				host_name = urlparse(res.url.encode()).hostname
                                # Create thread
                                t = threading.Thread(target=self.__getGoogleResults, args=(host_name,latest,pluginname,cve))
                                self.all_run.append(t)
                                # run thread
                                self.all_run[len(self.all_run)-1].start()
				


				
	except SearchError, e:
  		print "Search failed: %s" % e


    # Private search for each thread
    def __getGoogleResults(self,host_name,latest,pluginname,cve):
        version = ""
	version2 = ""
	results = []
	if host_name:
		readme = self.searchReadme(host_name, pluginname, cap="nocap")
		if readme: 
		        version = self.getVersion(readme)
		if version == "Not result" or version == "":
			readme = self.searchReadme(host_name, pluginname, cap="cap")
			if readme: version2 = self.getVersion(readme)

			if verbose == True :
			        print "  - Site: " + host_name + " || Plugin: " + pluginname + "|| Only cached by Google"
			results.append([host_name,pluginname,"Only cached by Google",latest,version2.strip(),cve])			
		else: 
			if verbose == True: 
			        print "  - Site: " + host_name + " || Plugin: " + pluginname + "|| Yet installed on site"
			results.append([host_name,pluginname,"Yet installed on site",latest,version.strip(),cve])

        
	# write resulta to file
        self.writeFile.acquire()
        self.writeOutput(results)
	self.writeFile.release()

        del results

	self.checkSimultaneus.release()

    # Main method
    def Run(self):
        # Open the files
        self.openFiles()
        # List the results
	final_countdown = 1
	equalversion = 0
	nequalversion = 0
	totalplugins = 0
        while True:
            readed=(self.readNextPlugin())
            if not readed: break
	    try:
            	plugin,latestversion,cves=readed.split(",")
	    except:
		continue
	
	    # Check if there is to find those without CVE
	    if WhithCVE == True:
		continue

            # search           
            self.getGoogleResults(plugin,latestversion,cves)
	    # Sleep for few seconds
	    timeToSleep=random.randint(MinSleepTime,MaxSleepTime)
	    print ""
	    print "   **** Sleep " + str(timeToSleep) + " seconds..."
	    print ""
	    time.sleep(timeToSleep)

	    final_countdown += 1
	    if int(NumChecks) != -1 and final_countdown == int(NumChecks): 
		    break
	totalplugins = final_countdown
	self.outfile.close()

def reload_pluginlist():
	wordpress = Wordpress()
	wordpress.pluginlist_generate()


####################################################################################################################################################
#
# Begin of program
#
####################################################################################################################################################

try:
	opt, args = getopt.getopt(sys.argv[1:], "l:Gi:t:s:M:R:ho:cn:C",['google-search','input-file=','threads=','min-sleep-time=','max-sleep-time=','reload-plugin','help','output-file=','colored','try-num','without-cve'])
        options=dict(opt)
except getopt.GetoptError, err:
    if err.opt == "R":
                print ""
                print "[!] You must to specify file output for \"-R\" parameter."
                print ""
                
    if err.opt == "i":                
                print ""
                print "[!] You must to specify a input plugins file for \"-i\" parameters."
                print ""
                
    if err.opt == "o":                  
		print ""
		print "[!] You must specify output file for \"-o\"  parameters."
		print ""                
		
    if err.opt == "s":  
		print ""
		print "[!] You must to specify minimun sleep time for \"-s\" parameter."
		print ""   
		 
    if err.opt == "M":  
		print ""
		print "[!] You must to specify maximun sleep time for \"-M\" parameter."
		print ""   	
		
    if err.opt == "n":  
                print ""
                print "[!] You must to specify a number of check for \"-n\" parameter."
                print ""	
                
    if err.opt == "l":  
                print ""
                print "[!] You must to specify a number of limit results for google search \"-n\" parameter."
                print ""	                		
  
    sys.exit(-1)
    

if len(sys.argv) <= 1:
    print help
    print usage
    sys.exit(-1)

# Show help?
if "-h" in options:
	print help
	print usage
	sys.exit(0)

# Number of checks
if "-n" in options:
        try:
                NumChecks = options["-n"]
                if NumChecks < 0:
                        raise Exception
                print "[*] Num of checks set to: " + NumChecks
        except Exception:
                print ""
                print "[!] You must to specify a number of check for \"-n\" parameter."
                print ""
                sys.exit(-1)

# Reload option
if "-R" in options:
	PluginList = options["-R"]
	print "[*] Plugin file list set to: " + PluginList

	# Reload plugin options
	print ""
    	print "[*] Reloading plugins list..."

	try:
		r=Wordpress()
		r.pluginlist_generate()
	except KeyboardInterrupt:
		print ""
		print "[*] Exiting..."
		print ""
	print "[*] done."
	sys.exit(0)


# Input file plugins
if not "-i" in options:
        print ""
        print "[!] You must to specify \"-i\" parameter."
        print ""
        sys.exit(-1)
else:
        InputPluginList = options["-i"]
        print ""
        print "-------------------------------------------------"
        print "[*] Input plugin list set to: " + InputPluginList


# Output file for results
if "-o" in options:
	OutPutFile = options["-o"]
    	print "[*] Output file set to: " + OutPutFile


# Colored output?check if there is to find those without CVE
if "-c" in options:
    	print "[*] Colored output set on."
	ColoredOutput = True



# Without cve parameter
if "-C" in options:
	WhithCVE = False


# Num of threat parameter
if "-t" in options:
	NumThreats = options["-t"]
	if NumThreats < 1:
		print ""
		print "[!] Number of threats must be > 0."
		print ""
		sys.exit(-1)
    	print "[*] Num of threats set to: " + NumThreats


# Min sleep time
if "-s" in options:
    	MinSleepTime = int(options["-s"])
    	print "[*] Min sleep time set to: " + str(MinSleepTime)

# Max sleep time
if "-M" in options:
    	MaxSleepTime = int(options["-M"])
	# check if the minimun is not major than maximun
	if MinSleepTime > MaxSleepTime:
		print ""
		print "[!] The minimun sleep time can't be major than Maximun sleep time."
		print ""
    	print "[*] Max sleep time set to: " + str(MaxSleepTime)

# Googler search option
if "-G" in options:
	print "[*] Searching for google results... " 
	print ""
	# Output file
	if not "-o" in options:
		print ""
		print "[!] You must specify output file for \"-o\"  parameters."
		print ""                
		sys.exit(-1)
		
        # check if limit is set
	if "-l" in options:
	        limitForSearch = options["-l"]
                if not limitForSearch.isdigit():
		        print ""
		        print "[!] \"-l\" option must be interger number."
		        print "" 	
		        sys.exit(-1)	
		        
	OutPutFile = options["-o"]		        
	
    	print "[*] Max results set to: ",
	print limitForSearch 
    	print "[*] Output file set to: " + OutPutFile
        print "-------------------------------------------------"		        
        
        
	try:

		# Call the function
		s=gsearch(InputPluginList,OutPutFile)
		s.Run()
		print "[*] Done"
	except KeyboardInterrupt:
		print ""
		print "[*] Exiting..."
		print ""
	sys.exit(-1)


# Check target
try:     
	TargetURL = args[0]
except Exception:
	print ""
	print "[!] You must to specify a target. Try with \"-h to for more info\""
	print ""
	sys.exit(-1)



# close params header
print "-------------------------------------------------"

#
# Start of program
#
try:
        website = Wordpress()
	website.check_url(TargetURL)
except KeyboardInterrupt:
	print ""
	print "[*] Exiting..."
	print ""

