import re
import sys
import zlib
import time
import socket
import cPickle
import threading
import BaseHTTPServer

import pedrpc
import pgraph
import sex
import primitives


########################################################################################################################
class target:
    '''
    Target descriptor container.
    '''

    def __init__ (self, host, port, **kwargs):
        '''
        @type  host: String
        @param host: Hostname or IP address of target system
        @type  port: Integer
        @param port: Port of target service
        '''

        self.host      = host
        self.port      = port

        # set these manually once target is instantiated.
        self.netmon            = None
        self.procmon           = None
        self.vmcontrol         = None
        self.netmon_options    = {}
        self.procmon_options   = {}
        self.vmcontrol_options = {}
        self.running_flag      = True


    def pedrpc_connect (self):
        '''
        # pass specified target parameters to the PED-RPC server.
        '''

        # wait for the process monitor to come alive and then set its options.
        if self.procmon:
            while self.running_flag:
                try:
                    if self.procmon.alive():
                        break
                except:
                    sys.stderr.write("Procmon exception in sessions.py : self.procmon.alive()\n")

                time.sleep(1)

            # connection established.
            if self.running_flag:
                for key in self.procmon_options.keys():
                    eval('self.procmon.set_%s(self.procmon_options["%s"])' % (key, key))

        # wait for the network monitor to come alive and then set its options.
        if self.netmon:
            while self.running_flag:
                try:
                    if self.netmon.alive():
                        break
                except:
                    sys.stderr.write("Netmon exception in sessions.py : self.netmon.alive()\n")

                time.sleep(1)

            # connection established.
            if self.running_flag:
                for key in self.netmon_options.keys():
                    eval('self.netmon.set_%s(self.netmon_options["%s"])' % (key, key))


########################################################################################################################
class connection (pgraph.edge.edge):
    def __init__ (self, src, dst, callback=None):
        '''
        Extends pgraph.edge with a callback option. This allows us to register a function to call between node
        transmissions to implement functionality such as challenge response systems. The callback method must follow
        this prototype::

            def callback(session, node, edge, sock)

        Where node is the node about to be sent, edge is the last edge along the current fuzz path to "node", session
        is a pointer to the session instance which is useful for snagging data such as sesson.last_recv which contains
        the data returned from the last socket transmission and sock is the live socket. A callback is also useful in
        situations where, for example, the size of the next packet is specified in the first packet.

        @type  src:      Integer
        @param src:      Edge source ID
        @type  dst:      Integer
        @param dst:      Edge destination ID
        @type  callback: Function
        @param callback: (Optional, def=None) Callback function to pass received data to between node xmits
        '''

        # run the parent classes initialization routine first.
        pgraph.edge.edge.__init__(self, src, dst)

        self.callback = callback


