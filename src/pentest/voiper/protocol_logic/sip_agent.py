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
import threading
import sip_parser
import random
import string
import socket
import hashlib  # import md5 - this is deprecated - dookie
import sys

from Queue import Queue
from random import Random

from sip_transaction_manager import SIPTransaction
from sip_transaction_manager import TData
from sip_transaction_manager import EXTERNAL, GENERATOR
from sip_parser import SIPParser

T_INCOMPLETE = 1
T_INVALID_STATE = 2
T_COMPLETE_OK = 3

class SIPAgent:
    def __init__(self, response_q, request_q):
        '''
        This class is responsible for playing the part of a SIP agent in a transaction.
        The process_transaction method takes a dictionary describing the transaction and
        attempts to process it. The dictionary describes expected response codes and the
        functions to be called when these response codes are detected.
        
        @type response_q: Queue
        @param response_q: A queue which we will read data from the network off
        @type request_q: Queue
        @param request_q: A queue which we will write any responses too
        '''
        
        self.sp = sip_parser.SIPParser()
        self.previous_got_response = True
        self.in_queue = response_q
        self.out_queue = request_q

    def process_transaction(self, t_dict, extra_params=None):    
        '''
        @type t_dict: Dictionary
        @param t_dict: A dictionary describing the possible states this transaction
            may traverse and what actions to take upon entering them. See
            fuzzer/fuzzer_parents.py for examples
        @type extra_params: Dictionary
        @param extra_params: A dictionary containing any possible extra paramaters
            transaction initiating methods might need e.g sending an OPTIONS

        @r_type: Integer
        @return: An integer describing the result of attempting to process the
            given t_dict
        '''

        #wait_time = self.calculate_wait_time(False, self.previous_got_response, 1)
        wait_time = .8
        status = None
        if extra_params != None and extra_params.has_key('branch'):
            curr_branch = extra_params['branch']
        else:
            curr_branch = None
            
        while status == None:
            possible_r_codes = t_dict.keys()
            if possible_r_codes[0] != sip_parser.r_SEND:
                # Attempt to get a response matching the r_codes we are expecting
                (sip_t, r_code) = self.get_transaction(self.in_queue, possible_r_codes, curr_branch, wait_time)
                if not curr_branch and sip_t:
                    curr_branch = sip_t.t_data_list[0].p_data[sip_parser.BRANCH]
                # Only proceed if the transaction is in a valid states. Unexpected
                # responses invalidate the transaction state
                if r_code in possible_r_codes:
                    action_tuple = t_dict[r_code]
                    method = action_tuple[0]
                                  
                    # Some requests can result in 2 responses. One of which may need no further
                    # processing. e.g CANCEL can result in a 200 OK which can be ignored and a 487
                    # which must be ACK'ed                    
                    if method == None:
                        any_actions = False
                        # check if any of the r_codes have actions associated with them.
                        # If the don't we assume the transaction is considered complete
                        # when any are received and we return. If they do then we just ignore
                        # this response and get the next one off the queue
                        for r_code in t_dict.keys():
                            if t_dict[r_code][0] != None:
                                any_actions = True
                        if any_actions:
                            continue
                        else:
                            # No actions at this level and we got a response
                            # so the transaction completed correctly
                            status = T_COMPLETE_OK
                            break

                    method(sip_t, self.out_queue, extra_params)
                    t_dict = action_tuple[1]
                    if not t_dict:
                        status = T_COMPLETE_OK
                else:
                    # if sip_t == None: The transaction didn't complete correctly. This
                    # is probably because the fuzz request was so messed up that it was
                    # ignored. Otherwise we got a response but it did not conform to our
                    # transaction description
                    if sip_t == None:
                        print >> sys.stderr,  'SA: T_INCOMPLETE'
                        status = T_INCOMPLETE
                    else:
                        print >> sys.stderr,  'SA: T_INVALID_STATE'
                        status = T_INVALID_STATE
            else:
                # Initiating transaction
                action_tuple = t_dict[sip_parser.r_SEND]
                method = action_tuple[0]
                # r_SEND means a new transaction is being created so update the branch
                curr_branch = method(None, self.out_queue, extra_params)
                t_dict = action_tuple[1]
                if not t_dict:
                    status = T_COMPLETE_OK

        # Clear any remaining requests from the queue so as not to interfere
        # with the processing of the next transaction
        self.flush_queue()
        
        # if t_dict != None then we didn't complete the transaction mapping
        return (status, curr_branch)

    def flush_queue(self):
        '''
        Method to ensure any messages remaining on the input queue that have
        not been consumed are removed

        @type queue: Queue
        @param queue: The queue to flush
        '''

        try:
            while 1:
                self.in_queue.get(False)
        except:
            pass
        
    def get_transaction(self, queue, r_codes, curr_branch, wait_time):
        '''
        Method that attempts to retrieve a message with the given r_code from
        the queue

        @type queue: Queue
        @param queue: The queue to read off
        @type r_codes: List
        @param r_codes: A list of response codes that are considered a valid
            match
        @type wait_time: Float
        @param wait_time: The time to wait for responses before returning. This will
            be approached in intervals of .1 of a second.
        '''
        
        sleep_time = .1
        q_r_code = None
        slept_for = 0

        print >> sys.stderr,  'wait time ' + str(wait_time)
        print >> sys.stderr,  'SA-EXPECTING ' + str(r_codes)
        while slept_for <= wait_time:
            sip_t = None
            try:
                sip_t = queue.get(False)
                last_recv = sip_t.t_data_list[len(sip_t.t_data_list)-1]
                q_r_code = last_recv.p_data[sip_parser.RCODE]
                # Check the response is for the transaction we're interested in
                if not curr_branch or last_recv.p_data[sip_parser.BRANCH].find(curr_branch) != -1:
                    print >> sys.stderr, 'SA-GOT-CORRECT-BRANCH'
                    try:
                        r_codes.index(q_r_code)
                        print >> sys.stderr,  'SA-GOT-CORRECT-R-CODE ' + str(q_r_code) + ' # ' + str(r_codes)
                        break
                    except ValueError:
                        # We got an unscheduled message. The transaction has proceeded into an
                        # unexpected state.
                        print >> sys.stderr,  'SA-GOT-UNEXPECTED-R-CODE ' + str(q_r_code) + ' # ' + str(r_codes)
                        #return (sip_t, q_r_code)
                else:
                    sip_t = None
                    q_r_code = None
            except:
                pass            

            time.sleep(sleep_time)
            slept_for += sleep_time
        
        if sip_t:
            self.previous_got_response = True
        else:
            self.previous_got_response = False
            
        return (sip_t, q_r_code)

    def calculate_wait_time(self, previous_fuzz, previous_got_response, wait_time):
        # not sure if including this is a good idea as you can't really predict the probability
        # of a fuzz request generating a response. Always set to true for now
        if previous_fuzz:
            wait_time *= .8
            
        if not previous_got_response:
            wait_time *= .8

        return wait_time

    def require(self, x, y, z):
        # this method acts as a placeholder anywhere in the transaction dictionary
        # where a request MUST arrive but no response to it is generated 
        pass
        
