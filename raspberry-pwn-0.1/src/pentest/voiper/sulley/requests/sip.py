import base64
import string
import zlib

from random import Random

from sulley import *

'''
Contains fuzz cases for INVITE (all headers and the base headers) and
sdp
'''

def base64_encode(val):
    return base64.b64encode(val)

def gzip_encode(val):
    return zlib.compress(val)

################################################################################

s_initialize("INVITE_STRUCTURE")

if s_block_start("invite"):
    if s_block_start("invite_sip"):
        if s_block_start("request_line"):
            s_static("INVITE sip:TARGET_USER@HOST SIP/2.0\r\n")
        s_block_end()
        s_repeat("request_line", min_reps=2, max_reps=100, step=10)

        if s_block_start("invite_header"):
            # repeat of a line that shouldn't appear multiple times
            if s_block_start("cseq"):
                s_static("CSeq: 1 INVITE\r\n")
            s_block_end()
            s_repeat("cseq", min_reps=2, max_reps=1000, step=10)

            # repeat of a line that could appear multiple times
            if s_block_start("via"):
                s_static("Via: SIP/2.0/UDP LOCAL_IP:PORT;branch=z9hG4bKsomebranchvalue;rport\r\n")
            s_block_end()
            s_repeat("via", min_reps=2, max_reps=1000, step=10)

            s_static("From: \"nnp\" <sip:USER@LOCAL_IP>;tag=somefromtagvalue\r\n")

            # Fuzz the structure of a line
            s_string("Call-ID")
            s_delim(" ")
            s_delim(":")
            if s_block_start("call_id_body"):
                s_delim(" ")
                s_static("somecallidvalue@ubuntu")
                s_delim("\r\n")
            s_block_end()
            # this test will test where one attribute runs into another e.g no EOL
            s_repeat("call_id_body", min_reps=0, max_reps=1, step=1)        

            s_static("To:")
            if s_block_start("to_body"):
                s_static("<sip:TARGET_USER@HOST>")
            s_block_end()
            s_static("\r\n")
            # this test will test for an empty body
            s_repeat("to_body", min_reps=0, max_reps=1, step=1)        
            
            # Line folding
            s_static("Contact: <sip:USER@LOCAL_IP:PORT;transport=udp>\r\n")
            if s_block_start("line_folding"):
                #line folding
                s_static(" ,<sip:meh@LOCAL_IP:PORT;transport=udp>\r\n")
            s_block_end()
            s_repeat("line_folding", min_reps=2, max_reps=1000, step=10)
            
            s_static("Max-Forwards: 70\r\n\r\n")
        s_block_end()
        # repetition of the header portion of the INVITE
        s_repeat("invite_header", min_reps=2, max_reps=1000, step=10)
    s_block_end()
    # repitition of the SIP portion of the request
    s_repeat("invite_sip", min_reps=2, max_reps=1000, step=10)

    if not s_block_start("invite_sdp"):
        s_static("v=0\r\n")
        s_static("o=- 1190505265 1190505265 IN IP4 LOCAL_IP\r\n")
        s_static("s=Opal SIP Session\r\n")
        s_static("c=IN IP4 LOCAL_IP\r\n")
        s_static("t=0 0\r\n")
        s_static("m=audio 5028 RTP/AVP 101 96 3 107 110 0 8\r\n")
        s_static("a=rtpmap:101 telephone-event/8000\r\n")
        s_static("a=fmtp:101 0-15\r\n")
        s_static("a=rtpmap:96 SPEEX/16000\r\n")
        s_static("a=rtpmap:3 GSM/8000\r\n")
        s_static("a=rtpmap:107 MS-GSM/8000\r\n")
        s_static("a=rtpmap:110 SPEEX/8000\r\n")
        s_static("a=rtpmap:0 PCMU/8000\r\n")
        s_static("a=rtpmap:8 PCMA/8000\r\n")
        s_static("m=video 5030 RTP/AVP 31\r\n")
        s_static("a=rtpmap:31 H261/90000\r\n")
    s_block_end()
    # repitition of the SDP portion of the message
    s_repeat("invite_sdp", min_reps=2, max_reps=1000, step=10)
s_block_end()
# repitition of the entire INVITE
s_repeat("invite", min_reps=2, max_reps=1000, step=10)

################################################################################

s_initialize("INVITE_REQUEST_LINE")

if s_block_start("invite_request_line"):
    #s_static("INVITE sip:TARGET_USER:secretword@192.168.3.101?subject=weeee&priority=urgent;transport=udp SIP/2.0\r\n")
    s_string("INVITE")
    s_delim(" ")
    s_string("sip")
    s_delim(":")
    # userinfo
    s_string("TARGET_USER")
    # asterisk doesn't like this
    # s_delim(":")
    #s_string("password")
    s_delim("@")
    # hostport
    s_string("HOST")
    s_delim(":")
    s_string("PORT")
    # uri-parameters
    s_delim(";")
    s_string("transport")
    s_delim("=")
    s_string("udp")
    s_static(";")
    s_static("user=")
    s_string("udp")
    s_static(";")
    s_static("ttl=")
    s_string("67")
    s_static(";")
    s_static("method=")
    s_string("INVITE")
    s_static(";")
    s_static("maddr=")
    s_string("HOST")
    # headers
    s_delim("?")
    s_string("subject=")
    s_delim("=")
    s_string("hval")
    s_delim("&")
    s_static("hname2=hval")
    s_delim(" ")
    s_string("SIP")
    s_delim("/")
    s_string("2.0")
    s_delim("\r\n")
s_block_end()

if s_block_start("invite_header"):
    s_static("CSeq: 1 INVITE\r\n")
    s_static("Via: SIP/2.0/UDP LOCAL_IP:PORT;branch=z9hG4bKsomebranchvalue;rport\r\n")
    s_static("From: \"nnp\" <sip:USER@LOCAL_IP>;tag=somefromtagvalue\r\n")
    s_static("Call-ID: somecallidvalue@ubuntu\r\n")
    s_static("To: <sip:TARGET_USER@HOST>\r\n")
    s_static("Contact: <sip:USER@LOCAL_IP:PORT;transport=udp>\r\n")
    s_static("Max-Forwards: 70\r\n\r\n")
s_block_end()
    
################################################################################

s_initialize("INVITE_OTHER")

if s_block_start("invite_request_line"):
    s_static("INVITE sip:TARGET_USER@HOST SIP/2.0\r\n")
s_block_end()

if s_block_start("invite_header"):    
    s_static("CSeq: 1 INVITE\r\n")
    s_static("Via: SIP/2.0/UDP LOCAL_IP:5060;branch=z9hG4bKsomebranchvalue;rport\r\n")
    s_static("From: \"VoIPER\" <sip:USER@LOCAL_IP>;tag=somefromtagvalue\r\n")
    s_static("Call-ID: somecallidvalue@ubuntu\r\n")
    s_static("To: <sip:TARGET_USER@HOST>\r\n")
    s_static("Max-Forwards: 70\r\n")
    s_static("Contact: <sip:USER@LOCAL_IP:5060;transport=udp>\r\n")

    ##    Date          =  "Date" HCOLON SIP-date
    ##    SIP-date      =  rfc1123-date
    ##    rfc1123-date  =  wkday "," SP date1 SP time SP "GMT"
    ##    date1         =  2DIGIT SP month SP 4DIGIT
    ##                     ; day month year (e.g., 02 Jun 1982)
    ##    time          =  2DIGIT ":" 2DIGIT ":" 2DIGIT
    ##                     ; 00:00:00 - 23:59:59
    #s_static("Date: Sat, 22 Sep 2007 23:54:25 GMT\r\n")
    s_static("Date: ")
    s_string("Sat")
    s_delim(",")
    s_delim(" ")
    s_dword(22, fuzzable=True, format="ascii", signed=True)
    s_delim(" ")
    s_string("Sep")
    s_delim(" ")
    s_dword(2007, fuzzable=True, format="ascii", signed=True)
    s_static(" ")
    s_dword(23, fuzzable=True, format="ascii", signed=True)
    s_delim(":")
    s_dword(59, fuzzable=True, format="ascii", signed=True)
    s_static(":")
    s_dword(25, fuzzable=True, format="ascii", signed=True)
    s_static(" ")
    s_string("GMT")
    s_static("\r\n")
    
    #s_static("Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,NOTIFY,REFER,MESSAGE\r\n")
    s_static("Allow: ")
    s_string("INVITE")
    s_static(",")
    s_static("ACK,OPTIONS,BYE,CANCEL,NOTIFY,REFER,MESSAGE")
    s_static("\r\n")

    # Fuzzed in the basic fuzzer
    s_static("Content-Type: application/sdp\r\n")
    
    # Content-Length
    s_static("Content-Length: ")
    s_sizer("invite_sdp", format="ascii", fuzzable=False, signed=True)
    s_static("\r\n")

    #s_static("Expires: 3600\r\n")
    s_static("Expires: ")
    s_string("3600")
    s_static("\r\n")
    
    #s_static("User-Agent: Ekiga/2.0.3\r\n")
