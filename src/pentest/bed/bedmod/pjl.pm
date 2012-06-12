package bedmod::pjl;
use Socket;

# Plugin to check PJL Printer
# written to test a Lexmark T522
#
# i didnt read the pjl rfc or whatever just included
# the stuff if found by a quick google search :) 

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

    # check for missing args, set target and host
    if ($special_cfg{'p'} eq "") { $this->{port}='9100'; }
      else { $this->{port} = $special_cfg{'p'}; }

    $this->{vrfy} = "";
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# how to quit ?
sub getQuit{
	return("\33%-12345X\n"); 
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# we got no login procedure...
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
	# here we go with our commands
        $PI = "\33%-12345X\@PJL"; #  \n\@PJL
	@cmdArray = (
		$PI." ENTER XAXAX\n",
		$PI." ENTER LANGUAGE = XAXAX\n",
		$PI." JOB XAXAX\n",
		$PI." JOB NAME = XAXAX\n",
		$PI." JOB NAME = \"foo\" START = XAXAX\n",
		$PI." JOB NAME = \"foo\" END = XAXAX\n",
		$PI." JOB NAME = \"foo\" PASSWORD = XAXAX\n",
		$PI." EOJ XAXAX\n",
		$PI." EOJ NAME = XAXAX\n",
		$PI." DEFAULT XAXAX\n",
		$PI." DEFAULT LPARM: XAXAX\n",
		$PI." DEFAULT IPARM: XAXAX\n",
		$PI." SET XAXAX\n",
		$PI." SET LPARM: XAXAX\n",
		$PI." SET IPARM: XAXAX\n",
		$PI." INQUIRE XAXAX\n",
		$PI." INQUIRE LPARM: XAXAX\n",
		$PI." INQUIRE IPARM: XAXAX\n",
		$PI." DINQUIRE XAXAX\n",
		$PI." DINQUIRE LPARM: XAXAX\n",
		$PI." DINQUIRE IPARM: XAXAX\n",
		$PI." INFO XAXAX\n",
		$PI." ECHO XAXAX\n",
		$PI." USTATUS XAXAX\n",
		$PI." USTATUS A = XAXAX\n",
		$PI." OPMSG DISPLAY = XAXAX\n",
		$PI." RDYMSG DISPLAY = XAXAX\n",
		$PI." STMSG DISPLAY = XAXAX\n",                
		$PI." COMMENT XAXAX\n",
		$PI." SET PAGEPROTECT = XAXAX\n",
		$PI." SET LIMAGEENHANCE = XAXAX\n",
		$PI." LDPARM : PCL LCOLOREXTENSIONS = XAXAX\n",
		$PI." LJOBINFO XAXAX\n",
		$PI." LJOBINFO USERID = XAXAX\n",
		$PI." LJOBINFO HOSTID = XAXAX\n"
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
