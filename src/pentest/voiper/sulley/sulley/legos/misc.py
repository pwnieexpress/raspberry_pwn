import struct
from sulley import blocks, primitives, sex

########################################################################################################################
class ip_address_ascii (blocks.block):
    def __init__ (self, name, request, value, options={}):
        blocks.block.__init__(self, name, request, None, None, None, None)

        self.value   = value
        self.options = options

        if not self.value:
            raise sex.error("MISSING LEGO.tag DEFAULT VALUE")
        
        ip_arr = value.split(".")
        ctr = 0
        for ip_val in ip_arr:
            if ctr == 0: 
                self.push(primitives.string(ip_val))
                self.push(primitives.delim("."))
            else:
                self.push(primitives.static(ip_val))
                if ctr < 3:
                    self.push(primitives.delim("."))
            ctr += 1
        
########################################################################################################################
class ipv6_address_ascii (blocks.block):
    def __init__ (self, name, request, value, options={}):
        blocks.block.__init__(self, name, request, None, None, None, None)

        self.value   = value
        self.options = options

        if not self.value:
            raise sex.error("MISSING LEGO.tag DEFAULT VALUE")

        hex_arr = value.split(":")
        ctr = 0
        for hex_val in hex_arr:      
            if ctr == 0: 
                self.push(primitives.string(hex_val))
                self.push(primitives.delim(":"))
            else:
                self.push(primitives.static(hex_val))
                if ctr < 7:
                    self.push(primitives.static(":"))
            ctr += 1
            
########################################################################################################################
class dns_hostname (blocks.block):
    def __init__ (self, name, request, value, options={}):
        blocks.block.__init__(self, name, request, None, None, None, None)

        self.value   = value
        self.options = options

        if not self.value:
            raise sex.error("MISSING LEGO.tag DEFAULT VALUE")

        self.push(primitives.string(self.value))


    def render (self):
        '''
        We overload and extend the render routine in order to properly insert substring lengths.
        '''

        # let the parent do the initial render.
        blocks.block.render(self)

        new_str = ""

        # replace dots (.) with the substring length.
        for part in self.rendered.split("."):
            new_str += str(len(part)) + part

        # be sure to null terminate too.
        self.rendered = new_str + "\x00"

        return self.rendered


########################################################################################################################
class tag (blocks.block):
    def __init__ (self, name, request, value, options={}):
        blocks.block.__init__(self, name, request, None, None, None, None)

        self.value   = value
        self.options = options

        if not self.value:
            raise sex.error("MISSING LEGO.tag DEFAULT VALUE")

        # <example>
        # [delim][string][delim]

        self.push(primitives.delim("<"))
        self.push(primitives.string(self.value))
        self.push(primitives.delim(">"))
