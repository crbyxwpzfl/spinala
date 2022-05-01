import RPi.GPIO as GPIO
import time
import sys

def Get():
    GPIO.output(d['triggerpin'], True)
    time.sleep(0.00001) # see spec sheet trigger pin high for 0.01ms to init pulse
    GPIO.output(d['triggerpin'], False)
    while GPIO.input(d['echopin']) == 0: d['pulse'] = time.time() # time when pulse is out
    while GPIO.input(d['echopin']) == 1: d['echo'] = time.time() # time when echo returns
    d['h'] = int(( (d['echo']-(d['pulse']) -d['down'])/(d['up']-d['down']))*100 ) # 'echo' 'pulse' time delta translated into 1 to 100
    time.sleep(0.2) # pause for when called via while in 'Set' no good but one line shorter
    return d['h'] if sys.argv[1].strip("''") == 'Set' else print(d['h']) # return for 'Set' and print fot 'Get'

def Set():
    while Get() < int( sys.argv[4].strip("''") ) and GPIO.input(d['downpin']) == 0 : # lift when position delta pos and 'downpin' off
        GPIO.output(d['uppin'], True)

    while Get() > int( sys.argv[4].strip("''") ) and GPIO.input(d['uppin']) == 0 : # lowwer when position delta neg and 'uppin' off
        GPIO.output(d['downpin'], True)

    GPIO.output(d['downpin'], False) # stop driving
    GPIO.output(d['uppin'], False) # stop driving

d = {'Set': Set, 'Get': Get, 'triggerpin': 17, 'echopin': 27, 'uppin': 14, 'downpin': 15, 'up': 0.003370, 'down': 0.000545} # set 'pins' set 'up' 'down' to 'echo' - 'pulse' at position max min
GPIO.setmode(GPIO.BCM) # gpio Modus BOARD or BCM
GPIO.setup(d['triggerpin'], GPIO.OUT) # 'triggerpin' output
GPIO.setup(d['echopin'], GPIO.IN) # 'echopin' input
GPIO.setup(d['uppin'],GPIO.OUT)
GPIO.setup(d['downpin'],GPIO.OUT)
d.get(sys.argv[1].strip("''"))() # call 'Get' or 'Set'
GPIO.cleanup() # lots of warnings with conurrent calls because previous script doesnt reach cleanup dont know how to fix 




#neues problem wenn ontime < compensation dann negative ontime
import time

#import privates variable
import sys

characteristic = sys.argv[3].strip("''")
Heightpath = "/home/pi/spinala/hight.txt"

accbrakecompensation = 0
totaltime = 20 - accbrakecompensation #fahrzeit von 0-100 von unten bis ganz oben

singlesteptime = totaltime/100
diff = 0
value = 0

def go():
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    runter = 15
    hoch = 14
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(runter,GPIO.OUT)
    GPIO.output(runter,0)
    GPIO.setup(hoch,GPIO.OUT)
    GPIO.output(hoch,0)

    if diff < -1:
        ontime = abs(diff)*singlesteptime + accbrakecompensation
        if ontime > 0:
            GPIO.output(runter,1)
            time.sleep(ontime)
            GPIO.cleanup()

            f = open(Heightpath, 'w')
            f.write(value) #schrieb höhe nur wenn gefahren wird
            f.close

        
    if diff > 1:
        ontime = diff*singlesteptime + accbrakecompensation
        if ontime > 0:
            GPIO.output(hoch,1)
            time.sleep(ontime)
            GPIO.cleanup()

            f = open(Heightpath, 'w')
            f.write(value) #schrieb höhe nur wenn gefahren wird
            f.close


    sys.exit() #if diff 0 oder kleiner 0 nichts tun

if sys.argv[1] == "Get":
    characteristic = sys.argv[3].strip("''")
    if characteristic == "name":
        print("tisch")
        sys.exit()

    if characteristic == "On":
        f = open(Heightpath, 'r')
        status = f.read()
        f.close()
        if int(status) != 0:
            print("1") #höhe ungleich 0 heisst an
        if int(status) == 0:
            print("0") #höhe gleich 0 heisst aus
        sys.exit()

    if characteristic == "RotationSpeed":
        f = open(Heightpath, 'r')
        status = f.read()
        f.close()
        print(status)
        sys.exit()


if sys.argv[1] == "Set":
    value = sys.argv[4].strip("''")
    value = str(value)
    if value == "false":
        value = 0

    f = open(Heightpath, 'r')
    status = f.read() #lies alten höhen wert
    f.close()

    if characteristic == "On":
        if value == "0":
            diff = 0 - int(status) #fahr tisch auf 0  
            
            go()

        sys.exit() #wenn value 1 also anschalten tu nichts

    if characteristic == "RotationSpeed":
        diff = int(value) - int(status)

        go()
