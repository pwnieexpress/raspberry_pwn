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
import thread
import sip_parser
import sys

from transceiver import UDPTransceiver
from sip_parser import SIPParser
from Queue import Queue
from copy import deepcopy

GENERATOR=0
NETWORK=1
EXTERNAL=2

class TData:
    def __init__(self, data, p_data, source, addr=None, socket=None):
        '''
        A data class to represent the data of a message in a transaction along with
        who sent it
        
        @type data: String
        @param data: The data of a message in a transaction
        @type p_data: Dictionary
        @param p_data: A dictionary returned by the message parser with mappings of
            fields to their values parsed from the data
        @type source: Integer
        @param source: Indicates where this t_data originated in our system and
            as a result, what do do with it. If '0' the t_data came from one of
            the protocol generators and the data will be sent to the address
            stored in t_data.addr and added to/create an appropriate
            SIPTransaction. If '1' the t_data arrived from the network and will
            be added to the appropriate transaction. All queues will also be
            notified of its arrival. If '2' the data originated from some
            external source e.g the fuzzer. It is assumed to already have been
            sent. If it has a t_data.socket this will be added to the sockets
            the transceiver is monitoring. It will be added to/create a
            SIPTransaction            
        @type addr: Tuple
        @param addr: The (IP, port) tuple the data was sent to or received from
        @type socket: Socket
        @param socket: The socket that was used to send the data. Only necessary if
            this data structure was created outside the transaction manager and the
            data already sent. Without this we wouldn't be able to see any responses
            to this port
        '''

        self.data = data
        self.p_data = p_data
        self.source = source
        self.addr = addr
        self.socket = socket
        
class SIPTransaction:
    def __init__(self, branch, t_data_list, timestamp, timeout, addr=None):
        '''
        Data class to represent a SIP transaction and required data regarding
        it

        @type branch: String
        @param branch: The branch value from the SIP transaction. Used to
            uniquely identify transactions
        @type t_data_list: List
        @param t_data_list: A list of TData objects representing the data
            of the message and who sent it
        @type timestamp: Integer
        @param timestamp: The timestamp for when this transaction was last
            updated
        @type timeout: Integer
        @param timeout: The timeout from the timestamp after which the
            transaction will be disgarded
        @type addr: Tuple
        @param addr: The (IP, port) tuple from the last message in the t_data list
            to be received. If None it is assumed the last message was sent out by
            VoIPER
        '''

        self.branch = branch
        self.t_data_list = t_data_list
        self.timestamp = timestamp
        self.timeout = timeout
        # a list of sockets associated with this transaction
        self.sockets = []

    def add_response(self, t_data):
        '''
        This method should be used to add a new t_data object to the t_data_list.
        It prevents retransmissions being added to the transaction record

        @type t_data: TData
        @param t_data: A TData object representing the request

        @rtype: Boolean
        @return: Returns True if the t_data is added and returns false otherwise
            i.e. the t_data was a retransmission of a previous request
        '''

        try: 
            t_data_r_code = t_data.p_data[sip_parser.RCODE]
            for prev_data in self.t_data_list:
                if prev_data.p_data[sip_parser.RCODE] == t_data_r_code:
                    return False
        except KeyError:
            # It is possible that some of our fuzz requests will not
            # have a correct request code but thats OK
            pass

        self.t_data_list.append(t_data)
        return True
        