##    User-Agent  =  "User-Agent" HCOLON server-val *(LWS server-val)
##    server-val       =  product / comment
##    product          =  token [SLASH product-version]
##    product-version  =  token
    s_static("User-Agent: ")
    s_string("VoIPER")
    s_delim("/")
    s_string("0.02")
    s_delim(" ")
    s_string("Clack/0.02")
    s_static("\r\n")
    
    #s_static("Subject: This is a subject header field\r\n")
    s_static("Subject: ")
    s_string("Commander Vimes has been attacked by a turnip")
    s_static("\r\n")
    
    #s_static("Organization: This is an organization field\r\n")
    s_static("Organization: ")
    s_string("Ankh Morpok City Watch")
    s_static("\r\n")
    
    #s_static("Accept-Encoding: compress;q=0.5, identity\r\n")
    ##    Accept-Encoding  =  "Accept-Encoding" HCOLON
    ##                         [ encoding *(COMMA encoding) ]
    ##    encoding         =  codings *(SEMI accept-param)
    ##    codings          =  content-coding / "*"
    ##    content-coding   =  token
    s_static("Accept-Encoding: ")
    s_string("compress")
    s_static(";")
    s_lego("q_value")
    s_delim(",")
    s_static("identity")
    s_static("\r\n")
    
    #s_static("Alert-Info: <http://www.examplesite.com/something.wav>\r\n")
    ##    Alert-Info   =  "Alert-Info" HCOLON alert-param *(COMMA alert-param)
    ##    alert-param  =  LAQUOT absoluteURI RAQUOT *( SEMI generic-param )
    s_static("Alert-Info: ")
    s_delim("<")
    s_string("http://www.examplesite.com/")
    s_string("something.wav")
    s_delim(">")
    s_static(";")
    s_string("x")
    s_static("=")
    s_string("y")
    s_delim(",")
    s_string("<http://www.examplesite.com/something.wav>")    
    s_static("\r\n")
    
    #s_static("Call-Info: <http:/www.example.com/icon.jpg> ;purpose=icon,<http:/www.example.com/alice/> \
    #       ;purpose=info,<http:/www.example.com/card.vcard> ;purpose=card\r\n")
    ##    Call-Info   =  "Call-Info" HCOLON info *(COMMA info)
    ##    info        =  LAQUOT absoluteURI RAQUOT *( SEMI info-param)
    ##    info-param  =  ( "purpose" EQUAL ( "icon" / "info"
    ##                   / "card" / token ) ) / generic-param
    s_static("Call-Info: ")
    s_delim("<")
    s_string("http://www.examplesite.com/")
    s_string("something")
    s_delim(".")
    s_string("jpg")
    s_delim(">")
    s_delim(";")
    s_string("purpose")
    s_delim("=")
    s_group("call_info_params", values=['icon', 'info', 'card'])
    s_static(",")
    s_string("<http:/www.example.com/alice/>")
    s_static(";purpose=info,<http:/www.example.com/card.vcard> ;purpose=card\r\n")

    
    #s_static("Supported: 100rel\r\n")
    s_static("Supported: ")
    s_string("100rel")
    s_static(",")
    s_static("replaces")
    s_static("\r\n")
    
    #s_static("Content-Disposition: session\r\n")
    ##    Content-Disposition   =  "Content-Disposition" HCOLON
    ##                             disp-type *( SEMI disp-param )
    ##    disp-type             =  "render" / "session" / "icon" / "alert"
    ##                             / disp-extension-token
    ##
    ##    disp-param            =  handling-param / generic-param
    ##    handling-param        =  "handling" EQUAL
    ##                             ( "optional" / "required"
    ##                             / other-handling )
    ##    other-handling        =  token
    ##    disp-extension-token  =  token
    s_static("Content-Disposition: ")
    s_group("content_disposition_types", values=['session', 'icon', 'alert'])
    s_delim(";")
    s_static("handling")
    s_static("=")
    s_string("optional")
    s_static("\r\n")
    
    #s_static("Accept-Language: da,en-gb;q=0.8,en;q=0.7\r\n")
    ##    Accept-Language  =  "Accept-Language" HCOLON
    ##                         [ language *(COMMA language) ]
    ##    language         =  language-range *(SEMI accept-param)
    ##    language-range   =  ( ( 1*8ALPHA *( "-" 1*8ALPHA ) ) / "*" )
    s_static("Accept-Language: ")
    s_string("da")
    s_static(",")
    s_string("en")
    s_delim("-")
    s_string("gb")
    s_delim(";")
    s_lego("q_value")
    s_delim(",")
    s_string("en")
    s_static(";q=0.7\r\n")
    
    #s_static("Authorization: Digest username=\"nnp\", realm=\"bleh.com\", nonce=\"value\", response=\"value\"\r\n")
    s_static("Authorization: ")
    s_lego("static_credentials")
    s_static("\r\n")

    # fuzz this in an SDP fuzzer instead    
    #s_static("Content-Encoding: gzip\r\n")
    
    #s_static("Content-Language: en,da\r\n")
    s_static("Content-Language: ")
    s_string("da")
    s_delim(",")
    s_string("en")
    s_delim("-")
    s_string("gb")
    s_static("\r\n")
    
    #s_static("In-Reply-To: 1447@example.com\r\n")
    s_static("In-Reply-To: ")
    s_string("1447")
    s_delim("@")
    s_string("example.com")
    s_delim(",")
    s_string("1445@example.com")
    s_static("\r\n")

    #s_static("Priority: emergency\r\n")
    s_static("Priority: ")
    s_string("emergency")
    s_static("\r\n")
    
    #s_static("Proxy-Require: 100rel\r\n")
    s_static("Proxy-Require: ")
    s_string("replaces")
    s_delim(",")
    s_string("replaces")
    s_static("\r\n")
    
    #s_static("Require: 100rel\r\n")
    s_static("Require: ")
    s_string("replaces")
    s_delim(",")
    s_string("replaces")
    s_static("\r\n")
    
    #s_static("Record-Route: <sip:server10.biloxi.com;lr>, <sip:server11.biloxi.com;lr>\r\n")
    if s_block_start("record_route"):
        s_static("Record-Route: ")
        s_string("bob")
        s_delim(" ")
        s_delim("<")
        s_string("sip")
        s_delim(":")
        s_string("unprotectedhex.com")
        s_delim(";")
        s_string("lr")
        s_delim(">")
        s_static("\r\n")
    s_block_end()
    s_repeat("record_route", min_reps=10, max_reps=1000, step=10)
    
    #s_static("Reply-To: Bob <sip:bob@biloxi.com>\r\n")
    s_static("Reply-To: ")
    s_string("bob")
    s_delim(" ")
    s_delim("<")
    s_string("sip")
    s_delim(":")
    s_string("unprotectedhex.com")
    s_delim(";")
    s_string("lr")
    s_delim(">")
    s_static("\r\n")
    
    #s_static("Route: <sip:server10.biloxi.com;lr>, <sip:server11.biloxi.com;lr>\r\n")
    s_static("Route: ")
    if s_block_start("route_attributes"):
        s_delim("<")
        s_string("sip")
        s_delim(":")
        s_string("unprotectedhex.com")
        s_delim(";")
        s_string("lr")
        s_delim(">")
        s_delim(",")
        s_string("<pbx.smashthestack.org;lr>")
        s_static(",")
    s_block_end()
    s_repeat("route_attributes", min_reps=10, max_reps=1000, step=10)    
    s_static("\r\n")
    
    #s_static("Timestamp: 42\r\n")
    s_static("Timestamp: ")
    s_string("42")
    s_delim(".")
    s_string("42")
    s_static(" ")
    s_string("10")
    s_static("\r\n")
    
    #s_static("Accept: audio/*;q=0.2,audio/basic\r\n")
    s_static("Accept: ")
    s_string("audio")
    s_delim("/")
    s_string("*")
    s_delim(";")
    # should only be one of these
    if s_block_start("accept_q_value"):
        s_lego("q_value")
    s_block_end()
    s_repeat("accept_q_value", min_reps=2, max_reps=10, step=1)    
    s_delim(",")
    s_string("audio/basic")
    s_static(";")
    s_string("meh")
    s_delim("=")
    s_string("bleh")

    s_static("\r\n")
    
    #s_static("MIME-Version: 1.0\r\n")
    s_static("MIME-Version: ")
    s_string("1")
    s_delim(".")
    s_string("0")
    s_static("\r\n")

    #s_static("Authentication-Info: nextnonce=\"somemd5value\",qop=\"auth\",rspauth=\"somehexvalue\",nc=deadcafe,cnonce=\"somecnonce\"")
    s_static("Authentication-Info: ")
    s_string("nextnonce")
    s_delim("=")
    s_delim("\"")
    s_string("f84f1cec41e6cbe5aea9c8e88d359")
    s_delim("\"")
    s_delim(",")
    s_static("qop=")
    s_delim("\"")
    s_string("auth")
    s_delim("\"")
    s_static(",rspauth=")
    s_delim("\"")
    s_static("deadcafe")
    s_delim("\"")
    s_static(",nc=")
    s_string("deadcafe")
    s_static(",cnonce=")
    s_delim("\"")
    s_string("f84f1cec41e6cbe5aea9c8e88d359")
    s_delim("\"")
    s_static("\r\n")
    
    #s_static("Min-Expires: 60")
    s_static("Min-Expires: ")
    s_string("60")
    s_static("\r\n")

    #s_static("Retry-After: 60(some comment text);duration=3600
    s_static("Retry-After: ")
    s_string("60")
    s_delim("(")
    s_string("comment")
    s_delim(")")
    s_delim(";")
    s_string("duration")
    s_static("=")
    s_string("3600")
    s_static("\r\n")

    #s_static("Error-Info: <sip:not-in-service@atlanta.com>,<sip:not-in-service2@atlanta.com>")
    s_static("Error-Info: ")
    s_delim("<")
    s_string("sip:not-in-service@atlanta.com")
    s_delim(">")
    s_static(",<sip:not-in-service2@atlanta.com>")
    s_static("\r\n")
    
    #s_static("Unsupported: somestring, someotherstring")
    s_static("Unsupported: ")
    s_string("somestring")
    s_static(", bleh")
    s_static("\r\n")

    #s_static("Warning: 666 ServerName \"The Sky Is Falling\", 333 ServerName \"Says Chicken Little\"")
    s_static("Warning: ")
    s_dword(333, fuzzable=True, format="ascii", signed=True)
    s_delim(" ")
    s_string("ServerName")
    s_static(" ")
    s_delim("\"")
    s_string("The Sky Is Falling")
    s_delim("\"")
    s_static(",")
    s_string("333 ServerName \"Says Chicken Litle\"")
    s_static("\r\n")

    #s_static("Proxy-Authenticate: Digest realm=\"atlanta.com\",domain=\"sip:ss1.carrier.com\", \
    #qop=\"auth\",nonce="f84f1cec41e6cbe5aea9c8e88d359",opaque=\"5ccc069c403ebaf9f0171e9517f40e41\", stale=FALSE, algorithm=MD5)
    # this is a repeat of earlier Authenticate. probably no point in fuzzing
    s_static("Proxy-Authenticate: ")
    s_lego("static_challenge", options={'fuzzable' : False})
    s_static("\r\n")

    #s_static("Proxy-Authorization: Digest username=\"Alice\", realm=\"atlanta.com\", nonce=\"c60f3082ee1212b402a21831ae\",\
    #response=\"245f23415f11432b3434341c022\"")
    # this is a repeat of earlier Authorization. probably no point in fuzzing
    s_static("Proxy-Authorization: ")
    s_lego("static_credentials", options={'fuzzable' : False})
    s_static("\r\n")

    #s_static("Server: SomeServer v2")
    s_static("Server: ")
    s_string("Someserver")
    s_delim(" ")
    s_string("v2")
    s_static("\r\n")

    #s_static("WWW-Authenticate: Digest realm=\"atlanta.com\",domain=\"sip:ss1.carrier.com\", \
    #qop=\"auth\",nonce="f84f1cec41e6cbe5aea9c8e88d359",opaque=\"5ccc069c403ebaf9f0171e9517f40e41\", stale=FALSE, algorithm=MD5)
    s_static("WWW-Authenticate: ")
    s_lego("static_challenge")
    s_static("\r\n")
    
    s_static("\r\n")
