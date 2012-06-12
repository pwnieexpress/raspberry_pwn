from sulley import *

s_initialize("INVITE_VALID")

s_static('\r\n'.join(['INVITE sip:tester@192.168.3.104 SIP/2.0',
'CSeq: 1 INVITE',
'Via: SIP/2.0/UDP 192.168.3.102:5068;branch=z9hG4bKlm4zshdowki1t8c7ep6j0yavq2ug5r3x;rport',
'From: "nnp" <sip:nnp@192.168.3.104>;tag=so08p5k39wuv1dczfnij7bet4l2m6hrq',
'Call-ID: rzxd6tm98v0eal1cifg2py7sj3wk54ub@ubuntu',
'To: <sip:nnp@192.168.3.101>',
'Max-Forwards: 70',
'Content-Type: application/sdp',
'\r\n',
'v=0',
'o=somegimp 1190505265 1190505265 IN IP4 192.168.3.101',
's=Opal SIP Session',
'i=some information string',
'u=http://unprotectedhex.com/someuri.htm',
'e=email@address.com',
'c=IN IP4 192.168.3.101',
'b=CT:8',
't=0 1',
'm=audio 5028 RTP/AVP 101 96 107 110 0 8',
'a=rtpmap:101 telephone-event/8000',                     
]))

################################################################################

s_initialize("CANCEL_VALID")
s_static('\r\n'.join(['CANCEL sip:tester@192.168.3.104 SIP/2.0',
'CSeq: 1 CANCEL',
'Via: SIP/2.0/UDP 192.168.3.102:5068;branch=z9hG4bKlm4zshdowki1t8c7ep6j0yavq2ug5r3x;rport',
'From: "nnp" <sip:nnp@192.168.3.104>;tag=so08p5k39wuv1dczfnij7bet4l2m6hrq',
'Call-ID: rzxd6tm98v0eal1cifg2py7sj3wk54ub@ubuntu',
'To: <sip:nnp@192.168.3.101>',
'Max-Forwards: 70',
'\r\n'
]))


