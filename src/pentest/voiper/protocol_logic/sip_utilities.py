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

import select
import threading
import re
import time
import string
import random
import os

from Queue import Queue

from socket import *

from misc.utilities import Logger

class SIPMessageGenerator:
    def __init__(self):
        '''
        This class parses SIP messages and extracts the values of the
        attributes, it the fills in a given response/request with these values
        '''
        
        self.regex_dict = {'[BRANCH]' : r'branch\s*=\s*([\d\w-]+)',
                    '[FROMTAG]' : r'From.*;tag=([\w\d]+)',
                    '[CALL-ID]' : r'Call-ID\s*:\s*(\S+)',
                    '[CSEQ-NUM]' : r'CSeq\s*:\s*(\d+?)',
                    '[EXPIRES]' : r'Expires\s*:\s*(\d+)',
                    '[TO]' : 'To\\s*:\\s*(.*)\r\n',
                    '[TO-NOTAG]' : r'To\s*:\s*([\w\d\.:<>@]+=);?',
                    '[FROM]' : 'From\\s*:\\s*(.*)\r\n',
                    '[SIP-URI]' : \
                    r'[INVITE|CANCEL|REGISTER|OPTIONS]\s+(\S*)\s+SIP/2.0',
                    '[VIA]' : 'Via\\s*:\\s*([^(\r\n)]+)',
                    '[VIA-URI]' : r'Via\s*:\s*([\w\d\.:<>@/ ]+);',
                    }
    
    def generate(self, parse_msg, fill_msg, keys=None):
        '''
        Parses parse_msg for the all values defined in self.regex_dict and
        fills them into a template provided by fill_msg
        
        @type parse_msg: String
        @param parse_msg: The SIP message to parse
        @type fill_msg: String
        @param fill_msg: The SIP message to fill
        @type keys: List
        @param keys: The keys to fill from self.regex_dict
        
        
        @rtype: String
        @return: The filled in request/response
        '''

        tmp_dict = {}
        self.parse(parse_msg, tmp_dict, keys)
        return self.fill(fill_msg, tmp_dict)
        
    def parse(self, msg, dict, keys):
        '''
        Parses msg for the keys specified in dict and sets the value of the key
        to the value parsed from msg

        @type msg: String
        @param msg: The SIP message to parse
        @type dict: Dictionary
        @param dict: A dictionary who's keys correspond to the keys in
        self.regex_dict that you want to parse from the message. It will be
        filled with the values from msg
        @type keys: List
        @param keys: The keys to fill from self.regex_dict
        '''

        if keys == None:
            keys = self.regex_dict.keys()
            
        for regex_name in keys:
            regex = self.regex_dict[regex_name]
            value = re.search(regex, msg, re.IGNORECASE)
            if value and len(value.groups()) != 0:
                dict[regex_name] = value.group(1)
        
    def fill(self, msg, dict):
        '''
        Fills the msg with the data from dict by replacing the values in msg
        that correspond to the keys in dict
        
        @type msg: String
        @param msg: The request/response to fill in
        @type dict: Dictionary
        @param: The dictionary containing the data to insert

        @rtype: String
        @return: The filled in request/response
        '''
        
        for replace_name in dict.keys():
            if dict[replace_name] != '':
                msg = msg.replace(replace_name, dict[replace_name])

        return msg

