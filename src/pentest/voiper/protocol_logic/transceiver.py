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

import threading
import time
import sys

from select import select
from Queue import Queue
from socket import *

class UDPTransceiver:
    def __init__(self, port_list, lock):
        '''
        @type port_list: List of Integers
        @param port_list: A list of ports to listen on
        @type lock: Lock
        @param lock: A lock object to be used when performing socket operations
        '''

        self.port_list = port_list
        self.lock = lock
        self.socket_list = []
        self.to_close_list = []
        # these are tuples of queues connected to other classes that
        # will be notified when data arrives and the ports this queue
        # is interested in
        self.notify_q_list = []
        self.listening = False

    def send(self, data, addr):
        '''
        Sends the provided data to the target host and port and adds the
        socket used to the listen queue so we can receive any responses.

        @type data: String
        @param data: The data to send
        @type addr: Tuple
        @param addr: The (host, port) tuple to send the data to

        @rtype: Socket
        @return: Returns the socket that was used to send the data. This should
            be closed when the transaction has timed out.
        '''

        s = socket(AF_INET, SOCK_DGRAM)
        try:
            print >>sys.stderr, 'transceiver sending'
            if len(data) > 9216:
                data = data[:9216]
            s.sendto(data, addr)
            self.add_socket(s)
            return s
        except Exception, e:
            print e
            return None

    def listen(self, listening=True):
        '''
        Start/Stop listening on sockets
        @type listening: Boolean
        @param listening: Whether to have sockets in a listening state or not. All
            required callbacks must be registered before calling this
        '''

        self.listening = listening
        if listening:
            for port in self.port_list:
                recv_sock = socket(AF_INET, SOCK_DGRAM)
                recv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                recv_sock.bind(('0.0.0.0', port))
                self.socket_list.append(recv_sock)
            threading.Thread(target=self.__listen).start()

    def __listen(self):
        '''
        This method should not be called by anything other than the listen
        method of this class. It continues to run until listen(False) is called.
        '''
        
        while self.listening and len(self.notify_q_list) != 0:
            r_read, r_write, broken = select(self.socket_list, [], [], .01)        
            for sock in r_read:
                try:
                    data, addr = sock.recvfrom(2**16)
                except error:
                    continue
                
                for function_tuple in self.notify_q_list:
                    function_tuple[0].put((True, data, 1, addr, 1.5))
                    
            for sock in self.to_close_list:
                self.socket_list.remove(sock)
                sock.close()
                
            self.to_close_list = []        

    def add_socket(self, s):
        '''
        Add a socket to the list of sockets being monitored. This socket should
        be removed from the list via remove_socket and closed at some stage.

        @type s: Socket
        @param s: The socket to add to the list
        '''

        self.socket_list.append(s)

    def close_socket(self, s):
        '''
        Close a socket from the socket list
        
        @type s: Socket
        @param s: The socket to remove from the list
        '''

        self.to_close_list.append(s)
        
    def add_notify_queue(self, queue, port):
        '''
        Add a queue to the list of functions to be called when data is
        received on the given port. A tuple will be placed on the queue.
        The first element being the data received and the second being the
        address it was received from in the form ('ipaddress', port). 
        
        @type queue: Queue
        @param queue: The queue to add to the list
        @type port: Integer
        @param port: The port the provided function is a callback for
        '''

        self.notify_q_list.append((queue, port))

    def remove_notify_queue(self, queue, port):
        '''
        Remove a queue from the notify queue list

        @type queue: Queue
        @param The queue to remove from the list
        @type port: Integer
        @param port: The port the queue is associated with
        '''

        self.notify_q_list.remove((queue, port))
