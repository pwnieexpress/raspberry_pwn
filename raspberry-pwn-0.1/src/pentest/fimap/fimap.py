#!/usr/bin/python
#
# This file is part of fimap.
#
# Copyright(c) 2009-2010 Iman Karim(ikarim2s@smail.inf.fh-brs.de).
# http://fimap.googlecode.com
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
from plugininterface import plugininterface
from plugininterface import pluginXMLInfo
import baseClass, baseTools
from codeinjector import codeinjector
from crawler import crawler
import getopt
from googleScan import googleScan
from massScan import massScan
from singleScan import singleScan
import language
import sys,os
import tarfile, tempfile
import shutil
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="Iman Karim(ikarim2s@smail.inf.fh-brs.de)"
__date__ ="$30.08.2009 19:57:21$"
__version__ = "08.1"

config = {}

head =  "fimap v.%s by Iman Karim - Automatic LFI/RFI scanner and exploiter"%__version__ 

pluginlist = "http://fimap.googlecode.com/svn/wiki/PluginList.wiki"
defupdateurl = "http://fimap.googlecode.com/svn/trunk/src/config/"

def show_help(AndQuit=False):
    print "Usage: ./fimap.py [options]"
    print "## Operating Modes:"
    print "   -s , --single                 Mode to scan a single URL for FI errors."
    print "                                 Needs URL (-u). This mode is the default."
    print "   -m , --mass                   Mode for mass scanning. Will check every URL"
    print "                                 from a given list (-l) for FI errors."
    print "   -g , --google                 Mode to use Google to aquire URLs."
    print "                                 Needs a query (-q) as google search query."
    print "   -H , --harvest                Mode to harvest a URL recursivly for new URLs."
    print "                                 Needs a root url (-u) to start crawling there."
    print "                                 Also needs (-w) to write a URL list for mass mode."
    print "   -b , --enable-blind           Enables blind FI-Bug testing when no error messages are printed."
    print "                                 Note that this mode will cause lots of requests compared to the"
    print "                                 default method. Can be used with -s, -m or -g. Experimental."
    print "## Variables:"
    print "   -u , --url=URL                The URL you want to test."
    print "                                 Needed in single mode (-s)."
    print "   -l , --list=LIST              The URL-LIST you want to test."
    print "                                 Needed in mass mode (-m)."
    print "   -q , --query=QUERY            The Google Search QUERY."
    print "                                 Example: 'inurl:include.php'"
    print "                                 Needed in Google Mode (-g)"
    print "        --skip-pages=X           Skip the first X pages from the Googlescanner."
    print "   -p , --pages=COUNT            Define the COUNT of pages to search (-g)."
    print "                                 Default is 10."
    print "        --results=COUNT          The count of results the Googlescanner should get per page."
    print "                                 Possible values: 10, 25, 50 or 100(default)."
    print "        --googlesleep=TIME       The time in seconds the Googlescanner should wait"
    print "                                 befor each request. fimap will count the time between two requests"
    print "                                 and will sleep if it's needed to reach your cooldown. Default is 5."
    print "   -w , --write=LIST             The LIST which will be written if you have choosen"
    print "                                 harvest mode (-H). This file will be opened in APPEND mode."
    print "   -d , --depth=CRAWLDEPTH       The CRAWLDEPTH (recurse level) you want to crawl your target site"
    print "                                 in harvest mode (-H). Default is 1."
    print "   -P , --post=POSTDATA          The POSTDATA you want to send. All variables inside"
    print "                                 will also be scanned for file inclusion bugs."
    print "        --ttl=SECONDS            Define the TTL (in seconds) for requests. Default is 30 seconds."
    print "        --no-auto-detect         Use this switch if you don't want to let fimap automaticly detect"
    print "                                 the target language in blind-mode. In that case you will get some"
    print "                                 options you can choose if fimap isn't sure which lang it is."
    print "## Attack Kit:"
    print "   -x , --exploit                Starts an interactive session where you can"
    print "                                 select a target and do some action."
    print "## Disguise Kit:"
    print "   -A , --user-agent=UA          The User-Agent which should be sent."
    print "        --http-proxy=PROXY       Setup your proxy with this option. But read this facts:"
    print "                                   * The googlescanner will ignore the proxy to get the URLs,"
    print "                                     but the pentest\\attack itself will go thru proxy."
    print "                                   * PROXY should be in format like this: 127.0.0.1:8080"
    print "                                   * It's experimental"
    print "        --show-my-ip             Shows your internet IP, current country and user-agent."
    print "                                 Useful if you want to test your vpn\\proxy config."
    print "## Plugins:"
    print "        --plugins                List all loaded plugins and quit after that."
    print "   -I , --install-plugins        Shows some official exploit-mode plugins you can install "
    print "                                 and\\or upgrade."
    print "## Other:"
    print "        --update-def             Checks and updates your definition files found in the"
    print "                                 config directory."
    print "        --test-rfi               A quick test to see if you have configured RFI nicely."
    print "        --merge-xml=XMLFILE      Use this if you have another fimap XMLFILE you want to"
    print "                                 include to your own fimap_result.xml."
    print "   -C , --enable-color           Enables a colorful output. Works only in linux!"
    print "   -v , --verbose=LEVEL          Verbose level you want to receive."
    print "                                 LEVEL=3 -> Debug"
    print "                                 LEVEL=2 -> Info(Default)"
    print "                                 LEVEL=1 -> Messages"
    print "                                 LEVEL=0 -> High-Level"
    print "        --credits                Shows some credits."
    print "        --greetings              Some greetings ;)"
    print "   -h , --help                   Shows this cruft."
    print "## Examples:"
    print "  1. Scan a single URL for FI errors:"
    print "        ./fimap.py -u 'http://localhost/test.php?file=bang&id=23'"
    print "  2. Scan a list of URLS for FI errors:"
    print "        ./fimap.py -m -l '/tmp/urllist.txt'"
    print "  3. Scan Google search results for FI errors:"
    print "        ./fimap.py -g -q 'inurl:include.php'"
    print "  4. Harvest all links of a webpage with recurse level of 3 and"
    print "     write the URLs to /tmp/urllist"
    print "        ./fimap.py -H -u 'http://localhost' -d 3 -w /tmp/urllist"
    if (AndQuit):
        sys.exit(0)

