import struct
from sulley import blocks, primitives, sex

class q_value (blocks.block):
    def __init__ (self, name, request, value, options={}):
        blocks.block.__init__(self, name, request, None, None, None, None)

        self.value   = value
        self.options = options

        # fuzz by default
        if self.options.has_key('fuzzable'):
            fuzzable = self.options['fuzzable']
        else:
            fuzzable = True
            
        self.push(primitives.string("q" ,fuzzable=fuzzable))
        self.push(primitives.delim("="))
        self.push(primitives.string("0", fuzzable=fuzzable))
        self.push(primitives.delim("."))
        self.push(primitives.dword(5, fuzzable=True, signed=True, format="ascii"))

class static_challenge (blocks.block):
    def __init__ (self, name, request, value, options={}):
        blocks.block.__init__(self, name, request, None, None, None, None)

        self.value   = value
        self.options = options

        # fuzz by default
        if self.options.has_key('fuzzable'):
            fuzzable = self.options['fuzzable']
        else:
            fuzzable = True

        self.push(primitives.string("Digest" ,fuzzable=fuzzable))
        self.push(primitives.delim(" "))
        self.push(primitives.string("realm" ,fuzzable=fuzzable))
        self.push(primitives.delim("="))
        self.push(primitives.delim("\""))
        self.push(primitives.string("atlanta.com" ,fuzzable=fuzzable))
        self.push(primitives.delim("\""))
        self.push(primitives.delim(","))
        self.push(primitives.static("domain="))
        self.push(primitives.static("\""))
        self.push(primitives.string("sip:ss1.carrier.com" ,fuzzable=fuzzable))
        self.push(primitives.static("\",qop=\""))
        self.push(primitives.string("auth" ,fuzzable=fuzzable))
        self.push(primitives.delim(","))
        self.push(primitives.string("auth-int" ,fuzzable=fuzzable))
        self.push(primitives.static("\",nonce=\""))
        self.push(primitives.string("f84f1cec41e6cbe5aea9c8e88d359" ,fuzzable=fuzzable))
        self.push(primitives.static("\",opaque=\""))
        self.push(primitives.string("5ccc069c403ebaf9f0171e9517f40e41" ,fuzzable=fuzzable))
        self.push(primitives.static("\",stale="))
        self.push(primitives.string("FALSE" ,fuzzable=fuzzable))
        self.push(primitives.static(",algorithm="))
        self.push(primitives.static("MD5"))

class static_credentials (blocks.block):
    def __init__ (self, name, request, value, options={}):
        blocks.block.__init__(self, name, request, None, None, None, None)

        self.value   = value
        self.options = options
        
        # fuzz by default
        if self.options.has_key('fuzzable'):
            fuzzable = self.options['fuzzable']
        else:
            fuzzable = True
            
        self.push(primitives.string("Digest" ,fuzzable=fuzzable))
        self.push(primitives.delim(" "))

        self.push(primitives.string("username" ,fuzzable=fuzzable))
        self.push(primitives.delim("="))
        self.push(primitives.delim("\""))
        self.push(primitives.string("nnp" ,fuzzable=fuzzable))
        self.push(primitives.delim("\""))
        self.push(primitives.delim(","))
            
        self.push(primitives.static("realm"))
        self.push(primitives.static("="))
        self.push(primitives.static("\""))
        self.push(primitives.string("atlanta.com" ,fuzzable=fuzzable))
        self.push(primitives.static("\""))
        self.push(primitives.static(","))

        self.push(primitives.static("uri="))
        self.push(primitives.static("\""))
        self.push(primitives.string("http://www.unprotectedhex.com/" ,fuzzable=fuzzable))# rquest-uri
        self.push(primitives.static("\""))
        self.push(primitives.static(","))
            
        self.push(primitives.static("response="))
        self.push(primitives.static("\""))
        self.push(primitives.string("f84f1cec41e6cbe5aea9c8e88d359def" ,fuzzable=fuzzable))
        self.push(primitives.static("\""))
        self.push(primitives.static(","))

        self.push(primitives.static("qop="))
        self.push(primitives.static("\""))
        self.push(primitives.string("auth" ,fuzzable=fuzzable))
        self.push(primitives.static("\""))
        self.push(primitives.static(","))

        self.push(primitives.static("nc="))
        self.push(primitives.string("f84f1ce" ,fuzzable=fuzzable))  # 8LHEX
        self.push(primitives.static(","))

        self.push(primitives.static("cnonce="))
        self.push(primitives.static("\""))
        self.push(primitives.string("f84f1cec41e6cbe5aea9c8e88d359" ,fuzzable=fuzzable))
        self.push(primitives.static("\""))
        self.push(primitives.static(","))

        self.push(primitives.static("nonce="))
        self.push(primitives.static("\""))
        self.push(primitives.string("f84f1cec41e6cbe5aea9c8e88d359" ,fuzzable=fuzzable))
        self.push(primitives.static("\""))
        self.push(primitives.static(","))
            
        self.push(primitives.static("opaque="))
        self.push(primitives.static("\""))
        self.push(primitives.string("5ccc069c403ebaf9f0171e9517f40e41" ,fuzzable=fuzzable))
        self.push(primitives.static("\""))

