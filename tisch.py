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