class SIPInviteCanceler:
    def __init__(self, host, port, timeout):
        '''
        Cancels a given INVITE request. The publicly accessible cancel method
        puts the message to be cancelled onto a queue. Worker threads read from
        this queue and cancel the given messages after a specified timeout
        (default = 2.0 seconds). It also attempts to ACK any responses received
        to keep communications as normal as possible

        @type host: String
        @param host: The host to send the CANCEL to
        @type port: Integer
        @param port: The port to send the CANCEL to
        @type timeout: Float
        @param timeout: The timeout to wait before cancelling the INVITE
        '''

        self.host = host
        self.port = port
        self.queue = Queue(0)
        self.timeout = timeout
        self.sip_parser = SIPMessageGenerator()
        # get default logging method
        self.log = Logger().log
        self.alive = True
        
        # spawn off 30 worker threads
        # should never need more than timeoute * (fuzz msgs per second) + 1 or so
        self.num_threads = 30
        for x in range(self.num_threads):
            threading.Thread(target=self.__cancel).start()
     
        self.ack_msg = ''.join(['ACK [SIP-URI] SIP/2.0\r\n',
            'To: [TO]\r\n',
            'From: [FROM]\r\n',
            'Call-ID: [CALL-ID]\r\n',
            'CSeq: 1 ACK\r\n',
            'Via: [VIA]\r\n',
            'Max-Forwards: 70\r\n',
            'Content-Length: 0\r\n\r\n'])
        
        self.cancel_template = '\r\n'.join(['CANCEL [SIP-URI] SIP/2.0',
            'CSeq: [CSEQ-NUM] CANCEL',
            #'Via: [VIA-URI];branch=[BRANCH];rport',
            'Via: [VIA]',
            'From: [FROM]',
            'Call-ID: [CALL-ID]',
            #'To: [TO-NOTAG]',
            'To: [TO]',
            'Max-Forwards: 70',
            'Contact: <sip:nnp@192.168.3.104:5068;transport=udp>']) + '\r\n\r\n'

        self.ack_msgs = ['481 Call Leg/Transaction Does Not Exist',
                        '488 Not Acceptable Here',
                        '487 Request Terminated',
                        '603 Decline',
                        '486 Busy Here',
                        '400 Bad Request',
                        ]
    
    def cancel(self, sock, invite_data):
        '''
        Places a cancel for invite_data onto the cancellation queue
        
        @type sock: Socket
        @param sock: The socket that sent the INVITE request
        @type invite_data: String
        @param invite_data: An invite message used to initialise a call

        @todo: Add TCP support
        '''

        cancel_msg = self.sip_parser.generate(invite_data, self.cancel_template,
                                         ['[SIP-URI]', '[CSEQ-NUM]', '[VIA]',
                                          '[BRANCH]', '[FROM]', '[CALL-ID]',
                                          '[TO]'])
               
        # truncate the data for udp sending
        if len(cancel_msg) > 65507:
            cancel_msg = cancel_msg[:65507]
        
        self.queue.put((sock, cancel_msg))

    def kill_cancel_threads(self):
        for x in range(self.num_threads):
            self.queue.put((None, None))
            
    def __cancel(self):
        '''
        This method attempts to cancel the call initiated by sending
        invite_data. It simply replaces the INVITE keyword with CANCEL and
        resends the data. It runs as a worker thread and gives a timeout of
        self.timeout before cancelling the INVITE

        @todo: Remove 'select' statement. Pointless when using UDP
        '''
        
        while 1:
            invite_sock, cancel_msg = self.queue.get()
            # die when done fuzzing
            if not (invite_sock or cancel_msg):
                break

            # allow sufficient time for the INVITE to be processed
            time.sleep(self.timeout)
            cancel_sock = socket(AF_INET, SOCK_DGRAM)
            cancel_sock.connect((self.host, self.port))
            cancel_sock.send(cancel_msg)

            # Some implementations of SIP don't function correctly if they
            # don't receive an ACK
            for x in range(5):
                # Use select to avoid unecessary CPU hogging
                ready_to_read, ready_to_write, brokeded = \
                    select.select([cancel_sock, invite_sock], [], [], \
                    self.timeout)
                if len(ready_to_read) != 0:
                    for read_sock in ready_to_read:
                        try:
                            data, addr = read_sock.recvfrom(65507)
                        except error:
                            self.log("SocketError cancelling request. Ensure target is listening.")
                            continue
                        for response_line in self.ack_msgs:
                            if data.find(response_line) != -1:
                                # according to the rfc the to field should come
                                # from the response whereas the call id, from, via and request
                                # uri should come from the INVITE request, which is
                                # the same as the CANCEL here
                                response = self.sip_parser.generate(data, \
                                    self.ack_msg, ['[TO]'])
                                response = self.sip_parser.generate(cancel_msg, \
                                    response, ['[CALL-ID]', '[FROM]', \
                                    '[SIP-URI]', '[VIA]'])
                                invite_sock.send(response[:65507])
                else:
                    # nothing recieved, time to leave
                    break
            
            cancel_sock.close()
            invite_sock.close()
        