s_block_end()

if not s_block_start("invite_sdp"):
    s_static("v=0\r\n")
    s_static("o=- 1190505265 1190505265 IN IP4 LOCAL_IP\r\n")
    s_static("s=Opal SIP Session\r\n")
    s_static("c=IN IP4 LOCAL_IP\r\n")
    s_static("t=0 0\r\n")
    s_static("m=audio 5028 RTP/AVP 101 96 3 107 110 0 8\r\n")
    s_static("a=rtpmap:101 telephone-event/8000\r\n")
    s_static("a=fmtp:101 0-15\r\n")
    s_static("a=rtpmap:96 SPEEX/16000\r\n")
    s_static("a=rtpmap:3 GSM/8000\r\n")
    s_static("a=rtpmap:107 MS-GSM/8000\r\n")
    s_static("a=rtpmap:110 SPEEX/8000\r\n")
    s_static("a=rtpmap:0 PCMU/8000\r\n")
    s_static("a=rtpmap:8 PCMA/8000\r\n")
    s_static("m=video 5030 RTP/AVP 31\r\n")
    s_static("a=rtpmap:31 H261/90000\r\n")
s_block_end()

################################################################################

s_initialize("INVITE_COMMON")

if s_block_start("invite_request_line"):
    s_static("INVITE sip:TARGET_USER@HOST SIP/2.0\r\n")
s_block_end()

