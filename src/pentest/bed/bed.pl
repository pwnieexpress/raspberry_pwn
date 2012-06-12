#!/usr/bin/perl
#
# This program comes with ABSOLUTELY NO WARRANTY.
# This is free software, and you are welcome to redistribute it
# under certain conditions. See docs/GPL.txt for details.
#
# written by mjm ( www.codito.de ) and snakebyte ( www.snake-basket.de )
#
use Getopt::Std;
use Socket;
my $SOCKET = "";

# which plugins do we support? insert your plugin ( dummy ) here...
@plugins = ( "ftp", "smtp", "pop", "http", "irc", "imap", "pjl", "lpd", "finger", "socks4", "socks5" );


# what we test...
# the hope is to overwrite a return pointer on the stack,
# making the server execute invalid code and crash
# the last two entries in the overflowstringsarray are a DoS attempt for ftp/http
my @overflowstrings = ("A" x 33, "A" x 254, "A" x 255, "A" x 1023, "A" x 1024, "A" x 2047, "A" x 2048, "A" x 5000, "A" x 10000, "\\" x 200, "/" x 200);
my @formatstrings = ("%s" x 4, "%s" x 8, "%s" x 15, "%s" x 30, "%.1024d", "%.2048d", "%.4096d");
# three ansi overflows, two ansi format strings, two OEM Format Strings
my @unicodestrings = ("\0x99"x4, "\0x99"x512, "\0x99"x1024, "\0xCD"x10, "\0xCD"x40, "\0xCB"x10, "\0xCB"x40);
my @largenumbers = ("255", "256", "257", "65535", "65536", "65537", "16777215", "16777216", "16777217", "0xfffffff", "-1", "-268435455", "-20");
my @miscstrings = ("/", "%0xa", "+", "<", ">", "%". "-", "+", "*", ".", ":", "&", "%u000", "\r", "\r\n", "\n");


print ("\n BED 0.5 by mjm ( www.codito.de ) & eric ( www.snake-basket.de )\n\n");

# get the parameters we need for every test
getopts('s:t:o:p:u:v:w:x:');
&usage unless(defined $opt_s);

$opt_s = lc($opt_s);                         # convert it to lowercase

# load the specified module
$module = undef;
foreach $plug (@plugins){
 if ( $opt_s eq $plug ){
  eval("use bedmod::$plug;");
  $a = "bedmod::$plug";
  $module = new $a;
 }
}

&usage unless(defined $module);

%special_cfg=(
  "t" => "$opt_t",                           # target
  "o" => "$opt_o",                           # timeOut
  "p" => "$opt_p",                           # port

  "u" => "$opt_u",                           # special parameters for the plugin...
  "v" => "$opt_v",
  "w" => "$opt_w",
  "x" => "$opt_x"
);

$module->{proto}        = undef; 
$module->{target}       = undef;
$module->{port}         = undef;
$module->{vrfy}         = ""; 
$module->{timeout}      = undef;
$module->{sport}        = 0;

if ($special_cfg{'t'} eq "") { $module->{target}='127.0.0.1'; }
  else { $module->{target} = $special_cfg{'t'}; }
if ($special_cfg{'o'} eq "") { $module->{timeout}='2'; }
  else { $module->{timeout} = $special_cfg{'o'}; }

$module->init(%special_cfg);

# test stuff that might happen during login
@cmdArray = $module->getLoginarray;          # which login stuff do we test

if ( @cmdArray[0] ne "" ){
        print (" + Buffer overflow testing:\n");
        &testThis(@overflowstrings);
        print (" + Formatstring testing:\n");
        &testThis(@formatstrings);
}

# test the stuff that might happen during normal protocol events ( after login )
print ("* Normal tests\n");
@cmdArray = $module->getCommandarray;
@login = $module->getLogin;
print (" + Buffer overflow testing:\n");
&testThis(@overflowstrings);
print (" + Formatstring testing:\n");
&testThis(@formatstrings);
print (" + Unicode testing:\n");
&testThis(@unicodestrings);
printf(" + random number testing:\n");
&testThis(@largenumbers);

