#!/usr/bin/env python

from bin.include import print_banner
from bin.nsecommon import get_target,runnse

def nmapsmbcheckvulns_run():

    """ Main execution logic: reuse common 
        nse modules for this nse script """
    
    self_banner = """ **  Nmap Scripting Engine: Script - smb-check-vulns            **
 **                                                             **
 **  Checks a host or network     MS08-067                      **
 **      for vulnerability to:    Conficker infection           **
 **                               regsvc DoS: (When enabled)    **
 **                               SMBv2 DoS: (When enabled)     **
 *****************************************************************
 """
      
    # BEGIN MAIN EXECUTION
    counter = 0
    print_banner()
    print self_banner
    print "    <ctrl>-c at any time to Cancel"
   
    # get the host or network to operate on
    target = get_target(counter,self_banner)
    
    # enable or disable this scripts arguments
    aggressive = raw_input("""\n    Do you want to enable aggressive testing (regsvc, SMBv2 DoS)?
          WARNING: these checks can cause a Denial of Service! [y|n]: """)
    
    # check answer on aggressive mode
    if aggressive == "y" or aggressive == "yes":
        command = "nmap --script smb-check-vulns --script-args=unsafe=1 -p445 %s" % target
        runnse(command)
    if aggressive == "n" or aggressive == "no":
        command = "nmap --script smb-check-vulns -p445 %s" % target
        runnse(command)

if __name__ == "__main__":  # Allow this module to be run as a standalone script
    nmapsmbcheckvulns_run()
    