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
import os

from optparse import OptionParser
from fuzzer import fuzzers
from protocol_logic.sip_utilities import SIPRegistrar
from misc.config import parse_config

CONFIG_FILE = 'voiper.config'
opt_parser = OptionParser()

################################################################################
opt_parser.add_option('-l', action='store_true', dest='list_fuzzers',\
help='Display a list of available fuzzers or display help on a specific fuzzer \
if the -f option is also provided')

opt_parser.add_option('-r', action='store_true', dest='registrar', \
help='If passed, listen on port 5060 for a register request before fuzzing. Used for\
fuzzing clients. To register with a server see voiper.config')

opt_parser.add_option('-e', action='store_true', dest='register', \
help='If passed VoIPER will attempt to register with the target. If this option\
is used a file must be created in the current directory titled voiper.config to specify the\
registration details. See voiper.config.sample for an example of how this should be set up.')

opt_parser.add_option('-f', '--fuzzer', dest='fuzzer_type', help='The type of \
fuzzer to use. For a list of valid fuzzers pass the -l flag')

opt_parser.add_option('-i', '--host', dest='host', help='Host to fuzz')

opt_parser.add_option('-p', '--port', dest='port', help='Port to connect to')

#opt_parser.add_option('-x', '--proto', dest='proto', help='UDP or TCP')

opt_parser.add_option('-c', '--crash', dest='crash_detection', help='Crash \
detection settings. 0 - Disabled, 1 - Crashes logged, 2 - Crashes logged and \
fuzzer paused, 3 - Use (nix/win)_process_monitor.py (recommended)')

opt_parser.add_option('-P', '--rpcport', dest='rpc_port', default=26002,\
help='(Optional, def=26002)The port the remote process_monitor is running on. Only relevant\
with -c 4')

opt_parser.add_option('-R','--restartinterval', dest='restart_interval', default=0,\
help='(Optional, def=0) How many test cases to send before the target is restarted. Only relevant \
with -c 3')

opt_parser.add_option('-S', '--startcommand', dest='start_command', \
help='The command used on the system being tested to start the target. Only relevant\
with -c 3')

opt_parser.add_option('-t', '--stopcommand', dest='stop_command', \
help='The command used on the system being tested to stop the target. Only relevant\
with -c 3. If omitted the target PID will be sent a SIGKILL on *nix and terminated \
via taskkill on Windows')

opt_parser.add_option('-a', '--auditfolder', dest='audit_folder', \
help='The folder in sessions to store audit related information')

opt_parser.add_option('-s', '--skip', dest='skip', default=0, \
help='(Optional, def=0)The number of tests to skip')

opt_parser.add_option('-m', '--max_len', dest='max_len', default=8192, \
help='(Optional, def=8192)The maximum length of fuzz strings to be used.')

################################################################################
(options, args) = opt_parser.parse_args()                                                               
if options.list_fuzzers:
    for cls in dir(fuzzers):
        if cls.find('Fuzzer') != -1 and cls.find('Abstract') == -1:
            if options.fuzzer_type and options.fuzzer_type == cls:
                print eval('fuzzers.' + options.fuzzer_type + '.info()')
                break
            elif not options.fuzzer_type:
                print cls
    sys.exit(0)
    
if options.audit_folder == None or \
   options.host == None or options.port == None or options.crash_detection == None:
    opt_parser.print_help()
    sys.exit(-1) 

crash_detection = int(options.crash_detection)
if crash_detection == 3 and options.start_command == None:
    print '[!] Crash detection of 3 requires a start command specified via -S'
    opt_parser.print_help()
    sys.exit(-1) 

stop_command = options.stop_command
if crash_detection == 3 and stop_command == None:
    stop_command = 'TERMINATE_PID'

if not os.path.exists(options.audit_folder):
    print '[!] Path %s does not exist or we do not have sufficient permissions.' % options.audit_folder
    print '[+] Attempting to create %s' % options.audit_folder
    os.mkdir(options.audit_folder)
    if not os.path.exists(options.audit_folder):
        print '[!] Could not create directory %s. Please provide a different path'
        sys.exit(-1)
    else:
        print '[+] Successfully created %s' % options.audit_folder


config_options = None
try:
    config_options, err_line = parse_config(CONFIG_FILE)
    if config_options == None:
        print '[!] voiper.config has an error on line %d (indexed from 0)' % err_line 
        sys.exit(-1)
except IOError:
    print '[!] voiper.config does not exist or we do not have sufficient permissions to read it'
    sys.exit(-1)
        
if options.registrar:
    sr = SIPRegistrar('0.0.0.0', 5060)
    print '[+] Waiting for register request'
    sr.waitForRegister()

try:
    fuzzer = getattr(fuzzers, options.fuzzer_type)
except:
    print '[!] Fuzzer name not recognised: %s' % options.fuzzer_type
    print '[!] Run %s -l for a list of valid fuzzer names' % sys.argv[0]
else:
    f = fuzzer(options.audit_folder, "udp", options.host,\
            int(options.port), crash_detection, skip=int(options.skip), \
            start_command=options.start_command, stop_command=stop_command, \
            procmon_port=int(options.rpc_port), restart_interval=int(options.restart_interval),\
            max_len=int(options.max_len), config_options=config_options)

    f.fuzz()

sys.exit(-1)

