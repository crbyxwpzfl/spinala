import RPi.GPIO as GPIO
import time
import sys

def Get():
    for i in range(0, 2):   # running 3 times

        GPIO.output(d['triggerpin'], True)
        time.sleep(0.00001) # see spec sheet trigger pin high for 0.01ms to init pulse
        GPIO.output(d['triggerpin'], False)
        
        while GPIO.input(d['echopin']) == 0: d['pulse'] = time.time() # when pulse is out
        while GPIO.input(d['echopin']) == 1: d['echo'] = time.time() # when echo returns
        
        d[i] = int( (d['echo'] - d['pulse']) * (343460 / 2) ) # time delta pulse to echo * soundspeed / 2 (back and forth)

        time.sleep(0.2) # pause meassurment

    h = int( (((d[0]+d[1])/2) - d['down'])/(d['up']-d['down'])*100 ) # mean two readouts then teanslate and scale readout into 1 to 100 
    print (h)
    return (h)

def Set():
    while Get() < int( sys.argv[4].strip("''") ) - 3 and Get() < int( sys.argv[4].strip("''") ) + 3 : # lift up
        GPIO.output(d['uppin'], True)

    while Get() > int( sys.argv[4].strip("''") ) - 3 and Get() > int( sys.argv[4].strip("''") ) + 3 : # lowwer down
        GPIO.output(d['downpin'], True)
    
    GPIO.output(d['downpin'], False)
    GPIO.output(d['uppin'], False)

d = {'Set': Set, 'Get': Get, 'pulse': 0, 'echo': 0, 'triggerpin': 17, 'echopin': 27, 'uppin': 14, 'downpin': 15, 'up': 570, 'down': 95} # set 'pins' set 'up' to max readout 'down' to min readot
GPIO.setmode(GPIO.BCM) # gpio Modus BOARD / BCM
GPIO.setup(d['triggerpin'], GPIO.OUT) # triggerpin output
GPIO.setup(d['echopin'], GPIO.IN) # echopin input
GPIO.setup(d['uppin'],GPIO.OUT)
GPIO.setup(d['downpin'],GPIO.OUT)

d.get(sys.argv[1].strip("''"))()
GPIO.cleanup()




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
