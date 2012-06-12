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

import socket
import os
import re
import sys

from protocol_logic.sip_utilities import SIPCrashDetector

class TortureMessage:
    def __init__(self, data, name, type, is_invite=False, invite_details=[]):
        '''
        Represents a torture message

        @type data: String
        @param data: The data of the torture message
        @type name: String
        @param name: The name of the test case
        @type type: String
        @param name: Either 'valid' or 'invalid'
        @type is_invite: Boolean
        @param is_invite: Whether the message is an INVITE or not
        @type invite_details: List
        @param invite_details: The details from the INVITE necessary to cancel
        it
        '''

        self.data = data
        self.name = name
        self.type = type
        self.response = ""
        self.is_invite = is_invite
        self.invite_details = invite_details

    def get_data(self):
        '''
        Returns the data of the torture message

        @rtype: String
        @return: The data of the torture message
        '''
        
        return self.data

class Dispatcher:
    def __init__(self, host, port, messages, proto="udp", timeout="3.0", \
        crash_detection=False):
        '''
        Handles the dispatching of a group of SIP torture messages extracted
        from RFC 4475
        
        @type host: String
        @param host: The host to send the test messages to
        @type port: Integer
        @param port: The port to send the test messages to
        @type messages: Dictionary
        @param messages: A dictionary containing lists of valid and invalid
        test messages
        @type proto: String
        @param proto: (Optional, def=udp) The protocol to encapsulate the test
        messages in
        @type timeout: Float
        @param timeout: (Optional, def=3.0) Timeout for all socket operations
        @type crash_detection: Boolean
        @param crash_detection: (Optional, def=False) Attempt to detect crashes
        using OPTIONS probes or not
        '''
        
        self.host = host
        self.port = port
        self.proto = proto
        self.messages = messages
        self.timeout = timeout
        self.last_recv = ""
        self.crash_detection = crash_detection
        if self.crash_detection:
            self.crash_detector = SIPCrashDetector(self.host, self.port, \
                                                   timeout)
                    
    def __target_responding(self):
        '''
        Attempts to detect if the target application has crashed using the
        SIPCrashDetector class
        '''

        return self.crash_detector.is_responding()

    def __send(self, torture_msg):
        '''
        Send a torture message

        @type torture_msg: TortureMessage
        @param torture_msg: The torture message to be sent
        '''

        data = torture_msg.get_data()
        
        if self.proto == "udp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            if len(data) > 9216:
                print "Too much data for UDP, truncating to 9216 bytes"
                data = data[:9216]
            sock.sendto(data, (self.host, self.port))
            try:
                self.last_recv = sock.recvfrom(4096)[0]
            except Exception, e:
                self.last_recv = ""
            print '[=] Response : ' + self.last_recv
        elif self.proto == "tcp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((self.host, self.port))
            total_sent = 0
            while total_sent < len(data):
                sent = sock.send(data[totalSent:])
                if sent == 0:
                    raise RuntimeError("Error on socket.send()")
                total_sent += sent
            try:
                self.last_recv = sock.recv(4096)
            except Exception, e:
                self.last_recv = ""

    def dispatch(self, type="all"):
        '''
        Dispatch all the test messages of which match the type

        @type type: String
        @param type: (Optional, def=all) The type of messages to send. Can be 
        'all', 'valid' or 'invalid'
        '''
        
        valid_msgs = self.messages['valid']
        invalid_msgs = self.messages['invalid']
        
        if type == "all" or type == "valid":
            print '[+] Sending VALID messages'
            for msg in valid_msgs:
                print '[-] Sending ' + msg.name
                self.__send(msg)
                msg.response = self.last_recv

                if self.crash_detection:
                    if not self.__target_responding():
                        print "Possible crash detected after test" + \
                        msg.name
                        raw_input("Press any key to continue testing.....")

        if type == "all" or type == "invalid":
            print '[+] Sending INVALID messages'
            for msg in invalid_msgs:
                print '[-] Sending ' + msg.name
                self.__send(msg)
                msg.response = self.last_recv
                
                if self.crash_detection:
                    if self.__detect_crash():
                        print "Possible crash detected after test" + \
                        msg.name
                        raw_input("Press any key to continue testing.....")

