package bedmod::socks4;
use Socket;

# socks5 plugin
#
# not yet tested, got bored just by looking at the protocol

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# create a new instance of this object
sub new{
	my $this = {};
	$this->{username}     = undef;
        $this->{password}     = undef;
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

    if (( $special_cfg{'u'} eq "" ) || ( $special_cfg{'v'} eq "" )){
        print qq~
    Parameters for the Socks5 plugin:
                -u <username>
                -v <password>

~;
        exit(1);
    }

    $this->{username} = $special_cfg{'u'};
    $this->{password} = $special_cfg{'v'};
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
		"XAXAX\n",
                # if the programmer is clever enough he always receives the packet
                # in a buffer which is bigger than ~0x128 :)
                "\x05\x01\x00\x04\xFF\x10",     # check for buffer access which should give a gpf
                "\x05\x01\x00\x04\x50\x10"      # same here different value... lame :)
                                
	);
	return(@cmdArray);
}



# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# what to send to login ?
sub getLogin{ 		# login procedure
	my $this = shift;
        $count1 = char(length($this->{username}));
        $count2 = char(length($this->{password}));

	@login = (
                #protocol version #nr. of authentication methods #username+password
                "\x05\x01\x02",
                #protocol #username len #username #pass len #password
                "\x05$count1$this->{username}$count2$this->{password}";
        );
	return(@login);
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# here we can test everything besides buffer overflows and format strings
sub testMisc{
	my $this = shift;
	return();
}


1;
