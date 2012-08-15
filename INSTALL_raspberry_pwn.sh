#!/bin/bash

###
### Raspberry Pwn 0.1 : A Raspberry Pi Pentesting suite by Pwnie Express
### pwnieexpress.com
### Installer Revision 08.14.2012
###

echo ""

# Verify we are root
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root" 1>&2
  exit 1
fi

# Verify Raspberry Pwn 0.1 is not already installed
if [ "`grep -o 0.1 /etc/motd.tail`" == "0.1" ] ; then 
  echo "[-] Raspberry Pwn 0.1 already installed. Please install on a fresh wheezy system..."
  exit 1
fi

# Verify Raspberry Pwn 0.2 is not already installed
if [ "`grep -o 0.2 /etc/motd.tail`" == "0.2" ] ; then 
  echo "[-] Raspberry Pwn 0.2 already installed. Aborting..."
  exit 1
fi

# If we can't detect version, warn the user
if ! [ -f /etc/motd.tail ]; then
  echo "Unable to detect version"
  echo "Press ENTER to continue, CTRL+C to abort."
  read INPUT
fi

echo "  _____      ___  _ ___ ___   _____  _____ ___ ___ ___ ___      "
echo " | _ \ \    / / \| |_ _| __| | __\ \/ / _ \ _ \ __/ __/ __|     "
echo " |  _/\ \/\/ /| .\ || || _|  | _| >  <|  _/   / _|\__ \__ \    "
echo " |_|   \_/\_/ |_|\_|___|___| |___/_/\_\_| |_|_\___|___/___/     "
echo ""
echo "              === Raspberry Pwn Release 0.2 ===                 "
echo "     A Raspberry Pi Pentesting suite by PwnieExpress.com        "
echo ""
echo "----------------------------------------------------------------"
echo " This installer will load a comprehensive security pentesting   "
echo " software suite onto your Raspberry Pi. Note that the Debian    "
echo " Raspberry Pi distribution must be installed onto the SD card   "
echo " before proceeding. See README.txt for more information.       "
echo ""
echo "Press ENTER to continue, CTRL+C to abort."
read INPUT
echo ""

# Make sure all installer files are owned by root
chown -R root:root .

# Update sources.list to include the main debian repos too
rm /etc/apt/sources.list
echo "deb http://archive.raspbian.org/raspbian wheezy main contrib non-free rpi" >> /etc/apt/sources.list
echo "deb-src http://archive.raspbian.org/raspbian wheezy main contrib non-free rpi" >> /etc/apt/sources.list
echo "deb http://ftp.debian.org/debian/ wheezy main contrib non-free" >> /etc/apt/sources.list

# Update base debian packages
echo "[+] Updating base system Debian packages..."
apt-get -y update
#apt-get -y upgrade
echo "[+] Base system Debian packages updated."

# Install baseline pentesting tools via apt
echo "[+] Installing baseline pentesting tools/dependencies..."
apt-get -y install git-core build-essential perl-base python
apt-get -y install ruby irb ri rubygems libruby ruby-dev libpcap-dev
apt-get -y install telnet btscanner libnet-dns-perl hostapd nmap dsniff netcat nikto 
apt-get -y install xprobe python-scapy wireshark tcpdump ettercap-text-only hping3 medusa macchanger 
apt-get -y install nbtscan john ptunnel p0f ngrep tcpflow openvpn iodine httptunnel cryptcat 
apt-get -y install sipsak yersinia smbclient sslsniff tcptraceroute pbnj netdiscover netmask 
apt-get -y install udptunnel dnstracer sslscan medusa ipcalc dnswalk socat onesixtyone tinyproxy
apt-get -y install dmitry fcrackzip ssldump fping ike-scan gpsd darkstat swaks arping tcpreplay 
apt-get -y install sipcrack proxychains proxytunnel siege sqlmap wapiti skipfish libssl-dev 
apt-get -y install libpcap-dev libpcre3 libpcre3-dev libnl-dev libncurses5-dev subversion 
apt-get -y install python-twisted-web python-pymssql
echo "[+] Baseline pentesting tools installed."

# Remove unneeded statup items
echo "[+] Remove unneeded startup items..."
update-rc.d -f gpsd remove
update-rc.d -f tinyproxy remove
update-rc.d -f ntp remove
apt-get -y purge portmap
apt-get -y autoremove
echo "[+] Unneeded startup items removed."

# Install wireless pentesting tools
echo "[+] Installing wireless pentesting tools..."
apt-get -y install kismet

# Currently broken on Raspian
#cd src/aircrack-ng-1.1
#chmod +x evalrev
#make install
#cd ../..

echo "[+] Wireless pentesting tools installed."

# Install Metasploit -- Note this will require changing the default RAM allocation 
echo "[+] Installing latest Metasploit Framework..."
mkdir /opt/metasploit
cd /opt/metasploit
git clone https://github.com/pwnieexpress/metasploit-framework.git msf3
ln -sf /opt/metasploit/msf3/msf* /usr/local/bin/
echo "[+] Latest Metasploit Framework installed."

# Install Perl/Python tools to /pentest
echo "[+] Installing Perl/Python tools to /pentest..."
mv src/pentest/ /
chown -R root:root /pentest/
chmod +x /pentest/cisco-auditing-tool/CAT
chmod +x /pentest/easy-creds/easy-creds.sh
chmod +x /pentest/goohost/goohost.sh
chmod +x /pentest/lbd/lbd.sh
chmod +x /pentest/sslstrip/sslstrip.py
echo "[+] Perl/Python tools installed in /pentest."

# Install SET
echo "[+] Installing latest SET framework to /pentest..."
svn co http://svn.secmaniac.com/social_engineering_toolkit /pentest/set/
cd src/pexpect-2.3/
python setup.py install
cd ../..
echo "[+] SET framework installed in /pentest."

# Update motd to show Raspberry Pwn release
cp src/motd.tail.raspberrypwn /etc/motd.tail

# Install Exploit-DB - removed to save space
#echo "[+] Installing Exploit-DB to /pentest..."
#svn co svn://www.exploit-db.com/exploitdb /pentest/exploitdb/
#echo "[+] Exploit-DB installed in /pentest."

echo "[+] Setting default RAM allocation"
cp /boot/arm224_start.elf /boot/start.elf

# Remove the debian sources from the apt sources.list - prevents problems w/ the apt package itself
rm /etc/apt/sources.list
echo "deb http://archive.raspbian.org/raspbian wheezy main contrib non-free rpi" >> /etc/apt/sources.list
echo "deb-src http://archive.raspbian.org/raspbian wheezy main contrib non-free rpi" >> /etc/apt/sources.list

echo ""
echo "---------------------------------------------------------------"
echo "Raspberry Pwn Release 0.2 installed successfully!"
echo "---------------------------------------------------------------"
echo ""


echo "[+] In order for the new RAM allocation to take effect, we must"
echo "[+] now reboot the pi. Press [Ctrl-C] to exit without rebooting."
echo ""
read
reboot

