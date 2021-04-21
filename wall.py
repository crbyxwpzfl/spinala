output = subprocess.Popen(['ping', '-c', '1', '-w', '1', '10.3.141.165'], stdout=subprocess.PIPE)
print(str(output.stdout.read()))


import requests

#import privates variable
import sys
import os
sys.path.append(os.path.abspath("/home/pi/Desktop/config/"))
import privates

volumepath = os.path.join(privates.filepath, 'volume.txt')

characteristic = sys.argv[3].strip("''")

#get tv an/aus status
status = 0 #standard tv ist aus
import subprocess
from requests.auth import HTTPDigestAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def req():
    global status
    try:
        response = requests.get(f'https://{privates.ip}:1926/6/powerstate', verify=False, timeout=2, auth=HTTPDigestAuth(privates.user, privates.pw))

    except requests.exceptions.ConnectionError:    
        import subrocess
        output = subprocess.Popen(['ping', '-c', '1', '-w', '1', '10.3.141.224'], stdout=subprocess.PIPE)
        if "100% packet loss" in str(output.stdout.read()): 
            output = subprocess.Popen(['sudo', '/etc/raspap/hostapd/servicestart.sh', '--seconds', '3'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print("----no connecting now restarting hotspot----")
            response = requests.get('http://localhost:8080/motion?pi')
        print("----no connection but ping good----")
        sys.exit()
    
    except requests.exceptions.Timeout:
        import subprocess
        output = subprocess.Popen(['ping', '-c', '1', '-w', '1', '10.3.141.224'], stdout=subprocess.PIPE)
        if "100% packet loss" in str(output.stdout.read()):
            output = subprocess.Popen(['sudo', '/etc/raspap/hostapd/servicestart.sh', '--seconds', '3'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print("----timeout now restarting hotspot----")
            response = requests.get('http://localhost:8080/motion?pi')
        print("----timeout but ping good----")
        sys.exit()

    else:
        if "On" in str(response.content):
            status = 1


if sys.argv[1] == "Get":
    if characteristic == "Brightness":
        f = open(volumepath, 'r')
        volume = int(f.read())
        f.close()
        print(volume)
        sys.exit()

    if characteristic == "On":
        req()
        print(status)
        sys.exit()

if sys.argv[1] == "Set":
    value = sys.argv[4].strip("''")
    req()

    #set volume nur wenn tv an
    if characteristic == "Brightness" and int(status) == 1:     
        data = f"{{ muted: false, current: {int(value)} }}"
        response = requests.post(f'https://{privates.ip}:1926/6/audio/volume', timeout=2, data=data, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
        
        f = open(volumepath, 'w')
        f.write(value)
        f.close()
        sys.exit()
    
    if characteristic == "On":
        #nur wenn gerade aus dann mach an
        if int(value) == 1 and int(status) == 0:
            data = '{key: Standby}'
            response = requests.post(f'https://{privates.ip}:1926/6/input/key', timeout=2, data=data, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
            sys.exit()
    
        #nur wenn gerade an dann mach aus
        if int(value) == 0 and int(status) == 1:
            data = '{key: Standby}'
            response = requests.post(f'https://{privates.ip}:1926/6/input/key', timeout=2, data=data, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
            sys.exit()

    sys.exit()
