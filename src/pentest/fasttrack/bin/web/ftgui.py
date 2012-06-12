#!/usr/bin/env python
"""
Fast-Track Web GUI Front-End, very very beta... This is my first attempt at throwing something
together that is easier to use... It will be a gradual progression and improve as time goes along.
Thanks to everyone for the help and support through this and testing, much appreciated to everyone.
Muts, ShamanVirtual, MaJ, Sleep, TheX1le, Stazz, Leroy (Jenkem), Sasquatch, whipsmack, 
and everyone else that has given me ideas, and testing things out.
"""
# Import modules needed here..all standard Python modules
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import string,sys,os,re,subprocess,datetime
# Define current working directory
definepath=os.getcwd()
sys.path.append("%s/bin/setup/" % (definepath))
# Start count to check all system requirements
import depend
# End Dependency check
# Def request handlers to handle GET/POST
sys.path.append("%s/bin/web/" % (definepath))
def load_header(self):
      headeropen=file("bin/web/html/header", "r").readlines()
      for line in headeropen:
          self.wfile.write(line)
  # define left hand nav section for webpage
def load_nav(self):
      navopen=file("bin/web/html/nav", "r").readlines()
      for line in navopen:
          self.wfile.write(line)
  # Define footer section for webpage
def load_footer(self):
      footeropen=file("bin/web/html/footer", "r").readlines()
      for line in footeropen:
          self.wfile.write(line)
