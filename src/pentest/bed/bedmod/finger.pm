package bedmod::finger;
use Socket;

# lame finger plugin :)

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# create a new instance of this object
sub new{
	my $this = {};
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

    if ($special_cfg{'p'} eq "") { $this->{port}='79'; }
      else { $this->{port} = $special_cfg{'p'}; }
    $this->{sport} = 0;
    $this->{vrfy} = "root\n";
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# how to quit ?
sub getQuit{
	return("");
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# what to test without doing a login before
# ..mainly the login stuff *g*
sub getLoginarray {
 my $this = shift;
 @Loginarray = ("");
 return (@Loginarray);
}


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# which commands does this protocol know ?
sub getCommandarray {
	my $this = shift;
	# the XAXAX will be replaced with the buffer overflow / format string
	# place every command in this array you want to test
	@cmdArray = (
		"XAXAX\n"
	);
	return(@cmdArray);
}


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# what to send to login ?
sub getLogin{ 		# login procedure
	my $this = shift;
	@login = ("");
	return(@login);
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# here we can test everything besides buffer overflows and format strings
sub testMisc{
	my $this = shift;
	return();
}


1;
