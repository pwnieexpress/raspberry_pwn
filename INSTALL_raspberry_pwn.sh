#!/bin/bash
# Raspberry Pwn 0.3 : A Raspberry Pi Pentesting suite by Pwnie Express
# pwnieexpress.com
# Installer Revision 11.7.2014

echo ""

# Verify we are root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Verify Raspberry Pwn 0.3 is not already installed
if [ "`grep -o 0.3 /etc/motd.tail`" == "0.3" ] ; then 
        echo "[-] Raspberry Pwn 0.3 already installed. Aborting..."
        exit 1
fi


echo "  _____      ___  _ ___ ___   _____  _____ ___ ___ ___ ___      "
echo " | _ \ \    / / \| |_ _| __| | __\ \/ / _ \ _ \ __/ __/ __|     "
echo " |  _/\ \/\/ /| .\` || || _|  | _| >  <|  _/   / _|\__ \__ \    "
echo " |_|   \_/\_/ |_|\_|___|___| |___/_/\_\_| |_|_\___|___/___/     "
echo ""
echo "              === Raspberry Pwn Release 0.3 ===                 "
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
#commenting this out... don't need it!
#echo "deb http://ftp.debian.org/debian/ squeeze main contrib non-free" > /etc/apt/sources.list
aptitude -y update
aptitude -y upgrade
echo "[+] Base system Debian packages updated."

# Install baseline pentesting tools via aptitude
echo "[+] Installing baseline pentesting tools/dependencies..."
aptitude -y install telnet btscanner libnet-dns-perl hostapd nmap dsniff netcat nikto xprobe python-scapy wireshark tcpdump ettercap-graphical hping3 medusa macchanger nbtscan john ptunnel p0f ngrep tcpflow openvpn iodine httptunnel cryptcat sipsak yersinia smbclient sslsniff tcptraceroute pbnj netdiscover netmask udptunnel dnstracer sslscan medusa ipcalc dnswalk socat onesixtyone tinyproxy dmitry fcrackzip ssldump fping ike-scan gpsd darkstat swaks arping tcpreplay sipcrack proxychains proxytunnel siege sqlmap wapiti skipfish w3af libssl-dev libpcap-dev libpcre3 libpcre3-dev libnl-dev libncurses-dev subversion python-twisted-web python-pymssql iw mc zip links w3m lynx arj dbview odt2txt gv catdvi djvulibre-bin python-boto python-tz

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
cd src/aircrack-ng-1.2-rc1
chmod +x evalrev
make install
cd ../..
echo "[+] Wireless pentesting tools installed."

# Install Metasploit -- Note this will require changing the default RAM allocation 
echo "[+] Installing latest Metasploit Framework..."
aptitude -y install ruby irb ri rubygems libruby ruby-dev libpcap-dev
mkdir /opt/metasploit
wget http://downloads.metasploit.com/data/releases/framework-latest.tar.bz2
tar jxvf framework-latest.tar.bz2 -C /opt/metasploit
ln -sf /opt/metasploit/msf3/msf* /usr/local/bin/
echo "[+] Latest Metasploit Framework installed."

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
git clone https://github.com/trustedsec/social-engineer-toolkit/ /pentest/set/
cd src/pexpect-2.3/
python setup.py install
cd ../..
echo "[+] SET framework installed in /pentest."

# Update motd to show Raspberry Pwn release
cp src/motd.tail.raspberrypwn /etc/motd.tail
# Update motd for pi user to show Raspberry Pwn release
cp src/motd.tail.raspberrypwn /etc/motd

# Install Exploit-DB
echo "[+] Installing Exploit-DB to /pentest..."
mkdir -p /pentest/exploitdb
cd /pentest/exploitdb/
wget  http://www.exploit-db.com/archive.tar.bz2
tar -xjvf archive.tar.bz2 
echo "[+] Exploit-DB installed in /pentest."

echo "[+] Setting default RAM allocation (disabled!)"
echo "[!] If your RPi board only has 256MB ram please set split to"
echo "    224/32 using raspi-config."
#cp /boot/arm224_start.elf /boot/start.elf

echo ""
echo "---------------------------------------------------------------"
echo "Raspberry Pwn Release 0.3 installed successfully!"
echo "---------------------------------------------------------------"
echo ""


echo "[+] In order for the new RAM allocation to take effect, we must"
echo "[+] now reboot the pi. Press [Ctrl-C] to exit without rebooting."
echo ""
read
reboot

