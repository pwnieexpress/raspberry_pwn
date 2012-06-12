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

import sys
import os
import string
import socket
import time

# Props to Pedram Amini and Aaron Portnoy for creating such a great framework
sys.path.append(''.join([os.getcwd(), '/sulley']))
from sulley import *

from protocol_logic.sip_transaction_manager import SIPTransactionManager

from protocol_logic import sip_agent
from protocol_logic.sip_agent import SIPCancel
from protocol_logic.sip_agent import SIPAck
from protocol_logic.sip_agent import SIPAgent
from protocol_logic.sip_agent import SIPRegister
from protocol_logic.sip_agent import SIPOptions
from protocol_logic.sip_agent import SIPInvite

from protocol_logic import sip_parser
from misc.utilities import Logger

from random import Random
from Queue import Queue   

class AbstractFuzzer:    
    def __init__(self, audit_folder, proto, host, port, crash_detection, skip=0, start_command='', stop_command='TERMINATE_PID', \
                 procmon_port=26002, restart_interval=0, log_function=None, trans_in_q=None, max_len=8192, config_options=None):
        '''
        Abstract class to be implemented by the various fuzzers. Does not
        provide any 'fuzzing' implementation, just utility functions.
        Basically an abstraction around a Sulley fuzzer to make things a
        bit nicer for integration and management of a variety of requests.

        @type audit_folder: String
        @param audit_folder: The folder to which session information is stored
        @type proto: String
        @param proto: (Optional, def=udp) The protocol to use. TCP or UDP
        @type host: String
        @param host: The host to target
        @type port: Integer
        @param port: The port to target
        @type crash_detection: Integer
        @param crash_detection: Controls crash detection settings. 0 -
        Disabled, 1 - Logging enabled, 2 - Logging enabled and fuzzer paused, 3 - use process monitoring scripts in sulley/ subdirectory
        @type skip: Number of tests to skip
        @param skip: Integer
        @type start_command: String
        @param start_command: The command used on the target system to start the target program
        @type stop_command: String
        @param stop_command: (Optional, def=TERMINATE_PID)The command used on the target system to stop the target program
        @type procmon_port: Integer
        @param procmon_port: (Optional, def=26002)The port the remote process monitoring script is listening on
        @type log_function: Function
        @param log_functin: A function taking a string and a log level that the class will use to log data
        @type restart_interval: Integer
        @param restart_interval: The interval with which to restart the target application. Only applies with crash_detection == 3
        @type trans_in_q: Queue
        @param trans_in_q: A queue connected to the transaction manager onto which sent fuzz cases can be placed
        @type max_len: Integer
        @param max_len: The maximum length of fuzz strings to use        
        @type max_len: Integer
        @param max_len: The maximum length of fuzz strings to use
        '''
        
        self.audit_folder = audit_folder
        self.proto = proto.lower()
        self.host = host
        self.port = port
        self.crash_detection = crash_detection
        self.skip = skip
        
        # This actually causes me physical discomfort!
        # The reason I've had to resort to it is due to the way Sulley is set up
        # When you import your protocol mapping the strings are created; so to allow
        # the user to specify string length I have had to move that string generation
        # to another method, call it manually and then import the protocol mapping
        primitives.gen_strings(max_len)
        from requests import sip

        self.sess = sessions.session(session_filename=self.audit_folder + \
        '/sulley.session', skip=self.skip, proto=self.proto, audit_folder=self.audit_folder, \
        restart_interval=restart_interval, trans_in_q=trans_in_q)
        
        self.target = sessions.target(self.host, self.port)
        self.start_command = start_command
        self.stop_command = stop_command
        self.procmon_port = procmon_port
        self.using_GUI = False
        # this flag can be set by any of the functions in the post send list
        # to indicate they have verified the target is alive and the dedicated
        # crash detection code doesn't need to run
        self.target_alive = False
        # get default logging method. This can be overridden by a GUI interface
        if log_function:
            self.log = log_function
        else:
            self.log = Logger().log

        self.sess.log = self.log

        # this is used to schedule things like REGISTER at different intervals
        self.sent_request_count = 0

        if self.crash_detection == 3:
            self.target.procmon = pedrpc.client(self.host, self.procmon_port)
            self.target.procmon_options = \
                       {
                           "stop_commands" : [self.stop_command],
                           "start_commands" : [self.start_command],
                        }
        # the following two variables are lists of functions that will be
        # registered as pre/post send methods with Sulley
        self.pre_send_functions = []
        self.post_send_functions = []
        self.sess.pre_send = self.pre_send
        self.sess.post_send = self.post_send
        # The transaction manager will handle this 
        self.sess.close_socket = self.empty_close_func
        
        if config_options != None:
            for option in config_options.keys():
                print 'setting %s to %s' % (option, config_options[option])
                setattr(self, option, config_options[option])
 
    def fuzz(self):
        pass

    def pre_send(self, sock):
        '''
        Iterates through the list of registered pre send functions and calls
        them 

        @type sock: Socket
        @param sock: Socket used to send the last test case
        '''
        
        for function in self.pre_send_functions:
            function(sock)

    def post_send(self, sock):
        '''
        Iterates through the list of registered post send functions and calls
        them 

        @type sock: Socket
        @param sock: The socket used to send the last test case
        '''

        self.target_alive = False
        for function in self.post_send_functions:
            function(sock)
      
        # if there are no methods reading from the queue then there will be a 
        # backlog of responses
        if len(self.pre_send_functions) == 0 and len(self.post_send_functions) == 0:
            self.sip_agent.flush_queue()

    def detect_crash(self):
        '''
        Interface method to be implemented by child classes
        '''
        pass

    def empty_close_func(self, socket):
        '''
        Procedure with no functionality. 
        '''
        pass

    def pause_GUI(self):
        self.log("The GUI implementation should have overridden this method")