# test different sizes
for ($i = 1; $i < 20; $i++ ) {
	printf(" + testing misc strings $i:\n");
	&testThis(@miscstrings);
	for ($j = 0; $j < @miscstrings; $j++) {
		$miscstrings[$j] = $miscstrings[$j].$miscstrings[$j];
	}
}

# make the module test all other stuff
print ("* Other tests:\n");
$module->testMisc();
print ("* All tests done.\n\n");
exit(0);




# this function tests each of the two arrays ( buffer overflow and format string )
sub testThis(){
        @testArray = @_;
        if ( $module->{proto} eq "udp" ){  $socktype = SOCK_DGRAM;
        } else {                           $socktype = SOCK_STREAM;
        }

        $count = 0;
        $quit = $module->getQuit;
        foreach $cmd (@cmdArray){
                $count++;

                $cmd2 = $cmd;
                $cmd2 =~ s/\n|\r|[\00-\33]//ig;                              # remove \r and \n for nice displaying
                $cmd2 = substr($cmd2, 0, 30);

                $a = system("echo -n \"\t\ttesting: $count\t$cmd2\t\"");     # crude hack, i didnt want to use Term::ProgressBar...
                foreach $LS (@testArray){
                        $a = system("echo -n .");

                        $command = $cmd;
                        $command =~ s/XAXAX/$LS/ig;                   # prepare the string
                        $iaddr = inet_aton($module->{target})             || die "Unknown host: $module->{target}\n";
                        $paddr = sockaddr_in($module->{port}, $iaddr)     || die "getprotobyname: $!\n";
                        $proto = getprotobyname($module->{proto})         || die "getprotobyname: $!\n";
                        socket(SOCKET, PF_INET, $socktype, $proto)        || die "socket: $!\n";
                        $sockaddr = sockaddr_in($module->{sport}, INADDR_ANY);
                	while ( !bind(SOCKET, $sockaddr) ) {}         # we need to bind for LPD for example
                        connect(SOCKET, $paddr)                           || die "connection attempt failed: $!\n";

                        # login ...
                        foreach $log (@login){
                                if ( $log ne "" ){
                                        send(SOCKET, $log, 0);
                                        sleep(1);                     # some daemons need some time to reply
                                }
                        }
                        send(SOCKET, $command, 0);                    # send the attack and verify that the server is still alive
                                                                      # Is there a possibility to check within connection?
                        if ($module->{vrfy} ne "") {
                                    send(SOCKET, $module->{vrfy},0)               || die "Problem (1) occured with -$count-$cmd2-\n";
                                    $recvbuf = <SOCKET>                           || die "Problem (2) occured with -$count-$cmd2-\n";
                                    send(SOCKET, $quit, 0);           # close the connection
                                    close SOCKET;
                        } else {
                                close SOCKET;
                                $iaddr = inet_aton($module->{target})             || die "Unknown host: $module->{target}\n";
                                $paddr = sockaddr_in($module->{port}, $iaddr)     || die "getprotobyname: $!\n";
                                $proto = getprotobyname($module->{proto})         || die "getprotobyname: $!\n";
                                socket(SOCKET, PF_INET, $socktype, $proto)        || die "socket: $!\n";
                                connect(SOCKET, $paddr)                           || die "Problem (3) occured with -$count-$cmd2-\n";
                                close SOCKET;
                        }

                sleep($module->{timeout});                                             # some servers would kick us for too fast logins
                }
                print "\n";
        }
}


# how to use these scripts...
sub usage {
print qq~
 Usage:

 $0 -s <plugin> -t <target> -p <port> -o <timeout> [ depends on the plugin ]

 <plugin>   = FTP/SMTP/POP/HTTP/IRC/IMAP/PJL/LPD/FINGER/SOCKS4/SOCKS5
 <target>   = Host to check (default: localhost)
 <port>     = Port to connect to (default: standard port)
 <timeout>  = seconds to wait after each test (default: 2 seconds)
 use "$0 -s <plugin>" to obtain the parameters you need for the plugin.

 Only -s is a mandatory switch.

~;
exit(1);
}
