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
import time
# modify import path instead of adding a __init__.py as I want to keep 
# a the Sulley install as unmodified as possible to facilitate easy updating 
# if there are changes to it. 
# Props to Pedram Amini and Aaron Portnoy for creating such a great framework
sys.path.append(''.join([os.getcwd(), '/sulley']))

from random import Random

from protocol_logic.sip_agent import T_COMPLETE_OK
from protocol_logic.sip_utilities import SIPCrashDetector
from protocol_logic.sip_utilities import SIPInviteCanceler
from protocol_logic import sip_parser

from misc.utilities import Logger

from fuzzer_parents import AbstractFuzzer
from fuzzer_parents import AbstractSIPFuzzer
from fuzzer_parents import AbstractSIPInviteFuzzer

from socket import *        
from sulley import *

################################################################################
class Callable:
    def __init__(self, anycallable):
        '''
        Wrapper class so I can have unbound class methods. Apparently python doesn't
        allow these by default. This code/idiom came from some standard example on the
        Interwebs
        '''
        self.__call__ = anycallable

class SIPInviteStructureFuzzer(AbstractSIPInviteFuzzer):
    '''
    Fuzz the structure of an INVITE request e.g repeats, line folding etc
    '''
    def fuzz(self):
        self.sess.add_target(self.target)
        self.sess.connect(s_get("INVITE_STRUCTURE"), callback=self.generate_unique_attributes)
        self.sess.fuzz()

    def info(self=None):
        h = ["Name: SIPInviteStructureFuzzer\n",
             "Protocol: SIP\n",
             "Success Factor: Low\n",
             "Fuzzes the structure of a SIP request by repeating blocks, fuzzing delimiters and ",
             "generally altering how a SIP request is structured",
             ]
        return ''.join(h)

    info = Callable(info)
        
class SIPInviteRequestLineFuzzer(AbstractSIPInviteFuzzer):
    def fuzz(self):
        self.sess.add_target(self.target)
        self.sess.connect(s_get("INVITE_REQUEST_LINE"), callback=self.generate_unique_attributes)
        self.sess.fuzz()

    def info(self=None):
        h = ["Name: SIPInviteRequestLineFuzzer\n",
             "Protocol: SIP\n",
             "Success Factor: Low\n",
             "Extensively tests the first line of an INVITE request by including all valid parts ",
             "specified in SIP RFC 3375"
             ]
        return ''.join(h)

    info = Callable(info)
        
class SIPInviteCommonFuzzer(AbstractSIPInviteFuzzer):    
    def fuzz(self):
        self.sess.add_target(self.target)
        self.sess.connect(s_get("INVITE_COMMON"), callback=self.generate_unique_attributes)
        self.sess.fuzz()

    def info(self=None):        
        h = ["Name: SIPInviteCommonFuzzer\n",
             "Protocol: SIP\n",
             "Success Factor: High\n",
             "Fuzzes the headers commonly found and most likely to be processed in a SIP INVITE request\n"
             ]
        return ''.join(h)
    
    info = Callable(info)    

class SIPInviteOtherFuzzer(AbstractSIPInviteFuzzer):
    def fuzz(self):
        self.sess.add_target(self.target)
        self.sess.connect(s_get("INVITE_OTHER"), callback=self.generate_unique_attributes)
        self.sess.fuzz()

    def info(self=None):
        h = ["Name: SIPInviteOtherFuzzer\n",
             "Protocol: SIP\n",
             "Success Factor: Low\n",
             "Tests all other headers specified as part of an INVITE besides those found in the ",
             "SIPInviteCommonFuzzer. Many of these are seemingly unparsed and ignored by a lot of devices.\n"
             ]
        return ''.join(h)

    info = Callable(info)    

class SDPFuzzer(AbstractSIPInviteFuzzer):
    '''
    Extends the Abstract INVITE fuzzer because it requires the INVITE
    cancelling functionality. Fuzzes the SDP content of an INVITE.
    '''
    
    def fuzz(self):        
        self.sess.add_target(self.target)
        self.sess.connect(s_get("SDP"), callback=self.generate_unique_attributes)
        self.sess.fuzz()

    def info(self=None):
        h = ["Name: SDPFuzzer\n",
             "Protocol: SDP\n",
             "Success Factor: High\n",
             "Fuzzes the SDP protocol as part of a SIP INVITE\n"
             ]
        return ''.join(h)
            
    info = Callable(info)

class SIPDumbACKFuzzer(AbstractSIPFuzzer):
    '''
    A dumb ACK fuzzer that doesn't wait for any kind of responses or what not.    
    '''

    def fuzz(self):        
        self.sess.add_target(self.target)
        self.sess.connect(s_get("ACK"), callback=self.generate_unique_attributes)
        self.sess.fuzz()
        
    def info(self=None):
        h = ["Name: SIPDumbACKFuzzer\n",
             "Protocol: SIP\n",
             "Success Factor: Unknown\n",
             "A dumb ACK fuzzer with no transaction state awareness. \n",
             ]
        return ''.join(h)
            
    info = Callable(info)