class SIPCancel:
    
    def process(self, sip_t, output_q, extra_params=None):
        '''
        Process the next response for the given SIP transaction and put it on the output
        queue
        '''

        err = self.send_cancel(sip_t, output_q)
        return None
        
    def send_cancel(self, sip_transaction, output_q):
        '''        
        - We receive a 1XX provisional response to the initial INVITE which
        means we can now send the CANCEL

        @type sip_transaction: SIPTransaction
        @param sip_transaction: An object representing the entire transaction so
            far
        '''

        last_recv = sip_transaction.t_data_list[len(sip_transaction.t_data_list)-1]
        r_code = last_recv.p_data[sip_parser.RCODE]

        if r_code == sip_parser.r_1XX:
            # create and send CANCEL
            cancel_request = self.create_cancel(sip_transaction.t_data_list[0])            
            output_q.put((True, cancel_request, GENERATOR, last_recv.addr, 1.5))        

    def create_cancel(self, t_data):
        '''
        Method to generate a cancel request for a given INVITE. According to the
        RFC the following fields must match (including tags)

        - Request URI
        - Call-ID
        - To
        - Numeric part of the CSeq
        - From
        - Via (should contain only a single Via header matching the top Via
        header from the INVITE)

        The method part of the Cseq header must have a value of CANCEL

        @type t_data: TData
        @param t_data: A TData object representing the INVITE to be cancelled

        @rtype: String
        @return: The cancel request for the INVITE in t_data
        '''

        # retrieve the dictionary of parsed values 
        p_data = t_data.p_data
        cancel_template = [['CANCEL', p_data[sip_parser.RURI], 'SIP/2.0'],
            ['CSeq:', p_data[sip_parser.CSEQNUM], 'CANCEL'],
            ['Via:', p_data[sip_parser.VIA]],
            ['To:', p_data[sip_parser.TO]],                                            
            ['From:', p_data[sip_parser.FROM]],
            ['Call-ID:', p_data[sip_parser.CALLID]],
            ['Max-Forwards: 70']]

        cancel_request = []
        for line in cancel_template:
            cancel_request.append(' '.join(line))

        cancel_request = '\r\n'.join(cancel_request) + '\r\n\r\n'

        return cancel_request

