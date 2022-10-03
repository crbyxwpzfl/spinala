```
strg k #github spotlight
```

```
. #vs code in browser
alt #toggle menue bar
crtl shit g #source controll
crtl shift e #explorer
```

## switch to systemd networkd
```bash
~ $ sudo -Es
apt --autoremove purge ifupdown		# deinstall classic networking that is managed with file /etc/network/interfaces
rm -r /etc/network
apt --autoremove purge dhcpcd5		# deinstall default raspbian dhcpcd network management Hold programs
apt --autoremove purge isc-dhcp-client isc-dhcp-common
rm -r /etc/dhcp
apt --autoremove purge rsyslog
apt-mark hold ifupdown dhcpcd5 isc-dhcp-client isc-dhcp-common rsyslog raspberrypi-net-mods openresolv	# hold stuff
systemctl enable systemd-networkd.service	# enable systemd service
systemctl enable systemd-resolved.service	# then enable systemd-resolved
systemctl status dbus.service			# check D-Bus software interface
apt --autoremove purge avahi-daemon		# configure NSS software interface
apt-mark hold avahi-daemon
apt install libnss-resolve			# install the systemd-resolved software interface.
ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf	# configure DNS stub listener interface
```

### interfaces fot eth0 to subnet wlan0 bridged with eth1
`# cat > /etc/systemd/network/04-eth0.network <<EOF`
```editorconfig
[Match]
Name=eth0

[Network]
MulticastDNS=yes
DHCP=yes
```
`# cat > /etc/systemd/network/02-br0.netdev <<EOF`
```editorconfig
[NetDev]
Name=br0
Kind=bridge
```
`# cat > /etc/systemd/network/10-eth1.network <<EOF`
```editorconfig
[Match]
Name=eth1

[Network]
MulticastDNS=yes
Bridge=br0
```
`# cat > /etc/systemd/network/16-br0_up.network <<EOF`
```editorconfig
[Match]
Name=br0
[Network]
Address=192.168.2.1/24
MulticastDNS=yes
#IPMasquerade is doing NAT
IPMasquerade=yes
DHCPServer=yes
[DHCPServer]
DNS=1.1.1.1 8.8.8.8
```

#### install hostpad
```
~ $ sudo -Es
systemctl disable wpa_supplicant.service
apt update
apt full-upgrade
apt install hostapd
systemctl stop hostapd.service
```
`# cat >/etc/hostapd/hostapd.conf <<EOF`
```editorconfig
interface=wlan0		# interface and driver
bridge=br0
driver=nl80211

country_code=DE		# country setup
ieee80211d=1

hw_mode=a		# a-5ghz g-2.4ghz !!hostapd does not like inline comments here
channel=48		# 0-hostapd chooses channel is broken 36 40 44 48 are working to see avalible channels $ iwlist wlan0 channel

ssid=zimmer
ignore_broadcast_ssid=0		# 0-open 1-empty 2-empty but correct lenght ssid advertising

ieee80211n=1		# draft-n mode
wmm_enabled=1

max_num_sta=20		# max client count

auth_algs=1		# 1-open 2-WEP 3-both
wpa=2			# 1-WPA 2-WPA2 3-both
wpa_passphrase=homesharing
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP	# offer wpa2 encryption
```
```bash
~ $ sudo -Es
chmod 600 /etc/hostapd/hostapd.conf	# set accessrights
sed -i 's/^#DAEMON_CONF=.*$/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf"/' /etc/default/hostapd 	# set config file
systemctl reboot
```

#### others
```bash
~ $ sudo -ES
systemctl status hostapd		# start stop restart enable unmask status
rfkill unblock wlan			# never sleep wifi module
systemd-resolve --status wlan0		# check multicast dns
systemd-resolve --set-mdns=yes --interface=wlan0	# allow mdns
iw dev wlan0 info				# check transmit power
iw dev welan0 set txpower limit 100		# set transmit power
/usr/sbin/hostapd /etc/hostapd/hostapd.conf	# test manually for errors
```

## instal librarys for mcp3008
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip
sudo pip3 install --upgrade setuptools
cd ~
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
sudo pip3 install adafruit-circuitpython-mcp3xxx
```

## ssh
```bash
nano ~/etc/ssh/sshd_config 	# disable PasswordAuth and enable keypassAuth
cd home/pi/.ssh/authorized_keys 	# add openssh public here 
```

## [nordvpn linux](https://support.nordvpn.com/Connectivity/Linux/1325531132/Installing-and-using-NordVPN-on-Debian-Ubuntu-Raspberry-Pi-Elementary-OS-and-Linux-Mint.htm)
```bash
sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)	# install
nordvpn login 		# login
nordvpn status 		# show status
nordvpn settings 	# show settings
nordvpn c 		# to connect
nordvpn countries # list countries 

nordvpn whitelist add subnet 192.168.0.0/16 	# whitlist subnet

sysctl -w net.ipv6.conf.all.disable_ipv6=1	# disable ipv6
sysctl -w net.ipv6.conf.default.disable_ipv6=1
sysctl -w net.ipv6.conf.tun0.disable_ipv6=1

sudo apt-get update	# update nordvpn
sudo apt-get upgrade
sudo apt-get install nordvpn
```

## switch hostname
```sh
sudo raspi-config # network hostname then reboot
```

## switch username
```sh
sudo passwd  # root pw to lgoin later
sudo nano /etc/ssh/sshd_config  # edit ssh so permitrootlogin, PasswordAuthentication, ChallengeResponseAuthentication is yes
sudo service ssh restart
# lgin as root
usermod -l userneme pi #  first new name then old name default pi
usermod -m -d /home/username username #  rename home dir
# login with new user theretically no reboot
sudo passwd -l root #  perhaps lock root user again
```
