#!/usr/bin/perl
#Written by RSnake <h@ckers.org>
#Yes, it sucks, feel free to modify it at will.
#This is vulnerable to XSS (duh) so don't throw it on a production machine.
#No RTFM here, if you don't know what this does you probably shouldn't be
#messing with it anyway.  This is for people doing XSS research only, if those
#words don't resonate with you, you've got the wrong program.

#Defaults
#----------------------------------------------------------------------
$disable_checks = "0"; #change this to "1" to disable remote upgrade checks
$default_charset = "UTF-8";


#I wouldn't recommend editing below here unless you know what you're doing
#----------------------------------------------------------------------

$version = "1.1";

sub GetPostArgs {
  read( STDIN, $a, $ENV{CONTENT_LENGTH});
  &parse($a,'&');
}

sub parse {
    local($argstring,$splitcharacter) = @_;
    foreach (split("$splitcharacter", $argstring)) { 
     if (/(.*)=(.*)/) {
          ($nam, $val) = ($1, $2);
          $val =~ s/\+/ /g ;
          $val =~ s/%(..)/pack('c',hex($1))/eg;  # unescape characters
          if (defined $in{$nam}) {       
            $in{$nam} .= "#" . $val
	  } else {
            $in{$nam} = $val;                
    	  }
         }
     }
    @k = keys(%in);                # I couldn't find a better way of counting
    $noin = $#k; $noin++;          # entries in %in.  do YOU know one?
}

&GetPostArgs;
$v=$in{'v'};
$w=$in{'w'};
$x=$in{'x'};
$y=$in{'y'};
$z=$in{'z'};
$v=~ s/&quot;/"/g;
$w=~ s/&quot;/"/g;
$x=~ s/&quot;/"/g;
$y=~ s/&quot;/"/g;
$z=~ s/&quot;/"/g;

@encoding = (
              'BIG5',
              'EUC-JP',
              'EUC-KR',
              'GB18030',
              'GB2312',
              'ISO-8859-1',
              'ISO-8859-5',
              'SHIFT_JIS',
              #'UTF-16', #ruins the entire fuzzer output
              #'UTF-7',  #this just causes too many problems
              'UTF-8',
              'US-ASCII',
              'Windows-1252'
             );

#Some default ranges to test that happen to often show issues.
#This is an array so if you want to work with specific ranges
#you can modify them here.
@default_ranges = (
                   "0-255"
                  );

foreach (@encoding) {
  if ($in{'encoding'} eq $_) {
    $charset = $in{'encoding'};
  }
}
unless ($charset) {
#Set a default charset to get started, and check for version only 
#if it's default as to reduce annoyance for anyone using this.
  $charset = $default_charset;
  $enc_not_found = "Encoding defaulted to $charset";
  $versioncheck = 1;
}
unless (($v) || ($w) || ($x) || ($y) || ($z)) {
#Some default values to get started, and check for version only 
#if it's default as to reduce annoyance for anyone using this.
$versioncheck = $versioncheck + 1;
$v =<<EOHTMLV;
<IMG SRC="" ALT="XSS
EOHTMLV
$w =<<EOHTMLW;
">ABCD" onerror='XSS_ME("
EOHTMLW
$x =<<EOHTMLX;
")'>
EOHTMLX
$y =<<EOHTMLY;
EOHTMLY
$z =<<EOHTMLZ;
EOHTMLZ
}
chomp($v, $w, $x, $y, $z);
$v_un = $v;
$w_un = $w;
$x_un = $x;
$y_un = $y;
$z_un = $z;
$v_un =~ s/"/&quot;/g;
$w_un =~ s/"/&quot;/g;
$x_un =~ s/"/&quot;/g;
$y_un =~ s/"/&quot;/g;
$z_un =~ s/"/&quot;/g;

