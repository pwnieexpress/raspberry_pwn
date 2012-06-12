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

from sip_parser import *

data1 = '\r\n'.join(['INVITE sip:nnp@192.168.3.104 SIP/2.0',
'Date: Sun, 23 Sep 2007 00:23:19 GMT',
'CSeq: 13456 INVITE',
'Via: SIP/2.0/UDP 192.168.3.102:5071;branch=z9hG4bKa8f5f4da-d867-dc11-8c7d-000c29da463b;rport',
'User-Agent: Ekiga/2.0.3',
'From: "nnp nnp" <sip:nnp@192.168.3.102>;tag=a68cf4d7-d867-dc11-8c7d-000c29da463b',
'Call-ID: MOFOID@ubuntu',
'To: <sip:nnp@192.168.3.104>',
'Contact: <sip:nnp@192.168.3.102:5062>',
'WWW-Authenticate: Digest algorithm=MD5, realm="192.168.3.101", nonce="6eec05-jhg6jhg"',                     
'Allow: INVITE',
'Content-Type: application/sdp',
'Content-Length: 389',
'Max-Forwards: 70']) + '\r\n\r\n'
                      
data1 = data1 + '\r\n'.join(['v=0',
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

data2 = """SIP/2.0 200 OK sip:nnp@192.168.3.104 SIP/2.0
Date: Sun, 23 Sep 2007 00:23:19 GMT
CSeq: 1 INVITE
Via: SIP/2.0/UDP 192.168.3.102:5071;branch=z9hG4bKa8f5f4da-d867-dc11-8c7d-000c29da463b;rport
User-Agent: Ekiga/2.0.3
From: "nnp nnp" <sip:nnp@192.168.3.102>;tag=a68cf4d7-d867-dc11-8c7d-000c29da463b
Call-ID: MOFOID@ubuntu
To: <sip:nnp@192.168.3.104>
Contact: <sip:nnp@192.168.3.102>
Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,NOTIFY,REFER,MESSAGE
Content-Type: application/sdp
Content-Length: 389
Max-Forwards: 70
"""

data3 = """ACK sip:nnp@192.168.3.104 SIP/2.0
Date: Sun, 23 Sep 2007 00:23:19 GMT
CSeq: 1 ACK
Via: SIP/2.0/UDP 192.168.3.102:5071;branch=z9hG4bKa8f5f4da-d867-dc11-8c7d-000c29da463b;rport
User-Agent: Ekiga/2.0.3
From: "nnp nnp" <sip:nnp@192.168.3.102>;tag=a68cf4d7-d867-dc11-8c7d-000c29da463b
Call-ID: MOFOID@ubuntu
To: <sip:nnp@192.168.3.104>
Contact: <sip:nnp@192.168.3.102:5071;transport=udp>
Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,NOTIFY,REFER,MESSAGE
Content-Type: application/sdp
Content-Length: 389
Max-Forwards: 70
"""

data4 = '\r\n'.join(['REGISTER sip:nnp@192.168.3.104 SIP/2.0',
'Date: Sun, 23 Sep 2007 00:23:19 GMT',
'CSeq: 1 REGISTER',
'Via: SIP/2.0/UDP 192.168.3.102:5071;branch=z9hG4bKa8f5f4da-d867-dc11-8c7d-000c29da463b;rport',
'User-Agent: Ekiga/2.0.3',
'From: "nnp nnp" <sip:nnp@192.168.3.102>;tag=a68cf4d7-d867-dc11-8c7d-000c29da463b',
'Call-ID: MOFOID@ubuntu',
'To: <sip:nnp@192.168.3.104>',
'Contact: <sip:nnp@192.168.3.102:5071;transport=udp>',
'WWW-Authenticate: Digest algorithm=MD5, realm="asterisk", nonce="6eec05"'                     
'Allow: INVITE',
'Content-Type: application/sdp',
'Max-Forwards: 70']) + '\r\n\r\n'

parser = SIPParser()

res = parser.parse(data1, [CONTACT])
assert(res == {CONTACT : '<sip:nnp@192.168.3.102:5062>'})

res = parser.parse(data2, [CONTACT])
assert(res == {CONTACT : '<sip:nnp@192.168.3.102>'})

res = parser.parse(data3, [CONTACT])
assert(res == {CONTACT : '<sip:nnp@192.168.3.102:5071;transport=udp>'})

res = parser.parse(data4, [WWW_AUTHEN_REALM])
assert(res == {WWW_AUTHEN_REALM : 'asterisk'})

res = parser.parse(data1, [WWW_AUTHEN_REALM])
assert(res == {WWW_AUTHEN_REALM : '192.168.3.101'})

res = parser.parse(data4, [WWW_AUTHEN_NONCE])
assert(res == {WWW_AUTHEN_NONCE : '6eec05'})

res = parser.parse(data1, [WWW_AUTHEN_NONCE])
assert(res == {WWW_AUTHEN_NONCE : '6eec05-jhg6jhg'})

res = parser.parse(data1, [BRANCH])
assert(res == {BRANCH : 'z9hG4bKa8f5f4da-d867-dc11-8c7d-000c29da463b'})

res = parser.parse(data1, [FROM])
assert(res == {FROM : '"nnp nnp" <sip:nnp@192.168.3.102>;tag=a68cf4d7-d867-dc11-8c7d-000c29da463b'})

res = parser.parse(data1, [TO])
assert(res == {TO : '<sip:nnp@192.168.3.104>'})

res = parser.parse(data1, [FROMTAG])
assert(res == {FROMTAG : 'a68cf4d7-d867-dc11-8c7d-000c29da463b'})

res = parser.parse(data1, [CALLID])
assert(res == {CALLID : 'MOFOID@ubuntu'})

res = parser.parse(data1, [CSEQNUM])
assert(res == {CSEQNUM : '13456'})

res = parser.parse(data2, [RCODE])
assert(res == {RCODE : r_2XX})

res = parser.parse(data4, [RCODE])
assert(res == {RCODE : r_REGISTER})

res = parser.parse(data3, [RCODE])
assert(res == {RCODE : r_ACK})

res = parser.parse(data1, [RURI])
assert(res == {RURI : 'sip:nnp@192.168.3.104'})

res = parser.parse(data1, [VIA])
assert(res == {VIA : 'SIP/2.0/UDP 192.168.3.102:5071;branch=z9hG4bKa8f5f4da-d867-dc11-8c7d-000c29da463b;rport'})