class SIPAck:
    
    def process(self, sip_t, output_q, extra_params=None):
        '''
        @type input_tuple: Tuple
        @param sinput_tuple: See SIPCancel
        '''

        err = self.send_ack(sip_t, output_q)

        return None
    
    def send_ack(self, sip_transaction, output_q):
        '''        
        We receive a 487 response indicating the INVITE has been cancelled.
        This must be ACK'ed

        @type sip_transaction: SIPTransaction
        @param sip_transaction: An object representing the entire transaction so
            far
        '''

        last_recv = sip_transaction.t_data_list[len(sip_transaction.t_data_list)-1]
        r_code = last_recv.p_data[sip_parser.RCODE]

        ack_request = self.create_ack(last_recv, sip_transaction.t_data_list[0])        
        output_q.put((True, ack_request, GENERATOR, last_recv.addr, 1.5))

    def create_ack(self, request_to_ack, orig_request):
        '''
        Method to create an ACK for a request. According to the SIP RFC the
        following fields must match the request that created the transaction

        - Call ID
        - From
        - Request URI
        - Via (should contain only a single Via header matching the top Via
        header from the INVITE)
        - Numeric part of the CSeq

        The To header should match the To header from request that is being
        acknowledged.

        @type request_to_ack: TData
        @param request_to_ack: The request that the ACK is being generated for
        @type orig_request: TData
        @param orig_request: The request that started the transaction

        @rtype: String
        @return: The ACK for the given request

        '''

        p_data_req_ack = request_to_ack.p_data
        p_data_orig = orig_request.p_data

        try:
            r_uri = p_data_orig[sip_parser.RURI]
        except KeyError:
            r_uri = 'user@192.168.3.100'
    
        try:
            cseq_num = p_data_orig[sip_parser.CSEQNUM]
        except KeyError:
            cseq_num = '3'

        try:
            via = p_data_orig[sip_parser.VIA]
        except KeyError:
            via = 'SIP/2.0/UDP 192.168.3.102:5068;branch=z9hG4bKlm4zshdowki1t8c7ep6j0yavq2ug5r3x;rport'

        try:
            to = p_data_req_ack[sip_parser.TO]
        except KeyError:
            to = '<sip:nnp@192.168.3.101>'

        try:
            p_from =  p_data_orig[sip_parser.FROM]
        except KeyError:
            p_from = '"nnp" <sip:nnp@192.168.3.104>;tag=so08p5k39wuv1dczfnij7bet4l2m6hrq'

        try:
            call_id = p_data_orig[sip_parser.CALLID]
        except KeyError:
            call_id = 'rzxd6tm98v0eal1cifg2py7sj3wk54ub@voiper'

        ack_template = [['ACK', r_uri, 'SIP/2.0'],
            ['CSeq:', cseq_num, 'ACK'],
            ['Via:', via],
            ['To:', to],                                            
            ['From:', p_from],
            ['Call-ID:', call_id],
            ['Max-Forwards: 70']]


        ack_request = []
        for line in ack_template:
            ack_request.append(' '.join(line))

        ack_request = '\r\n'.join(ack_request) + '\r\n\r\n'

        return ack_request

