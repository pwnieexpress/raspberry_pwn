#
# Quickly hacked Module to test some LPD Stuff,
# not everything ... yeah I am lazy too :)
#
package bedmod::lpd;
use Socket;


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# create a new instance of this object
sub new{
        my $this = {};

        # these ones must be defined
        $this->{sport}              = 721;
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


    if ($special_cfg{'p'} eq "") { $this->{port}='515'; }
      else { $this->{port} = $special_cfg{'p'}; }

    $this->{vrfy} = "";
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# how to quit ?
sub getQuit{
        return("\1\n");
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# what to test without doing a login before
# ..mainly the login stuff *g*
sub getLoginarray {
 my $this = shift;
 @Loginarray = (
                "XAXAX",
                "\01XAXAX\n",
                "\02XAXAX\n",
                "\03XAXAX all\n",
                "\03default XAXAX\n",
                "\04XAXAX all\n",
                "\04default XAXAX\n",
                "\05XAXAX root all\n",
                "\05default XAXAX all\n",
                "\05default root XAXAX\n"
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
                "\0294XAXAX001test\n",
                "\0294cfA001XAXAX\n",
                "\0394XAXAX001test\n",
                "\0394cfA001XAXAX\n",
                
        );
        return(@cmdArray);
}


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# what to send to login ?
sub getLogin{                 # login procedure
        my $this = shift;
        @login = ("\02default\n");
        return(@login);
}

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# here we can test everything besides buffer overflows and format strings
sub testMisc{
        my $this = shift;
        return();
}


1;
