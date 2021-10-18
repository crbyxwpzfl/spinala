## eth0 into subnet on wlan0 and eth1
Deinstall classic networking that is managed with file `/etc/network/interfaces` and deinstall default Raspbian `dhcpcd network management. Hold programs.
```
# apt --autoremove purge ifupdown`
# rm -r /etc/network`
# apt --autoremove purge dhcpcd5`
# apt --autoremove purge isc-dhcp-client isc-dhcp-common`
# rm -r /etc/dhcp`
# apt --autoremove purge rsyslog`
# apt-mark hold ifupdown dhcpcd5 isc-dhcp-client isc-dhcp-common rsyslog raspberrypi-net-mods openresolv`
```
enable systemd-networkd.
`systemctl enable systemd-networkd.service`

then enable systemd-resolved.
`systemctl enable systemd-resolved.service`

check D-Bus software interface.
`systemctl status dbus.service`

Configure NSS software interface.
`apt --autoremove purge avahi-daemon`
`apt-mark hold avahi-daemon`

install the systemd-resolved software interface.
`apt install libnss-resolve`

configure DNS stub listener interface
`ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf`

#### eth0 interface
```
# cat > /etc/systemd/network/04-eth0.network <<EOF
[Match]
Name=eth0

[Network]
DHCP=yes

EOF
```

#### eth1 interface
```
# cat > /etc/systemd/network/10-eth1.network <<EOF
[Match]
Name=eth1

[Network]
Address=192.168.2.1/24
MulticastDNS=yes
#IPMasquerade is doing NAT
IPMasquerade=yes
DHCPServer=yes

[DHCPServer]
DNS=1.1.1.1 8.8.8.8

EOF
```

#### wlan0 interface
```
# cat > /etc/systemd/network/08-wlan0.network <<EOF
[Match]
Name=wlan0

[Network]
Address=192.168.3.1/24
MulticastDNS=yes
#IPMasquerade is doing NAT
IPMasquerade=yes
DHCPServer=yes

[DHCPServer]
DNS=1.1.1.1 8.8.8.8

EOF
```

#### install hostpad
```
$ sudo -Es
# systemctl disable wpa_supplicant.service
# apt update
# apt full-upgrade
# apt install hostapd
# systemctl stop hostapd.service
```

configure the access point host software hostapd with this file.
```
# cat >/etc/hostapd/hostapd.conf <<EOF
interface=wlan0
driver=nl80211
ssid=MyTestAP
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=VerySecretPw
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF
```

`# chmod 600 /etc/hostapd/hostapd.conf`

set DAEMON_CONF="/etc/hostapd/hostapd.conf" in /etc/default/hostapd with
```
# sed -i 's/^#DAEMON_CONF=.*$/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf"/' /etc/default/hostapd
# systemctl reboot
```

trouble shooting
```
# systemctl status hostapd
# systemctl unmask hostapd
# systemctl enable hostapd
# systemctl start hostapd
# rfkill unblock wlan
```

## raspberry pi inital setup
`pinout` prints rpis pinout __ACHTUNG__ diff between gpioNr. and board pinNr.<br>
`ifconfig` list interfaces<br>
`read temp: vcgencmd measure_temp` return fantemp<br>
<br>
ssh disable PasswordAuth in `~/etc/ssh/sshd_config`<br>
ssh enable keypassAuth<br>
add openssh public to `home/pi/.ssh/authorized_keys`<br>

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


## shairport sync
[shairport sync](https://github.com/mikebrady/shairport-sync/tree/development)

## sudo apt-get install screen
to launche screen on boot add this to `~/.bash_profile`
```bash
if  [ -z $STY ] && [ $TERM != "screen" ]; then
/usr/bin/screen -xRR;
else
/usr/bin/screen -X hardstatus alwayslastline '[%H] %Lw%=%u %d.%m.%y %c '
fi
```
`screen -ls` list screens<br>
`screen -d` detach from screen<br>
`screen -r` resume attache to screen<br>
`exit` close screen window<br>
`Strg a c` new screen window<br>
`Strg a ESC` enter scroll mode 'Strg u d' up down<br>
`Strg a SPACE` cycle screen windows<br>
`Strg a |` vertical split<br>
`Strg a TAB` move between splits<br>
`Strg a :remove` to remove split<br>

## nordvpn linux
`sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)` install<br>
`nordvpn login` login<br>
`nordvpn status` show status<br>
`nordvpn settings` show settings<br>
`nordvpn c` to connect<br>
`nordvpn whitelist add subnet 192.168.0.0/16` whitlist subnet<br>
#### disable ipv6
```bash
sysctl -w net.ipv6.conf.all.disable_ipv6=1
sysctl -w net.ipv6.conf.default.disable_ipv6=1
sysctl -w net.ipv6.conf.tun0.disable_ipv6=1
```

## homebridge setup
[install guide](https://github.com/homebridge/homebridge/wiki/Install-Homebridge-on-Raspbian) __ACHTUNG__ dont use hb-service<br>
add `priates=/path/to/private/` with `/paht/to/private/privates.py` to `/etc/environment`<br>
use `sudo su` meanwhile `homebridge -D -U /var/lib/homerbidge` to start server<br>
to choose intervace `/var/lib/homerbidge/config.json`<br> 
```json
{
	"mdns": {"intervace": "ip-of-interface"},
	"bridge": {
		"name": "...",
		"username": "...",
		"port": ...,
		"pin": "..."
	},
	"description": "...",
	"accessories": [
		...
	],
	"platforms": [
...
	]
}
```
#### camera ffmpeg plugin
replace `/usr/lib/node_modules/homebridge-camera-ffmpeg/node_modules/ffmpeg-for-homebridge/ffmpeg` #ffmpeg bundled with plugin<br>
with `usr/bin/ffmpeg` #ffmpeg bundled with rasbian full img<br>
to capture desktop when booting to desktop use this in config<br>
```json
"source": "-f x11grab -r 10 -video_size 1280x720 -i :0.0",
"stillImageSource": "-f x11grab -t 1 -video_size 1280x720 -i :0.0 -vframes 1",
```
to capture cli when booting to cli use this in config<br>
```
"source": "-f fbdev -framerate 15 -i /dev/fb0"
"stillimageSource": "-f fbdev -i /dev/fb0 -t 1 -vframes 1"
```

## python
to control fan<br>
```python
import RPi.GPIO as GPIO
fan = 8
GPIO.setmode(GPIO.BOARD)
GPIO.output(fan, 1)
GPIO.cleanup()
```

to read mcp3008<br>
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

to gert cpu temp<br>
```pyhton
from gpiozero import CPUTemperature

cpu = CPUTemperature()
print(round(cpu.temperature))
```