def show_credits():
    print "## Credits:"
    print "## Developer: Iman Karim(ikarim2s@smail.inf.fh-brs.de)"
    print "#"
    print "## Project Home: http://fimap.googlecode.com"
    print "#"
    print "## Additional Thanks to:"
    print "   - Peteris Krumins (peter@catonmat.net) for xgoogle python module."
    print "   - Pentestmonkey from www.pentestmonkey.net for php-reverse-shell."
    print "   - Crummy from www.crummy.com for BeautifulSoup."
    sys.exit(0)


def show_greetings():
    print "## Greetings:"
    print " - Rita, because you are the best girl on earth."
    print "## Circle of awesome people:"
    print " - Exorzist"
    print " - Invisible"
    print " - Ruun"
    sys.exit(0)

def show_ip():
    print "Heading to 'http://85.214.27.38/show_my_ip'..."
    print "----------------------------------------------"
    tester = codeinjector(config)
    result = tester.doGetRequest("http://85.214.27.38/show_my_ip")
    if (result == None):
        print "result = None -> Failed! Maybe you have no connection or bad proxy?"
        sys.exit(1)
    print result.strip()
    sys.exit(0)

def list_results(lst = os.path.join(os.path.expanduser("~"), "fimap_result.xml")):
    if (not os.path.exists(lst)):
        print "File not found! ~/fimap_result.xml"
        sys.exit(1)
    c = codeinjector(config)

    c.start()

    sys.exit(0)


def show_report():
    if (len(baseClass.new_stuff.items()) > 0):
        print "New FI Bugs found in this session:"
        for k,v in baseClass.new_stuff.items():
            print "\t- %d (probably) usable FI-Bugs on '%s'."%(v, k)