################################################################################

class AbstractSIPFuzzer(AbstractFuzzer):
    def __init__(self, audit_file, proto, host, port, crash_detection, skip=0, start_command='TERMINATE_PID', stop_command='', 
                 procmon_port=26002, restart_interval=0, log_function=None, max_len=8192, config_options=None):
        '''
        Abstract parent class for all SIP based fuzzers. Simply updates the default
        fuzzer to include SIP specific crash detection
        '''

        # the fuzzer will put requests it sends onto this queue so they can be monitored
        # by the transaction manager
        self.request_q = Queue(0)
        AbstractFuzzer.__init__(self, audit_file, proto, host, port, 
            crash_detection, skip, start_command, stop_command, procmon_port,
            restart_interval, log_function, self.request_q, max_len, config_options)

        # queue onto which transactions to be added are put
        self.response_q = Queue(0)
        self.sip_agent = SIPAgent(self.response_q, self.request_q)
        self.ack = SIPAck()
        self.cancel = SIPCancel()
        self.options = SIPOptions()
        self.register = SIPRegister()
        self.invite = SIPInvite()
        self.curr_invite_branch = None
        
        self.curr_invite_branch = None
        self.curr_cd_branch = None

        self.local_ip = socket.gethostbyname(socket.gethostname())        

        SIPTransactionManager(self.request_q, self.response_q).start()

        if self.crash_detection > 0 and self.crash_detection < 3:
            self.options_transaction_dict = {sip_parser.r_SEND :
                                             (self.options.process,
                                               {
                                                   sip_parser.r_1XX : (None, None),                                                                             
                                                   sip_parser.r_2XX : (None, None),  
                                                   sip_parser.r_3XX : (None, None),                                                                           
                                                   sip_parser.r_4XX : (None, None),
                                                   sip_parser.r_5XX : (None, None),
                                                   sip_parser.r_6XX : (None, None),                                                                             
                                                }
                                               )
                                             }
            
            self.invite_dict = {sip_parser.r_SEND :
                             (self.invite.process,
                              {
                                  sip_parser.r_1XX :
                                  (self.cancel.process,
                                   {
                                       sip_parser.r_1XX : (None, None),
                                       sip_parser.r_2XX : (None, None),                           
                                       sip_parser.r_6XX : (self.ack.process, None),
                                       sip_parser.r_4XX : (self.ack.process, None)
                                       }
                                   )
                               }
                              )
                            }
            
            self.post_send_functions.append(self.detect_crash)

        if self.do_register:
            self.register_dict = {sip_parser.r_SEND :
                             (self.register.process,
                              {
                                  sip_parser.r_401 :
                                  (self.register.process,
                                   {
                                       sip_parser.r_2XX : (self.sip_agent.require, None),
                                       sip_parser.r_1XX : (None, None)
                                       }
                                   ),
                                  sip_parser.r_1XX : (None, None),
                                  # If a password is not required then no need for a second request
                                  sip_parser.r_2XX : (self.sip_agent.require, None),
                               }
                              )
                             }
            
            self.pre_send_functions.append(self.sip_register)
            
    def sip_register(self, sock):
        '''
        Function to register with the registrar. Sock is the socket
        provided by Sulley that the next fuzz request will be sent through
        but is not used here
        '''
       
        # only re-register every 50 requests
        if self.sent_request_count % 50 == 0:
            result, self.curr_register_branch = self.sip_agent.process_transaction(
                self.register_dict,
                {'user' : self.user,
                 'password' : self.password, 
                 'host' : self.host,
                 'port' : self.port}
                )        
        
        self.sent_request_count += 1

    def generate_unique_attributes(self, session, node, edge, sock):
        '''
        In SIP a number of fields need to be unique/random e.g branch. Without
        this some implementations freak out and don't function in a normal
        fashion, thus artificially interfering with the fuzzing process. The
        SIP rfc specifies cryptographically random values should be used but
        for our purposes the pseudo random values generated should do.
       
        @rtype: String
        @return: Returns the SIP message with the fields requiring random
        identifiers filled in correctly when possible i.e if they're not being
        fuzzed
        '''

        data = node.render()
        # branch
        if not self.curr_invite_branch:
            self.curr_invite_branch = ''.join(Random().sample(string.ascii_lowercase+string.digits, 32))
            
        data = data.replace('somebranchvalue', self.curr_invite_branch)
        data = data.replace('somefromtagvalue', self.curr_invite_branch)
        data = data.replace('somecallidvalue', self.curr_invite_branch)            

        # This stuff is new in this function and should be moved elsewhere
        # Works fine here for now though
        data = data.replace('TARGET_USER', self.target_user)
        data = data.replace('USER', self.user)
        data = data.replace('HOST', self.host)
        # For some legos we need to pass them a valid IP address
        # to begin with so they can fuzz it correctly but we still need
        # a recognisable IP to replace. Hopefully this one won't pop up
        # in a valid context. Hacky as fuck!
        data = data.replace('192.168.96.69', self.host)
        data = data.replace('192.168.99.99', self.local_ip)        
        data = data.replace('PORT', str(self.port))
        data = data.replace('LOCAL_IP', self.local_ip)
       
        return data
        
    def detect_crash(self, sock):
        '''
        This method is registered as the post-send callback with Sulley and
        attempts to detect crashes by sending an OPTIONS message to the target
        and waiting for a response. If no response is received it will notify
        the user and log the last request sent.

        @type sock: Socket
        @param sock: The socket used to send the last test case. Unused in this
        method but necessary as a parameter as it is passed to all post_send
        methods

        @todo: Change second crash detection message to something besides OPTIONS
        '''

        # if some other previous part of the session has verified the target is
        # alive then accept that
        if self.target_alive:
            return

        # To minimise the chance of a false positive two
        for x in range(2):
            res = self.send_options()
            if res != sip_agent.T_INCOMPLETE:
                self.target_alive = True
                break
            else:
                self.target_alive = False

        if not self.target_alive:
            self.log('[*] No response to OPTIONS based crash detection.')
            self.log('[*] Sleeping for 2 seconds and then attempting once more with INVITE')
            time.sleep(2)
            res = self.send_invite()
            if res != sip_agent.T_INCOMPLETE:
                self.target_alive = True            
            
        if not self.target_alive:
            self.log('\n[*] The target program has stopped responding')
            crash_log_name = self.audit_folder + '/' + \
                str(self.sess.fuzz_node.id) + '_' + \
                str(self.sess.total_mutant_index) + '.crashlog'
            crash_log = open(crash_log_name, 'w')
            crash_log.write(self.sess.fuzz_node.sent_data)
            crash_log.close()
            self.log('[*] Fuzz request logged to ' + crash_log_name)
            if self.crash_detection == 2:
                if self.using_GUI:
                    self.pause_GUI()
                else:
                    raw_input('\nPress the any key to continue\n')

    def send_options(self):
        print 'Sending options'
        res, self.curr_cd_branch = self.sip_agent.process_transaction(
            self.options_transaction_dict, {'host' : self.host,
                                            'port' : self.port,
                                            'user' : self.user,
                                            'target_user' : self.target_user}
            )

        return res

    def send_invite(self):
        print 'Sending invite'
        res, self.curr_cd_branch = self.sip_agent.process_transaction(
            self.invite_dict, {'host' : self.host,
                                'port' : self.port,
                                'user' : self.user,
                                'target_user' : self.target_user}
            )

        return res    
        