########################################################################################################################
class session (pgraph.graph):
    def __init__ (self, session_filename=None, audit_folder=None,skip=0, sleep_time=.2, log_level=2, proto="tcp", restart_interval=0, timeout=5.0, web_port=26001, crash_threshold=3, trans_in_q=None):
        '''
        Extends pgraph.graph and provides a container for architecting protocol dialogs.

        @type  session_filename: String
        @kwarg session_filename: (Optional, def=None) Filename to serialize persistant data to
        @type  skip:             Integer
        @kwarg skip:             (Optional, def=0) Number of test cases to skip
        @type  sleep_time:       Float
        @kwarg sleep_time:       (Optional, def=1.0) Time to sleep in between tests
        @type  log_level:        Integer
        @kwarg log_level:        (Optional, def=2) Set the log level, higher number == more log messages
        @type  proto:            String
        @kwarg proto:            (Optional, def="tcp") Communication protocol
        @type  timeout:          Float
        @kwarg timeout:          (Optional, def=5.0) Seconds to wait for a send/recv prior to timing out
        @type  restart_interval: Integer
        @kwarg restart_interval  (Optional, def=0) Restart the target after n test cases, disable by setting to 0
        @type  crash_threshold:  Integer
        @kwarg crash_threshold   (Optional, def=3) Maximum number of crashes allowed before a node is exhaust
        '''

        # run the parent classes initialization routine first.
        pgraph.graph.__init__(self)

        self.session_filename    = session_filename
        self.audit_folder        = audit_folder
        self.skip                = skip
        self.sleep_time          = sleep_time
        self.log_level           = log_level
        self.proto               = proto
        self.restart_interval    = restart_interval
        self.timeout             = timeout
        self.web_port            = web_port
        self.crash_threshold     = crash_threshold
        self.trans_in_q          = trans_in_q

        self.total_num_mutations = 0
        self.total_mutant_index  = 0
        self.crashes_detected    = 0
        self.fuzz_node           = None
        self.targets             = []
        self.netmon_results      = {}
        self.procmon_results     = {}
        self.pause_flag          = False
        self.running_flag        = True
        self.crashing_primitives = {}

        if self.proto == "tcp":
            self.proto = socket.SOCK_STREAM
        elif self.proto == "udp":
            self.proto = socket.SOCK_DGRAM
        else:
            raise sex.error("INVALID PROTOCOL SPECIFIED: %s" % self.proto)

        # import settings if they exist.
        self.import_file()
        
        # create a root node. we do this because we need to start fuzzing from a single point and the user may want
        # to specify a number of initial requests.
        self.root       = pgraph.node()
        self.root.name  = "__ROOT_NODE__"
        self.root.label = self.root.name
        self.last_recv  = None

        self.add_node(self.root)


    ####################################################################################################################
    def decrement_total_mutant_index(self, val):
        if self.total_mutant_index - val > 0:
            self.total_mutant_index -= val
        else:
            self.total_mutant_index = 0

    def add_node (self, node):
        '''
        Add a pgraph node to the graph. We overload this routine to automatically generate and assign an ID whenever a
        node is added.

        @type  node: pGRAPH Node
        @param node: Node to add to session graph
        '''

        node.number = len(self.nodes)
        node.id     = len(self.nodes)

        if not self.nodes.has_key(node.id):
            self.nodes[node.id] = node

        return self


    ####################################################################################################################
    def add_target (self, target):
        '''
        Add a target to the session. Multiple targets can be added for parallel fuzzing.

        @type  target: session.target
        @param target: Target to add to session
        '''

        # pass specified target parameters to the PED-RPC server.
        target.pedrpc_connect()
        # add target to internal list.
        self.targets.append(target)


    ####################################################################################################################
    def connect (self, src, dst=None, callback=None):
        '''
        Create a connection between the two requests (nodes) and register an optional callback to process in between
        transmissions of the source and destination request. Leverage this functionality to handle situations such as
        challenge response systems. The session class maintains a top level node that all initial requests must be
        connected to. Example::

            sess = sessions.session()
            sess.connect(sess.root, s_get("HTTP"))

        If given only a single parameter, sess.connect() will default to attaching the supplied node to the root node.
        This is a convenient alias and is identical to the second line from the above example::

            sess.connect(s_get("HTTP"))

        If you register callback method, it must follow this prototype::

            def callback(session, node, edge, sock)

        Where node is the node about to be sent, edge is the last edge along the current fuzz path to "node", session
        is a pointer to the session instance which is useful for snagging data such as sesson.last_recv which contains
        the data returned from the last socket transmission and sock is the live socket. A callback is also useful in
        situations where, for example, the size of the next packet is specified in the first packet. As another
        example, if you need to fill in the dynamic IP address of the target register a callback that snags the IP
        from sock.getpeername()[0].

        @type  src:      String or Request (Node)
        @param src:      Source request name or request node
        @type  dst:      String or Request (Node)
        @param dst:      Destination request name or request node
        @type  callback: Function
        @param callback: (Optional, def=None) Callback function to pass received data to between node xmits

        @rtype:  pgraph.edge
        @return: The edge between the src and dst.
        '''

        # if only a source was provided, then make it the destination and set the source to the root node.
        if not dst:
            dst = src
            src = self.root

        # if source or destination is a name, resolve the actual node.
        if type(src) is str:
            src = self.find_node("name", src)

        if type(dst) is str:
            dst = self.find_node("name", dst)

        # if source or destination is not in the graph, add it.
        if src != self.root and not self.find_node("name", src.name):
            self.add_node(src)

        if not self.find_node("name", dst.name):
            self.add_node(dst)

        # create an edge between the two nodes and add it to the graph.
        edge = connection(src.id, dst.id, callback)
        self.add_edge(edge)

        return edge


    ####################################################################################################################
    def export_file (self):
        '''
        Dump various object values to disk.

        @see: import_file()
        '''

        if not self.session_filename:
            return

        data = {}
        data["session_filename"]    = self.session_filename
        data["skip"]                = self.total_mutant_index
        data["sleep_time"]          = self.sleep_time
        data["log_level"]           = self.log_level
        data["proto"]               = self.proto
        data["crashes_detected"]    = self.crashes_detected
        data["restart_interval"]    = self.restart_interval
        data["timeout"]             = self.timeout
        data["web_port"]            = self.web_port
        data["crash_threshold"]     = self.crash_threshold
        data["total_num_mutations"] = self.total_num_mutations
        data["total_mutant_index"]  = self.total_mutant_index
        data["netmon_results"]      = self.netmon_results
        data["procmon_results"]     = self.procmon_results
        data["pause_flag"]          = self.pause_flag

        fh = open(self.session_filename, "wb+")
        fh.write(zlib.compress(cPickle.dumps(data, protocol=2)))
        fh.close()
    ####################################################################################################################

    def waitForRegister(self):
        '''
        This method should be overwritten by any fuzzer that needs to wait for the client to register after it has restarted
        '''
        pass
    
    ####################################################################################################################
        
    def updateProgressBar(self, x, y):
        '''
        This method should be overridden by the GUI
        '''
        pass
        
    ####################################################################################################################
    def fuzz (self, this_node=None, path=[]):
        '''
        Call this routine to get the ball rolling. No arguments are necessary as they are both utilized internally
        during the recursive traversal of the session graph.

        @type  this_node: request (node)
        @param this_node: (Optional, def=None) Current node that is being fuzzed.
        @type  path:      List
        @param path:      (Optional, def=[]) Nodes along the path to the current one being fuzzed.
        '''

        # if no node is specified, then we start from the root node and initialize the session.
        if not this_node:
            # we can't fuzz if we don't have at least one target and one request.
            if not self.targets:
                raise sex.error("NO TARGETS SPECIFIED IN SESSION")

            if not self.edges_from(self.root.id):
                raise sex.error("NO REQUESTS SPECIFIED IN SESSION")

            this_node = self.root

            try:    self.server_init()
            except: return

        # XXX - TODO - complete parallel fuzzing, will likely have to thread out each target
        target = self.targets[0]

        # step through every edge from the current node.
        for edge in self.edges_from(this_node.id):
            # the destination node is the one actually being fuzzed.
            self.fuzz_node = self.nodes[edge.dst]
            num_mutations  = self.fuzz_node.num_mutations()

            # keep track of the path as we fuzz through it, don't count the root node.
            # we keep track of edges as opposed to nodes because if there is more then one path through a set of
            # given nodes we don't want any ambiguity.
            if edge.src != self.root.id:
                path.append(edge)

            current_path  = " -> ".join([self.nodes[e.src].name for e in path])
            current_path += " -> %s" % self.fuzz_node.name

            self.log("current fuzz path: %s" % current_path, 2)            
            self.log("fuzzed %d of %d total cases" % (self.total_mutant_index, self.total_num_mutations), 2)
            self.updateProgressBar(self.total_mutant_index, self.total_num_mutations)
            self.update_GUI_crashes(self.crashes_detected)

            done_with_fuzz_node = False
            crash_count         = 0

            # loop through all possible mutations of the fuzz node.
            while not done_with_fuzz_node:
                # the GUI sets unsets this flag when it wants the fuzzer to die
                # command line users can just ctrl-c/z or ctrl-alt-delete
                if not self.running_flag:
                    break                
                # if we need to pause, do so.
                self.pause()

                # if we have exhausted the mutations of the fuzz node, break out of the while(1).
                # note: when mutate() returns False, the node has been reverted to the default (valid) state.
                if not self.fuzz_node.mutate():
                    self.log("all possible mutations for current fuzz node exhausted", 2)
                    done_with_fuzz_node = True
                    continue

                # make a record in the session that a mutation was made.
                self.total_mutant_index += 1

                # if we don't need to skip the current test case.
                if self.total_mutant_index > self.skip:
                    # if we've hit the restart interval, restart the target.
                    if self.restart_interval and self.total_mutant_index % self.restart_interval == 0:
                        self.log("restart interval of %d reached" % self.restart_interval)
                        self.restart_target(target)
                        # call this method in case we should wait for the client app to register with us after a restart
                        self.waitForRegister()
                        self.log("fuzzing %d of %d" % (self.fuzz_node.mutant_index, num_mutations), 2)

                    # attempt to complete a fuzz transmission. keep trying until we are successful, whenever a failure
                    # occurs, restart the target.
                    while 1:
                        try:
                            # instruct the debugger/sniffer that we are about to send a new fuzz.
                            if target.procmon: target.procmon.pre_send(self.total_mutant_index)
                            if target.netmon:  target.netmon.pre_send(self.total_mutant_index)

                            # establish a connection to the target.
                            self.host = target.host
                            self.port = target.port
                            sock = socket.socket(socket.AF_INET, self.proto)
                            sock.settimeout(self.timeout)                           

                            # if the user registered a pre-send function, pass it the sock and let it do the deed.
                            self.pre_send(sock)

                            # send out valid requests for each node in the current path up to the node we are fuzzing.
                            for e in path:
                                node = self.nodes[e.src]
                                self.transmit(sock, node, e, target)

                            # now send the current node we are fuzzing.
                            self.transmit(sock, self.fuzz_node, edge, target)
                            self.updateProgressBar(self.total_mutant_index, self.total_num_mutations)

                            # if we reach this point the send was successful for break out of the while(1).
                            break

                        except sex.error, e:
                            sys.stderr.write("CAUGHT SULLEY EXCEPTION\n")
                            sys.stderr.write("\t" + e.__str__() + "\n")
                            sys.exit(1)

                        # close the socket.                        
                        self.close_socket(sock)

                        self.log("failed connecting to %s:%d" % (target.host, target.port))
                        
                        self.log("restarting target and trying again")
                        self.restart_target(target)

                    # if the user registered a post-send function, pass it the sock and let it do the deed.
                    # we do this outside the try/except loop because if our fuzz causes a crash then the post_send()
                    # will likely fail and we don't want to sit in an endless loop.
                    self.post_send(sock)

                    # done with the socket.
                    # The following is necessary because in the case of a
                    # CANCEL being sent to an INVITE we need the socket to live
                    # for a little longer
                    # sock.close()
                    self.close_socket(sock)

                    # delay in between test cases.
                    self.log("sleeping for %f seconds" % self.sleep_time, 5)
                    time.sleep(self.sleep_time)

                    # poll the PED-RPC endpoints (netmon, procmon etc...) for the target.
                    self.poll_pedrpc(target)

                    # serialize the current session state to disk.
                    self.export_file()

            # recursively fuzz the remainder of the nodes in the session graph.
            if not self.running_flag:
                break            
            self.fuzz(self.fuzz_node, path)

        # finished with the last node on the path, pop it off the path stack.
        if path:
            path.pop()

    ####################################################################################################################
    def close_socket(self, sock):
        '''
        Closes a given socket. Meant to be overridden by VoIPER
        
        @type sock: Socket
        @param sock: The socket to be closed
        '''
        
        sock.close()
    
    ####################################################################################################################
    def import_file (self):
        '''
        Load varous object values from disk.

        @see: export_file()
        '''

        try:
            fh   = open(self.session_filename, "rb")
            data = cPickle.loads(zlib.decompress(fh.read()))
            fh.close()
        except:
            return

        # update the skip variable to pick up fuzzing from last test case.        
        self.skip                = data["total_mutant_index"]

        self.session_filename    = data["session_filename"]
        self.sleep_time          = data["sleep_time"]
        self.log_level           = data["log_level"]
        self.proto               = data["proto"]
        self.restart_interval    = data["restart_interval"]
        self.timeout             = data["timeout"]
        self.web_port            = data["web_port"]
        self.crash_threshold     = data["crash_threshold"]
        self.total_num_mutations = data["total_num_mutations"]
        self.total_mutant_index  = data["total_mutant_index"]
        self.netmon_results      = data["netmon_results"]
        self.procmon_results     = data["procmon_results"]
        self.pause_flag          = data["pause_flag"]
        self.crashes_detected    = data["crashes_detected"]


    ####################################################################################################################
    def log (self, msg, level=1):
        '''
        If the supplied message falls under the current log level, print the specified message to screen.

        @type  msg: String
        @param msg: Message to log
        '''

        if self.log_level >= level:
            print "[%s] %s" % (time.strftime("%I:%M.%S"), msg)


    ####################################################################################################################
    def num_mutations (self, this_node=None, path=[]):
        '''
        Number of total mutations in the graph. The logic of this routine is identical to that of fuzz(). See fuzz()
        for inline comments. The member varialbe self.total_num_mutations is updated appropriately by this routine.

        @type  this_node: request (node)
        @param this_node: (Optional, def=None) Current node that is being fuzzed.
        @type  path:      List
        @param path:      (Optional, def=[]) Nodes along the path to the current one being fuzzed.

        @rtype:  Integer
        @return: Total number of mutations in this session.
        '''

        if not this_node:
            this_node                = self.root
            self.total_num_mutations = 0

        for edge in self.edges_from(this_node.id):
            next_node                 = self.nodes[edge.dst]
            self.total_num_mutations += next_node.num_mutations()

            if edge.src != self.root.id:
                path.append(edge)

            self.num_mutations(next_node, path)

        # finished with the last node on the path, pop it off the path stack.
        if path:
            path.pop()

        return self.total_num_mutations


    ####################################################################################################################
    def pause (self):
        '''
        If thet pause flag is raised, enter an endless loop until it is lowered.
        '''

        while 1:
            if self.pause_flag:
                time.sleep(1)
            else:
                break


    ####################################################################################################################
    def poll_pedrpc (self, target):
        '''
        Poll the PED-RPC endpoints (netmon, procmon etc...) for the target.

        @type  target: session.target
        @param target: Session target whose PED-RPC services we are polling
        '''

        # kill the pcap thread and see how many bytes the sniffer recorded.
        if target.netmon:
            bytes = target.netmon.post_send()
            self.log("netmon captured %d bytes for test case #%d" % (bytes, self.total_mutant_index), 2)
            self.netmon_results[self.total_mutant_index] = bytes

        # check if our fuzz crashed the target. procmon.post_send() returns False if the target access violated.
        if target.procmon:
            # had to include this because an error in the connection can result in nothing being returned. Which is
            # annoying
            ret_val = None
            while not ret_val:
                ret_val = target.procmon.post_send()
            
            alive = ret_val[0]
            crash_type = ret_val[1]
            if not alive:
                self.log("procmon detected %s on test case #%d" % (crash_type, self.total_mutant_index))
                self.crashes_detected += 1
                self.update_GUI_crashes(self.crashes_detected)

                # retrieve the primitive that caused the crash and increment it's individual crash count.
                self.crashing_primitives[self.fuzz_node.mutant] = self.crashing_primitives.get(self.fuzz_node.mutant, 0) + 1

                # notify with as much information as possible.
                if not self.fuzz_node.mutant.name: msg = "primitive lacks a name, "
                else:                              msg = "primitive name: %s, " % self.fuzz_node.mutant.name

                msg += "type: %s, default value: %s" % (self.fuzz_node.mutant.s_type, self.fuzz_node.mutant.original_value)
                self.log(msg)

                # print crash synopsis if access violation
                if crash_type == "access violation":
                    self.procmon_results[self.total_mutant_index] = target.procmon.get_crash_synopsis()
                    self.log(self.procmon_results[self.total_mutant_index].split("\n")[0], 2)

                # log the sent data to disk
                if self.audit_folder != None:
                    crash_log_name = self.audit_folder + '/' + \
                        str(self.fuzz_node.id) + '_' + \
                        str(self.total_mutant_index) + '.crashlog'
                    crash_log = open(crash_log_name, 'w')
                    crash_log.write(self.fuzz_node.sent_data)
                    crash_log.close()
                    self.log('Fuzz request logged to ' + crash_log_name, 2)

                # if the user-supplied crash threshold is reached, exhaust this node.
                if self.crashing_primitives[self.fuzz_node.mutant] >= self.crash_threshold:
                    # as long as we're not a group
                    if not isinstance(self.crashing_primitives[self.fuzz_node.mutant], primitives.group):
                        skipped = self.fuzz_node.mutant.exhaust()
                        self.log("crash threshold reached for this primitive, exhausting %d mutants." % skipped)
                        self.total_mutant_index += skipped
                        
                # start the target back up.
                self.restart_target(target, stop_first=False)


    ####################################################################################################################

    def update_GUI_crashes(self, num_crashes):
        '''
        Method to be overridden by a GUI that wants and update of the number of crashes detected
        '''
        pass
    
    ####################################################################################################################
    def post_send (self, sock):
        '''
        Overload or replace this routine to specify actions to run after to each fuzz request. The order of events is
        as follows::

            pre_send() - req - callback ... req - callback - post_send()

        When fuzzing RPC for example, register this method to tear down the RPC request.

        @see: pre_send()

        @type  sock: Socket
        @param sock: Connected socket to target
        '''

        # default to doing nothing.
        pass


    ####################################################################################################################
    def pre_send (self, sock):
        '''
        Overload or replace this routine to specify actions to run prior to each fuzz request. The order of events is
        as follows::

            pre_send() - req - callback ... req - callback - post_send()

        When fuzzing RPC for example, register this method to establish the RPC bind.

        @see: pre_send()

        @type  sock: Socket
        @param sock: Connected socket to target
        '''

        # default to doing nothing.
        pass


    ####################################################################################################################
    def restart_target (self, target, stop_first=True):
        '''
        Restart the fuzz target. If a VMControl is available revert the snapshot, if a process monitor is available
        restart the target process. Otherwise, do nothing.

        @type  target: session.target
        @param target: Target we are restarting
        '''

        # vm restarting is the preferred method so try that first.
        if target.vmcontrol:
            self.log("restarting target virtual machine")
            target.vmcontrol.restart_target()

        # if we have a connected process monitor, restart the target process.
        elif target.procmon:
            self.log("restarting target process")
            if stop_first:
                target.procmon.stop_target()

            target.procmon.start_target()

            # give the process a few seconds to settle in.
            time.sleep(3)

        # otherwise all we can do is wait a while for the target to recover on its own.
        else:
            self.log("no vmcontrol or procmon channel available ... sleeping for 5 minutes")
            time.sleep(300)

        # pass specified target parameters to the PED-RPC server to re-establish connections.
        target.pedrpc_connect()


    ####################################################################################################################
    def server_init (self):
        '''
        Called by fuzz() on first run (not on recursive re-entry) to initialize variables, web interface, etc...
        '''

        self.total_mutant_index  = 0
        self.total_num_mutations = self.num_mutations()

        # spawn the web interface.
        t = web_interface_thread(self)
        t.start()


    ####################################################################################################################
    def transmit (self, sock, node, edge, target):
        '''
        Render and transmit a node, process callbacks accordingly.

        @type  sock:   Socket
        @param sock:   Socket to transmit node on
        @type  node:   Request (Node)
        @param node:   Request/Node to transmit
        @type  edge:   Connection (pgraph.edge)
        @param edge:   Edge along the current fuzz path from "node" to next node.
        @type  target: session.target
        @param target: Target we are transmitting to
        '''

        data = None

        self.log("xmitting: [%d.%d]" % (node.id, self.total_mutant_index), level=2)

        # if the edge has a callback, process it. the callback has the option to render the node, modify it and return.
        if edge.callback:
            data = edge.callback(self, node, edge, sock)

        # if not data was returned by the callback, render the node here.
        if not data:
            data = node.render()

        # if data length is > 65507 and proto is UDP, truncate it.
        # XXX - this logic does not prevent duplicate test cases, need to address this in the future.
        if self.proto == socket.SOCK_DGRAM:
            # max UDP packet size.
            if len(data) > 65507:
                #self.log("Too much data for UDP, truncating to 65507 bytes")
                data = data[:65507]

        # pass the data off to the transaction manager to be added to a transaction
        if self.trans_in_q:
            self.trans_in_q.put((True, data, 2, (self.host, self.port), 1.5, sock))
        try:            
            sock.sendto(data, (self.host, self.port))
            node.sent_data = data
        except Exception, inst:
            self.log("Socket error, send: %s" % inst[1])

        if self.proto == socket.SOCK_STREAM:
            # XXX - might have a need to increase this at some point. (possibly make it a class parameter)
            try:
                self.last_recv = sock.recv(10000)
            except Exception, e:
                self.log("Nothing received on socket.", 5)
                self.last_recv = ""
        else:
            self.last_recv = ""

        if len(self.last_recv) > 0:
            self.log("received: [%d] %s" % (len(self.last_recv), self.last_recv), level=10)


