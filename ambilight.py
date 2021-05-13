import requests
import math

#import privates variable
import sys
import os
sys.path.append(os.environ.get('privates'))
import privates

Huepath = os.path.join(privates.hbpipath, 'Hue.txt')
Brightnesspath = os.path.join(privates.hbpipath, 'Brightness.txt')
Saturationpath = os.path.join(privates.hbpipath, 'Saturation.txt')
Onpath = os.path.join(privates.hbpipath, 'On.txt')

characteristic = sys.argv[3].strip("''")
charapath = os.path.join(privates.hbpipath, f'{characteristic}.txt')


def go():
    f = open(Huepath, 'r')
    h = float(((int(f.read())-7)%360)/360) #((x-farb angleichung)%360 rest ist neuer hue wert)/360 ausgabe von 0-1
    f.close()
    f = open(Saturationpath, 'r')
    s = float(math.pow((int(f.read())/100),0.5)) #(x/100)^0.5 um tv saturation settings aus zu gleichen
    f.close()
    f = open(Brightnesspath, 'r')
    v = float(f.read())/100
    f.close()
    
    if s == 0.0: v*=255; r, g, b = v, v, v
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    if i == 0: r, g, b = v, t, p
    if i == 1: r, g, b = q, v, p
    if i == 2: r, g, b = p, v, t
    if i == 3: r, g, b = p, q, v
    if i == 4: r, g, b = t, p, v
    if i == 5: r, g, b = v, p, q

    body = f"{{r: {int(r)}, g: {int(g)}, b: {int(b)}}}"

    try:
        response = requests.post(f'http://{privates.ip}:1925/6/ambilight/cached', timeout=2, data=body)
    except requests.exceptions.ConnectionError:
        print("  ----  error connecting setting ambi ----  ")
        sys.exit()
    except requests.exceptions.Timeout:
        print("  ----  timeout error setting ambi  ----  ")
        sys.exit()

if sys.argv[1] == "Get":
        f = open(charapath, 'r')
        print(int(f.read()), end='')
        f.close()
        sys.exit()

if sys.argv[1] == "Set":
    #get tv an/aus status
    from requests.auth import HTTPDigestAuth         
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    status = 0 #standard tv ist aus
    try:
        response = requests.get(f'https://{privates.ip}:1926/6/powerstate', verify=False, timeout=2, auth=HTTPDigestAuth(privates.user, privates.pw))
    except requests.exceptions.ConnectionError:
        print("  ----  error connecting getting pow  ----  ")
        sys.exit()
    except requests.exceptions.Timeout:
        print("  ----  timeout error getting pow  ----  ")
        sys.exit()
    else:
        if "On" in str(response.content):
            status = 1
    
    value = sys.argv[4].strip("''")
    
    if characteristic != "On" and int(status) == 0: #nur wenn tv aus ist
        f = open(charapath, 'w')
        f.write(value)
        f.close()
        
        go()
        go() #ohne wdh wird abundzu falsche farbe angezeigt
        
        sys.exit()

    if characteristic == "On" and int(status) == 0: #nur wenn tv aus ist
        if int(value) == 1:
            go()
            
            f = open(charapath, 'w')
            f.write(value)
            f.close()
            sys.exit()
            
        if int(value) == 0:
            body = "{r: 0, g: 0, b: 0}"

            try:
                response = requests.post(f'http://{privates.ip}:1925/6/ambilight/cached', timeout=2, data=body)
            except requests.exceptions.ConnectionError:
                print("  ----  error connecting turning ambi off ----  ")
                sys.exit()
            except requests.exceptions.Timeout:
                print("  ----  timeout error turning ambi off ----  ")
                sys.exit()

                
            f = open(charapath, 'w')
            f.write(value)
            f.close()
            sys.exit()

print("---- end of file sth went wrong -----")
sys.exit() #wenn tv an und ich will an machen tu nichts
