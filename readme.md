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

#### interfaces fot eth0 to subnet wlan0 bridged with eth1
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
iwconfig				# check transmit power
iwconfig wlan0 txpower 10mW		# set transmit power
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

## nordvpn linux
```bash
sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)	# install
nordvpn login 		# login
nordvpn status 		# show status
nordvpn settings 	# show settings
nordvpn c 		# to connect
nordvpn whitelist add subnet 192.168.0.0/16 	# whitlist subnet
sysctl -w net.ipv6.conf.all.disable_ipv6=1	# disable ipv6
sysctl -w net.ipv6.conf.default.disable_ipv6=1
sysctl -w net.ipv6.conf.tun0.disable_ipv6=1
```

## sudo apt-get install screen
to launche screen on boot add this to `~/.bash_profile`
```bash
if  [ -z $STY ] && [ $TERM != "screen" ]; then
/usr/bin/screen -xRR;
else
/usr/bin/screen -X hardstatus alwayslastline '[%H] %Lw%=%u %d.%m.%y %c '
fi
```
```bash
screen -ls 	# list screens<br>
screen -d 	# detach from screen<br>
screen -r	# resume attache to screen<br>
exit 		# close screen window<br>
Strg a c	# new screen window<br>
Strg a ESC 	# enter scroll mode 'Strg u d' up down<br>
Strg a SPACE 	# cycle screen windows<br>
Strg a | 	# vertical split<br>
Strg a TAB 	# move between splits<br>
Strg a :remove 	# to remove split<br>
```

# [homebridge](https://github.com/homebridge/homebridge/wiki/Install-Homebridge-on-Raspbian)
```bash
nano /etc/environment 		# append privates=/path/to/private/ with /paht/to/private/privates.py
sudo homebridge -D -U /path/to/ 	# with path/to/config.js to start hb manually
```
#### hb service configuration
```bash
nano /etc/default/homebridge 	# append privates=/path/to/private/ 
				# set HOMEBRIDGE_OPTS=-D -U "/path/to" and UIX_STORAGE_PATH="/path/to" with path/to/config.js

nano /etc/systemd/system/homebridge.service 	# change user to root to run hb as root
nano /etc/default/homebridge 			# HOMEBRIDGE_OPTS=-D -U "/path/to/config" --allow-root
```

#### to choose network intervace `/var/lib/homerbidge/config.json`<br>
```json
{
	"mdns": {"intervace": "ip-of-interface"},
	"bridge": {
		"name": "...",
		"username": "...",
		"port": ...,
		"pin": "..."
```
#### camera ffmpeg plugin
```bash
cp -f usr/bin/ffmpeg /usr/lib/node_modules/homebridge-camera-ffmpeg/node_modules/ffmpeg-for-homebridge/ffmpeg
	# replace ffmpeg bundled with plugin with ffmpeg bundled with rasbian full img
```
```json
"_comment": "to capture desktop when booting to desktop use this in config",
"source": "-f x11grab -r 10 -video_size 1280x720 -i :0.0",
"stillImageSource": "-f x11grab -t 1 -video_size 1280x720 -i :0.0 -vframes 1",

"_comment": "to capture cli when booting to cli use this in config",
"source": "-f fbdev -framerate 15 -i /dev/fb0"
"stillimageSource": "-f fbdev -i /dev/fb0 -t 1 -vframes 1"
```

## usefull others
```bash
pinout 		# prints rpis pinout __ACHTUNG__ diff between gpioNr. and board pinNr
ifconfig 	# list interfaces
vcgencmd measure_temp	# return fantemp
```
[shairport sync](https://github.com/mikebrady/shairport-sync/tree/development)

#### python to control fan
```python
import RPi.GPIO as GPIO
fan = 8
GPIO.setmode(GPIO.BOARD)
GPIO.output(fan, 1)
GPIO.cleanup()
```

#### python to read mcp3008
```python
mport os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)

print('Raw ADC Value: ', chan0.value)
print('ADC Voltage: ' + str(chan0.voltage) + 'V')

while True:
    print('Raw ADC Value: ', chan0.value)

    # hang out and do nothing for a half second
    time.sleep(0.2)
```

#### python to gert cpu temp
```pyhton
from gpiozero import CPUTemperature

cpu = CPUTemperature()
print(round(cpu.temperature))
```
