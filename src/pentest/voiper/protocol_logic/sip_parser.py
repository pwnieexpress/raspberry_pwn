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

import re

BRANCH = 1
FROM = 2
TO = 3
RCODE = 4
TOTAG = 5
CALLID = 6
CSEQNUM = 7
FROMTAG = 8
RURI = 9
VIA = 10
WWW_AUTHEN_NONCE = 11
WWW_AUTHEN_REALM = 12
CONTACT = 13

r_1XX = 99
r_2XX = 98
r_3XX = 97
r_4XX = 96
r_5XX = 95
r_6XX = 94

r_ACK = 89
r_INVITE = 88
r_REGISTER = 87
r_OPTIONS = 86
r_CANCEL = 85

r_UNKNOWN = 69
r_SEND = 68

r_401 = 59
r_180 = 58

class SIPParser:
    def __init__(self):
        '''
        A class to implement all the functionality required to parse the
        relevant fields from a SIP message
        '''
                
        self.regex_dict = {BRANCH : r'^Via.*?branch\s*?=\s*?(?P<target>[\d\w-]+)',
                    FROMTAG : r'^From.*?;tag=(?P<target>[\w\d-]+)',
                    CALLID : r'^Call-ID\s*?:\s*(?P<target>\S+)',
                    CSEQNUM : r'^CSeq\s*?:\s*(?P<target>\d+)',                    
                    TO : r'^To\s*?:\s*(?P<target>.+)\r\n',                    
                    FROM : r'^From\s*?:\s*(?P<target>.+)\r\n',
                    RCODE : r'^(?P<target>INVITE|CANCEL|OPTIONS|REGISTER|SIP/2\.0 \d{3}|ACK)',
                    RURI : r'(INVITE|CANCEL|OPTIONS|REGISTER)\s+(?P<target>.+?)\s+SIP/2.0',
                    VIA : r'^Via\s*?:\s*(?P<target>.+)\r\n',
                    WWW_AUTHEN_NONCE : r'^WWW-Authenticate\s*?:\s*Digest.+nonce="(?P<target>[\w\d\.-]+)"',
                    WWW_AUTHEN_REALM : r'^WWW-Authenticate\s*?:\s*Digest.+realm="(?P<target>[\w\d\.@]+)"',
                    CONTACT : r'^Contact\s*?:\s*?(?P<target><sip:[\w\d]+@[\w\d\.]+(:[\d]+)?(;transport=(udp|tcp))?>)',
                   }
        
        self.regex_c = {}
        # compile those filthy regexs ;) 
        for r_name in self.regex_dict.keys():
            r_val = self.regex_dict[r_name]
            r = re.compile(r_val, re.IGNORECASE | re.MULTILINE)
            self.regex_c[r_name] = r

    def parse(self, data, fields=None):
        '''
        Parses the provided data and extracts the relevant fields and their
        values into a dictionary

        @type data: String
        @param data: The SIP message to be parsed
        @type field: List
        @param field: A list of the fields to parse identified by the constants
            defined in the __init__ of this class. If None all fields are parsed

        @rtype: Dictionary
        @return: A dictionary of fields to and their associated values
        '''

        if fields == None:
            fields = self.regex_c.keys()

        res_dict = {}
        for r_name in fields:
            val = self.regex_c[r_name].search(data)
            if val and len(val.groups()) != 0:
                res_dict[r_name] = val.group('target')

        return self.normalise_rcodes(res_dict)

    def normalise_rcodes(self, data_dict):
        '''
        Method to change textual response codes to one of the constants
        defined in the __init__ method

        @type data_dict: Dictionary
        @param data_dict: A dictionary of message fields to their values
            parsed from a SIP message

        @rtype: Dictionary
        @return: A dictionary where the response code strings have been
            converted to constants defined in this class
        '''

        if data_dict.has_key(RCODE):
            r_code = data_dict[RCODE]
            if r_code.upper() == 'ACK':
                r_code = r_ACK
            elif r_code.upper() == 'INVITE':
                r_code = r_INVITE
            elif r_code.upper() == 'REGISTER':
                r_code = r_REGISTER
            elif r_code.upper() == 'OPTIONS':
                r_code = r_OPTIONS
            elif r_code.upper() == 'CANCEL':
                r_code = r_CANCEL       
            elif r_code.find('SIP/2.0') != -1:
                data = r_code.split(" ")
                r_code = data[1]
                
                if r_code[0] == '1':
                    r_code = r_1XX
                elif r_code[0] == '2':
                    r_code = r_2XX
                elif r_code[0] == '3':
                    r_code = r_3XX                    
                elif r_code[0] == '4':
                    r_code = r_4XX
                elif r_code[0] == '5':
                    r_code = r_5XX                    
                elif r_code[0] == '6':
                    r_code = r_6XX
                elif r_code == '401':
                    r_code = r_401
                elif r_code == '180':
                    r_code = r_180                    
            else:
                r_code = r_UNKNOWN
                
            data_dict[RCODE] = r_code

        return data_dict

    def denormalise_rcode(self, r_code):
        '''
        Convert the int representation of a rcode to its textual value

        @type r_code: Integer
        @param r_code: The rcode to convert

        @rtype: String
        @return: The textual value corresponding to the given rcode
        '''

        r_dict = { 99 : 'r_1XX',
            98 : 'r_2XX',
            97 : 'r_3XX',
            96 : 'r_4XX',                   
            95 : 'r_5XX',
            94 : 'r_6XX',
                   
            89 : 'r_ACK',            
            88 : 'r_INVITE',
            87 : 'r_REGISTER',
            86 : 'r_OPTIONS',
            85 : 'r_CANCEL',

            68 : 'r_UNKNOWN',
            59 : 'r_401',
            58 : 'r_180',
        }

        return r_dict[r_code]
