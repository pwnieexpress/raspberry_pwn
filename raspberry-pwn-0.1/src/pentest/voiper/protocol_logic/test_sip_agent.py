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

from sip_agent import SIPCanceler
from sip_parser import SIPParser
from sip_transaction_manager import TData

invite1 = '\r\n'.join(['INVITE sip:nnp@192.168.3.104 SIP/2.0',
'Date: Sun, 23 Sep 2007 00:23:19 GMT',
'CSeq: 1 INVITE',
'Via: SIP/2.0/UDP 192.168.3.102:5071;branch=z9hG4bKa8f5f4da-d867-dc11-8c7d-000c29da463b;rport',
'User-Agent: Ekiga/2.0.3',
'From: "nnp nnp" <sip:nnp@192.168.3.102>;tag=a68cf4d7-d867-dc11-8c7d-000c29da463b',
'Call-ID: MOFOID@ubuntu',
'To: <sip:nnp@192.168.3.104>',
'Contact: <sip:nnp@192.168.3.102:5071;transport=udp>',
'Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,NOTIFY,REFER,MESSAGE',
'Content-Type: application/sdp',
'Content-Length: 389',
'Max-Forwards: 70']) + '\r\n\r\n'
                      
invite1 = invite1 + '\r\n'.join(['v=0',
'o=- 1190506999 1190506999 IN IP4 192.168.3.102',
's=Opal SIP Session',
'c=IN IP4 192.168.3.102',
't=0 0',
'm=audio 5040 RTP/AVP 101 96 3 107 110 0 8',
'a=rtpmap:101 telephone-event/8000',
'a=fmtp:101 0-15',
'a=rtpmap:96 SPEEX/-1',
'a=rtpmap:3 GSM/8000',
'a=rtpmap:107 MS-GSM/8000',
'a=rtpmap:110 SPEEX/-1',
'a=rtpmap:0 PCMU/8000',
'a=rtpmap:8 PCMA/8000',
'm=video 5042 RTP/AVP 31',
'a=rtpmap:31 H261/-1']) + '\r\n'

cancel1 = '\r\n'.join(['CANCEL sip:nnp@192.168.3.104 SIP/2.0',
'CSeq: 1 CANCEL',
'Via: SIP/2.0/UDP 192.168.3.102:5071;branch=z9hG4bKa8f5f4da-d867-dc11-8c7d-000c29da463b;rport',
'To: <sip:nnp@192.168.3.104>',                       
'From: "nnp nnp" <sip:nnp@192.168.3.102>;tag=a68cf4d7-d867-dc11-8c7d-000c29da463b',
'Call-ID: MOFOID@ubuntu',
'Max-Forwards: 70']) + '\r\n\r\n'

data_dict = SIPParser().parse(invite1)
t_data = TData(invite1, data_dict, None)

s_canceler= SIPCanceler(None, None)
cancel_request = s_canceler.create_cancel(t_data)
assert(cancel_request == cancel1)

