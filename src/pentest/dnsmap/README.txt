INTRODUCTION

dnsmap was originally released back in 2006 and was inspired by the
fictional story "The Thief No One Saw" by Paul Craig, which can be found
in the book "Stealing the Network - How to 0wn the Box"

dnsmap is mainly meant to be used by pentesters during the information
gathering/enumeration phase of infrastructure security assessments. During the
enumeration stage, the security consultant would typically discover the target
company's IP netblocks, domain names, phone numbers, etc ...

Subdomain brute-forcing is another technique that should be used in the
enumeration stage, as it's especially useful when other domain enumeration
techniques such as zone transfers don't work (I rarely see zone transfers
being *publicly* allowed these days by the way).

If you are interested in researching stealth computer intrusion techniques,
I suggest reading this excellent (and fun) chapter which you can find for
*free* on the web:

http://www.ethicalhacker.net/content/view/45/2/

I'm happy to say that dnsmap was included in Backtrack 2, 3 and 4 and has
been reviewed by the community:

http://backtrack.offensive-security.com/index.php?title=Tools
http://www.networkworld.com/community/node/57543
http://www.linuxhaxor.net/2007/07/14/backtrack-2-information-gathering-all-dnsmap/
http://www.darknet.org.uk/2009/03/dnsmap-022-released-subdomain-bruteforcing-tool/
http://www.gnucitizen.org/blog/new-version-of-dnsmap-out/


COMPILING

Compiling should be straightforward:

$ make

Or:

$ gcc -Wall dnsmap.c -o dnsmap


INSTALLATION

Example of manual installation:

# cp ./dnsmap /usr/local/bin/dnsmap

If you wish to bruteforce several target domains in bulk fashion, you can use the
included dnsmap-bulk.sh script. Just copy the script to /usr/local/bin/ so you can 
call it from any location. e.g.:

# cp ./dnsmap-bulk.sh /usr/local/bin/

And set execute permissions. e.g.:

# chmod ugo+x /usr/local/bin/dnsmap-bulk.sh


LIMITATIONS

Lack of multi-threading. This speed issue will hopefully be resolved in future versions.


FUN THINGS THAT CAN HAPPEN

1. Finding interesting remote access servers (e.g.: https://extranet.targetdomain.com)

2. Finding badly configured and/or unpatched servers (e.g.: test.targetdomain.com)

3. Finding new domain names which will allow you to map non-obvious/hard-to-find netblocks
   of your target organization (registry lookups - aka whois is your friend)

4. Sometimes you find that some bruteforced subdomains resolve to internal IP addresses
   (RFC 1918). This is great as sometimes they are real up-to-date "A" records which means
   that it *is* possible to enumerate internal servers of a target organization from the
   Internet by only using standard DNS resolving (as oppossed to zone transfers for instance).

5. Discover embedded devices configured using Dynamic DNS services (e.g.: linksys-cam.com).
   This method is an alternative to finding devices via Google hacking techniques

USAGE

Bruteforcing can be done either with dnsmap's built-in wordlist or a user-supplied wordlist.
Results can be saved in CSV and human-readable format for further processing. dnsmap does
NOT require root privileges to be run, and should NOT be run with such privileges for
security reasons.

The usage syntax can be obtained by simply running dnsmap without any parameters:

$ ./dnsmap

dnsmap 0.30 - DNS Network Mapper by pagvac (gnucitizen.org)

usage: dnsmap <target-domain> [options]
options:
-w <wordlist-file>
-r <regular-results-file>
-c <csv-results-file>
-d <delay-millisecs>
-i <ips-to-ignore> (useful if you're obtaining false positives)

Note: delay value is a maximum random value. e.g.: if you enter 1000, each DNS request
will be delayed a *maximum* of 1 second. By default, dnsmap uses a value of 10 milliseconds
of maximum delay between DNS lookups


EXAMPLES
Subdomain bruteforcing using dnsmap's built-in word-list:

$ ./dnsmap targetdomain.foo

Subdomain bruteforcing using a user-supplied wordlist:

$ ./dnsmap targetdomain.foo -w wordlist.txt

Subdomain bruteforcing using the built-in wordlist and saving the results to /tmp/ :

$ ./dnsmap targetdomain.foo -r /tmp/

Since no filename was provided in the previous example, but rather only a path, dnsmap would
create an unique filename which includes the current timestamp. e.g.:
/tmp/dnsmap_targetdomain_foo_2009_12_15_234953.txt

Example of subdomain bruteforcing using the built-in wordlist, saving the results to /tmp/,
and waiting a random maximum of 3 milliseconds between each request:

$ ./dnsmap targetdomain.foo -r /tmp/ -d 300

It is recommended to use the -d (delay in milliseconds) option in cases where dnsmap is
interfering with your online experience. i.e.: killing your bandwidth

Subdomain bruteforcing with 0.8 seconds delay, saving results in regular and CSV format,
filtering 2 user-provided IP and using a user-supplied wordlist:

$ ./dnsmap targetdomain.foo -d 800 -r /tmp/ -c /tmp/ -i 10.55.206.154,10.55.24.100 -w ./wordlist_TLAs.txt

For bruteforcing a list of target domains in a bulk fashion use the bash script provided. e.g.:

$ ./dnsmap-bulk.sh domains.txt /tmp/results/


WORDLISTS

http://packetstormsecurity.org/Crackers/wordlists/dictionaries/
http://www.cotse.com/tools/wordlists1.htm
http://wordlist.sourceforge.net/


OTHER SIMILAR TOOLS - choice is freedom!

WS-DNS-BFX
http://ws.hackaholic.org/tools/WS-DNS-BFX.tgz

DNSDigger
http://www.ernw.de/download/dnsdigger.zip

Fierce Domain Scan
http://ha.ckers.org/fierce/

Desperate
http://www.sensepost.com/research_misc.html

DNSenum
http://dnsenum.googlecode.com/files/dnsenum1.2.tar.gz

ReverseRaider
http://complemento.sourceforge.net/

Knock
http://knock.gianniamato.it/


--
pagvac | GNUCITIZEN.org
Feb 2010