class SIPDumbCANCELFuzzer(AbstractSIPFuzzer):
    '''
    A dumb CANCEL fuzzer that doesn't wait for any kind of responses or what not.    
    '''

    def fuzz(self):        
        self.sess.add_target(self.target)
        self.sess.connect(s_get("CANCEL"), callback=self.generate_unique_attributes)
        self.sess.fuzz()
        
    def info(self=None):
        h = ["Name: SIPDumbCANCELFuzzer\n",
             "Protocol: SIP\n",
             "Success Factor: Unknown\n",
             "A dumb CANCEL request fuzzer with no transaction state awareness\n",
             ]
        return ''.join(h)
            
    info = Callable(info) 

class SIPDumbREGISTERFuzzer(AbstractSIPFuzzer):

    def fuzz(self):        
        self.sess.add_target(self.target)
        self.sess.connect(s_get("REGISTER"), callback=self.generate_unique_attributes)
        self.sess.fuzz()
        
    def info(self=None):
        h = ["Name: SIPDumbREGISTERFuzzer\n",
             "Protocol: SIP\n",
             "Success Factor: Unknown\n",
             "A dumb REGISTER request fuzzer with no transaction state awareness\n",
             ]
        return ''.join(h)
            
    info = Callable(info)
    
class SIPSUBSCRIBEFuzzer(AbstractSIPFuzzer):

    def fuzz(self):        
        self.sess.add_target(self.target)
        self.sess.connect(s_get("SUBSCRIBE"), callback=self.generate_unique_attributes)
        self.sess.fuzz()
        
    def info(self=None):
        h = ["Name: SIPSUBSCRIBEFuzzer\n",
             "Protocol: SIP\n",
             "Success Factor: Unknown\n",
             "A fuzzer for the SUBSCRIBE SIP verb\n",
             ]
        return ''.join(h)
            
    info = Callable(info)

class SIPNOTIFYFuzzer(AbstractSIPFuzzer):

    def fuzz(self):        
        self.sess.add_target(self.target)
        self.sess.connect(s_get("NOTIFY"), callback=self.generate_unique_attributes)
        self.sess.fuzz()
        
    def info(self=None):
        h = ["Name: SIPNOTIFYFuzzer\n",
             "Protocol: SIP\n",
             "Success Factor: Unknown\n",
             "A fuzzer for the NOTIFY SIP verb\n",
             ]
        return ''.join(h)
            
    info = Callable(info)

class SIPACKFuzzer(AbstractSIPFuzzer):

    def fuzz(self):
        self.invite_cancel_dict = {
            sip_parser.r_SEND : (self.invite.process, 
                {sip_parser.r_1XX : (self.cancel.process,
                 {sip_parser.r_4XX : (None, None),
                  sip_parser.r_5XX : (None, None),                                                  
                  sip_parser.r_6XX : (None, None),
                  sip_parser.r_2XX : (None, None),
                  }
                 )
                }
            )
        }
        
        self.pre_send_functions.append(self.invite_cancel)
        self.sess.add_target(self.target)
        self.sess.connect(s_get("ACK"), callback=self.generate_unique_attributes)
        self.sess.fuzz()
        
    def info(self=None):
        h = ["Name: SIPACKFuzzer\n",
             "Protocol: SIP\n",
             "Success Factor: Unknown\n",
             "A fuzzer for the ACK SIP verb that first attempts to manipulate the target device into a state where it would expect an ACK\n",
             ]
        return ''.join(h)
            
    info = Callable(info)

    def invite_cancel(self, sock):
        result = None
        while result != T_COMPLETE_OK:
            result, self.curr_invite_branch = self.sip_agent.process_transaction(
                self.invite_cancel_dict,
                self.response_q,
                self.request_q,
                {'user' : self.user,
                 'target_user' : self.target_user,
                 'host' : self.host,
                 'port' : self.port}
                )

            if result != T_COMPLETE_OK:
                print >>sys.stderr, 'Invite cancel for ACK fuzz didnt complete. Trying again'
                time.sleep(.2)
'''
class SDPEncodedFuzzer(AbstractSIPInviteFuzzer):
    
    def fuzz(self):        
        self.sess.add_target(self.target)
        self.sess.connect(s_get("SDP_ENCODED"), callback=self.generate_unique_attributes)
        self.sess.fuzz()

class OptionsFuzzer(AbstractSIPFuzzer):
    def fuzz(self):
        self.sess.add_target(self.target)
        self.sess.connect(s_get("OPTIONS"), callback=self.generate_unique_attributes)
        self.sess.fuzz()
'''
        
################################################################################