print "Content-Type: text/html;charset=$charset\n\n";
print "<HTML>\n<BODY><A HREF=\"http://ha.ckers.org/\">XSSFuzz by ha.ckers.org</A><BR>";
if (($versioncheck == 2) && ($disable_checks < 1)) {
  print "<SCRIPT SRC=\"http://ha.ckers.org/fuzzer/fuzzer-version.cgi?$version\"></SCRIPT>";
  print "<BR><FONT COLOR=\"red\">Note: This default test in the Input boxes is designed for <B>Internet Explorer</B> to test the variable width encoding issue:</FONT></BR>";
}
if ($ENV{'QUERY_STRING'} ne "start") {
  $v_char_char = " SELECTED";
  $w_dec_char = " SELECTED";
  $x_dec_char = " SELECTED";
  $y_none_char = " SELECTED";
} else {
  if ($in{'v_char'} eq "") {
    $v_none_char = " SELECTED";
  } elsif ($in{'v_char'} eq "char") {
    $v_char_char = " SELECTED";
  } elsif ($in{'v_char'} eq "dec") {
    $v_dec_char = " SELECTED";
  } elsif ($in{'v_char'} eq "hex") {
    $v_hex_char = " SELECTED";
  }
  if ($in{'w_char'} eq "") {
    $w_none_char = " SELECTED";
  } elsif ($in{'w_char'} eq "char") {
    $w_char_char = " SELECTED";
  } elsif ($in{'w_char'} eq "dec") {
    $w_dec_char = " SELECTED";
  } elsif ($in{'w_char'} eq "hex") {
    $w_hex_char = " SELECTED";
  }
  if ($in{'x_char'} eq "") {
    $x_none_char = " SELECTED";
  } elsif ($in{'x_char'} eq "char") {
    $x_char_char = " SELECTED";
  } elsif ($in{'x_char'} eq "dec") {
    $x_dec_char = " SELECTED";
  } elsif ($in{'x_char'} eq "hex") {
    $x_hex_char = " SELECTED";
  }
  if ($in{'y_char'} eq "") {
    $y_none_char = " SELECTED";
  } elsif ($in{'y_char'} eq "char") {
    $y_char_char = " SELECTED";
  } elsif ($in{'y_char'} eq "dec") {
    $y_dec_char = " SELECTED";
  } elsif ($in{'y_char'} eq "hex") {
    $y_hex_char = " SELECTED";
  }
}
print<<EOHTML;
<BR>
<DIV ALIGN="CENTER">
<TABLE>
  <TR>
    <TD VALIGN="TOP">
      <TABLE>
        <TR>
          <TD COLSPAN="2"><DIV ALIGN="CENTER"><B>Input:</B></DIV>
          </TD>
        </TR>
        <TR>
          <TD>Strings to concatinate
          </TD>
          <TD>Delimiters to fuzz
          </TD>
        </TR>
        <TR>
          <TD>
            <FORM METHOD="POST" ACTION="?start">
              <input type=text value="$v_un" name="v"><BR>
              <input type=text value="$w_un" name="w"><BR>
              <input type=text value="$x_un" name="x"><BR>
              <input type=text value="$y_un" name="y"><BR>
              <input type=text value="$z_un" name="z">
          </TD>
          <TD valign=top>
            <select name="v_char">
              <option value=""$v_none_char></option>
              <option value="char"$v_char_char>character</option>
              <option value="dec"$v_dec_char>decimal</option>
              <option value="hex"$v_hex_char>hexidecimal</option>
            </select><BR>
            <select name="w_char">
              <option value=""$w_none_char></option>
              <option value="char"$w_char_char>character</option>
              <option value="dec"$w_dec_char>decimal</option>
              <option value="hex"$w_hex_char>hexidecimal</option>
            </select><BR>
            <select name="x_char">
              <option value=""$x_none_char></option>
              <option value="char"$x_char_char>character</option>
              <option value="dec"$x_dec_char>decimal</option>
              <option value="hex"$x_hex_char>hexidecimal</option>
            </select><BR>
            <select name="y_char">
              <option value=""$y_none_char></option>
              <option value="char"$y_char_char>character</option>
              <option value="dec"$y_dec_char>decimal</option>
              <option value="hex"$y_hex_char>hexidecimal</option>
            </select><BR>
          </TD>
        <TR>
      </TABLE>
    </TD>
    <TD width="50">
    </TD>
    <TD VALIGN="TOP" width="300">
      <DIV ALIGN="CENTER"><B>Output:</B><BR>
      <TEXTAREA ID=Textbox SIZE=20 ROWS=5 value=""></TEXTAREA></DIV><BR>
      <SMALL>These characters represent the output of the fuzzer function XSS_ME(). They are probably vulnerable (and are not necessarily in order).</SMALL>
    </TD>
  <TR>