class SIPTransactionManager(threading.Thread):
    def __init__(self, add_trans_queue, global_update_queue, listen_port=5060):
        '''
        @type add_trans_queue: Queue
        @param add_trans_queue: A queue that this class will listen on for
            tuples of the form identical to the parameters to the
            add_transaction method of this class except with an extra parameter
            at the start that can be False to indicate to this class to shutdown
            or True otherwise. The data this queue receives will be added to the
            transaction list this class is monitoring
        @type global_update_queue: Queue
        @param global_update_queue: A queue that will receive a SIPTransaction
            object every time an update from the network arrives for that
            SIPTransaction
        '''
        
        self.add_trans_queue = add_trans_queue
        self.global_update_queue = global_update_queue
        self.listen_port = listen_port

        self.lock = thread.allocate_lock()
        self.transceiver = UDPTransceiver([self.listen_port], self.lock)
        self.transceiver.add_notify_queue(self.add_trans_queue, self.listen_port)
        self.transceiver.listen(True)
        
        # A dictionary mapping branch values to SIPTransaction objects
        self.transaction_dict = {}
        self.sip_parser = SIPParser()

        threading.Thread.__init__(self)

    def run(self):
        while True:
            new_trans_tuple = None
            try:
                new_trans_tuple = self.add_trans_queue.get()
            except:
                pass

            if new_trans_tuple != None:
                #print >> sys.stderr,  'TM: Got data'
                if new_trans_tuple[0] == False:
                    #signal to listener first to exit
                    print >>stderr, 'tm returning cause tuple thingy was false'
                    print >>stderr, new_trans_tuple
                    return
                else:                    
                    data = new_trans_tuple[1]
                    source = new_trans_tuple[2]
                    addr = new_trans_tuple[3]
                    timeout = new_trans_tuple[4]
                    socket = None
                    # only interested in the socket if the data came from
                    # a source outside the core. Sources inside the core
                    # will be monitored by default
                    if source == EXTERNAL:
                        socket = new_trans_tuple[5]
                    elif source == GENERATOR:
                        print >>sys.stderr, 'got something from generator off queue'
                    self.add_data_to_transactions(data, source, addr,\
                                                   timeout, socket)
            
    def add_data_to_transactions(self, data, source, addr, timeout, socket=None):
        data_dict = self.sip_parser.parse(data)
        # no branch no fun
        if data_dict.has_key(sip_parser.BRANCH):
            t_data = TData(data, data_dict, source, addr, socket)
            self.add_transaction(t_data, timeout=timeout)

    def add_transaction(self, t_data, timeout=None):
        '''
        Function to add a SIP transaction to the list of the transactions
        this manager is taking care of. If a transaction with this branch
        already exists then this data and queue are appended to their lists
        and all other fields in the old sip_transaction are updated to
        the new values.

        If not a new SIPTransaction object is created with the provided details
        and added to the list.

        @type t_data: TData
        @param data: A TData object representing the data, its parsed fields and
            its origin
        @type timeout: Integer
        @param timeout: A timeout after which this transaction will no
            longer be monitored
        '''

        # parse all fields
        timestamp = time.time()
        data_dict = t_data.p_data

        # First identify the transaction the data is for or create a new
        # transaction for it
        t_data_added = False
        if self.transaction_dict.has_key(data_dict[sip_parser.BRANCH]):
            sip_t = self.transaction_dict[data_dict[sip_parser.BRANCH]]
            t_data_added = sip_t.add_response(t_data)
                    
            if timeout: sip_t.timeout = timeout
        else:
            # If the source is the network then check that the request is
            # of a type that is allowed to create a new transaction. For
            # now we only allow a few types. More may be added in the future if required

            try:                
                r_code = data_dict[sip_parser.RCODE]
            except KeyError:
                # Some of our fuzz requests will not have a request code
                # matching the defined pattern due to fuzzing but thats OK
                r_code = -1
                
            if t_data.source != NETWORK or (r_code <= sip_parser.r_INVITE and
                                             r_code >= sip_parser.r_CANCEL):
                sip_t = SIPTransaction(data_dict[sip_parser.BRANCH], [t_data], \
                                       timestamp, timeout)
                self.transaction_dict[data_dict[sip_parser.BRANCH]] = sip_t
            else:
                return
            
        # Now perform some actions based on the source of the data
        if t_data.source == GENERATOR:
            # Data was generated by the SIP backend. Send it and add the socket
            # used to the list being monitored
            print >> sys.stderr, 'Source is generator. Sending'
            send_sock = self.transceiver.send(t_data.data, t_data.addr)
            if send_sock:
                sip_t.sockets.append(send_sock)
        elif t_data.source == NETWORK and t_data_added:
            # Data originated from another node on the network. Put on the
            # notify queue. A copy is used in case another update arrives
            # before this one is processed and cloaks this one in the t_data list        
            self.global_update_queue.put(deepcopy(sip_t))
        elif t_data.source == EXTERNAL:
            # Data came from an external source e.g the fuzzer and has already
            # been sent. We just need to monitor for responses
            if t_data.socket:
                sip_t.sockets.append(t_data.socket)
                self.transceiver.add_socket(t_data.socket)
                
        self.__check_timeouts()

    def __check_timeouts(self):
        '''
        Checks to see if any of the transactions have timed out and Removes
        them if so
        '''

        curr_time = time.time()
        print >>sys.stderr, 'TM: %d transactions being monitored' % len(self.transaction_dict)
        for branch in self.transaction_dict.keys():
            transaction = self.transaction_dict[branch]
            if curr_time - transaction.timestamp >= transaction.timeout:
                for sock in transaction.sockets:    
                    self.transceiver.close_socket(sock)
                del self.transaction_dict[branch]
        
    def unregister_from_transceiver(self):
        '''
        Function to remove this transaction managers queue from the
        list of queues registered with the transceiver
        '''
        
        self.transceiver.remove_notify_queue((self.incoming_data_queue, self.listen_port))
        