########################################################################################################################
class web_interface_handler (BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.session = None


    def commify (self, number):
        number     = str(number)
        processing = 1
        regex      = re.compile(r"^(-?\d+)(\d{3})")

        while processing:
            (number, processing) = regex.subn(r"\1,\2",number)

        return number


    def do_GET (self):
        self.do_everything()


    def do_HEAD (self):
        self.do_everything()


    def do_POST (self):
        self.do_everything()


    def do_everything (self):
        if "pause" in self.path:
            self.session.pause_flag = True

        if "resume" in self.path:
            self.session.pause_flag = False

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if "view_crash" in self.path:
            response = self.view_crash(self.path)
        elif "view_pcap" in self.path:
            response = self.view_pcap(self.path)
        else:
            response = self.view_index()

        self.wfile.write(response)


    def log_error (self, *args, **kwargs):
        pass


    def log_message (self, *args, **kwargs):
        pass


    def version_string (self):
        return "Sulley Fuzz Session"


    def view_crash (self, path):
        test_number = int(path.split("/")[-1])
        return "<html><pre>%s</pre></html>" % self.session.procmon_results[test_number]


    def view_pcap (self, path):
        return path


    def view_index (self):
        response = """
                    <html>
                    <head>
                        <title>Sulley Fuzz Control</title>
                        <style>
                            a:link    {color: #FF8200; text-decoration: none;}
                            a:visited {color: #FF8200; text-decoration: none;}
                            a:hover   {color: #C5C5C5; text-decoration: none;}

                            body
                            {
                                background-color: #000000;
                                font-family:      Arial, Helvetica, sans-serif;
                                font-size:        12px;
                                color:            #FFFFFF;
                            }

                            td
                            {
                                font-family:      Arial, Helvetica, sans-serif;
                                font-size:        12px;
                                color:            #A0B0B0;
                            }

                            .fixed
                            {
                                font-family:      Courier New;
                                font-size:        12px;
                                color:            #A0B0B0;
                            }

                            .input
                            {
                                font-family:      Arial, Helvetica, sans-serif;
                                font-size:        11px;
                                color:            #FFFFFF;
                                background-color: #333333;
                                border:           thin none;
                                height:           20px;
                            }
                        </style>
                    </head>
                    <body>
                    <center>
                    <table border=0 cellpadding=5 cellspacing=0 width=750><tr><td>
                    <!-- begin bounding table -->

                    <table border=0 cellpadding=5 cellspacing=0 width="100%%">
                    <tr bgcolor="#333333">
                        <td><div style="font-size: 20px;">Sulley Fuzz Control</div></td>
                        <td align=right><div style="font-weight: bold; font-size: 20px;">%(status)s</div></td>
                    </tr>
                    <tr bgcolor="#111111">
                        <td colspan=2 align="center">
                            <table border=0 cellpadding=0 cellspacing=5>
                                <tr bgcolor="#111111">
                                    <td><b>Total:</b></td>
                                    <td>%(total_mutant_index)s</td>
                                    <td>of</td>
                                    <td>%(total_num_mutations)s</td>
                                    <td class="fixed">%(progress_total_bar)s</td>
                                    <td>%(progress_total)s</td>
                                </tr>
                                <tr bgcolor="#111111">
                                    <td><b>%(current_name)s:</b></td>
                                    <td>%(current_mutant_index)s</td>
                                    <td>of</td>
                                    <td>%(current_num_mutations)s</td>
                                    <td class="fixed">%(progress_current_bar)s</td>
                                    <td>%(progress_current)s</td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <form method=get action="/pause">
                                <input class="input" type="submit" value="Pause">
                            </form>
                        </td>
                        <td align=right>
                            <form method=get action="/resume">
                                <input class="input" type="submit" value="Resume">
                            </form>
                        </td>
                    </tr>
                    </table>

                    <!-- begin procmon results -->
                    <table border=0 cellpadding=5 cellspacing=0 width="100%%">
                        <tr bgcolor="#333333">
                            <td nowrap>Test Case #</td>
                            <td>Crash Synopsis</td>
                            <td nowrap>Captured Bytes</td>
                        </tr>
                    """

        keys = self.session.procmon_results.keys()
        keys.sort()
        for key in keys:
            val   = self.session.procmon_results[key]
            bytes = "&nbsp;"

            if self.session.netmon_results.has_key(key):
                bytes = self.commify(self.session.netmon_results[key])

            response += '<tr><td class="fixed"><a href="/view_crash/%d">%06d</a></td><td>%s</td><td align=right>%s</td></tr>' % (key, key, val.split("\n")[0], bytes)

        response += """
                    <!-- end procmon results -->
                    </table>

                    <!-- end bounding table -->
                    </td></tr></table>
                    </center>
                    </body>
                    </html>
                   """

        # what is the fuzzing status.
        if self.session.pause_flag:
            status = "<font color=red>PAUSED</font>"
        else:
            status = "<font color=green>RUNNING</font>"

        # if there is a current fuzz node.
        if self.session.fuzz_node:
            # which node (request) are we currently fuzzing.
            if self.session.fuzz_node.name:
                current_name = self.session.fuzz_node.name
            else:
                current_name = "[N/A]"

            # render sweet progress bars.
            progress_current     = float(self.session.fuzz_node.mutant_index) / float(self.session.fuzz_node.num_mutations())
            num_bars             = int(progress_current * 50)
            progress_current_bar = "[" + "=" * num_bars + "&nbsp;" * (50 - num_bars) + "]"
            progress_current     = "%.3f%%" % (progress_current * 100)

            progress_total       = float(self.session.total_mutant_index) / float(self.session.total_num_mutations)
            num_bars             = int(progress_total * 50)
            progress_total_bar   = "[" + "=" * num_bars + "&nbsp;" * (50 - num_bars) + "]"
            progress_total       = "%.3f%%" % (progress_total * 100)

            response %= \
            {
                "current_mutant_index"  : self.commify(self.session.fuzz_node.mutant_index),
                "current_name"          : current_name,
                "current_num_mutations" : self.commify(self.session.fuzz_node.num_mutations()),
                "progress_current"      : progress_current,
                "progress_current_bar"  : progress_current_bar,
                "progress_total"        : progress_total,
                "progress_total_bar"    : progress_total_bar,
                "status"                : status,
                "total_mutant_index"    : self.commify(self.session.total_mutant_index),
                "total_num_mutations"   : self.commify(self.session.total_num_mutations),
            }
        else:
            response %= \
            {
                "current_mutant_index"  : "",
                "current_name"          : "",
                "current_num_mutations" : "",
                "progress_current"      : "",
                "progress_current_bar"  : "",
                "progress_total"        : "",
                "progress_total_bar"    : "",
                "status"                : "<font color=yellow>UNAVAILABLE</font>",
                "total_mutant_index"    : "",
                "total_num_mutations"   : "",
            }

        return response


########################################################################################################################
class web_interface_server (BaseHTTPServer.HTTPServer):
    '''
    http://docs.python.org/lib/module-BaseHTTPServer.html
    '''

    def __init__(self, server_address, RequestHandlerClass, session):
        BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.RequestHandlerClass.session = session


########################################################################################################################
class web_interface_thread (threading.Thread):
    def __init__ (self, session):
        threading.Thread.__init__(self)

        self.session = session
        self.server  = None


    def run (self):
        self.server = web_interface_server(('', self.session.web_port), web_interface_handler, self.session)
        self.server.serve_forever()
