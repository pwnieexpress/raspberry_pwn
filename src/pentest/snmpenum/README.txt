README SNMPENUM.PL
---------------------
WHAT YOU NEED:
_____________

- perl (if you got windows, check out activestateperl)
- Net::SNMP module (install from CPAN) 
- brains
- a target which runs snmp and supports v2

HOWDUZZITWORK?:
______________

-It's basically an snmp tabledump. I included a couple of OID's which might be interesting

- "perl snmpenum.pl <IP> <COMMUNITY> <FILE>"

if you don't know what IP is or community, RTFM

The FILE consists of 3 tab delimited values;
The first value is neglectable, it's just a system description, which
I was gonna use later but I got lazy and...I just left it like that :)
The second value is a description of the OID-table, which is the the third value.
I provided 3 example files which already give some useful info.
If the output is empty it mostly means the MIB is not supported.

You can make your own file by just doing an snmpwalk and getting the OIDs you needa nd dumping them in a file of the same format.

SOWHYIZZITUSEFUL?
________________

- If you don't think it's useful, .... don't use it.

------
Filip