if s_block_start("invite_header"):
    #s_static("CSeq: 1 INVITE\r\n")
    ##    CSeq  =  "CSeq" HCOLON 1*DIGIT LWS Method
    s_static("CSeq: ")
    s_dword(1, fuzzable=True, format="ascii")
    s_delim(" ")
    s_string("INVITE")
    s_static("\r\n")
    
    #s_static("Via: SIP/2.0/UDP 192.168.3.104:5068;branch=z9hG4bKsomebranchvalue;rport\r\n")
    ##    Via               =  ( "Via" / "v" ) HCOLON via-parm *(COMMA via-parm)
    ##    via-parm          =  sent-protocol LWS sent-by *( SEMI via-params )
    ##    via-params        =  via-ttl / via-maddr
    ##                         / via-received / via-branch
    ##                         / via-extension
    ##    via-ttl           =  "ttl" EQUAL ttl
    ##    via-maddr         =  "maddr" EQUAL host
    ##    via-received      =  "received" EQUAL (IPv4address / IPv6address)
    ##    via-branch        =  "branch" EQUAL token
    ##    via-extension     =  generic-param
    ##    sent-protocol     =  protocol-name SLASH protocol-version
    ##                     SLASH transport
    ##    protocol-name     =  "SIP" / token
    ##    protocol-version  =  token
    ##    transport         =  "UDP" / "TCP" / "TLS" / "SCTP"
    ##                     / other-transport
    ##    sent-by           =  host [ COLON port ]
    ##    ttl               =  1*3DIGIT ; 0 to 255
    s_static("Via: ")
    s_string("SIP")
    s_delim("/")
    s_string("2.0")
    s_delim("/")
    s_string("UDP")
    s_static(" ")
    s_lego("ip_address_ascii", "192.168.99.99")
    s_delim(":")
    s_string("PORT")
    s_delim(";")
    s_string("branch")
    s_delim("=")
    s_string("z9hG4bK")
    s_string("somebranchvalue")
    s_static(";")
    s_static("ttl")
    s_static("=")
    s_string("70")
    s_static(";")
    s_static("maddr=")
    s_lego("ipv6_address_ascii", "aaaa:aaaa:aaaa:aaaa:aaaa:aaaa:aaaa:aaaa")
    s_static(";")
    s_static("received=")
    s_lego("ipv6_address_ascii", "aaaa:aaaa:aaaa:aaaa:aaaa:aaaa:aaaa:aaaa")
    s_static(";")
    s_string("rport")
    s_static("\r\n")

    #s_static("From: \"Negativa\" <sip:nnp@192.168.3.104>;tag=somefromtagvalue\r\n")
    ##    From        =  ( "From" / "f" ) HCOLON from-spec
    ##    from-spec   =  ( name-addr / addr-spec )
    ##                   *( SEMI from-param )
    ##    from-param  =  tag-param / generic-param
    ##    tag-param   =  "tag" EQUAL token
    ##    name-addr      =  [ display-name ] LAQUOT addr-spec RAQUOT
    ##    addr-spec      =  SIP-URI / SIPS-URI / absoluteURI        
    s_static("From: ")
    s_delim("\"")
    s_string("VoIPER")
    s_delim("\"")
    s_delim(" ")
    s_delim("<")
    s_lego("from_sip_uri", options={'fuzzable' : True})
    s_delim(">")
    s_delim(";")
    s_string("tag")
    s_string("=")
    s_string("somefromtagval")
    s_static("\r\n")

    #s_static("Call-ID: somecallidvalue@ubuntu\r\n")
    ##    Call-ID  =  ( "Call-ID" / "i" ) HCOLON callid
    ##    callid   =  word [ "@" word ]
    s_static("Call-ID: ")
    s_string("somecallidvalue")
    s_delim("@")
    s_string("TheKlatchianHead")
    s_static("\r\n")

    #s_static("To: <sip:nnp@192.168.1.1>\r\n")
    ##    To        =  ( "To" / "t" ) HCOLON ( name-addr
    ##                 / addr-spec ) *( SEMI to-param )
    ##    to-param  =  tag-param / generic-param
    s_static("To: ")
    s_delim("\"")
    s_string("TARGET_USER")
    s_delim("\"")
    s_delim(" ")
    s_delim("<")
    s_lego("to_sip_uri", options={'fuzzable' : True})
    s_delim(">")
    s_static("\r\n")
    
    #s_static("Contact: <sip:nnp@192.168.3.104:5068;transport=udp>\r\n")
    ##    Contact        =  ("Contact" / "m" ) HCOLON
    ##                      ( STAR / (contact-param *(COMMA contact-param)))
    ##    contact-param  =  (name-addr / addr-spec) *(SEMI contact-params)
    ##    name-addr      =  [ display-name ] LAQUOT addr-spec RAQUOT
    ##    addr-spec      =  SIP-URI / SIPS-URI / absoluteURI
    ##    display-name   =  *(token LWS)/ quoted-string
    ##
    ##    contact-params     =  c-p-q / c-p-expires
    ##                          / contact-extension
    ##    c-p-q              =  "q" EQUAL qvalue
    ##    c-p-expires        =  "expires" EQUAL delta-seconds
    ##    contact-extension  =  generic-param
    s_static("Contact: ")
    s_delim("<")
    s_lego("from_sip_uri", options={'fuzzable' : True})
    s_delim(">")
    s_lego("q_value")   
    s_static(";")
    s_static("expires")
    s_static("=")
    s_string("1337")
    s_static(";")
    s_static("sometoken")
    s_delim("=")
    s_string("somevalue")
    s_static("\r\n")

    #s_static("Max-Forwards: 70\r\n")
    ##    Max-Forwards  =  "Max-Forwards" HCOLON 1*DIGIT
    s_static("Max-Forwards: ")
    s_string("70")
    s_static("\r\n")

    #s_static("Content-Type: application/sdp\r\n")
    ##    Content-Type     =  ( "Content-Type" / "c" ) HCOLON media-type
    ##    media-type       =  m-type SLASH m-subtype *(SEMI m-parameter)
    ##    m-type           =  discrete-type / composite-type
    ##    discrete-type    =  "text" / "image" / "audio" / "video"
    ##                        / "application" / extension-token
    ##    composite-type   =  "message" / "multipart" / extension-token
    ##    extension-token  =  ietf-token / x-token
    ##    ietf-token       =  token
    ##    x-token          =  "x-" token
    ##    m-subtype        =  extension-token / iana-token
    ##    iana-token       =  token
    ##    m-parameter      =  m-attribute EQUAL m-value
    ##    m-attribute      =  token
    ##    m-value          =  token / quoted-string
    s_static("Content-Type: ")
    s_group("content_type_discrete", values=['application', 'image', 'audio', 'video', 'text'])
    if s_block_start("content_type_media", group="content_type_discrete"):
        s_delim("/")
        s_string("sdp")
        s_delim(";")
        s_static("mattr")
        s_static("=")
        s_string("mvalue")
    s_block_end()
    s_static("\r\n")

    ##    Content-Length  =  ( "Content-Length" / "l" ) HCOLON 1*DIGIT
    s_static("Content-Length: ")
    s_sizer("invite_sdp", format="ascii", fuzzable=True, signed=True)
    
    s_static("\r\n\r\n")
s_block_end()

if s_block_start("invite_sdp"):
    s_static("v=0\r\n")
    s_static("o=- 1190505265 1190505265 IN IP4 LOCAL_IP\r\n")
    s_static("s=Opal SIP Session\r\n")
    s_static("c=IN IP4 LOCAL_IP\r\n")
    s_static("t=0 0\r\n")
    s_static("m=audio 5028 RTP/AVP 101 96 3 107 110 0 8\r\n")
    s_static("a=rtpmap:101 telephone-event/8000\r\n")
    s_static("a=fmtp:101 0-15\r\n")
    s_static("a=rtpmap:96 SPEEX/16000\r\n")
    s_static("a=rtpmap:3 GSM/8000\r\n")
    s_static("a=rtpmap:107 MS-GSM/8000\r\n")
    s_static("a=rtpmap:110 SPEEX/8000\r\n")
    s_static("a=rtpmap:0 PCMU/8000\r\n")
    s_static("a=rtpmap:8 PCMA/8000\r\n")
    s_static("m=video 5030 RTP/AVP 31\r\n")
    s_static("a=rtpmap:31 H261/90000\r\n")
