#!/usr/bin/env python
	
"""Web Crawler/Spider
	
This module implements a web crawler. This is very _basic_ only
and needs to be extended to do anything usefull with the
traversed pages.
"""
import unicodedata
import re
import sys
import time
import urllib2
import urlparse
import optparse
import collections
from BeautifulSoup import BeautifulSoup
import os
definepath=os.getcwd()	
#try:
#	import psyco
#	psyco.full()
#except ImportError:
#	pass
	
import spider
import pymills
from pymills.web import escape
from pymills.misc import duration
from pymills import __version__ as systemVersion

USAGE = "%prog [options] <url>"
VERSION = "%prog v" + systemVersion

AGENT = "%s-%s/%s" % (pymills.__name__, spider.__name__, pymills.__version__)

class Crawler(object):
	
	def __init__(self, root, depth, lock=True):
		self._root = root
		self._depth = depth
		self._lock = lock

		self._host = urlparse.urlparse(root)[1]
		self._startTime = 0
		self._countLinks = 0
		self._countFollowed = 0

	def getStats(self):
		return (self._startTime, self._countLinks, self._countFollowed)

	def crawl(self):
		crawled = open('%s/bin/appdata/crawled.txt' % (definepath), 'w')
		
		self._startTime = time.time()

	        page = Fetcher(self._root)
	        page.fetch()
	        urls = collections.deque(page.getURLS())
		number = len(urls)
	        followed = [self._root]
	
	        n = -1
	        done = False
	
	        while not done:
	                n += 1
			try:
	                	url = urls.popleft()
			except IndexError:
				break
			if url not in followed:
	                        host = urlparse.urlparse(url)[1]
	                        if self._lock and re.match(".*%s" % self._host, host):
					if (str(re.search('javascript', url)) == "None") and (str(re.search('mailto', url)) == "None") and (str(re.search('pdf', url)) == "None") and (str(re.search('doc', url)) == "None") and (str(re.search('mpg', url)) == "None") and (str(re.search('wmv', url)) == "None") and (str(re.search('tif', url)) == "None") and (str(re.search('jpg', url)) == "None"):
						followed.append(url)
	                                	self._countFollowed += 1
	                                	print "Following: %s" % url
						print >> crawled, url
	                                	page = Fetcher(url)
						try:
	                                		page.fetch()
                                                
						except UnicodeEncodeError:
							pass

	                                for i, url in enumerate(page):
	                                        if url not in urls:
	                                                self._countLinks += 1
							if (str(re.search('javascript', url)) == "None") and (str(re.search('mailto', url)) == "None") and (str(re.search('pdf', url)) == "None") and (str(re.search('doc', url)) == "None") and (str(re.search('mpg', url)) == "None") and (str(re.search('wmv', url)) == "None") and (str(re.search('tif', url)) == "None") and (str(re.search('jpg', url)) == "None"):
								urls.append(url)
								number = number + 1
                                                                try:
              	                                                	print "New: %s" % url
                                                                except Exception: pass
								print >> crawled, url
			if n == (number - 1) and self._depth > 0:
				done = True
					
		crawled.close()
class Fetcher(object):
  try:
	
	def __init__(self, url):
		self._url = url
	        self._root = self._url
	        self._tags = []
	        self._urls = []

	def __getitem__(self, y):
	        return self._urls[y]
	
	def _add_headers(self, request):
	        request.add_header("User-Agent", AGENT)
	
	def getURLS(self):
	        return self._urls
	
	def open(self):
	        url = self._url

	        try:
	                request = urllib2.Request(url)
	                handle = urllib2.build_opener()
	        except IOError:
	                return None

	        return (request, handle)
	
	def fetch(self):
	        (request, handle) = self.open()
	        self._add_headers(request)
	        if handle is not None:
	                try:
	                        content = handle.open(request).read()
				soup = BeautifulSoup(content)
	                        if soup.html is not None:
                                        try:
              	                                title = soup.html.head.title.string
                                        except Exception: pass
	                        else:
	                                title = ""
	                        tags = soup('a')
	                except urllib2.HTTPError, error:
	                          if error.code == 404:
	                                  print "%s -> %s" % (error, error.url)
	                          else:
	                                  print error
	                          tags = []
	                except urllib2.URLError, error:
	                          print error
	                          tags = []
			except UnicodeDecodeError:
				tags = []
	                for tag in tags:
	                        try:
	                                url = urlparse.urljoin(self._url, escape(tag['href']))
	                        except KeyError:
	                                continue

	                        self._urls.append(url)
  except KeyboardInterrupt:pass
		
def getLinks(url):
  try:
	page = Fetcher(url)
	page.fetch()
	for i, url in enumerate(page):
	        print "%d. %s" % (i, url)
  except KeyboardInterrupt:pass
	
def parse_options():
  try:
	        """parse_options() -> opts, args
	
	        Parse any command-line options given returning both
	        the parsed options and arguments.
	        """

	        parser = optparse.OptionParser(usage=USAGE, version=VERSION)
	
	        parser.add_option("-q", "--quiet",
	                        action="store_true", default=False, dest="quiet",
	                        help="Enable quiet mode")

	
	        parser.add_option("-l", "--links",
	                        action="store_true", default=False, dest="links",
	                        help="Get links for specified url only")
	
	        parser.add_option("-d", "--depth",
	                        action="store", default=30, dest="depth",
	                        help="Maximum depth to traverse")
	
	        opts, args = parser.parse_args()
	
	        if len(args) < 1:
	                parser.print_help()
	                raise SystemExit, 1
	
	        return opts, args
  except KeyboardInterrupt:pass
	
def main():
   try:
	
	opts, args = parse_options()
	
	url = args[0]
	
        if opts.links:	                
		getLinks(url)              
		raise SystemExit, 0
	
        depth = int(opts.depth)

        print >> sys.stderr, "Crawling %s (Max Depth: %d)" % (
                        url, depth)
        crawler = Crawler(url, depth)
        crawler.crawl()
        print >> sys.stderr, "DONE"
        startTime, countLinks, countFollowed = crawler.getStats()
        print >> sys.stderr, "Found %d links, following %d urls in %s+%s:%s:%s" % ((countLinks, countFollowed,) + duration(time.time() - startTime))
	if (countLinks == 0):
		crawled = open('%s/bin/appdata/crawled.txt' % (definepath), 'w')
		print >> crawled, url
		crawled.close()
   except KeyboardInterrupt: pass
try:	
   if __name__ == "__main__":
        	main()
except Exception: pass
