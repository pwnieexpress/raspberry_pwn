''' Created on Sep 20, 2010
@author: j0fer '''

import re
import string

# Header section for webpage
def load_header(self):
    headeropen = file("bin/web/html/header", "r").readlines()
    for line in headeropen:
        self.wfile.write(line)

# Left hand nav section for webpage
def load_nav(self):
    navopen = file("bin/web/html/nav", "r").readlines()
    for line in navopen:
        self.wfile.write(line)

# Footer section for webpage
def load_footer(self):
    footeropen = file("bin/web/html/footer", "r").readlines()
    for line in footeropen:
        self.wfile.write(line)

# Standard function to draw exploit page
def draw_frame(self):
    frame = (self.path).lstrip('/')
    load_header(self)
    load_nav(self)
    currentdata = file("bin/web/html/" + frame, "r").readlines()
    for line in currentdata:
        self.wfile.write(line)
    load_footer(self)

# Draw frames which read from textfile(s)
def draw_complexframe(self, title, textfile):
    load_header(self)
    load_nav(self)
    frame_head1 = file("bin/web/html/frame_head1", "r").readlines()
    for line in frame_head1:
        self.wfile.write(line)
    self.wfile.write(title)
    frame_head2 = file("bin/web/html/frame_head2", "r").readlines()
    for line in frame_head2:
        self.wfile.write(line)
    currentdata = file(textfile, "r").readlines()
    for line in currentdata:
        self.wfile.write(line + "<br>")
    frame_foot = file("bin/web/html/frame_foot", "r").readlines()
    for line in frame_foot:
        self.wfile.write(line)
    load_footer(self)

# Common task code, displays 'finished' message
def dofinishedpost(self):
    load_header(self)
    load_nav(self)
    finishedpost = file("bin/web/html/finished", "r").readlines()
    for line in finishedpost:
        self.wfile.write(line)
    load_footer(self)


# Common task code, performs exploitation tasks
def doexploitpost(self):
    content_length = string.atoi(self.headers.dict["content-length"])
    raw_post_data = self.rfile.read(content_length)
    raw_post_data = re.split('=|&', raw_post_data)
    self.send_response(200)
    self.end_headers()
    ipaddr = raw_post_data[1].rstrip()
    ipaddr = ipaddr.replace("+", " ")
    dofinishedpost(self)
      
# Common error message code
def showposterror(self):
    print "Exiting Fast-Track Web GUI.."
    print "\nType <ctrl>-c again to exit Fast-Track Web Gui.."
