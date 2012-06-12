'''
This file is part of VoIPER.

VoIPER is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

VoIPER is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with VoIPER.  If not, see <http://www.gnu.org/licenses/>.

Copyright 2008, http://www.unprotectedhex.com
Contact: nnp@unprotectedhex.com
'''

import time
import os

from socket import *

from protocol_logic.sip_utilities import SIPInviteCanceler

class CrashFile:
    def __init__(self, name):
        self.name = name
        self.contents = ''
        
class CrashFileReplay:
    def __init__(self, host, port, timeout=0):
        '''
        Takes a directory and allows the user to replay every file with the
        .crashlog extension in it

        @type host: String
        @param host: The host to send the crash files to
        @type port: Integer
        @param: The port to send the crash files to
        @type timeout: Integer
        @param timeout: (Optional) Timeout to send a cancel
            for the replayed request if possible
        '''

        self.host = host
        self.port = port
        self.timeout = timeout
        self.crash_files = []

        if timeout != 0:
            self.canceler = SIPInviteCanceler(host, port, timeout)

        self.poc_template = '''# Created by VoIPER
# http://www.unprotectedhex.com
import sys
from socket import *

if len(sys.argv) != 3:
    sys.exit(-1)

host = sys.argv[1]
port = int(sys.argv[2])

kill_msg = \'\'\'PLACEHOLDER\'\'\'

print '[+] Host : ' + host
print '[+] Port : ' + str(port)

s = socket(AF_INET, SOCK_DGRAM)
print 'Sent ' + str(s.sendto(kill_msg, (host, port))) + ' bytes'
s.close()
            '''

    def __send_cancel(self, sock, data):
        '''
        @type sock: Socket
        @param sock: The socket used to send 'data'
        @type data: String
        @param data: The data sent to the target constituting the request to be cancelled
        '''

        self.canceler.cancel(sock, data)
        
    def parse_directory(self, directory):
        '''
        Parses the directory specified for crashlog
        files and adds them to a class list

        @type directory: String
        @param directory: The directory containing the .crashlog files to replay
        '''

        self.directory = directory
        dirList = os.listdir(directory)
        for fname in dirList:
            if fname.find('.crashlog') != -1:
               self.crash_files.append(CrashFile(fname))

    def replay_name(self, name):
        '''
        Sends the crashlog specified by name to the host:port

        @type name: String 
        @param name: The path of the crashlog file to replay 
        '''
        
        s = socket(AF_INET, SOCK_DGRAM)
        file = open(name, 'r')
        contents = file.read()
        file.close()
        s.sendto(contents, (self.host, self.port))
        if self.timeout != 0: 
            self.__send_cancel(s, contents)
            print "[+] Request is being cancelled. Waiting for %d + 1 seconds" % self.timeout
            time.sleep(self.timeout+1)
        else:
            # the canceller will take care of this otherwise
            s.close()
    
    def replay_num(self, num):
        '''
        Sends the crashlog specified by num to the host:port

        @type num: Integer
        @param num: Index into the crash_files array of the file to send
        '''

        s = socket(AF_INET, SOCK_DGRAM)
        file = open(self.directory + '/' + self.crash_files[num].name, 'r')
        contents = file.read()
        file.close()
        s.sendto(contents, (self.host, self.port))
        if self.timeout != 0: 
            self.__send_cancel(s, contents)
            print "[+] Request is being cancelled. Waiting for %d + 1 seconds" % self.timeout
            time.sleep(self.timeout+1)
        else:
            # the canceller will take care of this otherwise
            s.close()

    def create_poc(self, crash_file_name, out_file_name):
        '''
        Creates a self contained proof of concept python script for the
        give crash file. If a timeout was specified when creating this class
        then the cancel request will be included in that POC with the given
        timeout

        @type crash_file_name: String
        @param crash_file_name: The name of the file that caused a crash
        @type out_file_name: String
        @param out_file_name: The name of the file to create
        '''

        crash_file = open(crash_file_name, 'r')
        crash_contents = crash_file.read()
        crash_file.close()
        out_file = open(out_file_name, 'wb')

        out_data = self.poc_template.replace('PLACEHOLDER', crash_contents)
        out_file.write(out_data)
        out_file.close()
        