if __name__ == "__main__":
    config["p_url"] = None
    config["p_mode"] = 0 # 0=single ; 1=mass ; 2=google ; 3=crawl
    config["p_list"] = None
    config["p_verbose"] = 2
    config["p_useragent"] = "fimap.googlecode.com/v%s" %__version__
    config["p_pages"] = 10
    config["p_query"] = None
    config["p_exploit_filter"] = ""
    config["p_write"] = None
    config["p_depth"] = 1
    config["p_maxtries"] = 5
    config["p_skippages"] = 0
    config["p_monkeymode"] = False
    config["p_proxy"] = None
    config["p_ttl"] = 30
    config["p_post"] = ""
    config["p_autolang"] = True
    config["p_color"] = False
    config["p_mergexml"] = None
    config["p_results_per_query"] = 100
    config["p_googlesleep"] = 5; 
    doPluginsShow = False
    doRFITest = False
    doInternetInfo = False
    doInstallPlugins = False
    doUpdateDef = False
    doMergeXML = False

    print head

    if (len(sys.argv) == 1):
        #show_help(True)
        print "Use -h for some help."
        sys.exit(0)

    try:
        longSwitches = ["url="          , "mass"        , "single"      , "list="       , "verbose="        , "help",
                        "user-agent="   , "query="      , "google"      , "pages="      , "credits"         , "exploit",
                        "harvest"       , "write="      , "depth="      , "greetings"   , "test-rfi"        , "skip-pages=",
                        "show-my-ip"    , "enable-blind", "http-proxy=" , "ttl="        , "post="           , "no-auto-detect",
                        "plugins"       , "enable-color", "update-def"  , "merge-xml="  , "install-plugins" , "results=",
                        "googlesleep="]
        optlist, args = getopt.getopt(sys.argv[1:], "u:msl:v:hA:gq:p:sxHw:d:bP:CI", longSwitches)

        startExploiter = False

        for k,v in optlist:
            if (k in ("-u", "--url")):
                config["p_url"] = v
            if (k in ("-s", "--single")):
                config["p_mode"] = 0
            if (k in ("-m", "--mass")):
                config["p_mode"] = 1
            if (k in ("-g", "--google")):
                config["p_mode"] = 2
            if (k in ("-H", "--harvest")):
                config["p_mode"] = 3
            if (k in ("-l", "--list")):
                config["p_list"] = v
            if (k in ("-q", "--query")):
                config["p_query"] = v
            if (k in ("-v", "--verbose")):
                config["p_verbose"] = int(v)
            if (k in ("-p", "--pages")):
                config["p_pages"] = int(v)
            if (k in ("--results",)):
                config["p_results_per_query"] = int(v)
            if (k in ("--googlesleep",)):
                config["p_googlesleep"] = int(v)
            if (k in ("-A", "--user-agent")):
                config["p_useragent"] = v
            if (k in ("--http-proxy",)):
                config["p_proxy"] = v
            if (k in ("-w", "--write")):
                config["p_write"] = v
            if (k in ("-d", "--depth")):
                config["p_depth"] = int(v)
            if (k in ("--ttl",)):
                config["p_ttl"] = int(v)
            if (k in ("-h", "--help")):
                show_help(True)
            if (k in ("--test-rfi",)):
                doRFITest = True
            if (k in ("-b", "--enable-blind")):
                config["p_monkeymode"] = True
            if (k in ("-C", "--enable-color")):
                config["p_color"] = True
            if (k in ("--skip-pages",)):
                config["p_skippages"] = int(v)
            if (k in("--credits",)):
                show_credits()
            if (k in ("--greetings",)):
                show_greetings()
            if (k in ("--show-my-ip",)):
                doInternetInfo = True
            if (k in("-x", "--exploit")):
                startExploiter = True
            if (k in ("-P", "--post")):
                config["p_post"] = v
            if (k in ("--no-auto-detect", )):
                config["p_autolang"] = False
            if (k in ("--plugins",)):
                doPluginsShow = True
            if (k in ("-I", "--install-plugins")):
                doInstallPlugins = True
            if (k in ("--update-def",)):
                doUpdateDef = True
            if (k in ("--merge-xml",)):
                doMergeXML = True
                config["p_mergexml"] = v
            #if (k in("-f", "--exploit-filter")):
            #    config["p_exploit_filter"] = v

        xmlsettings = language.XML2Config(config)
        config["XML2CONFIG"] = xmlsettings  
        
        plugman = plugininterface(config)
        config["PLUGINMANAGER"] = plugman
                      
        if startExploiter:
            list_results()

    except getopt.GetoptError, err:
        print (err)
        sys.exit(1)

    if (doUpdateDef):
        xmlconfig = config["XML2CONFIG"]
        tools = baseTools.baseTools()
        tester = codeinjector(config)
        print "Checking for definition file updates..."
        #print "Testing 'generic.xml'..."
        generic_xml_ver = xmlconfig.getVersion()
        
        # Get generic.xml from SVN repository and parse out its version.
        generic_xml_online = tester.doGetRequest(defupdateurl + "generic.xml")
        tmpFile = tempfile.mkstemp()[1] + ".xml"
        f = open(tmpFile, "w")
        f.write(generic_xml_online)
        f.close()
        generic_xml_ver_online = tools.getAttributeFromFirstNode(tmpFile, "revision")

        if (generic_xml_ver < generic_xml_ver_online):
            print "'generic.xml' (v.%s) is older than the online version (v.%s)!" %(generic_xml_ver, generic_xml_ver_online)
            tools.suggest_update(xmlconfig.getRealFile(), tmpFile)
        else:
            print "'generic.xml' is up-to-date." 
        
        print "Testing language sets defined in 'generic.xml'..."
        langsets = xmlconfig.getAllLangSets()
        for name, langclass in langsets.items():
            fname = os.path.basename(langclass.getLangFile())
            #print "Testing language '%s' for updates..." %(fname)
            langurl = defupdateurl + fname
            # Download and save XML from SVN repository.
            xml_content = tester.doGetRequest(langurl)
            if (xml_content != None):
                tmpFile = tempfile.mkstemp()[1] + ".xml"
                f = open(tmpFile, "w")
                f.write(xml_content)
                f.close()
                # Parse out version number.
                version_online = tools.getAttributeFromFirstNode(tmpFile, "revision")
                # Get installed version.
                version = langclass.getVersion()
                if (version < version_online):
                    print "'%s' (v.%s) is older than the online version (v.%s)!" %(fname, version, version_online)
                    tools.suggest_update(langclass.getLangFile(), tmpFile)
                else:
                    print "'%s' is up-to-date." %(fname)
            else:
                print "Failed to check '%s'!" %(fname)
            
        
        sys.exit(1)
        

    if (doInstallPlugins):
        print "Requesting list of plugins..."
        tester = codeinjector(config)
        result = tester.doGetRequest(pluginlist)
        
        choice = {}
        idx = 1
        for line in result.split("\n"):
            tokens = line.split("|")
            label = tokens[0].strip()
            name = tokens[1].strip()
            version = int(tokens[2].strip())
            url = tokens[3].strip()
            choice[idx] = (label, name, version, url)
            idx += 1
        pluginman = config["PLUGINMANAGER"]
        
        tools = baseTools.baseTools()
        header = "LIST OF TRUSTED PLUGINS"
        boxarr = []
        for k,(l,n,v,u) in choice.items():
            instver = pluginman.getPluginVersion(n)
            if (instver == None):
                boxarr.append("[%d] %s - At version %d not installed." %(k, l, v))
            elif (instver < v):
                boxarr.append("[%d] %s - At version %d has an UPDATE." %(k, l, v))
            else:    
                boxarr.append("[%d] %s - At version %d is up-to-date and installed." %(k, l, v))
        boxarr.append("[q] Cancel and Quit.")
        tools.drawBox(header, boxarr, False)
        nr = None    
    
        nr = raw_input("Choose a plugin to install: ")
        if (nr != "q"):
            (l,n,v,u) = choice[int(nr)]
            print "Downloading plugin '%s' (%s)..." %(n, u)
            plugin = tester.doGetRequest(u)
            if (plugin != None):
                tmpFile = tempfile.mkstemp()[1] + ".tar.gz"
                f = open(tmpFile, "wb")
                f.write(plugin)
                f.close()
                
                print "Unpacking plugin..."
                try:
                    tar = tarfile.open(tmpFile, 'r:gz')
                    tmpdir = tempfile.mkdtemp()
                    tar.extractall(tmpdir)
                    pluginxml = os.path.join(tmpdir, n, "plugin.xml")
                    pluginsdir = os.path.join(sys.path[0], "plugins")
                     
                    
                    if (os.path.exists(pluginxml)):
                        info = pluginXMLInfo(pluginxml)
                        ver = pluginman.getPluginVersion(info.getStartupClass())
                        if (ver != None):
                            inp = ""
                            if (ver > info.getVersion()):
                                inp = raw_input("Do you really want to downgrade this plugin? [y/N]")
                            elif (ver == info.getVersion()):
                                inp = raw_input("Do you really want to reinstall this plugin? [y/N]")

                            if (inp == "Y" or inp == "y"):
                                dir = info.getStartupClass()
                                deldir = os.path.join(pluginsdir, dir)
                                print "Deleting old plugin directory..."
                                shutil.rmtree(deldir)
                            else:
                                print "OK aborting..." 
                                sys.exit(0)
                        tar.extractall(os.path.join(pluginsdir))
                        print "Plugin '%s' installed successfully!" %(info.getName())
                    else:
                        print "Plugin doesn't have a plugin.xml! (%s)" %pluginxml
                        sys.exit(1)
                    
                except:
                    print "Unpacking failed!"
                    #sys.exit(0)
            else:
                print "Failed to download plugin package!"
        
        sys.exit(0)


    if (doPluginsShow):
        plugins = config["PLUGINMANAGER"].getAllPluginObjects()
        if (len(plugins) > 0):
            for plug in plugins:
                print "[Plugin: %s] by %s (%s)" %(plug.getPluginName(), plug.getPluginAutor(), plug.getPluginEmail())
        else:
            print "No plugins :T"
        sys.exit(0)
    
    if (doMergeXML):
        tester = codeinjector(config)
        newVulns, newDomains = tester.mergeXML(config["p_mergexml"])
        print "%d new vulnerabilitys added from %d new domains." %(newVulns, newDomains)
        sys.exit(0)
        
    # Upgrade XML if needed...
    bc = baseClass.baseClass(config)
    bc.testIfXMLIsOldSchool()
        
    if (doRFITest):
        injector = codeinjector(config)
        injector.testRFI()
        sys.exit(0)

    if (config["p_proxy"] != None):
        print "Using HTTP-Proxy '%s'." %(config["p_proxy"])

    if (doInternetInfo):
        show_ip()

    if (config["p_url"] == None and config["p_mode"] == 0):
        print "Target URL required. (-u)"
        sys.exit(1)
    if (config["p_list"] == None and config["p_mode"] == 1):
        print "URLList required. (-l)"
        sys.exit(1)
    if (config["p_query"] == None and config["p_mode"] == 2):
        print "Google Query required. (-q)"
        sys.exit(1)
    if (config["p_url"] == None and config["p_mode"] == 3):
        print "Start URL required for harvesting. (-u)"
        sys.exit(1)
    if (config["p_write"] == None and config["p_mode"] == 3):
        print "Output file to write the URLs to is needed in Harvest Mode. (-w)"
        sys.exit(1)

    if (config["p_monkeymode"] == True):
        print "Experimental blind FI-error checking enabled."



    try:
        if (config["p_mode"] == 0):
            single = singleScan(config)
            single.setURL(config["p_url"])
            single.scan()

        elif(config["p_mode"] == 1):
            if (not os.path.exists(config["p_list"])):
                print "Your defined URL-List doesn't exist: '%s'" %config["p_list"]
                sys.exit(0)
            print "MassScanner is loading URLs from file: '%s'" %config["p_list"]
            m = massScan(config)
            m.startMassScan()
            show_report()

        elif(config["p_mode"] == 2):
            print "GoogleScanner is searching for Query: '%s'" %config["p_query"]
            g = googleScan(config)
            g.startGoogleScan()
            show_report()

        elif(config["p_mode"] == 3):
            print "Crawler is harvesting URLs from start URL: '%s' with depth: %d and writing results to: '%s'" %(config["p_url"], config["p_depth"], config["p_write"])
            c = crawler(config)
            c.crawl()

    except KeyboardInterrupt:
        print "\n\nYou have terminated me :("
        
    except Exception, err:
        print "\n\n========= CONGRATULATIONS! ========="
        print "You have just found a bug!"
        print "If you are cool, send the following stacktrace to the bugtracker on http://fimap.googlecode.com/"
        print "Please also provide the URL where fimap crashed."
        raw_input("Push enter to see the stacktrace...")
        print "cut here %<--------------------------------------------------------------"
        print "Exception: %s" %err
        raise
