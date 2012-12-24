 ```
 _____      ___  _ ___ ___   _____  _____ ___ ___ ___ ___
 | _ \ \    / / \| |_ _| __| | __\ \/ / _ \ _ \ __/ __/ __|
 |  _/\ \/\/ /| .` || || _|  | _| >  <|  _/   / _|\__ \__ \
 |_|   \_/\_/ |_|\_|___|___| |___/_/\_\_| |_|_\___|___/___/
```

 Raspberry Pwn : A Raspberry Pi pentesting suite by Pwnie Express (pwnieexpress.com)
 
 Release 0.2 (December 2012)

----------------------------------------------
Legal Stuff
----------------------------------------------

This software is provided free of charge under the GNU Public License (http://www.gnu.org/licenses/gpl.html). 

As with any software application, downloads/transfers of this software is subject to export controls under the U.S. Commerce Department's Export Administration Regulations (EAR). By using this software you certify your complete understanding of and compliance with these regulations.

All Pwnie Express products/releases are for legally authorized uses only. Under NO circumstances is Pwnie Express, Rapid Focus Security, or any of its affiliates, tradenames, or subsidiaries liable for any damage, loss of data, or misuse resulting from the use of this software.

----------------------------------------------
Important
----------------------------------------------
* Raspberry Pwn is built on DEBIAN - not RASPBIAN - and will not work on RASPBIAN images!! This install guide was tested with the "Soft-float Debian Wheezy" build and works as expected.

----------------------------------------------
What you will need
----------------------------------------------

1. A stock Raspberry Pi board (http://www.raspberrypi.org/)
2. The Debian (not Raspbian) Raspberry Pi distribution. The Debian build is regularly updated,
   so look at http://www.raspberrypi.org/downloads for the latest download.
3. An SD card of at least 4GB in size
4. SSH/console access to the Raspberry Pi
5. Internet access from the Raspberry Pi

----------------------------------------------
Installation Steps
----------------------------------------------

1. Follow the steps on http://www.raspberrypi.org/downloads to image your SD card. Don't forget to perform, at least, the following steps through the post-installation wizard :
  1. extend the root partition to utilize the whole SD card.
  1. enable the SSH server

2. ssh into your Raspberry Pi :

```
ssh pi@[ip address of your Raspberry Pi]
```

  the default password for the 'pi' user is 'raspberry'. With ssh enabled you might want to change that.

3. change your default password :

```
passwd
```

1. Change to the root user:

```
$ sudo -i
```

3. Confirm you have internet access from your Raspberry Pi :

```
ping google.com
```

4. update your apt :

```
apt-get update
```

5. Install git:

```
apt-get install git
```

6. Download the Raspberry Pwn installer from the Pwnie Express Github repository:

```
git clone https://github.com/pwnieexpress/Raspberry-Pwn.git
```

7. CD into the Raspberry-Pwn folder and run the install script:

```
cd Raspberry-Pwn
./INSTALL_raspberry_pwn.sh
```

[optional]

8. Install a wireless adapter :

  if you want to install a wireless adapter, follow this guide :
  http://www.raspberrypi-tutorials.co.uk/set-raspberry-pi-wireless-network/

----------------------------------------------
Known Issues
----------------------------------------------

Raspberry Pwn is NOT compatible with the Hard-float (armhf) Raspbian images.

----------------------------------------------
Support
----------------------------------------------

Feature requests / bug reports:
https://github.com/pwnieexpress/Raspberry-Pwn/issues

Community Support Forum:
http://forum.pwnieexpress.com

----------------------------------------------
Thanks!
----------------------------------------------
Special thanks to those contributors that have helped with the project:

* alecthegeek
* g13net
* Wim Remes