################################################################################

class AbstractSIPInviteFuzzer(AbstractSIPFuzzer):
    def __init__(self, audit_file, proto, host, port, crash_detection, skip=0, start_command='TERMINATE_PID', stop_command='', 
                 procmon_port=26002, restart_interval=0, log_function=None, max_len=8192, config_options=None):


        '''
        Abstract parent class for all SIP INVITE  based fuzzers. Updates the default
        SIP fuzzer to include CANCEL messages for the sent INVITES to prevent
        certain clients dying from INVITE floods (not really that interested in
        finding those ;) )
        '''
        
        AbstractSIPFuzzer.__init__(self, audit_file, proto, host, port,\
            crash_detection, skip, start_command, stop_command, procmon_port, \
            restart_interval, log_function, max_len, config_options)
        
       # The following mapping describes how we expect the transaction to go.
       # We wait for a 1XX provisional response, then send a CANCEL request.
       # After that we are expect a 200 response to the CANCEL as well as a
       # r_4XX, r_5XX or r_6XX response to the INVITE. The CANCEL and its
       # responses are technically a different transaction so I should probably
       # represent that here somehow but this works fine for now.
        
        self.cancel_transaction_dict = {sip_parser.r_1XX : (self.cancel.process,
                                                 {sip_parser.r_4XX : (self.ack.process,
                                                                    None),
                                                  sip_parser.r_5XX : (self.ack.process,
                                                                    None),                                                  
                                                  sip_parser.r_6XX : (self.ack.process,
                                                                    None),
                                                  sip_parser.r_2XX : (None, None),
                                                  }
                                                 ),
                                        sip_parser.r_4XX : (self.ack.process, None),
                             }
                          
        # this is a post send function that could also perform the role of crash detection so
        # put it at the start to try to kill two birds with the one stone
        # If self.do_cancel is false it is probably advisable to have the phone you are testing
        # set up to auto ignore the incoming call 
        if self.do_cancel:
            self.post_send_functions.insert(0, self.process_invite)
    
    def process_invite(self, sock):
        '''
        Calls an external class to cancel the last INVITE sent

        @type sock: Socket
        @param sock: The socket used to send the last test case
        '''

        res = self.sip_agent.process_transaction(self.cancel_transaction_dict, {'branch' : self.curr_cd_branch}) 
        if res[0] != sip_agent.T_INCOMPLETE:
            self.target_alive = True
        else:
            self.target_alive = False
        # if the transaction ended in the state T_COMPLETE or T_INVALID we know the target is
        # at least alive. Here is where I will include the option to check for T_INVALID as well
            
################################################################################