</TABLE>
<SCRIPT LANGUAGE=JavaScript>
function XSS_ME(XSS) {
    var a = document.getElementById("Textbox").value + XSS + "\\n";
    document.getElementById("Textbox").value = a;
}
</SCRIPT>
</DIV>
<BR>Switch encoding method from $charset:
<select name="encoding">
EOHTML
foreach (@encoding) {
  if ($_ eq $charset) {
    print "<option value=\"$_\" selected>$_</option>\n";
  } else {
    print "<option value=\"$_\">$_</option>\n";
  }
}
print "</select>\n";
if ($enc_not_found) {
  print "<BR><SMALL>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<FONT COLOR=\"FF0000\"><B>Note:</B> $enc_not_found</FONT></SMALL>";
}
print "<BR><B>Optional</B> character range to test (IE: 0 - 13): ";
$bottom = $in{'bottom'};
$top = $in{'top'};
print "<input type=text value=\"$bottom\" name=\"bottom\" size=\"7\"> - \n";
print "<input type=text value=\"$top\" name=\"top\" size=\"7\"><BR>\n";
print "<SMALL>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<B>Note:</B> if range is left blank it will default to: ";
foreach (@default_ranges) {
  print "$_ ";
}
print "</SMALL><BR><input type=\"submit\" value=\"Submit\"></FORM>\n";
print "</DIV>\n<BR>\n<HR>\n";

if ($ENV{'QUERY_STRING'} eq "start") {
  if ((($in{'bottom'}) || ($in{'bottom'} == 0)) && ($in{'top'})) {
    foreach $num ($in{'bottom'} .. $in{'top'}) {
      printf ("%s", $v);
      if ($in{'v_char'} eq "char") {
        printf ("%c", $num);
      } elsif ($in{'v_char'} eq "dec") {
        printf ("%d", $num);
      } elsif ($in{'v_char'} eq "hex") {
        printf ("%x", $num);
      }
      printf ("%s", $w);
      if ($in{'w_char'} eq "char") {
        printf ("%d", $num);
      } elsif ($in{'w_char'} eq "dec") {
        printf ("%d", $num);
      } elsif ($in{'w_char'} eq "hex") {
        printf ("%x", $num);
      }
      printf ("%s", $x);
      if ($in{'x_char'} eq "char") {
        printf ("%d", $num);
      } elsif ($in{'x_char'} eq "dec") {
        printf ("%d", $num);
      } elsif ($in{'x_char'} eq "hex") {
        printf ("%x", $num);
      }
      printf ("%s", $y);
      if ($in{'y_char'} eq "char") {
        printf ("%d", $num);
      } elsif ($in{'y_char'} eq "dec") {
        printf ("%d", $num);
      } elsif ($in{'y_char'} eq "hex") {
        printf ("%x", $num);
      }
      printf ("%s<BR>\n", $z);
    }
  } else {
    foreach (@default_ranges) {
      @range = split(/-/, $_);
      foreach $b ($range[0] .. $range[1]){
        printf ("%s", $v);
        if ($in{'v_char'} eq "char") {
          printf ("%c", $b);
        } elsif ($in{'v_char'} eq "dec") {
          printf ("%d", $b);
        } elsif ($in{'v_char'} eq "hex") {
          printf ("%x", $b);
        }
        printf ("%s", $w);
        if ($in{'w_char'} eq "char") {
          printf ("%c", $b);
        } elsif ($in{'w_char'} eq "dec") {
          printf ("%d", $b);
        } elsif ($in{'w_char'} eq "hex") {
          printf ("%x", $b);
        }
        printf ("%s", $x);
        if ($in{'x_char'} eq "char") {
          printf ("%c", $b);
        } elsif ($in{'x_char'} eq "dec") {
          printf ("%d", $b);
        } elsif ($in{'x_char'} eq "hex") {
          printf ("%x", $b);
        }
        printf ("%s", $y);
        if ($in{'y_char'} eq "char") {
          printf ("%c", $b);
        } elsif ($in{'y_char'} eq "dec") {
          printf ("%d", $b);
        } elsif ($in{'y_char'} eq "hex") {
          printf ("%x", $b);
        }
        printf ("%s<BR>\n", $z);
      } 
    }
  }
}

print "\n</BODY>\n</HTML>\n";