class SIPOptions:
    
    def process(self, sip_t, out_queue, extra_params):
        '''
        @type params: Dictionary
        @param params: A dictionary containing the host and port to send the OPTIONS to
        @type out_queue: Queue
        @param out_queue: A queue onto which the OPTIONS will be put to be sent
        '''

        self.host = extra_params['host']
        self.port = extra_params['port']
        self.user = extra_params['user']
        self.target_user = extra_params['target_user']

        self.branch = None
        if extra_params.has_key('branch'):
            self.branch = extra_params['branch']
            
        self.send_options(out_queue)

        return self.branch
        
    def send_options(self, out_queue):
        options_request = self.create_options()
        out_queue.put((True, options_request, GENERATOR, (self.host, self.port), 1.5))

    def create_options(self):
        sip_uri = ''.join(['sip:', self.host])        
        r_data = ''.join(Random().sample(string.ascii_lowercase+string.digits, 32))
        to_line = ''.join(['<sip:', self.target_user, '@', self.host, '>'])
        from_line = ''.join(['"VoIPER" <sip:', self.user, '@', self.host, '>', ';tag=', r_data])
        local_ip = socket.gethostbyname(socket.gethostname())

        if self.branch:
            via_line = ''.join([local_ip, ';branch=z9hG4bKk', self.branch])
        else:
            via_line = ''.join([local_ip, ';branch=z9hG4bKk', r_data])
            self.branch = r_data
            
        call_id_line = ''.join(['options.', r_data])
        uri = ''.join(['sip:', self.host])
        contact_line = ''.join(['<sip:', self.user, '@', local_ip, '>'])

        options_template = [['OPTIONS', sip_uri, 'SIP/2.0'],
            ['CSeq:', str(random.randint(1000, 100000)), 'OPTIONS'],
            ['Via: SIP/2.0/UDP', via_line],
            ['To:', to_line],                                            
            ['From:', from_line],
            ['Call-ID:', call_id_line],
            ['Max-Forwards: 70'],
            ['Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,NOTIFY,REFER,MESSAGE'],
            ['Accept: application/sdp'],
            ['Contact:', contact_line]]

        options_request = []
        for line in options_template:
            options_request.append(' '.join(line))

        options_request = '\r\n'.join(options_request) + '\r\n\r\n'

        return options_request