class myRequestHandler(BaseHTTPRequestHandler):
 try:
  def do_GET(self):
    # Always Accept GET
    # Site root: Main Menu
    if self.path == "/":
       self.printCustomHTTPResponse(200)
       load_header(self)
       load_nav(self)
       indexopen=file("bin/web/html/index","r").readlines()
       for line in indexopen:
            self.wfile.write(line)
       load_footer(self)

    # Style.CSS
    if self.path == "/fast_track.css":
       self.send_response(200)
       self.send_header('Content_type', 'text/css')
       self.end_headers()
       cssopen=file("bin/web/html/fast_track.css","r").readlines()
       for line in cssopen:
           self.wfile.write(line)

    # Spacer
    if self.path == "/images/spacer.gif":
       spacer=file("bin/web/html/images/spacer.gif","rb").readlines()
       for line in spacer:
            self.wfile.write(line)

    # Left graphic image for nav
    if self.path == "/images/ft_left_pane_1.jpg":
       spacer=file("bin/web/html/images/ft_left_pane_1.jpg","rb").readlines()
       for line in spacer:
            self.wfile.write(line)

    # Bullet
    if self.path == "/images/bullet.jpg":
       bullet=file("bin/web/html/images/bullet.jpg","rb").readlines()
       for line in bullet:
            self.wfile.write(line)

    # Content
    if self.path == "/images/content.gif":
       content=file("bin/web/html/images/content.gif","rb").readlines()
       for line in content:
            self.wfile.write(line)

    # Fast_Track_01
    if self.path == "/images/fast_track_01.jpg.gif":
       ft1=file("bin/web/html/images/fast_track_01.jpg","rb").readlines()
       for line in ft1:
            self.wfile.write(line)

    # Fast_Track_03
    if self.path == "/images/fast_track_03.jpg":
       ft3=file("bin/web/html/images/fast_track_03.jpg","rb").readlines()
       for line in ft3:
            self.wfile.write(line)

    # Fast_Track_08
    if self.path == "/images/fast_track_08.jpg":
       ft8=file("bin/web/html/images/fast_track_08.jpg","rb").readlines()
       for line in ft8:
            self.wfile.write(line)

    # Fast_Track_09
    if self.path == "/images/fast_track_09.jpg":
       ft9=file("bin/web/html/images/fast_track_09.jpg","rb").readlines()
       for line in ft9:
            self.wfile.write(line)

    # Fast_Track_10
    if self.path == "/images/fast_track_10.jpg":
       ft=file("bin/web/html/images/fast_track_10.jpg","rb").readlines()
       for line in ft:
            self.wfile.write(line)

    # Fast_Track_11
    if self.path == "/images/fast_track_11.jpg":
       ft9=file("bin/web/html/images/fast_track_11.jpg","rb").readlines()
       for line in ft9:
            self.wfile.write(line)

    # Fast_Track_15
    if self.path == "/images/fast_track_15.jpg":
       ft9=file("bin/web/html/images/fast_track_15.jpg","rb").readlines()
       for line in ft9:
            self.wfile.write(line)

    # Fast_Track_16
    if self.path == "/images/fast_track_16.jpg":
       ft9=file("bin/web/html/images/fast_track_16.jpg","rb").readlines()
       for line in ft9:
            self.wfile.write(line)

    # Fast_Track_18
    if self.path == "/images/fast_track_18.jpg":
       ft9=file("bin/web/html/images/fast_track_18.jpg","rb").readlines()
       for line in ft9:
            self.wfile.write(line)

    # Fast_Track_21
    if self.path == "/images/fast_track_21.jpg":
       ft9=file("bin/web/html/images/fast_track_21.jpg","rb").readlines()
       for line in ft9:
            self.wfile.write(line)

    # Fast_Track_25
    if self.path == "/images/fast_track_25.jpg":
       ft9=file("bin/web/html/images/fast_track_25.jpg","rb").readlines()
       for line in ft9:
            self.wfile.write(line)

    # Fast_Track_26
    if self.path == "/images/fast_track_26.jpg":
       ft9=file("bin/web/html/images/fast_track_26.jpg","rb").readlines()
       for line in ft9:
            self.wfile.write(line)

    # FT_header_04
    if self.path == "/images/ft_header_04.jpg":
       ft9=file("bin/web/html/images/ft_header_04.jpg","rb").readlines()
       for line in ft9:
            self.wfile.write(line)

    # ft_header_hover_03
    if self.path == "/images/ft_header_hover_03.jpg":
       ft9=file("bin/web/html/images/ft_header_hover_03.jpg","rb").readlines()
       for line in ft9:
            self.wfile.write(line)

    # ft_header_hover_04
    if self.path == "/images/ft_header_hover_04.jpg":
       ft9=file("bin/web/html/images/ft_header_hover_04.jpg","rb").readlines()
       for line in ft9:
            self.wfile.write(line)

    # ft_header_hover_05
    if self.path == "/images/ft_header_hover_05.jpg":
       ft9=file("bin/web/html/images/ft_header_hover_05.jpg","rb").readlines()
       for line in ft9:
            self.wfile.write(line)

    # ft_header_hover_07
    if self.path == "/images/ft_header_hover_07.jpg":
       ft9=file("bin/web/html/images/ft_header_hover_07.jpg","rb").readlines()
       for line in ft9:
            self.wfile.write(line)

    # page_bg
    if self.path == "/images/page_bg.jpg":
       ft9=file("bin/web/html/images/page_bg.jpg","rb").readlines()
       for line in ft9:
            self.wfile.write(line)

    # btn1
    if self.path == "/images/btn_launch_1.jpg":
       spacer=file("bin/web/html/images/btn_launch_1.jpg","rb").readlines()
       for line in spacer:
            self.wfile.write(line)

    # btn2
    if self.path == "/images/btn_launch_2.jpg":
       spacer=file("bin/web/html/images/btn_launch_2.jpg","rb").readlines()
       for line in spacer:
            self.wfile.write(line)

    # btn3
    if self.path == "/images/btn_launch_3.jpg":
       spacer=file("bin/web/html/images/btn_launch_3.jpg","rb").readlines()
       for line in spacer:
            self.wfile.write(line)

    # msautopwn
    if self.path == "/images/btn_msautopwn.jpg":
       spacer=file("bin/web/html/images/btn_msautopwn.jpg","rb").readlines()
       for line in spacer:
            self.wfile.write(line)

    # btn_reset
    if self.path == "/images/btn_reset.jpg":
       spacer=file("bin/web/html/images/btn_reset.jpg","rb").readlines()
       for line in spacer:
            self.wfile.write(line)

    # btn_browse
    if self.path == "/images/btn_browse.jpg":
       spacer=file("bin/web/html/images/btn_browse.jpg","rb").readlines()
       for line in spacer:
            self.wfile.write(line)

    # btn_updateall
    if self.path == "/images/btn_updateall.jpg":
       spacer=file("bin/web/html/images/btn_updateall.jpg","rb").readlines()
       for line in spacer:
            self.wfile.write(line)

    # updateft
    if self.path == "/images/btn_updateft.jpg":
       spacer=file("bin/web/html/images/btn_updateft.jpg","rb").readlines()
       for line in spacer:
            self.wfile.write(line)

    # meta update
    if self.path == "/images/btn_updatems.jpg":
       spacer=file("bin/web/html/images/btn_updatems.jpg","rb").readlines()
       for line in spacer:
            self.wfile.write(line)

    # Fast_Track_10
    if self.path == "/images/fast_track_10.jpg":
       ft10=file("bin/web/html/images/fast_track_10.jpg","rb").readlines()
       for line in ft10:
            self.wfile.write(line)

    # Update: Update Menu for Fast-Track and various other tools
    if self.path == "/update":
       load_header(self)
       load_nav(self)
       update=file("bin/web/html/updates","r").readlines()
       for line in update:
            self.wfile.write(line)
       load_footer(self)
 
    # Autopwn: Metasploit Autopwn Automated
    if self.path == "/autopwn":
       load_header(self)
       load_nav(self)
       autopwn=file("bin/web/html/autopwn","r").readlines()
       for line in autopwn:
            self.wfile.write(line)
       load_footer(self)

    # SQL Brute Main: Sql brute forcing Main Menu
    if self.path == "/sqlbrute":
       load_header(self)
       load_nav(self)
       sqlbrute=file("bin/web/html/sqlbrutemain","r").readlines()
       for line in sqlbrute:
           self.wfile.write(line)
       load_footer(self)
       # Quick brute option: SQL brute forcing using quick (like 50 passwords)
    if self.path == "/quickbrute":
       load_header(self)
       load_nav(self)
       sqlbrutequick=file("bin/web/html/quickbrute","r").readlines()
       for line in sqlbrutequick:
           self.wfile.write(line)
       load_footer(self)

       # Wordlist brute option wordlist: Import an external wordlist and brute force against one or many hosts
    if self.path == "/wordlistbrute":
       load_header(self)
       load_nav(self)
       wordlistbrute=file("bin/web/html/wordlistbrute","r").readlines()
       for line in wordlistbrute:
           self.wfile.write(line)
       load_footer(self)

       # Binary Convert: Convert binarys to a pasteable format to a windows shell to compile it..used as a PAYLOAD delivery method
    if self.path == "/binaryconvert":
       load_header(self)
       load_nav(self)
       binaryconvert=file("bin/web/html/binaryconvert","r").readlines()
       for line in binaryconvert:
           self.wfile.write(line)
       load_footer(self)

    # Changelog: Fast-Track updates, uses CHANGELOG under readme to generate the info dynamically
    if self.path == "/changelog":
       load_header(self)
       load_nav(self)
       changelog=file("bin/web/html/changelog","r").readlines()
       for line in changelog:
           self.wfile.write(line)
           match2=re.search('<div style="overflow:scroll;', line)
           if match2:
               menuopen=file("readme/CHANGELOG","r").readlines()
               for line in menuopen:
                   self.wfile.write('<p class="box_text">'+line+"</p>")
       load_footer(self)
    # Tutorials for Fast-Track, generate the info dynamically
    if self.path == "/tutorials":
       load_header(self)
       load_nav(self)
       tutorials=file("bin/web/html/tutorials","r").readlines()
       for line in tutorials:
           self.wfile.write(line)
       load_footer(self)
    # Credits for Fast-Track, generate the info dynamically
    if self.path == "/credits":
       load_header(self)
       load_nav(self)
       tutorials=file("bin/web/html/credits","r").readlines()
       for line in tutorials:
           self.wfile.write(line)
       load_footer(self)
    # SQL Injector Main: Find an injectable parameter and this trys to exploit it: Main Menu
    if self.path == "/sqlinjector":
       load_header(self)
       load_nav(self)
       sqlinjectormain=file("bin/web/html/sqlinjector","r").readlines()
       for line in sqlinjectormain:
           self.wfile.write(line)
       load_footer(self)
       # SQL Injector Binary Payload: Use binary to hex conversions to deliver our payload through SQL Injection
    if self.path == "/binarypayload":
       load_header(self)
       load_nav(self)
       binarypayload=file("bin/web/html/binarypayload","r").readlines()
       for line in binarypayload:
           self.wfile.write(line)
       load_footer(self)
       # SQL Injector FTP Payload: Use FTP as a median for transfer, delivers a netcat payload
    if self.path == "/ftppayload":
       load_header(self)
       load_nav(self)
       ftppayload=file("bin/web/html/ftppayload","r").readlines()
       for line in ftppayload:
           self.wfile.write(line)
       load_footer(self)
       # SQL Injector POST Binary Payload:
    if self.path == "/postpayload":
       load_header(self)
       load_nav(self)
       postpayload=file("bin/web/html/postpayload","r").readlines()
       for line in postpayload:
           self.wfile.write(line)
       load_footer(self)
       # SQL Injector Manual Payload: Setup everything manual for you, i.e nc listening on port x and ip of x
    if self.path == "/manualpayload":
       load_header(self)
       load_nav(self)
       manualpayload=file("bin/web/html/manualpayload","r").readlines()
       for line in manualpayload:
           self.wfile.write(line)
       load_footer(self)
    if self.path == "/massclient":
       load_header(self)
       load_nav(self)
       massclient=file("bin/web/html/massclient","r").readlines()
       for line in massclient:
           self.wfile.write(line)
       load_footer(self)
       # Payload Generator
    if self.path == "/payloadgen":
       load_header(self)
       load_nav(self)
       payloadgen=file("bin/web/html/payloadgen","r").readlines()
       for line in payloadgen:
           self.wfile.write(line)
       load_footer(self)
    # Exploits Main
    if self.path == "/exploits":
       load_header(self)
       load_nav(self)
       exploitsmain=file("bin/web/html/exploits","r").readlines()
       for line in exploitsmain:
           self.wfile.write(line)
       load_footer(self)

    # HP OpenView CGI Exploit
    if self.path == "/openviewcgi":
       load_header(self)
       load_nav(self)
       openviewcgi=file("bin/web/html/openviewcgi","r").readlines()
       for line in openviewcgi:
           self.wfile.write(line)
       load_footer(self)

    # IBM Tivoli Exploit
    if self.path == "/ibmtivoli":
       load_header(self)
       load_nav(self)
       ibmtivoli=file("bin/web/html/ibmtivoli","r").readlines()
       for line in ibmtivoli:
           self.wfile.write(line)
       load_footer(self)

    # HP OpenView NNM Exploit
    if self.path == "/openviewnnm":
       load_header(self)
       load_nav(self)
       openviewnnm=file("bin/web/html/openviewnnm","r").readlines()
       for line in openviewnnm:
           self.wfile.write(line)
       load_footer(self)
    # Quicktime RTSP 
    if self.path == "/quicktime":
       load_header(self)
       load_nav(self)
       ibmtivoli=file("bin/web/html/quicktime","r").readlines()
       for line in ibmtivoli:
           self.wfile.write(line)
       load_footer(self)

    # Goodtech
    if self.path == "/goodtech":
       load_header(self)
       load_nav(self)
       goodtech=file("bin/web/html/goodtech","r").readlines()
       for line in goodtech:
           self.wfile.write(line)
       load_footer(self)

    # \MS08-067
    if self.path == "/ms08067":
       load_header(self)
       load_nav(self)
       ms08067=file("bin/web/html/ms08067","r").readlines()
       for line in ms08067:
           self.wfile.write(line)
       load_footer(self)

    # \MS09-002
    if self.path == "/ms09002":
       load_header(self)
       load_nav(self)
       ms09002=file("bin/web/html/ms09002","r").readlines()
       for line in ms09002:
           self.wfile.write(line)
       load_footer(self)


    # MIRC
    if self.path == "/mirc":
       load_header(self)
       load_nav(self)
       mirc=file("bin/web/html/mirc","r").readlines()
       for line in mirc:
           self.wfile.write(line)
       load_footer(self)

    # TFTP
    if self.path == "/tftp":
       load_header(self)
       load_nav(self)
       tftp=file("bin/web/html/tftp","r").readlines()
       for line in tftp:
           self.wfile.write(line)
       load_footer(self)

    # IE XML Corruption
    if self.path == "/xmlcorruptionbo":
       load_header(self)
       load_nav(self)
       xml=file("bin/web/html/xmlcorruptionbo","r").readlines()
       for line in xml:
           self.wfile.write(line)
       load_footer(self)


    # MS Internet Explorer 7 DirectShow (msvidctl.dll) Heap Spray
    if self.path == "/directshowheap":
       load_header(self)
       load_nav(self)
       xml=file("bin/web/html/directshowheap","r").readlines()
       for line in xml:
           self.wfile.write(line)
       load_footer(self)

    # FireFox 3.5 Heap Spray
    if self.path == "/firefox35":
       load_header(self)
       load_nav(self)
       xml=file("bin/web/html/firefox35","r").readlines()
       for line in xml:
           self.wfile.write(line)
       load_footer(self)


    # SQLPwnage Main Menu
    if self.path == "/sqlpwnage":
       load_header(self)
       load_nav(self)
       sqlpwnagemain=file("bin/web/html/sqlpwnage","r").readlines()
       for line in sqlpwnagemain:
           self.wfile.write(line)
       load_footer(self)
    # SQLPwnage Blind Menu
    if self.path == "/sqlpwnageblind":
       load_header(self)
       load_nav(self)
       sqlpwnagemain=file("bin/web/html/sqlpwnageblind","r").readlines()
       for line in sqlpwnagemain:
           self.wfile.write(line)
       load_footer(self)
    # SQLPwnage Blind POST Menu
    #if self.path == "/sqlpwnageblindpost":
    #   sqlpwnagemain=file("bin/web/html/sqlpwnageblindpost.html","r").readlines()
    #   for line in sqlpwnagemain:
    #       self.wfile.write(line)
    #       match=re.search('<ul id="navlist" title="menu">', line)
    #       if match:
    #           menuopen=file("bin/web/html/menu.html","r").readlines()
    #           for line in menuopen:
    #               self.wfile.write(line)
    # SQLPwnage Error Menu
    if self.path == "/sqlpwnageerror":
       load_header(self)
       load_nav(self)
       sqlpwnagemain=file("bin/web/html/sqlpwnageerror","r").readlines()
       for line in sqlpwnagemain:
           self.wfile.write(line)
       load_footer(self)



    # Close any html body tags
    self.wfile.write("</html></body>")

  # Start POST
  def do_POST(self):
   ###################### START UPDATE EVERYTHING SECTION ##############################

   if self.path == "/updatepost":
      load_header(self)
      load_nav(self)
      updatepost=file("bin/web/html/finished","r").readlines()
      for line in updatepost:
          self.wfile.write(line)
      load_footer(self)
      try:
         update=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track Auto-Update" -e "python %s/fast-track.py -c 1 2" 2> /dev/null""" % (definepath), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END UPDATE EVERYTHING SECTION ##############################

   ###################### START UPDATE FT ONLY SECTION ##############################

   if self.path == "/updateftpost":
      load_header(self)
      load_nav(self)
      updatepost=file("bin/web/html/finished","r").readlines()
      for line in updatepost:
          self.wfile.write(line)
      load_footer(self)
      try:
         update=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track Auto-Update" -e "python %s/fast-track.py -c 1 1" 2> /dev/null""" % (definepath), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END UPDATE FT ONLY SECTION ##############################

   ###################### START AUTOPWN SECTION ##############################
   if self.path == "/autopwnpost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      ipaddr=raw_post_data[1].rstrip()
      ipaddr=ipaddr.replace("+"," ")
      ipaddr=ipaddr.replace("%2C",",")
      ipaddr=ipaddr.replace("%2F","/")
      option1=raw_post_data[3].rstrip()
      load_header(self)
      load_nav(self)
      autopwn=file("bin/web/html/finished","r").readlines()    
      for line in autopwn:
          self.wfile.write(line)
      load_footer(self)
      try:
         metapwn=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track Metasploit Autopwn Automated" -e "python %s/fast-track.py -c 2 \'%s\' %s" 2> /dev/null""" % (definepath,ipaddr,option1), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END AUTOPWN SECTION ##############################

   ###################### START METASPLOIT UPDATE SECTION ##############################
   if self.path == "/metaupdatepost":
      self.send_response(200)
      self.end_headers()
      load_header(self)
      load_nav(self)
      metaupdatepost=file("bin/web/html/finished","r").readlines()    
      for line in metaupdatepost:
          self.wfile.write(line) 
      load_footer(self)
      try:
         metaupdate=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track Metasploit Autopwn Automated" -e "python %s/bin/ftsrc/updatemeta.py" 2> /dev/null""" % (definepath), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END METASPLOIT UPDATE SECTION ##############################

   ###################### START SQL QUICK BRUTE ##############################
   if self.path == "/quickbrutepost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      ipaddr=raw_post_data[1].rstrip()
      ipaddr=ipaddr.replace("%2F","/")
      payload=raw_post_data[3].rstrip()
      username=raw_post_data[5].rstrip()
      load_header(self)
      load_nav(self)
      quickbrute=file("bin/web/html/finished","r").readlines()    
      for line in quickbrute:
          self.wfile.write(line)
      load_footer(self)
      try:
         quickbrute=subprocess.Popen(r"""xterm -geometry 80x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track SQL Quick Brute" -e "python %s/fast-track.py -c 4 1 %s %s %s" """ % (definepath,ipaddr,username,payload), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END SQL QUICK BRUTE ##############################

   ###################### START SQL WORDLIST BRUTE ##############################
   if self.path == "/wordlistbrutepost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
 #     print raw_post_data
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      ipaddr=raw_post_data[1].rstrip()
      payload=raw_post_data[3].rstrip()
      username=raw_post_data[5].rstrip()
      wordlist=raw_post_data[7].rstrip()
      wordlist=wordlist.replace("%2F","/")
      ipaddr=ipaddr.replace("%2F", "/")
      load_header(self)
      load_nav(self)
      wordlistbrute=file("bin/web/html/finished","r").readlines()
      for line in wordlistbrute:
           self.wfile.write(line)
      load_footer(self)
      try:
         wordlist=subprocess.Popen(r'''xterm -geometry 80x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track SQL Wordlist Brute" -e "python %s/fast-track.py -c 4 2 %s %s %s %s"''' % (definepath,ipaddr,username,wordlist,payload), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END SQL WORDLIST BRUTE ##############################


   ###################### START BINARYCONVERT ##############################
   if self.path == "/binaryconvertpost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      print raw_post_data
      binpath=raw_post_data[1].rstrip()
      binpath=binpath.replace("%2F","/")
      binaryconvertpost=file("bin/web/html/finished","r").readlines()
      load_header(self)
      load_nav(self)
      for line in binaryconvertpost:
          self.wfile.write(line)
      load_footer(self)
      try:
        binconvert=subprocess.Popen("""python %s/fast-track.py -c 5 %s""" % (definepath,binpath), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END BINARYCONVERT ##############################

   ###################### START SQL INJECTOR BINARY PAYLOAD ##############################
   if self.path == "/binarypayloadpost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      url=raw_post_data[1].rstrip()
      url=url.replace("%3A",":")
      url=url.replace("%2F","/")
      url=url.replace("%3F","?")
      url=url.replace("%3D","=")
      url=url.replace("%27","'")
      url=url.replace("%26","&")
      # Used to escape the ' and & in shell
      url=url.replace("'","\\'")
      url=url.replace("&","\\&")
      load_header(self)
      load_nav(self)
      binarypayload=file("bin/web/html/finished","r").readlines()
      for line in binarypayload:
          self.wfile.write(line) 
      load_footer(self) 
      try:
         
         binarypayload=subprocess.Popen('''xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track SQL Injector Binary Payload" -e "python %s/fast-track.py -c 3 1 %s" 2> /dev/null''' % (definepath,url), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."
      except Exception:
         pass

   ###################### END SQL INJECTOR BINARY PAYLOAD ##############################

   ###################### START SQL INJECTOR FTP PAYLOAD ##############################
   if self.path == "/ftppayloadpost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      url=raw_post_data[1].rstrip()
      url=url.replace("%3A",":")
      url=url.replace("%2F","/")
      url=url.replace("%3F","?")
      url=url.replace("%3D","=")
      url=url.replace("%27","'")
      url=url.replace("%26","&")
      # Used to escape the ' and & in shell
      url=url.replace("'","\\'")
      url=url.replace("&","\\&")
      load_header(self)
      load_nav(self)
      ftppayloadpost=file("bin/web/html/finished","r").readlines()
      for line in ftppayloadpost:
           self.wfile.write(line)
      load_footer(self)
      try:
         ftppayload=subprocess.Popen('''xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track SQL Injector Binary Payload" -e "python %s/fast-track.py -c 3 2 %s" 2> /dev/null'''% (definepath,url), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."
      except Exception:
         pass

    ###################### END SQL INJECTOR FTP PAYLOAD ##############################

   ###################### START SQL INJECTOR MANUAL PAYLOAD ##############################
   if self.path == "/manualpayloadpost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      url=raw_post_data[1].rstrip()
      url=url.replace("%3A",":")
      url=url.replace("%2F","/")
      url=url.replace("%3F","?")
      url=url.replace("%3D","=")
      url=url.replace("%27","'")
      url=url.replace("%26","&")
      # Used to escape the ' and & in shell
      url=url.replace("'","\\'")
      url=url.replace("&","\\&")
      ipaddr=raw_post_data[3].rstrip()
      portnum=raw_post_data[5].rstrip()
      load_header(self)
      load_nav(self)
      manualpayloadpost=file("bin/web/html/finished","r").readlines()
      for line in manualpayloadpost:
          self.wfile.write(line)
      load_footer(self)
      try:
         manualpayload=subprocess.Popen('''xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track SQL Injector Binary Payload" -e "python %s/fast-track.py -c 3 3 %s %s %s" 2> /dev/null''' % (definepath,url,ipaddr,portnum), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."
      except Exception:
         pass

    ###################### END SQL INJECTOR MANUAL PAYLOAD ##############################

   ###################### START SQL INJECTOR BINARY PAYLOAD POST ##############################
   if self.path == "/postpayloadpost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      url=raw_post_data[1].rstrip()
      url=url.replace("%3A",":")
      url=url.replace("%2F","/")
      url=url.replace("%3F","?")
      url=url.replace("%3D","=")
      url=url.replace("%27","'")
      url=url.replace("%26","&")
      # Used to escape the ' and & in shell
      url=url.replace("'","\\'")
      url=url.replace("&","\\&")
      load_header(self)
      load_nav(self)
      postpayload=file("bin/web/html/finished","r").readlines()
      for line in postpayload:
          self.wfile.write(line)
      load_footer(self)
      try:
         ftppayload=subprocess.Popen('''xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track SQL Injector Binary Payload" -e "python %s/fast-track.py -c 3 4 %s" 2> /dev/null'''% (definepath,url), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."
      except Exception:
         pass

    ###################### END SQL INJECTOR BINARY PAYLOAD POST ##############################

   ###################### START METASPLOIT CLIENT ATTACK ##############################
   if self.path == "/massclientpost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      ipaddr=raw_post_data[1].rstrip()
      choice=raw_post_data[3].rstrip()
      try:
         etterchoice=raw_post_data[5].rstrip()
      except Exception,e:
          print e 
          etterchoice=0
      try:
         ettercap=raw_post_data[7].rstrip()
      except Exception: ettercap=0
      load_header(self)
      load_nav(self)
      massclientpost=file("bin/web/html/finished","r").readlines()
      for line in massclientpost:
          self.wfile.write(line)     
      load_footer(self)
      print choice
      try:
         massclient=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track Metasploit Mass Client Attack" -e "python %s/fast-track.py -c 6 %s %s %s %s" 2> /dev/null""" % (definepath,ipaddr,choice,etterchoice,ettercap), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END METASPLOIT CLIENT ATTACK ##############################

   ###################### START EXPLOITS OPENVIEWCGI ##############################
   if self.path == "/openviewcgipost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      ipaddr=raw_post_data[1].rstrip()
      ipaddr=ipaddr.replace("+"," ")
      load_header(self)
      load_nav(self)
      openviewcgi=file("bin/web/html/finished","r").readlines()    
      for line in openviewcgi:
          self.wfile.write(line)
      load_footer(self)
      try:
         openviewcgi=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track HP OpenView CGI Exploit" -e "python %s/fast-track.py -c 7 1 %s" 2> /dev/null""" % (definepath,ipaddr), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END EXPLOITS OPENVIEWCGI ##############################

   ###################### START EXPLOITS IBMTIVOLI ##############################
   if self.path == "/ibmtivolipost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      try:
         ipaddr=raw_post_data[1].rstrip()
         ipaddr=ipaddr.replace("+"," ")
      except IndexError: pass
      load_header(self)
      load_nav(self)
      ibmtivoli=file("bin/web/html/finished","r").readlines()    
      for line in ibmtivoli:
          self.wfile.write(line)
      load_footer(self)

      try:
         openviewcgi=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track IBM Tivoli Exploit" -e "python %s/fast-track.py -c 7 2 %s" 2> /dev/null""" % (definepath,ipaddr), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END EXPLOITS IBMTIVOLI ##############################

   ###################### START EXPLOITS OPENVIEWNNM ##############################
   if self.path == "/openviewnnmpost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      ipaddr=raw_post_data[1].rstrip()
      ipaddr=ipaddr.replace("+"," ")
      load_header(self)
      load_nav(self)
      openviewnnm=file("bin/web/html/finished","r").readlines()    
      for line in openviewnnm:
          self.wfile.write(line)
      load_footer(self)
      try:
         openviewcgi=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track HP OpenView NNM Exploit" -e "python %s/fast-track.py -c 7 2 %s" 2> /dev/null""" % (definepath,ipaddr), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END EXPLOITS OPENVIEWNNM ##############################

   ###################### START EXPLOITS QUICKTIME ##############################
   if self.path == "/quicktimepost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      quicktime=file("bin/web/html/finished","r").readlines()
      load_header(self)
      load_nav(self)
      for line in quicktime:
          self.wfile.write(line)
      load_footer(self)
      try:
         quicktime=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track RTSP 7.3 SEH Exploit" -e "python %s/fast-track.py -c 7 4" 2> /dev/null""" % (definepath), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END EXPLOITS QUICKTIME ##############################

   ###################### START EXPLOITS GOODTECH ##############################
   if self.path == "/goodtechpost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      load_header(self)
      load_nav(self)
      goodtech=file("bin/web/html/finished","r").readlines()
      for line in goodtech:
          self.wfile.write(line)
      load_footer(self)
      try:
         goodtech=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track Goodtech 6.4 Buffer Overflow Exploit" -e "python %s/fast-track.py -c 7 5" 2> /dev/null""" % (definepath), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END EXPLOITS GOODTECH ##############################

   ###################### START EXPLOITS MS08067 ##############################
   if self.path == "/ms08067post":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      load_header(self)
      load_nav(self)
      ms08067=file("bin/web/html/finished","r").readlines()
      for line in ms08067:
          self.wfile.write(line)
      load_footer(self)
      try:
         ms08067=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track MS08-067 Server Service Buffer Overflow Exploit" -e "python %s/fast-track.py -c 7 6" 2> /dev/null""" % (definepath), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END EXPLOITS MS08067 ##############################

   ###################### START EXPLOITS MS09002 ##############################
   if self.path == "/ms09002post":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      load_header(self)
      load_nav(self)
      ms09002=file("bin/web/html/finished","r").readlines()
      for line in ms09002:
          self.wfile.write(line)
      load_footer(self)
      try:
        ms09002=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track MS IE 7 Memory Corruption (MS09-002)" -e "python %s/fast-track.py -c 7 10" 2> /dev/null""" % (definepath), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END EXPLOITS MS09002 ##############################


   ###################### START EXPLOITS MIRC ##############################
   if self.path == "/mircpost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      load_header(self)
      load_nav(self)
      mirc=file("bin/web/html/finished","r").readlines()
      for line in mirc:
          self.wfile.write(line)
      load_footer(self)
      try:
         mirc=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track mIRC 6.34 Remote Buffer Overflow Exploit" -e "python %s/fast-track.py -c 7 7" 2> /dev/null""" % (definepath), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END EXPLOITS MIRC ##############################

   ###################### START EXPLOITS TFTP ##############################
   if self.path == "/tftppost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      load_header(self)
      load_nav(self)
      tftp=file("bin/web/html/finished","r").readlines()
      for line in tftp:
          self.wfile.write(line)
      load_footer(self)
      try:
         tftp=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track TFTP Server Windows V1.4 ST Buffer Overflow Exploit" -e "python %s/fast-track.py -c 7 8" 2> /dev/null""" % (definepath), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END EXPLOITS TFTP ##############################

   ###################### START EXPLOITS XML ##############################
   if self.path == "/xmlcorruptionbopost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      load_header(self)
      load_nav(self)
      xml=file("bin/web/html/finished","r").readlines()
      for line in xml:
          self.wfile.write(line)
      load_footer(self)
      try:
         xml=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track IE XML Corruption Heap Spray" -e "python %s/fast-track.py -c 7 9" 2> /dev/null""" % (definepath), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END EXPLOITS XML ##############################

   ###################### START EXPLOITS DIRECTSHOW ##############################
   if self.path == "/directshowheappost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      load_header(self)
      load_nav(self)
      xml=file("bin/web/html/finished","r").readlines()
      for line in xml:
          self.wfile.write(line)
      load_footer(self)
      try:
         xml=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track DirectShow Heap Spray" -e "python %s/fast-track.py -c 7 11" 2> /dev/null""" % (definepath), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END EXPLOITS DIRECTSHOW ##############################

   ###################### START EXPLOITS FireFox 3.5 ##############################
   if self.path == "/firefox35post":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      load_header(self)
      load_nav(self)
      xml=file("bin/web/html/finished","r").readlines()
      for line in xml:
          self.wfile.write(line)
      load_footer(self)
      try:
         xml=subprocess.Popen("""xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track FireFox 3.5 Heap Spray" -e "python %s/fast-track.py -c 7 12" 2> /dev/null""" % (definepath), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END EXPLOITS FireFox 3.5 ##############################



   ###################### START SQLPWNAGE BLIND ##############################
   if self.path == "/sqlpwnageblindpost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      url=raw_post_data[1].rstrip()
      url=url.replace("%3A",":")
      url=url.replace("%2F","/")
      url=url.replace("%3F","?")
      url=url.replace("%3D","=")
      url=url.replace("%27","'")
      url=url.replace("%26","&")
      # Used to escape the ' and & in shell
      url=url.replace("'","\\'")
      url=url.replace("&","\\&")
      ipaddr=raw_post_data[3].rstrip()
      payload=raw_post_data[5].rstrip()
      portnum=raw_post_data[7].rstrip()
      load_header(self)
      load_nav(self)
      manualpayloadpost=file("bin/web/html/finished","r").readlines()
      for line in manualpayloadpost:
          self.wfile.write(line)
      load_footer(self)
      try:
         manualpayload=subprocess.Popen('''xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track SQLPwnage Blind" -e "python %s/fast-track.py -c 8 1 %s %s %s %s"''' % (definepath,url,ipaddr,payload,portnum), shell=True)  
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."
      except Exception,e:
         print e
         pass

    ###################### END SQLPWNAGE BLIND ##############################

   ###################### START SQLPWNAGE Error ##############################
   if self.path == "/sqlpwnageerrorpost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      url=raw_post_data[1].rstrip()
      ipaddr=raw_post_data[3].rstrip()
      ipaddr=ipaddr.replace("%3A",":")
      ipaddr=ipaddr.replace("%2F","/")
      ipaddr=ipaddr.replace("%3F","?")
      ipaddr=ipaddr.replace("%3D","=")
      ipaddr=ipaddr.replace("%27","'")
      ipaddr=ipaddr.replace("%26","&")
      # Used to escape the ' and & in shell
      ipaddr=ipaddr.replace("'","\\'")
      ipaddr=ipaddr.replace("&","\\&")
      payload=raw_post_data[5].rstrip()
      portnum=raw_post_data[7].rstrip()
      load_header(self)
      load_nav(self)
      manualpayloadpost=file("bin/web/html/finished","r").readlines()
      for line in manualpayloadpost:
          self.wfile.write(line)
      load_footer(self)
      try:
         manualpayload=subprocess.Popen('''xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track SQLPwnage Blind" -e "python %s/fast-track.py -c 8 2 %s %s %s %s"''' % (definepath,url,ipaddr,payload,portnum), shell=True)  
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."
      except Exception,e:
         print e
         pass

    ###################### END SQLPWNAGE Error ##############################

   ###################### START PAYLOADGEN ##############################
   if self.path == "/payloadgenpost":
      content_length = string.atoi(self.headers.dict["content-length"])
      raw_post_data = self.rfile.read(content_length)
      raw_post_data=re.split('=|&',raw_post_data)
      self.send_response(200)
      self.end_headers()
      load_header(self)
      load_nav(self)
      payloadgen=file("bin/web/html/finished","r").readlines()
      for line in payloadgen:
          self.wfile.write(line)
      load_footer(self)
      try:
         payloadgen=subprocess.Popen('''xterm -geometry 60x20 -bg black -fg green -fn *-fixed-*-*-*-20-* -T "Fast-Track Payload Generator" -e "python %s/fast-track.py -c 9"''' % (definepath), shell=True)
      except OSError:
         print "Exiting Fast-Track Web GUI.."
         print "\nType <control>-c again to exit Fast-Track Web Gui.."

    ###################### END PayloadGen ##############################




  # Print standard browser headers
  def printBrowserHeaders(self):
    self.wfile.write("<p>Headers: <br>")
    header_keys = self.headers.dict.keys()
    for key in header_keys:
      self.wfile.write("<b>" + key + "</b>: ")
      self.wfile.write(self.headers.dict[key] + "<br>")

  # Print custom HTTP Response
  def printCustomHTTPResponse(self, respcode):
    self.send_response(respcode)
    self.send_header("Content-type", "text/html")
    self.send_header("Server", "myRequestHandler")
    self.end_headers()

 # In case of exceptions, pass them
 except Exception:
    pass
#
# Specify starting parameters..if you want to make this exposed remotely (highly not recommended) 
# just change '127.0.0.1' to ''. Warning on this, I didn't harden this at all, so use at your own
# risk externally.
#
try:
   port=sys.argv[2]
except IndexError:
   port='44444'

httpd = HTTPServer(('127.0.0.1', int(port)), myRequestHandler)
print "\n****************************************\nFast-Track Web GUI Front-End\nWritten by: David Kennedy (ReL1K)\n****************************************\n"
print "Starting HTTP Server on 127.0.0.1 port %s\n" % (port)
print "*** Open a browser and go to http://127.0.0.1:%s ***\n" % (port)
print "Type <control>-c to exit.."
try:
     # Uncomment if you want to launch firefox upon opening
     #print "Launching FireFox on Localhost port: %s" % (port)
     #launchfirefox=os.popen2("firefox localhost:%s" % (port))
     # Open sockets, open for business
     httpd.handle_request()
     # Serve HTTP server forever
     httpd.serve_forever() 
# Except Keyboard Interrupts and throw custom message
except KeyboardInterrupt:
   print "\n\nExiting Fast-Track Web Gui...\n\n"  
   # Remove old files
   cleanup=subprocess.Popen("rm sqlpassword 2> /dev/null;rm SqlScan.txt 2> /dev/null;rm sqlopen.txt 2> /dev/null;rm pentest 2> /dev/null;killall python 2> /dev/null", shell=True)
   # Terminate process
   sys.exit()
