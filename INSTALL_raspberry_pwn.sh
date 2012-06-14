#!/bin/bash
# Raspberry Pwn 0.1 : A Raspberry Pi Pentesting suite by Pwnie Express
# pwnieexpress.com
# Installer Revision 6.12.2012

echo ""

# Verify we are root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Verify Raspberry Pwn 0.1 is not already installed
if [ "`grep -o 0.1 /etc/motd.tail`" == "0.1" ] ; then 
        echo "[-] Raspberry Pwn 0.1 already installed. Aborting..."
        exit 1
fi


echo "  _____      ___  _ ___ ___   _____  _____ ___ ___ ___ ___      "
echo " | _ \ \    / / \| |_ _| __| | __\ \/ / _ \ _ \ __/ __/ __|     "
echo " |  _/\ \/\/ /| .\` || || _|  | _| >  <|  _/   / _|\__ \__ \    "
echo " |_|   \_/\_/ |_|\_|___|___| |___/_/\_\_| |_|_\___|___/___/     "
echo ""
echo "              === Raspberry Pwn Release 0.1 ===                 "
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

# Update base debian packages
echo "[+] Updating base system Debian packages..."
echo "deb http://ftp.debian.org/debian/ squeeze main contrib non-free" > /etc/apt/sources.list
aptitude -y update
aptitude -y upgrade
echo "[+] Base system Debian packages updated."

# Install baseline pentesting tools via aptitude
echo "[+] Installing baseline pentesting tools/dependencies..."
aptitude -y install hostapd nmap dsniff netcat nikto xprobe python-scapy wireshark tcpdump ettercap hping3 medusa macchanger nbtscan john ptunnel p0f ngrep tcpflow openvpn iodine httptunnel cryptcat sipsak yersinia smbclient sslsniff tcptraceroute pbnj netdiscover netmask udptunnel dnstracer sslscan medusa ipcalc dnswalk socat onesixtyone tinyproxy dmitry fcrackzip ssldump fping ike-scan gpsd darkstat swaks arping tcpreplay sipcrack proxychains proxytunnel siege sqlmap wapiti skipfish w3af libssl-dev libpcap-dev libpcre3 libpcre3-dev libnl-dev libncurses-dev subversion python-twisted-web python-pymssql
echo "[+] Baseline pentesting tools installed."

# Remove unneeded statup items
echo "[+] Remove unneeded startup items..."
update-rc.d -f gpsd remove
update-rc.d -f tinyproxy remove
update-rc.d -f ntp remove
apt-get -y purge portmap
apt-get -y autoremove gdm
apt-get -y autoremove
echo "[+] Unneeded startup items removed."

# Install wireless pentesting tools
echo "[+] Installing wireless pentesting tools..."
aptitude -y install kismet
cd src/aircrack-ng-1.1
chmod +x evalrev
make install
cd ../..
echo "[+] Wireless pentesting tools installed."

# Install Metasploit -- Removed for now. Not enough memory to run on Pi
#echo "[+] Installing latest Metasploit Framework..."
#aptitude -y install ruby irb ri rubygems libruby ruby-dev libpcap-dev
#mkdir /opt/metasploit
#cd /opt/metasploit
#wget http://downloads.metasploit.com/data/releases/framework-latest.tar.bz2
#tar jxvf framework-latest.tar.bz2
#ln -sf /opt/metasploit/msf3/msf* /usr/local/bin/
#echo "[+] Latest Metasploit Framework installed."

# Install Perl/Python tools to /pentest
echo "[+] Installing Perl/Python tools to /pentest..."
cp -a src/pentest/ /
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

echo ""
echo "---------------------------------------------------------------"
echo "Raspberry Pwn Release 0.1 installed successfully!"
echo "---------------------------------------------------------------"
echo ""
exit 1
