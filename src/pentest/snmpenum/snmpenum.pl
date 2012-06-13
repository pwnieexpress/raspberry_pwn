#! /usr/local/bin/perl -w
#
# Simple Perl script to enumerate information on Machines that are running SNMP
#
#        ----by filip waeytens 2003----
#        ----  DA SCANIT CREW www.scanit.be ----
#         filip.waeytens@hushmail.com
#
# Use it but don't abuse it. Read readme file.
# If you don't get all the output, the MIBS are probably not supported
# or the box only supports SNMPv1
#
# For Cisco: check this at
# http://www.cisco.com/public/sw-center/netmgmt/cmtk/mibs.shtml
#
# It's easy to add stuff, it's pretty straightforward.
# snmp stuff was taken from CPAN example :)
#
################################################################################

use strict;
use Fcntl;
use Net::SNMP qw(:snmp);

#declare global variables

my ($result,$v,$k);
my %request;

#usage

if (@ARGV!=3){
     print "Usage: perl enum.pl <IP-address> <community> <configfile>\n\n";
     exit 1;
}

#opening the config
my $config=$ARGV[2];
sysopen(CONFIG,$config, O_RDONLY)
    or die "Couldn't open file for reading: $!\n";

#assigning the hash

while (<CONFIG>){
        chomp $_;
        my @system= split /\t+/,$_;
        $request{$system[1]}=$system[2];
        }

#establishing the snmp session
#V2 needed for snmpbulkrequests

   my ($session, $error) = Net::SNMP->session(
      -version     => 'snmpv2c',
      -nonblocking => 1,
      -hostname    => shift || '@ARGV[0]',
      -community   => shift || '@ARGV[1]',
   );

#error message

   if (!defined($session)) {
      printf("ERROR: %s.\n", $error);
      exit 1;
   }

#handling each request and printing request headers

   while ( ($k,$v) = each %request ) {

   print "\n\n"."-"x40 ."\n\t$k\n"."-"x40 ."\n\n";


   my $result = $session->get_bulk_request(
      -callback       => [\&table_cb, {}],
      -maxrepetitions => 10,
      -varbindlist    => [$v]
   );

   if (!defined($result)) {
      printf("ERROR: %s.\n", $session->error);
      $session->close;
      exit 1;
   }

   snmp_dispatcher();
   }
   $session->close;

   exit 0;

#subroutine for snmp getbulk stuff - taken from CPAN

   sub table_cb
   {
      my ($session, $table) = @_;

      if (!defined($session->var_bind_list)) {

         printf("ERROR: %s\n", $session->error);

      } else {

         my $next;

         foreach my $oid (oid_lex_sort(keys(%{$session->var_bind_list}))) {
            if (!oid_base_match($v, $oid)) {
               $next = undef;
               last;
            }
            $next = $oid;
            $table->{$oid} = $session->var_bind_list->{$oid};
         }

         if (defined($next)) {

            $result = $session->get_bulk_request(
               -callback       => [\&table_cb, $table],
               -maxrepetitions => 10,
               -varbindlist    => [$next]
            );

            if (!defined($result)) {
               printf("ERROR: %s\n", $session->error);
            }

         } else {

            foreach my $oid (oid_lex_sort(keys(%{$table}))) {
                         printf("%s\n",$table->{$oid});
            }

         }
      }
   }