class SIPRegister:

    def process(self, sip_t, output_q, extra_params):
        host = extra_params['host']
        port = extra_params['port']
        username = extra_params['user']
        password = extra_params['password']
        self.branch = None
        
        if extra_params.has_key('branch'):
            self.branch = extra_params['branch']
            
        if sip_t:
            self.send_register_final(sip_t, output_q, username, password)
            return None
        else:
            self.send_register_init(host, port, username, output_q)
            return self.branch

    def send_register_init(self, host, port, username, output_q):
        register_request = self.create_register_init(host, username)
        print >> sys.stderr, 'sending register init'
        output_q.put((True, register_request, GENERATOR, (host, port), 1.5))        

    def send_register_final(self, sip_t, output_q, username, password):
        last_recv = sip_t.t_data_list[-1]
        orig_reg = sip_t.t_data_list[0]
        
        register_request = self.create_register_final(orig_reg, last_recv, username, password)
        output_q.put((True, register_request, GENERATOR, last_recv.addr, 1.5))

    def calculate_md5_response(self, username, password, realm, uri, nonce):
        '''
        See RFC 3261 section 22 and RFC 2069 section 2.1.2 for details.

        @type username: String
        @param username: The username to register on the registrar
        @type password: String
        @param password: The password that goes with the given username
        @type realm: String
        @param realm: The 'realm' value which will be returned by the server in
            response to the initial REGISTER request as part of the
            WWW-Authenticate header
        @type uri: String
        @param uri: The SIP/SIPS uri from the original request line. Will be of
            the form 'sip:192.168.3.101', without the quotes.
        @type nonce: String
        @param nonce: The 'nonce' value which will be returned by the server in
            response to the initial REGISTER request as part of the
            WWW-Authenticate header
        '''

        A1 = ':'.join([username, realm, password])
        A2 = ':'.join(['REGISTER', uri])

        md5_A1 = md5.new(A1).hexdigest()
        md5_A2 = md5.new(A2).hexdigest()

        return md5.new(':'.join([md5_A1, nonce, md5_A2])).hexdigest()
        
    def create_register_final(self, init_reg_request, auth_response, username, password):
        p_data_init = init_reg_request.p_data
        p_data_auth = auth_response.p_data

        cseq_num = str(int(p_data_init[sip_parser.CSEQNUM]) + 1)
        nonce = p_data_auth[sip_parser.WWW_AUTHEN_NONCE]
        realm = p_data_auth[sip_parser.WWW_AUTHEN_REALM]
        md5_response = self.calculate_md5_response(username, password, realm, p_data_init[sip_parser.RURI], nonce)

        auth_string = ''.join(['Digest username="',
             username, '", realm="',
             realm, '", nonce="',
             nonce, '", uri="',
             p_data_init[sip_parser.RURI],'", algorithm=md5, response="',
             md5_response, '"'])
        
        register_template = [['REGISTER', p_data_init[sip_parser.RURI], 'SIP/2.0'],
            ['CSeq:', cseq_num, 'REGISTER'],
            ['Via:', p_data_init[sip_parser.VIA]],
            ['To:', p_data_init[sip_parser.TO]],                                            
            ['From:', p_data_init[sip_parser.FROM]],
            ['Call-ID:', p_data_init[sip_parser.CALLID]],
            ['Authorization:', auth_string],
            ['Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,NOTIFY,REFER,MESSAGE'],
            ['Contact:', p_data_init[sip_parser.CONTACT]],
            ['Expires: 3600'],                        
            ['Max-Forwards: 70']]

        register_request = []
        for line in register_template:
            register_request.append(' '.join(line))

        register_request = '\r\n'.join(register_request) + '\r\n\r\n'

        return register_request

    def create_register_init(self, target_ip, user):
        r_data = ''.join(Random().sample(string.ascii_lowercase+string.digits, 32))
        to_line = ''.join(['<sip:', user, '@', target_ip, '>'])
        from_line = ''.join([to_line, ';tag=', r_data])
        local_ip = socket.gethostbyname(socket.gethostname())

        if self.branch:
            via_line = ''.join([local_ip, ';branch=z9hG4bKk', self.branch])
        else:
            self.branch = r_data
            via_line = ''.join([local_ip, ';branch=z9hG4bKk', r_data])
            
        call_id_line = ''.join(['register.', r_data])
        uri = ''.join(['sip:', target_ip])
        contact_line = ''.join(['<sip:', user, '@', local_ip, '>'])
        
        register_template = [['REGISTER', uri, 'SIP/2.0'],
            ['To:', to_line],
            ['From:', from_line],
            ['Call-ID:', call_id_line ],
            ['CSeq:', str(random.randint(1000, 100000)), 'REGISTER'],
            ['Via: SIP/2.0/UDP', via_line],
            ['Max-Forwards: 70'],
            ['Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,NOTIFY,REFER,MESSAGE'],
            ['Contact:', contact_line],                        
            ['Expires: 3600']]

        register_request = []
        for line in register_template:
            register_request.append(' '.join(line))

        register_request = '\r\n'.join(register_request) + '\r\n\r\n'

        return register_request
    
