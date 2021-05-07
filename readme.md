## raspberry pi inital setup
`pinout` prints rpis pinout __ACHTUNG__ diff between gpioNr. and board pinNr.<br>
`ifconfig` list interfaces<br>
`read temp: vcgencmd measure_temp` return fantemp<br>
<br>
ssh disable PasswordAuth in `~/etc/ssh/sshd_config`<br>
ssh enable keypassAuth<br>
add openssh public to `home/pi/.ssh/authorized_keys`<br>

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
#### disable ipv6
```bash
sysctl -w net.ipv6.conf.all.disable_ipv6=1
sysctl -w net.ipv6.conf.default.disable_ipv6=1
sysctl -w net.ipv6.conf.tun0.disable_ipv6=1
```

## [rasspAP](https://raspap.com/#quick)

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