class to_sip_uri (blocks.block):
    def __init__ (self, name, request, value, options={}):
        blocks.block.__init__(self, name, request, None, None, None, None)

        self.value   = value
        self.options = options

        # fuzz by default
        if self.options.has_key('fuzzable'):
            fuzzable = self.options['fuzzable']
        else:
            fuzzable = True
            
        self.push(primitives.string("sip" ,fuzzable=fuzzable))
        self.push(primitives.delim(":"))
        # userinfo
        self.push(primitives.string("TARGET_USER" ,fuzzable=fuzzable))
        self.push(primitives.delim(":"))
        self.push(primitives.string("password" ,fuzzable=fuzzable))
        self.push(primitives.delim("@"))
        # hostport
        self.push(primitives.string("HOST" ,fuzzable=fuzzable))
        self.push(primitives.delim(":"))
        self.push(primitives.string("PORT" ,fuzzable=fuzzable))
        # uri-parameters
        self.push(primitives.delim(";"))
        self.push(primitives.string("transport" ,fuzzable=fuzzable))
        self.push(primitives.delim("="))
        self.push(primitives.string("udp" ,fuzzable=fuzzable))
        self.push(primitives.static(";"))
        self.push(primitives.static("user="))
        self.push(primitives.string("udp" ,fuzzable=fuzzable))
        self.push(primitives.static(";"))
        self.push(primitives.static("ttl="))
        self.push(primitives.string("67" ,fuzzable=fuzzable))
        self.push(primitives.static(";"))
        self.push(primitives.static("method="))
        self.push(primitives.string("INVITE" ,fuzzable=fuzzable))
        self.push(primitives.static(";"))
        self.push(primitives.static("maddr="))
        self.push(primitives.string("HOST" ,fuzzable=fuzzable))
        # headers
        self.push(primitives.delim("?"))
        self.push(primitives.string("subject" ,fuzzable=fuzzable))
        self.push(primitives.delim("="))
        self.push(primitives.string("hval" ,fuzzable=fuzzable))
        self.push(primitives.delim("&"))
        self.push(primitives.static("hname2=hval"))