class SIPInvite:

    def process(self, sip_t, output_q, extra_params):
        self.host = extra_params['host']
        self.port = extra_params['port']
        self.user = extra_params['user']

        if extra_params.has_key('target_user'):
            self.target_user = extra_params['target_user']
        else:
            self.target_user = None

        self.branch = None
        if extra_params.has_key('branch'):
            self.branch = extra_params['branch']
            
        self.output_q = output_q

        self.send_invite()
        return self.branch

    def send_invite(self):
        invite_request = self.create_invite()
        self.output_q.put((True, invite_request, GENERATOR, (self.host, self.port), 2.0))

    def create_invite(self):
        '''
        According to the RFC the following headers SHOULD be present:
        - Allow
        - Supported

        Headers that MAY be present are not included by VoIPER. The following
        MUST be included:
        - From
        - Via
        - To
        - Call-ID
        - CSeq

        Content-type and Content-length are required for the SDP header
        '''

        if self.target_user:
            sip_uri = ''.join(['sip:', self.target_user, '@', self.host])
            to_line = ''.join(['<sip:', self.target_user, '@', self.host, '>'])
        else:
            sip_uri = ''.join(['sip:', self.host])
            to_line = ''.join(['<sip:', self.host, '>'])
            
        r_data = ''.join(Random().sample(string.ascii_lowercase+string.digits, 32))
        local_ip = socket.gethostbyname(socket.gethostname())
        from_line = ''.join(['"VoIPER" <sip:', self.user, '@', local_ip, '>;tag=', r_data])

        if self.branch:
            via_line = ''.join(['SIP/2.0/UDP ', local_ip, ';branch=z9hG4bKk', self.branch])
        else:
            self.branch = r_data
            via_line = ''.join(['SIP/2.0/UDP ',local_ip, ';branch=z9hG4bKk', r_data])        

        call_id_line = ''.join([r_data])
        contact_line = ''.join(['<sip:', self.user, '@', local_ip, '>'])        

        c_line = ' '.join(['c=IN IP4', local_ip])
        o_line = ' '.join(['o=- 1212861461 1212861461', c_line])

        # header ripped from ekiga 2.11 so it should
        # be compliant with most other SIP apps
        sdp_header = '\r\n'.join(['v=0',
            o_line,                                  
            's=VoIPER SIP Session',
            c_line,
            't=0 0',
            'm=audio 5000 RTP/AVP 112 113 3 105 108 0 8 101',
            'a=rtpmap:112 SPEEX/16000',
            'a=rtpmap:113 iLBC/8000',
            'a=rtpmap:3 GSM/8000',
            'a=rtpmap:105 MS-GSM/8000',
            'a=rtpmap:108 SPEEX/8000',
            'a=rtpmap:0 PCMU/8000',
            'a=rtpmap:8 PCMA/8000',
            'a=rtpmap:101 telephone-event/8000',
            'a=fmtp:101 0-15'])
                            
        invite_template = [['INVITE', sip_uri, 'SIP/2.0'],
            ['CSeq:', str(random.randint(1000, 100000)), 'INVITE'],
            ['Via:', via_line],
            ['To:', to_line],                                            
            ['From:', from_line],
            ['Call-ID:', call_id_line],
            ['Max-Forwards: 70'],
            ['Content-Type: application/sdp'],
            ['Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,NOTIFY,REFER,MESSAGE'],
            ['Contact:', contact_line],               
            ['Content-Length:', str(len(sdp_header))],
            ['']]

        invite_request = []
        for line in invite_template:
            invite_request.append(' '.join(line))

        invite_request = '\r\n'.join(invite_request)
        invite_request = '\r\n'.join([invite_request, sdp_header])                          

        return invite_request
