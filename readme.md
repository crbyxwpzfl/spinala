## sudo apt-get install screen scs
`Strg a c` new screen window<br>
`Strg a ESC` enter scroll mode 'Strg u d' up down<br>
`Strg a SPACE` cycle screen windows<br>

## sudo apt-get install screen cli
`screen -ls` list screens<br>
`screen -d` detach from screen<br>
`screen -r` resume attache to screen<br>
`exit` close screen window

##nordvpn linux
`sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)` install<br>
`nordvpn login` login<br>
`nordvpn status` show status<br>
`nordvpn settings` show settings<br>
`nordvpn c` to connect<br>

disable ipv6```bash
sysctl -w net.ipv6.conf.all.disable_ipv6=1
sysctl -w net.ipv6.conf.default.disable_ipv6=1
sysctl -w net.ipv6.conf.tun0.disable_ipv6=1
```

##rasspAP

##homebridge
to choose intervace config.json 
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
