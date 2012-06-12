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

from sip_agent import SIPOptions
from sip_agent import SIPAgent

response_q = Queue(0)
request_q = Queue(0)

sip_agent = SIPAgent()
options = SIPOptions()

SIPTransactionManager(request_q, response_q).start()

options_dict = {sip_parser.r_SEND :
                 (options.process,
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
                  
                  
result = sip_agent.process_transaction(
    options_dict,
    response_q,
    request_q,
    {
     'host' : sys.argv[1],
     'port' : int(sys.argv[2]),
     'user' : sys.argv[3],
     'target_user' : sys.argv[4]}
    )