s_block_end()

################################################################################

s_initialize("OPTIONS")

################################################################################

# This is a fairly basic SDP fuzz set based off a captured packet instead of the RFC
# Todo: Make RFC compliant

s_initialize("SDP")

if s_block_start("invite_header"):
    s_static("INVITE sip:TARGET_USER@HOST SIP/2.0\r\n")
    s_static("CSeq: 1 INVITE\r\n")
    s_static("Via: SIP/2.0/UDP LOCAL_IP:PORT;branch=z9hG4bKsomebranchvalue;rport\r\n")
    s_static("From: \"VoIPER\" <sip:USER@LOCAL_IP>;tag=somefromtagvalue\r\n")
    s_static("Call-ID: somecallidvalue@ubuntu\r\n")
    s_static("To: <sip:TARGET_USER@HOST>\r\n")
    s_static("Contact: <sip:USER@LOCAL_IP:PORT;transport=udp>\r\n")
    s_static("Max-Forwards: 70\r\n")
    s_static("Content-Type: application/sdp\r\n")
    s_static("Content-Length: ")
    s_sizer("invite_sdp", format="ascii", fuzzable=False, signed=True)
    s_static("\r\n\r\n")
s_block_end()

if s_block_start("invite_sdp"):
    #s_static("v=0\r\n")
    s_static("v=")
    s_dword(0, format='ascii', signed=True)
    s_static('\r\n')

    #s_static("o=- 1190505265 1190505265 IN IP4 192.168.3.104\r\n")
    if s_block_start("o"):
        s_static("o=")
        s_string("somegimp")
        s_delim(" ")
        s_dword(1190505265, format="ascii", signed=True)
        s_static(" ")
        s_dword(1190505265, format="ascii", signed=True)
        s_static(" ")
        s_string("IN")
        s_static(" ")
        s_string("IP4")
        s_static(" ")
        s_lego("ip_address_ascii", "192.168.99.99")
        s_static("\r\n")
    s_block_end()
    s_repeat("o", min_reps=2, max_reps=1000, step=10)
    
    #s_static("s=Opal SIP Session\r\n")
    # take this opportunity to fuzz EOL chars and attribite=delim
    s_string("s")
    s_delim("=")
    s_string("Opal SIP Session")
    s_delim("\r\n")

    s_static("i=")
    s_string("some information string")
    s_static("\r\n")

    s_static("u=")
    s_string("http://unprotectedhex.com/someuri.htm")
    s_static("\r\n")
    
    s_static("e=")
    s_string("email@address.com")
    s_static(" ")
    s_delim("(")
    s_string("someones name")
    s_delim(")")
    s_static("\r\n")

     #s_static("c=IN IP4 192.168.3.102\r\n")
    # repeated c lines cause an overflow in Asterisk at one point
    if s_block_start("c"):
        s_static("c=")
        s_string("IN")
        s_static(" ")
        s_string("IP4")
        s_static(" ")
        s_lego("ip_address_ascii", "192.168.99.99")
        s_static("\r\n")
    s_block_end()
    s_repeat("c", min_reps=2, max_reps=1000, step=10)

    #s_static("t=0 0\r\n")
    s_static("t=")
    s_dword(0, format="ascii", signed=True)
    s_static(" ")
    s_dword(1, format="ascii", signed=True)
    s_static("\r\n")

    s_static("p=")
    s_dword(232, format="ascii", fuzzable=True, signed=True)
    s_delim("-")
    s_string("343434")
    s_static("\r\n")
    
    s_static("b=")
    s_string("CT")
    s_static(":")
    s_dword(8, format=True, signed=True)
    s_static("\r\n")

    s_static("r=")
    s_dword(604800, format="ascii", signed=True)
    s_static(" ")
    s_dword(3600, format="ascii", signed=True, fuzzable=False)
    s_static(" ")
    s_dword(0, format="ascii", signed=True, fuzzable=False)
    s_static(" ")
    s_dword(9000, format="ascii", signed=True, fuzzable=False)
    s_static("\r\n")

    s_static("z=")
    s_dword(2882844526, format="ascii", signed=True)
    s_static(" ")
    s_string("-1h")
    s_static(" ")
    s_dword(2898848070, format="ascii", fuzzable=False)
    s_static(" ")
    s_dword(0, format="ascii", fuzzable=False)
    s_static("\r\n")

    s_static("k=")
    s_group("enc_types", values=['clear', 'base64', 'uri'])
    s_delim(":")
    
    if s_block_start("b64_encoded_key", dep="enc_types", dep_value="base64",\
        encoder=base64_encode):
        s_string("somefancypantsencryptionkey")
    s_block_end()
    
    if s_block_start("clear_key", dep="enc_types", dep_values=["clear", 'uri']):
        s_string("somefancypantsencryptionkey")
    s_block_end()
    
    s_static("\r\n")

    # end of session info, start of media config
    if s_block_start("audio_config"):
        #s_static("m=audio 5028 RTP/AVP 101 96 98 3 107 110 0 8\r\n")
        s_static("m=")
        s_string("audio")
        s_static(" ")
        s_dword(5028, format="ascii", signed=True)
        s_static(" ")
        s_string("RTP/AVP")
        s_delim(" ")
        s_dword(101, format="ascii", signed=True)
        s_static(" 96")
        s_delim(" ")
        s_string("107 110 0 8")
        s_static("\r\n")
    
        #s_static("a=rtpmap:101 telephone-event/8000\r\n")
        s_static("a=")
        s_string("rtpmap")
        s_delim(":")
        s_string("101")
        s_delim(" ")
        s_string("telephone-event")
        s_static("/")
        s_string("8000")
        s_static("\r\n")
    s_block_end()
    s_repeat("audio_config", min_reps=2, max_reps=1000, step=10)

    s_static("i=")
    s_string("some information string")
    s_static("\r\n")    
    
    if s_block_start("a"):
        s_static("a=rtpmap:98 L16/16000/2\r\n")
    s_block_end()
    s_repeat("a", min_reps=10, max_reps=1000, step=10)
    
    #s_static("a=rtpmap:96 SPEEX/16000\r\n")
    s_static("a=rtpmap:")
    s_dword(96, format="ascii", signed=True)
    s_static(" ")
    s_string("SPEEX")
    s_delim("/")
    s_dword(16000, format="ascii", signed=True)
    s_static("\r\n")

    s_static("a=rtpmap:3 GSM/8000\r\n")
    s_static("a=rtpmap:107 MS-GSM/8000\r\n")
    s_static("a=rtpmap:110 SPEEX/8000\r\n")
    s_static("a=rtpmap:0 PCMU/8000\r\n")
    s_static("a=rtpmap:8 PCMA/8000\r\n")
      
    s_static("m=video")
    s_static(" ")
    s_dword(5030, format="ascii", signed=True)
    s_delim("/")
    s_dword(2, signed=True, format="ascii")
    s_static(" ")
    s_string("RTP")    
    s_delim("/")
    s_static("AVP")
    s_static(" ")
    s_dword(31, format="ascii", signed=True)
    s_static("\r\n")
    
    #s_static("a=rtpmap:31 H261/90000\r\n")
    s_static("a=rtpmap:")
    s_dword(31, format="ascii", signed=True)
    s_static(" ")
    s_string("H261")
    s_delim("/")
    s_dword(90000, format="ascii", signed=True)
    s_static("\r\n")
    '''  
    # t38 stuff. There was an asterisk advisory about the processing
    # of this some time ago
    s_static("m=image ")
    s_dword(5004, format="ascii", signed=True)
    s_static(" UDPTL t38")
    s_static("\r\n")
    
    s_static("a=")
    s_string("T38FaxVersion")
    s_delim(":")
    s_dword(0, signed=True, format="ascii")
    s_static("\r\n")
    
    s_static("a=T38MaxBitRate:")
    s_string("14400")
    s_static("\r\n")

    s_static("a=T38FaxMaxBuffer:")
    s_dword(1024, signed=True, format="ascii")
    s_static("\r\n")
    
    s_static("a=T38FaxMaxDatagram:")
    s_dword(238, signed=True, format="ascii")
    s_static("\r\n")    
    s_static("a=T38FaxRateManagement:")
    s_string("transferredTFC")
    s_static("\r\n")
    
    s_static("a=T38FaxUdpEC:")
    s_string("t38UDPRedundancy")

    s_static("a=T38FaxFillBitRemoval:")
    s_dword(0, signed=True, format="ascii")
    s_static("\r\n")
    
    s_static("a=T38FaxTranscodingMMR:")
    s_string("0")
    s_static("\r\n")

    s_static("a=T38FaxTranscodingJBIG:")
    s_dword(0, signed=True, format="ascii")
    s_static("\r\n")
    '''
