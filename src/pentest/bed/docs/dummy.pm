package bedmod::dummy;
use Socket;

# Example plugin for bed2
#
# Feel free to fill in the gaps ... :)
#
# search bed.pl for "dummy" to see what you need to
# change to include your module
# (just one entry ... no need to be scared *g* )
#

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# create a new instance of this object
sub new{
	my $this = {};

	# define everything you might need
	$this->{dummy}         = undef;
	bless $this;
	return $this;
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# initialise some parameters
sub init{
	my $this = shift;
	%special_cfg=@_;

    # Set protocol tcp/udp
    $this->{proto} = "tcp"; 

    # insert your default port here...
    if ($special_cfg{'p'} eq "") { $this->{port}='110'; }
      else { $this->{port} = $special_cfg{'p'}; }

	# verify you got everything you need,
	# $special_cfg will provide you the commandline
	# switches from u, v, w and x
	if ( $special_cfg{'u'} eq "") {
		 print qq~
 	Parameters for the dummy plugin:

 		-u <description what the user should provide>

~;
		 exit(1);
	}

	# set info nessecairy for for your module..
	$this->{dummy} = $special_cfg{'u'};

	# how can bed check that the server is still alive
	# This string will simply be send to the server
	# ( server should reply something to this )
	$this->{vrfy} = "HELP\r\n";
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# how to quit ?
sub getQuit{
	# what to send to close the connection the right way
	return("QUIT\r\n");
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# what to test without doing a login before
# ..mainly the login stuff *g*
sub getLoginarray {
 my $this = shift;
 @Loginarray = (
 	"USER XAXAX\r\n",
 	"USER $this->{username}\r\nPASS XAXAX\r\n"
 )
 return (@Loginarray);
}


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# which commands does this protocol know ?
sub getCommandarray {
	my $this = shift;
	# the XAXAX will be replaced with the buffer overflow / format string data
	# place every command in this array you want to test
	@cmdArray = (
		"foo XAXAX\r\n",
		"bar XAXAX\r\n",
		"XAXAX\r\n"
	);
	return(@cmdArray);
}


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# what to send to login ?
sub getLogin{ 		# login procedure
	my $this = shift;
	@login = (
		"Hi, I am a dummy\r\n",
		"This is my pass: foobar\r\n"
	);
	return(@login);
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# here we can test everything besides buffer overflows and format strings
sub testMisc{
	# Insert your favourite directory traversal bug here :)
	my $this = shift;
	return();
}


1;
