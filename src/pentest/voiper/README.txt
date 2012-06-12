VoIPER - A VoIP Exploit Research toolkit
http://www.unprotectedhex.com
http://voiper.sourceforge.net

Author : nnp
Contact : nnp@unprotectedhex.com 
irc.smashthestack.org #social
License : GPLv2

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Introduction.

VoIPER is a security toolkit that aims to allow developers and security researchers
to easily, extensively and automatically test VoIP devices for security vulnerabilties.
It incorporates a fuzzing suite built on the Sulley fuzzing framework, a SIP torturer
tool based on RFC 4475 and a variety of auxilliary modules to assist in crash detection and
debugging. The primary goal of VoIPER is to create a toolkit with all
required testing functionality built in and to minimise the amount of effort an auditor
has to put into testing the security of a VoIP code base.

This is a beta release and has not been tested as extensively as I would like. That said,
it includes a number of new and useful fuzzers as well as a new SIP backend that greatly
increases protocol compliance and the ability to traverse the state tree of different
request types. It also means that protocol based crash detection is much more reliable
than before. Certain clients are quite odd in how they respond to fuzzing though (Ekiga
for example) and as a result process based crash detection is still recommended where
possible to avoid false positives.

In this release fuzzers were added for REGISTER, NOTIFY and SUBSCRIBE as well as new
fuzzers for CANCEL and ACK that aim to get the device into a state where it is expecting
a CANCEL or ACK before fuzzing it.

For the moment the fuzzer incorporates tests for
 - SIP INVITE (3 different test suites)
 - SIP ACK (Dumb and 'smart' versions)
 - SIP CANCEL (Dumb and 'smart' versions)
 - SIP NOTIFY
 - SIP SUBSCRIBE
 - SIP REGISTER
 - SIP request structure
 - SDP over SIP

This translates to well over 200,000 generated tests covering all SIP attributes
specified in RFC 3261 for the given messages.

It includes other features such as
 - Protocol and process based crash detection and recording
 - Fuzzer pause/restart functionality (SFF)
 - Supports clients that require registration prior to fuzzing
 - Simple to expand to new protocols
 - As far as possible, protocol compliance
 - Target process control (SFF)

SFF : Provided as part of the Sulley Fuzzing Framework, in some cases with my modifications
and fixes

Other features of the toolkit are
 - torturer.py - A tool that uses torture tests defined in rfc4475 (~50) to
   test SIP applications
 - crash_replay.py - A tool to replay the crash log files from fuzzer.py and
   torturer.py
   
VoIPER has been tested on Linux, OS X and Windows using Python 2.4/5. Check the BUGS.txt
file for some changes that have to be made for full functionality on OS X. The tool
sulley/utils/crashbin_explorer.py that is part of the Sulley fuzzing framework requires
ctypes and Python 2.4.

Comments, criticism, patches, bug reports etc etc are all more than welcome. If you use
the toolkit to discover bugs or use parts of it in a different tool it would be nice if you could
credit it (obviously the license implications have something to say about this too). 
If you don't want to do that then if you could notify me, at least I'll know the toolkit is proving useful ;)

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Usage (See USAGE.txt for examples)

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

The following are modifications I've made to Sulley for one reason or another.

- Moved the closing of the socket used to send the fuzz data in the fuzz()
  method to a seperate function in sulley/sessions.py. This is to allow me to
  override this function with my own methods that close the socket at a later
  time.
- Changed the generation of strings in sulley/sulley/primitives.py so that the fuzz
  strings are only generated once. This has a massive performance impact in Sulley
  if more than 10 or so s_string() definitions are used
- Added new fuzz strings to include SIP related delimiters
- Added new fuzz strings to attempt to avoid primitive overflow detection
- Added a 'sent_data' attribute to the request class. This is needed because
  INVITE messages are modified by a callback method in a non-deterministic
  fashion and these modifications need to be accessible by the methods that
  cancel the INVITE's
- Added an ascii format IP address (IPv4 and IPv6) lego (basically a structure for generating fuzzable IP's)
- Added a variety of SIP specific legos 
- Added code in the poll_pedrpc function of sulley/sessions.py to log the 
  sent fuzz data when a crash is detected using one of the process monitoring 
  scripts
- Added the ability to convert fuzzable ints to their hex equivalents. Only applicable
  when format="ascii". e.g if the int was 65535 and hex_vals=True the rendered value
  will be FFFF 
- Added some extra fuzz strings. Long strings interspersed with delimters
- Moved process_monitor.py to win_process_monitor.py
- Added nix_process_monitor.py
- In sessions.py I moved the check on the restart interval inside the loop that checks
  if the required number of tests have been skipped. Otherwise when the fuzzer is skipping
  over tests it will restart the target every time it hits the restart interval
- Changed how process_monitor.py starts a process to use os.startfile(). This is nicer
  in my opinion as you don't have to deal with escaping spaces etc
- Changed the stop_target method in process_monitor.py to use the terminate_process method
  provided by pydbg instead of 'taskkill'. taskkill doesn't work against certain programs
  for some reason. e.g Gizmo. This could have adverse effects I'm not aware of.
- Added an updateProgressBar method to sessions.py that will be overriden by the GUI to receive notifications
  when another fuzz case is sent
- Added an update_GUI_crashes method to sessions.py that will be overriden by the GUI to receive notifications
  when a crash occurs
- Changed the transmit function in sulley/sulley/sessions.py to differentiate between crashes
  that are a result of access violations and those that aren't.
- Changed win_process_monitor.py to return a textual cause of the crash as well as the status of the target  
- Changed win_process_monitor.py so that the time given to a restarted process to settle in can be 
  specified by the user
- Changed sulley/sulley/primitives.py so that you can specify the maximum lenght of fuzz strings
  to use                                                       
