package bedmod::imap;
use Socket;

# imap plugin for bed2

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# create a new instance of this object
sub new{
	my $this = {};

	# imap defines
	$this->{user}         = undef;
	$this->{pass}	      = undef;
	bless $this;
	return $this;
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# initialise some parameters
sub init{
	my $this = shift;
	%special_cfg=@_;

    # Set protocol tcp/udp
    $this->{proto} = "tcp"; 

    if ($special_cfg{'p'} eq "") { $this->{port}='143'; }
      else { $this->{port} = $special_cfg{'p'}; }

	if (( $special_cfg{'u'} eq "") || ($special_cfg{'v'} eq "" )) {
		 print qq~
 	Parameters for the imap plugin:

 		-u <username>
		-v <password>

~;
		 exit(1);
	}
	
        $this->{user} = $special_cfg{'u'};
	$this->{pass} = $special_cfg{'v'};
	# how can bed check that the server is still alive
	$this->{vrfy} = "A001 NOOP\r\n";
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# how to quit ?
sub getQuit{
	return("A001 LOGOUT\r\n");
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# what to test without doing a login before
# ..mainly the login stuff *g*
sub getLoginarray {
 my $this = shift;
 @Loginarray = (
	"A001 AUTHENTICATE XAXAX\r\n",
 	"A001 LOGIN XAXAX\r\n",
	"A001 LOGIN $this->{user} XAXAX\r\n"
 );
 return (@Loginarray);
}


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# which commands does this protocol know ?
sub getCommandarray {
	my $this = shift;
	# the XAXAX will be replaced with the buffer overflow / format string
	# place every command in this array you want to test
	@cmdArray = (
		"A001 CREATE myTest\r\n",  # just for testing...
		"FXXZ CHECK XAXAX\r\n",
		"LIST XAXAX\r\n",
		"A001 SELECT XAXAX\r\n",
		"A001 EXAMINE XAXAX\r\n",
		"A001 CREATE XAXAX\r\n",
		"A001 DELETE XAXAX\r\n",
		"A001 RENAME XAXAX\r\n",
		"A001 CREATE test\r\nA001RENAME test XAXAX\r\n",
		"A001 SUBSCRIBE XAXAX\r\n",
		"A001 UNSUBSCRIBE XAXAX\r\n",
		"A001 LIST XAXAX aa \r\n",
		"A001 LIST aa XAXAX\r\n",
		"A001 LIST * XAXAX\r\n",
		"A001 LSUB aa XAXAX\r\n",
		"A001 LSUB XAXAX aa \r\n",   # aa should be ""
		"A001 STATUS XAXAX\r\n",
		"A001 STATUS inbox (XAXAX)\r\n",
		"A001 APPEND XAXAX\r\n",
		"A001 SELECT myTest\r\nA001 SEARCH XAXAX\r\n",
		"A001 SELECT myTest\r\nA001 FETCH XAXAX\r\n",
		"A001 SELECT myTest\r\nA001 FETCH 1:2 XAXAX\r\n",
		"A001 SELECT myTest\r\nA001 STORE XAXAX\r\n",
		"A001 SELECT myTest\r\nA001 STORE 1:2 XAXAX\r\n",
		"A001 SELECT myTest\r\nA001 COPY XAXAX\r\n",
		"A001 SELECT myTest\r\nA001 COPY 1:2 XAXAX\r\n",
		"A001 SELECT myTest\r\nA001 UID XAXAX\r\n",
		"A001 SELECT myTest\r\nA001 UID FETCH XAXAX\r\n",
		"A001 UID XAXAX\r\n",
		"A001 CAPABILITY XAXAX\r\n",
		"A001 DELETEACL XAXAX\r\n",
		"A001 GETACL XAXAX\r\n",
		"A001 LISTRIGHTS XAXAX\r\n",
		"A001 MYRIGHTS XAXAX\r\n",
		"A001 XAXAX\r\n"
	);
	return(@cmdArray);
}


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# what to send to login ?
sub getLogin{ 		# login procedure
	my $this = shift;
	@login = ("A001 LOGIN $this->{user} $this->{pass}\r\n");
	return(@login);
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# here we can test everything besides buffer overflows and format strings
sub testMisc{
	my $this = shift;
	return();
}


1;
