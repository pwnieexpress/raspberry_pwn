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

from Queue import Queue

import sip_parser

from sip_transaction_manager import SIPTransactionManager

from sip_agent import SIPCancel
from sip_agent import SIPAck
from sip_agent import SIPAgent
from sip_agent import SIPRegister
from sip_agent import SIPInvite


response_q = Queue(0)
request_q = Queue(0)

sip_agent = SIPAgent()

ack = SIPAck()
cancel = SIPCancel()
register = SIPRegister()
invite = SIPInvite()

SIPTransactionManager(request_q, response_q).start()

invite_dict = {sip_parser.r_SEND :
                 (invite.process,
                  {
                      sip_parser.r_1XX :
                      (cancel.process,
                       {
                           sip_parser.r_1XX : (None, None),
                           sip_parser.r_2XX : (None, None),                           
                           sip_parser.r_6XX : (ack.process, None),
                           sip_parser.r_4XX : (ack.process, None)
                           }
                       )
                   }
                  )
                }

result = sip_agent.process_transaction(
    invite_dict,
    response_q,
    request_q,
    {'user' : sys.argv[1],
     'host' : sys.argv[2],
     'port' : int(sys.argv[3])}
    )