class from_sip_uri (blocks.block):
    def __init__ (self, name, request, value, options={}):
        blocks.block.__init__(self, name, request, None, None, None, None)

        self.value   = value
        self.options = options

        # fuzz by default
        if self.options.has_key('fuzzable'):
            fuzzable = self.options['fuzzable']
        else:
            fuzzable = True
            
        self.push(primitives.string("sip" ,fuzzable=fuzzable))
        self.push(primitives.delim(":"))
        # userinfo
        self.push(primitives.string("USER" ,fuzzable=fuzzable))
        self.push(primitives.delim(":"))
        self.push(primitives.string("password" ,fuzzable=fuzzable))
        self.push(primitives.delim("@"))
        # hostport
        self.push(primitives.string("LOCAL_IP" ,fuzzable=fuzzable))
        self.push(primitives.delim(":"))
        self.push(primitives.string("PORT" ,fuzzable=fuzzable))
        # uri-parameters
        self.push(primitives.delim(";"))
        self.push(primitives.string("transport" ,fuzzable=fuzzable))
        self.push(primitives.delim("="))
        self.push(primitives.string("udp" ,fuzzable=fuzzable))
        self.push(primitives.static(";"))
        self.push(primitives.static("user="))
        self.push(primitives.string("udp" ,fuzzable=fuzzable))
        self.push(primitives.static(";"))
        self.push(primitives.static("ttl="))
        self.push(primitives.string("67" ,fuzzable=fuzzable))
        self.push(primitives.static(";"))
        self.push(primitives.static("method="))
        self.push(primitives.string("INVITE" ,fuzzable=fuzzable))
        self.push(primitives.static(";"))
        self.push(primitives.static("maddr="))
        self.push(primitives.string("LOCAL_IP" ,fuzzable=fuzzable))
        # headers
        self.push(primitives.delim("?"))
        self.push(primitives.string("subject" ,fuzzable=fuzzable))
        self.push(primitives.delim("="))
        self.push(primitives.string("hval" ,fuzzable=fuzzable))
        self.push(primitives.delim("&"))
        self.push(primitives.static("hname2=hval"))        

########################################################################################################################

class from_sip_uri_basic (blocks.block):
    def __init__ (self, name, request, value, options={}):
        blocks.block.__init__(self, name, request, None, None, None, None)

        self.value   = value
        self.options = options

        # fuzz by default
        if self.options.has_key('fuzzable'):
            fuzzable = self.options['fuzzable']
        else:
            fuzzable = True
            
        self.push(primitives.string("sip" ,fuzzable=fuzzable))
        self.push(primitives.delim(":"))
        # userinfo
        self.push(primitives.string("USER" ,fuzzable=fuzzable))
        self.push(primitives.delim("@"))
        # hostport
        self.push(primitives.string("LOCAL_IP" ,fuzzable=fuzzable))
        self.push(primitives.delim(":"))
        self.push(primitives.string("PORT" ,fuzzable=fuzzable))
        # uri-parameters
        self.push(primitives.delim(";"))
        self.push(primitives.string("transport" ,fuzzable=fuzzable))
        self.push(primitives.delim("="))
        self.push(primitives.string("udp" ,fuzzable=fuzzable))

########################################################################################################################

class to_sip_uri_basic (blocks.block):
    def __init__ (self, name, request, value, options={}):
        blocks.block.__init__(self, name, request, None, None, None, None)

        self.value   = value
        self.options = options

        # fuzz by default
        if self.options.has_key('fuzzable'):
            fuzzable = self.options['fuzzable']
        else:
            fuzzable = True
            
        self.push(primitives.string("sip" ,fuzzable=fuzzable))
        self.push(primitives.delim(":"))
        # userinfo
        self.push(primitives.string("TARGET_USER" ,fuzzable=fuzzable))
        self.push(primitives.delim("@"))
        # hostport
        self.push(primitives.string("HOST" ,fuzzable=fuzzable))
        self.push(primitives.delim(":"))
        self.push(primitives.string("PORT" ,fuzzable=fuzzable))
        # uri-parameters
        self.push(primitives.delim(";"))
        self.push(primitives.string("transport" ,fuzzable=fuzzable))
        self.push(primitives.delim("="))
        self.push(primitives.string("udp" ,fuzzable=fuzzable))
