package bedmod::pop;
use Socket;

# This package is an extension to bed, to check
# for pop server vulnerabilities.

sub new{
	my $this = {};
	$this->{username}     = undef; # specific for just this
	$this->{password}     = undef; # module
	bless $this;
	return $this;
}

sub init{
	my $this = shift;
	%special_cfg=@_;

	$this->{proto}="tcp";

        if ($special_cfg{'p'} eq "") { $this->{port}='110'; }
          else { $this->{port} = $special_cfg{'p'}; }

	if (( $special_cfg{'u'} eq "") || ( $special_cfg{'v'} eq "")){
		 print qq~
 	Parameters for the POP plugin:

 		-u <username>
 		-v <password>

~;
	 exit(1);
	}

	$this->{username} = $special_cfg{'u'};
	$this->{password} = $special_cfg{'v'};
	$this->{vrfy} = "NOOP\r\n";
 	$iaddr = inet_aton($this->{target})             || die "Unknown host: $host\n";
	$paddr = sockaddr_in($this->{port}, $iaddr)     || die "getprotobyname: $!\n";
 	$proto = getprotobyname('tcp')                  || die "getprotobyname: $!\n";
 	socket(SOCKET, PF_INET, SOCK_STREAM, $proto)    || die "socket: $!\n";
 	connect(SOCKET, $paddr)			 	|| die "connection attempt failed: $!\n";
 	send(SOCKET, "USER $this->{username}\r\n", 0)   || die "USER failed: $!\n";
 	$recvbuf = <SOCKET>;
 	sleep(1);
 	send(SOCKET, "PASS $this->{password}\r\n", 0)   || die "PASS failed: $!\n";

	$recvbuf = <SOCKET>;
	if ( $recvbuf =~ "-ERR" ){
		print ("Username or Password incorrect, can't login\n");
		exit(1);
	}
	send(SOCKET, "QUIT\r\n", 0)

}

sub getQuit{
	return("QUIT\r\n");
}

sub getLoginarray {
 my $this = shift; 
 @Loginarray = (   
        "USER XAXAX\r\n",
        "USER $this->{username}\r\nPASS XAXAX\r\n",
	"APOP XAXAX aaa\r\n",
	"APOP $this->{username} XAXAX\r\n"
 );
 return (@Loginarray);
}

sub getCommandarray {
	my $this = shift;
	# the XAXAX will be replaced with the buffer overflow / format string
	# just comment them out if you don't like them..
	@cmdArray = (
		"LIST XAXAX\r\n",
		"STAT XAXAX\r\n",
		"NOOP XAXAX\r\n",
		"APOP XAXAX\r\n",
		"RSET XAXAX\r\n",
		"RETR XAXAX\r\n",
		"DELE XAXAX\r\n",
		"TOP XAXAX 1\r\n",
		"TOP 1 XAXAX\r\n",
		"UIDL XAXAX\r\n",
	);
	return(@cmdArray);
}

sub getLogin{ 		# login procedure
	my $this = shift;
	@login = ("USER $this->{username}\r\n", "PASS $this->{password}\r\n");
	return(@login);
}

sub testMisc{
	return();
}

1;