s_block_end()

################################################################################

s_initialize("ACK")

if s_block_start("ack_request_line"):
    s_static("ACK sip:TARGET_USER@HOST SIP/2.0\r\n")
s_block_end()

if s_block_start("invite_header"):
    s_static("CSeq: ")
    s_string("1")
    s_delim(" ")
    s_string("ACK")
    s_static("\r\n")
    
    s_string("Via: ")
    s_string("SIP")
    s_delim("/")
    s_string("2.0")
    s_delim("/")
    s_string("UDP")
    s_static(" ")
    s_lego("ip_address_ascii", "192.168.99.99")
    s_delim(":")
    s_string("5068")
    s_delim(";")
    s_string("branch")
    s_delim("=")
    s_string("z9hG4bK")
    s_string("somebranchvalue")
    s_static(";")
    s_static("ttl")
    s_static("=")
    s_string("70")
    s_static(";")
    s_static("maddr=")
    s_lego("ipv6_address_ascii", "aaaa:aaaa:aaaa:aaaa:aaaa:aaaa:aaaa:aaaa")
    s_static(";")
    s_static("received=")
    s_lego("ipv6_address_ascii", "aaaa:aaaa:aaaa:aaaa:aaaa:aaaa:aaaa:aaaa")
    s_static(";")
    s_string("rport")
    s_static("\r\n")
     
    s_static("From: ")
    s_delim("\"")
    s_string("Negativa")
    s_delim("\"")
    s_delim(" ")
    s_delim("<")
    s_lego("from_sip_uri_basic", options={'fuzzable' : True})
    s_delim(">")
    s_delim(";")
    s_string("tag")
    s_string("=")
    s_string("somefromtagval")
    s_static("\r\n")

    s_static("Call-ID: ")
    s_string("somecallidvalue")
    s_delim("@")
    s_string("TheKlatchianHead")
    s_static("\r\n")

    s_static("To: ")
    s_delim("\"")
    s_string("Negativa")
    s_delim("\"")
    s_delim(" ")
    s_delim("<")
    s_lego("to_sip_uri_basic", options={'fuzzable' : True})
    s_delim(">")
    s_static("\r\n")

    s_static("Max-Forwards: ")
    s_string("70")

    
    s_static("\r\n\r\n")
s_block_end()

        
################################################################################
s_initialize("CANCEL")

if s_block_start("cancel_request_line"):
    s_static("CANCEL sip:TARGET_USER@HOST SIP/2.0\r\n")
s_block_end()

if s_block_start("invite_header"):
    s_static("CSeq: ")
    s_string("1")
    s_delim(" ")
    s_string("CANCEL")
    s_static("\r\n")
    
    s_string("Via: ")
    s_string("SIP")
    s_delim("/")
    s_string("2.0")
    s_delim("/")
    s_string("UDP")
    s_static(" ")
    s_lego("ip_address_ascii", "192.168.99.99")
    s_delim(":")
    s_string("5068")
    s_delim(";")
    s_string("branch")
    s_delim("=")
    s_string("z9hG4bK")
    s_string("somebranchvalue")
    s_static(";")
    s_static("ttl")
    s_static("=")
    s_string("70")
    s_static(";")
    s_static("maddr=")
    s_lego("ipv6_address_ascii", "aaaa:aaaa:aaaa:aaaa:aaaa:aaaa:aaaa:aaaa")
    s_static(";")
    s_static("received=")
    s_lego("ipv6_address_ascii", "aaaa:aaaa:aaaa:aaaa:aaaa:aaaa:aaaa:aaaa")
    s_static(";")
    s_string("rport")
    s_static("\r\n")
     
    s_static("From: ")
    s_delim("\"")
    s_string("Negativa")
    s_delim("\"")
    s_delim(" ")
    s_delim("<")
    s_lego("from_sip_uri_basic", options={'fuzzable' : True})
    s_delim(">")
    s_delim(";")
    s_string("tag")
    s_string("=")
    s_string("somefromtagval")
    s_static("\r\n")

    s_static("Call-ID: ")
    s_string("somecallidvalue")
    s_delim("@")
    s_string("TheKlatchianHead")
    s_static("\r\n")

    s_static("To: ")
    s_delim("\"")
    s_string("Negativa")
    s_delim("\"")
    s_delim(" ")
    s_delim("<")
    s_lego("to_sip_uri_basic", options={'fuzzable' : True})
    s_delim(">")
    s_static("\r\n")

    s_static("Max-Forwards: ")
    s_string("70")

    s_static("\r\n\r\n")
s_block_end()

################################################################################

s_initialize("REGISTER")

if s_block_start("register_request_line"):
    s_static("REGISTER sip:USER@HOST SIP/2.0\r\n")
s_block_end()