class SIPCrashDetector:
    def __init__(self, host, port, timeout=2.0):
        '''
        Attempts to detect a SIP device malfunctioning by sending an OPTIONS
        message to the host specified. All SIP implementations should respond
        to this when functioning correctly. If no response is received another
        request is sent, if this is also unanswered we assume the target has
        died a grisly death

        @type host: String
        @param host: The host to target
        @type port: Integer
        @param port: The port to target
        @type timeout: Float
        @param timeout: The timeout for waiting for a response to the probe
        '''

        random.seed(1986)
        
        self.host = host
        self.port = port
        self.timeout = timeout
        # get default logging method
        self.log = Logger().log
        self.alive = True

        self.options_msg = ''.join(['OPTIONS sip:user@example.com SIP/2.0\r\n',
            'To: sip:user@example.com\r\n',
            'From: sip:caller@192.168.3.102;tag=[RAND]\r\n',
            'Call-ID: crashdetection.[RAND]\r\n',
            'CSeq: [CSEQ-RAND] OPTIONS\r\n',
            'Via: SIP/2.0/UDP host1.example.com;branch=z9hG4bKk[RAND]\r\n',
            'Max-Forwards: 70\r\n',
            'Content-Length: 0\r\n\r\n'])
        
    def is_responding(self):
        '''
        Sends the OPTIONS message and waits for a response. We don't bother
        checking if the response to recieved is to the OPTIONS or to the INVITE
        as any sort of response should indicate the target is still alive.

        @type sock: Socket
        @param sock: The socket used to send the last fuzz case

        @rtype: Boolean
        @return: A boolean value indicating whether the target has is
        responding or not
        
        @todo: Add TCP support
        '''

        # Ekiga seems to send 200 OK responses back to 5060 regardless of the
        # source port. Possibly should move this to the __init__
        recv_sock = socket(AF_INET, SOCK_DGRAM)
        recv_sock.setblocking(0)
        recv_sock.settimeout(self.timeout)
        recv_sock.bind(('0.0.0.0', 5060))
       
        id_unique = ''.join([random.choice(string.letters) for x in xrange(32)]) 
        send_data = self.options_msg.replace('[CSEQ-RAND]', \
            str(random.randint(1000, 100000)))
        send_data = send_data.replace('[RAND]', id_unique) 
        
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.settimeout(self.timeout)
        sock.connect((self.host, self.port))
        sock.send(send_data)
        recv_sock.setblocking(0)

        responding = False
        
        # this checks the next 10 responses for the 200 OK response to the OPTIONS
        # if its not found we assume something went wrong - brutish but effective
        for x in range(10):
            ready_to_read, ready_to_write, brokeded = select.select([recv_sock, \
                sock], [], [], self.timeout)

            if len(ready_to_read) != 0:
                for read_sock in ready_to_read:
                    try:
                        data, addr = read_sock.recvfrom(65507)
                    except error:
                        self.log("SocketError when checking target status. Ensure target is listening.")
                        continue
                    if data:
                        responding = True
                        break
                if responding == True:
                    break
            else:
                # nothing was received and a correct response still hasn't been
                # received so we assume something has gone wrong
                break
                
        recv_sock.close()
        sock.close()
        
        return responding

class SIPRegistrar:
    def __init__(self, ip,  port):
        '''
        This class plays the part of a registrar and allows clients to register
        with the fuzzer. This is required for clients that don't support P2P
        SIP calls and are required to first register with a service provider.
        
        @type ip: String
        @param ip: The IP address to listen on
        @type port: Integer
        @param port: The port to listen on
        '''
        
        self.ip = ip
        self.port = port
        self.sip_parser = SIPMessageGenerator()
        # get default logging method
        self.log = Logger().log
        
        self.register_ok_msg = ''.join(['SIP/2.0 200 OK\r\n',
                'Via: SIP/2.0/UDP someserver.bleh.com:5060;branch=[BRANCH]\r\n',
                'To: user <sip:bleh@bleh.com>;tag=4343454\r\n',
                'From: user <sip:bleh@bleh.com>;tag=[FROMTAG]\r\n',
                'Call-ID: [CALL-ID]\r\n',
                'CSeq: [CSEQ-NUM] REGISTER\r\n',
                'Contact: <sip:bleh@bleh.com>\r\n',
                'Expires: [EXPIRES]\r\n',
                'Content-Length: 0\r\n\r\n'])

        self.attribute_dict = {'[BRANCH]' : '',
                    '[FROMTAG]' : '',
                    '[CALLID]' : '',
                    '[CSEQ]' : '', 
                    '[EXPIRES]' : '', 
                    }
 
    def waitForRegister(self):
        '''
        This function sits and waits for a connection on 5060 containing a
        REGISTER request and responds authorizing the connection
        '''
        
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind((self.ip, self.port))

        while 1:
            data, incoming_addr = sock.recvfrom(1024)
            if data.find('REGISTER') != -1:
                self.log('[+] Register request received from ' + \
                    str(incoming_addr))
                self.log('[+] Sending 200 OK response')
                self.allowRegister(incoming_addr, data)
                break

        sock.close()

    def allowRegister(self, host, register_request):
        '''
        This responds to a REGISTER request with a 200 OK response.

        @type host: Tuple
        @param host: A tuple containing the IP and port to respond to the
        request on
        @type register_request: String
        @param register_request: The original register request from the client
        '''
       
        response = self.sip_parser.generate(register_request,\
            self.register_ok_msg) 
        reply_sock = socket(AF_INET, SOCK_DGRAM)
        time.sleep(2)
        reply_sock.sendto(response, host)
        reply_sock.close()
