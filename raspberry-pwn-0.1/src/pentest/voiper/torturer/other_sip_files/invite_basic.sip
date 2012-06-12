INVITE [SIP-URI] SIP/2.0
CSeq: 1 INVITE
Via: SIP/2.0/UDP [OUR-IP]:5067;branch=z9hG4bK3862c2ce-526c-dc11-89e6-000c29da463b;rport
From: "nnp" <sip:nnp@[OUR-IP]>;tag=422ec2cb-526c-dc11-89e6-000c29da463b
Call-ID: 80e1c1cb-526c-dc11-89e6-000c29da463b@ubuntu
To: <[SIP-URI]>
Contact: <sip:nnp@[OUR-IP]:5067;transport=[TRANSPORT]>
Max-Forwards: 70

v=0
o=- 1190505265 1190505265 IN IP4 192.168.3.104
s=Opal SIP Session
c=IN IP4 192.168.3.102
t=0 0
m=audio 5028 RTP/AVP 101 96 3 107 110 0 8
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-15
a=rtpmap:96 SPEEX/16000
a=rtpmap:3 GSM/8000
a=rtpmap:107 MS-GSM/8000
a=rtpmap:110 SPEEX/8000
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
m=video 5030 RTP/AVP 31
a=rtpmap:31 H261/90000