class Parser:
    def __init__(self, directory):
        '''
        A parser for SIP test cases. Creates TortureMessage objects and stores
        them in a dictionary.
        
        @type directory: String
        @param directory: The directory in which to search for the SIP test
        cases
        '''

        self.directory = directory
        self.messages = {'valid' : [],
                        'invalid' : [],
                        }

    def parse(self):
        '''
        Parses all the files in a given directory for valid/invalid SIP test
        cases. The files are identified as valid/invalid based on the filename.
        Files that are valid should have the extension '.valid' and invalid
        files the extension '.invalid'

        @rtype: Dictionary
        @return: A dictionary of valid and invalid TortureMessage
        @todo: Extract the REGISTER tests from RFC 4475 and save them along
        with the other tests
        '''
        
        dirList = os.listdir(self.directory)
        for fname in dirList:
            if fname.find('.svn')!= -1:
                continue
            file = open(self.directory + '/' + fname, 'r')
            msg = self.__extract_packet(file)
            file.close()
            # detect INVITE messages so we can CANCEL them
            invite_msg = False
            invite_details = [] 
            '''
            Comment this stuff back in for cancelling sent INVITES
            if msg.find('INVITE') != -1:
                invite_msg = True
                invite_details = self.__extract_invite_details(msg)
            '''
            
            if fname.find('.valid') != -1:
                torture_msg = TortureMessage(msg, fname, 'Valid', \
                invite_msg, invite_details)
                self.messages['valid'].append(torture_msg)
            elif fname.find('.invalid') != -1:
                torture_msg = TortureMessage(msg, fname, 'Invalid', \
                invite_msg, invite_details)
                self.messages['invalid'].append(torture_msg)

        return self.messages

    def __extract_invite_details(self, msg):
        '''
        Parses out the details required to cancel an invite request

        @type msg: String
        @param msg: A SIP message

        @rtype: List
        @return: A list containing the details from the SIP message requires to
        cancel it
        
        @todo: Fix the regex's to work on the more screwed up test messages
        '''
        try:
            call_id = re.search('Call-ID\s*:\s*([\d\w@\.]+)', msg, re.IGNORECASE).group(1)
            uri = re.search('INVITE\s+([\d\w@\.:;-]+)\s+SIP/\d\.0', msg, re.IGNORECASE).group(1)
            to = re.search('To\s*:[\s*|\n |\n    ](.*)', msg, re.IGNORECASE).group(1)
            cseq_num = re.search('Cseq\s*:\s*(\d)+', msg, re.IGNORECASE).group(1)
            from_ = re.search('From\s*:\s*(.*)', msg, re.IGNORECASE).group(1)
        except IndexError, e:
            return None

        return [uri, call_id, to, cseq_num, from_]
        
    def __extract_packet(self, file):
        '''
        Parses the data in the file according to a set of rules to create 
        a packet that conforms with the intentions of RFC 4475

        The tags <allOneLine>, <hex> and <repeat> are parsed in accordance
        with RFC 4475
        
        @type file: File
        @param file: A file object containing a SIP message from RFC 4475

        @rtype: String
        @return: The parsed SIP packet
        '''

        # strip out any whitespace from the end of lines
        line_list = [line.rstrip() for line in file]
        packet = []
        x = 0
        while x < len(line_list):
            if line_list[x] == '<allOneLine>':
                y = x
                while line_list[y] != '</allOneLine>': 
                    y += 1
                x += 1
                line = ''.join(line_list[x: y])
                x = y + 1
            else:
                line = line_list[x]
                x += 1

            # the order of these parsings is important
            ctr = 0
            while line.find('<repeat') != -1:
                line = self.__parse_repeat(line)
            while line.find('<hex>') != -1:
                line = self.__parse_hex(line)

            packet.append(line)

        # end of packet == \r\n\r\n
        packet.append('\r\n')
        return '\r\n'.join(packet)

    def __parse_hex(self, line):
        '''
        Parses a line that contains the <hex> tag

        @type line: String
        @param line: The line containing the <hex> tag
        
        @rtype: String
        @return: The line with the tags removed and the string between them
        replaced with the correct hex digits
        '''
        
        x = 0
        # save these for later
        pre = line[:line.find('<hex')]
        post = line[line.find('</hex>') + 6:]
        
        line = line[line.find('<hex>') + 5:line.find('</hex>')]
        new_line = []
        while x < len(line):
            # get the next two hex digits
            tmp = ''.join(line[x:x+2])
            escaped = ('\\x' + tmp).decode('string_escape')
            new_line.append(escaped)
            x += 2
            
        return pre + ''.join(new_line) + post

    def __parse_repeat(self, line):
        '''
        Parses a line that contains the <repeat> tag

        @type line: String
        @param line: The line containing the <repeat> tag
        
        @rtype: String
        @return: The line with the tags removed and the string between them
        replaced with repeated sequence 'count' number of times
        '''
        
        # save these for later
        pre = line[:line.find('<repeat')]
        post = line[line.find('</repeat>') + 9:]

        m = re.search('<repeat count=(\d+)>(.*?)</repeat>', line)
        count = int(m.group(1))
        text = m.group(2)
       
        return pre + text*count + post
