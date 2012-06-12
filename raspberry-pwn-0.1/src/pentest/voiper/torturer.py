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

from optparse import OptionParser

from torturer.replay import *

opt_parser = OptionParser()
opt_parser.add_option('-i', '--ip', dest='ip', help='IP address to \
connect to')
opt_parser.add_option('-p', '--port', dest='port', help='(Default=5060) \
Port to connect to', default='5060')
opt_parser.add_option('-d', '--dir', dest='directory',help='(Default=torturer/\
rfc4475_tests) The directory containing SIP test files', \
default='torturer/rfc4475_tests')
opt_parser.add_option('-x', '--proto', dest='proto', help='(Default=udp) \
The protocol to use', default='udp')
opt_parser.add_option('-t', '--type', dest='type', help='(Default=all) \
Type of SIP test messages to send. valid, invalid or all', default='all')
opt_parser.add_option('-o', '--timeout', dest='timeout', help='(Default=3.0) \
Timeout to use on socket operations', default='3.0')
opt_parser.add_option('-c', '--crash-detect', dest='crash_detection',\
help='(Default=1) Enable crash detection or not. 0 to disable', default='1')

(options, args) = opt_parser.parse_args()
if options.ip == None:
    opt_parser.print_help()
    sys.exit(-1)

p = Parser(options.directory)
messages = p.parse()

dispatcher = Dispatcher(options.ip, int(options.port), messages, \
    options.proto, float(options.timeout), bool(int(options.crash_detection))) 
dispatcher.dispatch(options.type)
