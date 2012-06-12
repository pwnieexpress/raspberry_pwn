package bedmod::socks4;
use Socket;

# socks4 plugin (anyone still using this?)
# pretty few to test, i did not even find an rfc for this
# protocol *yuck*

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# create a new instance of this object
sub new{
	my $this = {};
	$this->{username}     = undef;
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

    # check for missing args, set target and host
    # every module has to do this
    if ($special_cfg{'p'} eq "") { $this->{port}='1080'; }
      else { $this->{port} = $special_cfg{'p'}; }
    $this->{sport} = 0;
    $this->{vrfy} = "";

    if ( $special_cfg{'u'} eq "" ){
        print qq~
    Parameters for the Socks4 plugin:
                -u <username>

~;
        exit(1);
    }

    $this->{username} = $special_cfg{'u'};

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

	# all there is to test is the username as far as it seems...
	@cmdArray = (
#		"XAXAX\n",
               # we use protocol version 04
               # destination port is 6668
               # destination ip is 192.168.0.1
               "\x04\x01\x1a\x0c\xc0\xA8\x00\x01XAXAX\x00",        # connect
               "\x04\x02\x1a\x0c\xc0\xA8\x00\x01XAXAX\x00",        # bind
               "\x04\x01\x1a\x0c\x00\x00\x00\x01$this->{username}\x00XAXAX",        # connect socks4a

               "\x04\x02\x1a\x0c\x00\x00\x00\x01$this->{username}\x00XAXAX"        # bind socks4a

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