if s_block_start("register_header"):
    #s_static("CSeq: 1 INVITE\r\n")
    ##    CSeq  =  "CSeq" HCOLON 1*DIGIT LWS Method
    s_static("CSeq: ")
    s_dword(2, fuzzable=True, format="ascii")
    s_delim(" ")
    s_string("REGISTER")
    s_static("\r\n")
    
    #s_static("Via: SIP/2.0/UDP 192.168.3.104:5068;branch=z9hG4bKsomebranchvalue;rport\r\n")
    ##    Via               =  ( "Via" / "v" ) HCOLON via-parm *(COMMA via-parm)
    ##    via-parm          =  sent-protocol LWS sent-by *( SEMI via-params )
    ##    via-params        =  via-ttl / via-maddr
    ##                         / via-received / via-branch
    ##                         / via-extension
    ##    via-ttl           =  "ttl" EQUAL ttl
    ##    via-maddr         =  "maddr" EQUAL host
    ##    via-received      =  "received" EQUAL (IPv4address / IPv6address)
    ##    via-branch        =  "branch" EQUAL token
    ##    via-extension     =  generic-param
    ##    sent-protocol     =  protocol-name SLASH protocol-version
    ##                     SLASH transport
    ##    protocol-name     =  "SIP" / token
    ##    protocol-version  =  token
    ##    transport         =  "UDP" / "TCP" / "TLS" / "SCTP"
    ##                     / other-transport
    ##    sent-by           =  host [ COLON port ]
    ##    ttl               =  1*3DIGIT ; 0 to 255
    s_static("Via: ")
    s_string("SIP")
    s_delim("/")
    s_string("2.0")
    s_delim("/")
    s_string("UDP")
    s_static(" ")
    s_lego("ip_address_ascii", "192.168.99.99")
    s_delim(":")
    s_string("PORT")
    s_delim(";")
    s_string("branch")
    s_delim("=")
    s_string("z9hG4bK")
    s_string("somebranchvalue")
    s_static(";")
    s_static("ttl")
    s_static("=")
    s_string("70")
    s_static(";")
    s_string("rport")
    s_static("\r\n")

    #s_static("From: \"Negativa\" <sip:nnp@192.168.3.104>;tag=somefromtagvalue\r\n")
    ##    From        =  ( "From" / "f" ) HCOLON from-spec
    ##    from-spec   =  ( name-addr / addr-spec )
    ##                   *( SEMI from-param )
    ##    from-param  =  tag-param / generic-param
    ##    tag-param   =  "tag" EQUAL token
    ##    name-addr      =  [ display-name ] LAQUOT addr-spec RAQUOT
    ##    addr-spec      =  SIP-URI / SIPS-URI / absoluteURI        
    s_static("From: ")
    s_delim("\"")
    s_string("Negativa")
    s_delim("\"")
    s_delim(" ")
    s_delim("<")
    s_lego("from_sip_uri", options={'fuzzable' : True})
    s_delim(">")
    s_delim(";")
    s_string("tag")
    s_string("=")
    s_string("somefromtagval")
    s_static("\r\n")

    #s_static("Call-ID: somecallidvalue@ubuntu\r\n")
    ##    Call-ID  =  ( "Call-ID" / "i" ) HCOLON callid
    ##    callid   =  word [ "@" word ]
    s_static("Call-ID: ")
    s_string("somecallidvalue")
    s_delim("@")
    s_string("TheKlatchianHead")
    s_static("\r\n")

    #s_static("To: <sip:nnp@192.168.1.1>\r\n")
    ##    To        =  ( "To" / "t" ) HCOLON ( name-addr
    ##                 / addr-spec ) *( SEMI to-param )
    ##    to-param  =  tag-param / generic-param
    s_static("To: ")
    s_delim("\"")
    s_string("Negativa")
    s_delim("\"")
    s_delim(" ")
    s_delim("<")
    s_lego("to_sip_uri", options={'fuzzable' : True})
    s_delim(">")
    s_static("\r\n")

    #s_static("Max-Forwards: 70\r\n")
    ##    Max-Forwards  =  "Max-Forwards" HCOLON 1*DIGIT
    s_static("Max-Forwards: ")
    s_string("70")
    s_static("\r\n")

    ##    Content-Length  =  ( "Content-Length" / "l" ) HCOLON 1*DIGIT
    s_static("Content-Length: ")
    s_dword(0, fuzzable=True, format="ascii")
    s_static("\r\n")

    #s_static("Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,NOTIFY,REFER,MESSAGE\r\n")
    s_static("Allow: ")
    s_string("INVITE")
    s_static(",")
    s_static("ACK,OPTIONS,BYE,CANCEL,NOTIFY,REFER,MESSAGE")
    s_static("\r\n")


    #s_static("Expires: 3600\r\n")
    s_static("Expires: ")
    s_string("3600")
    s_static("\r\n")
    
    #s_static("User-Agent: Ekiga/2.0.3\r\n")
##    User-Agent  =  "User-Agent" HCOLON server-val *(LWS server-val)
##    server-val       =  product / comment
##    product          =  token [SLASH product-version]
##    product-version  =  token
    s_static("User-Agent: ")
    s_string("VoIPER")
    s_delim("/")
    s_string("0.02")
    s_delim(" ")
    s_string("Clack/0.02")
    s_static("\r\n")    
    
    #s_static("Authorization: Digest username=\"nnp\", realm=\"bleh.com\", nonce=\"value\", response=\"value\"\r\n")
    s_static("Authorization: ")
    s_lego("static_credentials")
    s_static("\r\n")

    s_static("Contact: ")
    s_delim("<")
    s_lego("from_sip_uri", options={'fuzzable' : True})
    s_delim(">")

    s_static("\r\n")    
  
    s_static("\r\n")
s_block_end()

################################################################################

s_initialize("SUBSCRIBE")

if s_block_start("subscribe_request_line"):
    s_static("SUBSCRIBE sip:USER@HOST SIP/2.0\r\n")
s_block_end()

if s_block_start("subscribe_header"):
    s_static("CSeq: ")
    s_dword(3, fuzzable=True, format="ascii")
    s_static(" ")
    s_string("SUBSCRIBE")
    s_string("\r\n")

    # Via: SIP/2.0/UDP 192.168.3.104:5062;branch=z9hG4bK9a485f36-ebfb-1810-9783-0007e9ca58f2;rport    
    s_static("Via: ")
    s_string("SIP")
    s_delim("/")
    s_string("2.0")
    s_delim("/")
    s_string("UDP")
    s_static(" ")
    s_lego("ip_address_ascii", "192.168.99.99")
    s_delim(":")
    s_string("PORT")
    s_delim(";")
    s_string("branch")
    s_delim("=")
    s_string("z9hG4bK")
    s_string("somebranchvalue")
    s_static(";")
    s_static("ttl")
    s_static("=")
    s_dword(70, fuzzable=True, format="ascii")
    s_static(";")
    s_string("rport")
    s_static("\r\n")

    # User-Agent: Ekiga/2.0.9
    s_static("User-Agent: ")
    s_string("VoIPER")
    s_delim("/")
    s_string("0.02")
    s_delim(" ")
    s_string("Clack/0.02")
    s_static("\r\n")
    
    # From: <sip:1001@192.168.3.101>;tag=9a485f36-ebfb-1810-9782-0007e9ca58f2
    s_static("From: ")
    s_delim("\"")
    s_string("Negativa")
    s_delim("\"")
    s_delim(" ")
    s_delim("<")
    s_lego("from_sip_uri_basic", options={'fuzzable' : True})
    s_delim(">")
    s_delim(";")
    s_string("tag")
    s_string("=")
    s_string("somefromtagval")
    s_static("\r\n")
    
    # Call-ID: 5cff5e36-ebfb-1810-9772-0007e9ca58f2@N0N4M3
    s_static("Call-ID: ")
    s_string("somecallidvalue")
    s_delim("@")
    s_string("TheKlatchianHead")
    s_static("\r\n")
    
    # To: <sip:1001@192.168.3.101>
    # "To" is addressed to self in this case
    s_static("To: ")
    s_delim("\"")
    s_string("Negativa")
    s_delim("\"")
    s_delim(" ")
    s_delim("<")
    s_string("sip")
    s_delim(":")
    s_string("USER")
    s_delim("@")
    s_lego("ip_address_ascii", "192.168.96.69")
    s_delim(">")
    s_static("\r\n")
    
    # Contact: <sip:1001@192.168.3.104:5062;transport=udp>
    s_static("Contact: ")
    s_delim("<")
    s_lego("from_sip_uri_basic", options={'fuzzable' : True})
    s_delim(">")
    s_static("\r\n")
    
    # Accept: application/simple-message-summary
    s_static("Accept: ")
    s_string("application")
    s_delim("/")
    s_string("simple-message-summary")
    s_static("\r\n")    
    
    # Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,NOTIFY,REFER,MESSAGE
    s_static("Allow: ")
    s_string("INVITE")
    s_static(",")
    s_static("ACK,OPTIONS,BYE,CANCEL,NOTIFY,REFER,MESSAGE")
    s_static("\r\n")
    
    # Expires: 3600
    s_static("Expires: ")
    s_dword(3600, fuzzable=True, format="ascii")
    s_static("\r\n")

    # Event: message-summary
    s_static("Event: ")
    s_string("message-summary")
    s_static("\r\n")

    s_static("Content-Length: ")
    s_dword(0, fuzzable=True, format="ascii")
    s_static("\r\n")
    
    s_static("Max-Forwards: ")
    s_dword(70, fuzzable=True, format="ascii")
    s_static("\r\n")    
    s_static("\r\n")
    
s_block_end()

################################################################################

s_initialize("NOTIFY")

if s_block_start("notify_request_line"):
    s_static("NOTIFY sip:USER@HOST SIP/2.0\r\n")
s_block_end()

if s_block_start("notify_header"):
    s_static("CSeq: ")
    s_dword(3, fuzzable=True, format="ascii")
    s_string("SUBSCRIBE")
    s_string("\r\n")

    # Via: SIP/2.0/UDP 192.168.3.104:5062;branch=z9hG4bK9a485f36-ebfb-1810-9783-0007e9ca58f2;rport    
    s_static("Via: ")
    s_string("SIP")
    s_delim("/")
    s_string("2.0")
    s_delim("/")
    s_string("UDP")
    s_static(" ")
    s_lego("ip_address_ascii", "192.168.99.99")
    s_delim(":")
    s_string("PORT")
    s_delim(";")
    s_string("branch")
    s_delim("=")
    s_string("z9hG4bK")
    s_string("somebranchvalue")
    s_static(";")
    s_static("ttl")
    s_static("=")
    s_dword(70, fuzzable=True, format="ascii")
    s_static(";")
    s_string("rport")
    s_static("\r\n")

    # User-Agent: Ekiga/2.0.9
    s_static("User-Agent: ")
    s_string("VoIPER")
    s_delim("/")
    s_string("0.02")
    s_delim(" ")
    s_string("Clack/0.02")
    s_static("\r\n")
    
    # From: <sip:1001@192.168.3.101>;tag=9a485f36-ebfb-1810-9782-0007e9ca58f2
    s_static("From: ")
    s_delim("\"")
    s_string("Negativa")
    s_delim("\"")
    s_delim(" ")
    s_delim("<")
    s_lego("from_sip_uri_basic", options={'fuzzable' : True})
    s_delim(">")
    s_delim(";")
    s_string("tag")
    s_string("=")
    s_string("somefromtagval")
    s_static("\r\n")
    
    # Call-ID: 5cff5e36-ebfb-1810-9772-0007e9ca58f2@N0N4M3
    s_static("Call-ID: ")
    s_string("somecallidvalue")
    s_delim("@")
    s_string("TheKlatchianHead")
    s_static("\r\n")
    
    # To: <sip:1001@192.168.3.101>
    s_static("To: ")
    s_delim("\"")
    s_string("Negativa")
    s_delim("\"")
    s_delim(" ")
    s_delim("<")
    s_lego("to_sip_uri_basic", options={'fuzzable' : True})
    s_delim(">")
    s_static("\r\n")
    
    # Contact: <sip:1001@192.168.3.104:5062;transport=udp>
    s_static("Contact: ")
    s_delim("<")
    s_lego("from_sip_uri_basic", options={'fuzzable' : True})
    s_delim(">")
    s_static("\r\n")
    
    # Accept: application/simple-message-summary
    s_static("Accept: ")
    s_string("application")
    s_delim("/")
    s_string("simple-message-summary")
    
    # Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,NOTIFY,REFER,MESSAGE
    s_static("Allow: ")
    s_string("INVITE")
    s_static(",")
    s_static("ACK,OPTIONS,BYE,CANCEL,NOTIFY,REFER,MESSAGE")
    s_static("\r\n")
    
    # Expires: 3600
    s_static("Expires: ")
    s_dword(3600, fuzzable=True, format="ascii")
    s_static("\r\n")

    # Event: message-summary
    s_static("Event: ")
    s_string("message-summary")
    s_static("\r\n")

    s_static("Content-Length: ")
    s_dword(0, fuzzable=True, format="ascii")
    s_static("\r\n")
    
    s_static("Max-Forwards: ")
    s_dword(70, fuzzable=True, format="ascii")
    s_static("\r\n")

    # Supported: 100rel, precondition, timer
    s_static("Supported: ")
    if s_block_start("supported_block"):
        s_string("100rel")
        s_delim(",")
    s_block_end()
    s_repeat("supported_block", min_reps=2, max_reps=1000, step=10)
    
    s_string("precondition")
    s_static("\r\n")

    s_static("Allow-Events: ")
    if s_block_start("allow-events_block"):
        s_static("dialog, call-info, sla, include-session-description, presence.winfo, message-summary,")
    s_block_end()
    s_repeat("allow-events_block", min_reps=2, max_reps=1000, step=10)
    s_string("talk")
    s_static("\r\n")

    s_static("Subscription-State: ")
    s_string("terminated")
    s_delim(";")
    s_string("timeout")
    s_static("\r\n")

    s_string("Content-Type: ")
    s_string("application")
    s_delim("/")
    s_string("simple-message-summary")
    s_static("\r\n")    

    s_static("Content-Length: ")
    s_sizer("notify_body", format="ascii", fuzzable=True, signed=True)
    s_static("\r\n")    
    
s_block_end()

if s_block_start("notify_body"):
    s_string("Messages-Waiting: ")
    s_string("yes")
    s_delim("\r\n")
    s_static("Message-Account: ")
    s_lego("to_sip_uri_basic")
    s_static("\r\n")    
s_block_end()

################################################################################

'''
# Similar to the SDP fuzzer but the data is encoded
# Todo: finish
s_initialize("SDP_ENCODED")

if s_block_start("invite_header"):
    s_static("INVITE sip:TARGET_USER@192.168.3.104 SIP/2.0\r\n")
    s_static("CSeq: 1 INVITE\r\n")
    s_static("Via: SIP/2.0/UDP 192.168.3.102:5068;branch=z9hG4bKsomebranchvalue;rport\r\n")
    s_static("From: \"VoIPER\" <sip:USER@192.168.3.104>;tag=somefromtagvalue\r\n")
    s_static("Call-ID: somecallidvalue@ubuntu\r\n")
    s_static("To: <sip:nnp@192.168.3.101>\r\n")
    s_static("Contact: <sip:nnp@192.168.3.102:5068;transport=udp>\r\n")
    s_static("Max-Forwards: 70\r\n")
    s_static("Content-Type: application/sdp\r\n")
    s_static("Content-Length: ")
    s_sizer("invite_sdp", format="ascii", fuzzable=True, signed=True)
    
    #s_static("Content-Encoding: gzip\r\n")
    s_static("Content-Encoding: ")
    s_string("gzip")

    s_static("\r\n\r\n")
s_block_end()

if s_block_start("invite_sdp", encoder=gzip_encode):
    s_static("v=0\r\n")
    s_static("o=- 1190505265 1190505265 IN IP4 192.168.3.104\r\n")
    s_static("s=Opal SIP Session\r\n")

    #s_static("c=IN IP4 192.168.3.102\r\n")
    # repeated c lines cause an overflow in Asterisk at one point
    if s_block_start("c"):
        s_static("c=")
        s_string("IN")
        s_static(" ")
        s_string("IP4")
        s_static(" ")
        s_lego("ip_address_ascii", "192.168.96.69")
        s_static("\r\n")
    s_block_end()
    s_repeat("c", min_reps=2, max_reps=1000, step=10)
    
    s_static("t=0 0\r\n")
    s_static("m=audio 5028 RTP/AVP 101 96 3 107 110 0 8\r\n")
    s_static("a=rtpmap:101 telephone-event/8000\r\n")
    s_static("a=fmtp:101 0-15\r\n")
    s_static("a=rtpmap:96 SPEEX/16000\r\n")
    s_static("a=rtpmap:3 GSM/8000\r\n")
    s_static("a=rtpmap:107 MS-GSM/8000\r\n")
    s_static("a=rtpmap:110 SPEEX/8000\r\n")
    s_static("a=rtpmap:0 PCMU/8000\r\n")
    s_static("a=rtpmap:8 PCMA/8000\r\n")
    s_static("m=video 5030 RTP/AVP 31\r\n")
    s_static("a=rtpmap:31 H261/90000\r\n")
s_block_end()
'''
