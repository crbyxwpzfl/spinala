import RPi.GPIO as GPIO
import time
import sys


def inter(pin):
    if GPIO.input(pin) == 1:
        d['pulse'] = time.time()    # messung begint
    else:
        d['echo'] = time.time()     # messung bendet


def Get():
    for x in range(0, 3):   # running 3 times

        GPIO.output(d['triggerpin'], True)
        time.sleep(0.00001) # see spec sheet trigger pin high for 0.01ms to init pulse
        GPIO.output(d['triggerpin'], False)
        
        time.sleep(0.1)     # wait for interrupts
        
        if d['pulse'] < d['echo']:
            int(mm) = (d['echo'] - d['pulse']) * (343460 / 2)   # time delta pulse to echo * soundspeed / 2 (back and forth)

        print(mm)

        time.sleep(0.5)     # pause meassurment

    GPIO.cleanup()

def Set():
    print("to be done")
    GPIO.cleanup()

d = {'Set': Set, 'Get': Get, 'pulse': 0, 'echo': 0, 'triggerpin': 17, 'echopin': 27}

GPIO.setmode(GPIO.BCM)             # GPIO Modus (BOARD / BCM)
GPIO.setup(d['triggerpin'], GPIO.OUT)   # Trigger-Pin = Raspberry Pi Output
GPIO.setup(d['echopin'], GPIO.IN)       # Echo-Pin = raspberry Pi Input

GPIO.add_event_detect(d['echopin'], GPIO.BOTH, callback = inter)

d.get(sys.argv[1].strip("''"))()





#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time

# Ultraschall Sensor Konfiguration
US_SENSOR_TRIGGER = 
US_SENSOR_ECHO = 

Messung_Max = 0.1             # in sekunden
Messung_Trigger = 0.00001     # in sekunden
Messung_Pause = 0.2           # in sekunden
Messung_Faktor = (343460 / 2) # Schallgeschwindigkeit durch 2 (hin und zurück) in mm/s
        # Schallgeschwindigkeit gem. https://de.wikipedia.org/wiki/Schallgeschwindigkeit
        # +20°C 343,46m/s
        #   0°C 331,50m/s
        # −20°C 319,09m/s
Abstand_Max = 4000            # Max value in mm
Abstand_Max_Error = Abstand_Max + 1

def US_SENSOR_EchoInterrupt(US_SENSOR_ECHO):
    global StartZeit, StopZeit

    # Speichere Zeit
    Zeit = time.time()
    if GPIO.input(US_SENSOR_ECHO) == 1:
        # steigende Flanke
        StartZeit = Zeit
    else:
        # fallende Flanke
        StopZeit = Zeit
        
def US_SENSOR_GetDistance():
    global StartZeit, StopZeit
    
    # setze TRIGGER für min 0.01ms
    GPIO.output(US_SENSOR_TRIGGER, True)
    time.sleep(Messung_Trigger)
    GPIO.output(US_SENSOR_TRIGGER, False)

    # setzte Defaultwerte
    StartZeit = 0
    StopZeit = 0
    # warte Messzeit auf Interrupts
    time.sleep(Messung_Max)
        
    if StartZeit < StopZeit:
        # berechne Zeitdifferenz zwischen Start und Ankunft im Sekunden
        Zeit = StopZeit - StartZeit
        # berechne Distanz
        Distanz = Zeit * Messung_Faktor
    else:
        # setze Fehlerwert
        Distanz = Abstand_Max_Error

    # Distanz als Ganzzahl zurückgeben
    return int(Distanz)


if __name__ == '__main__':
    # Ultraschall Sensor Initialisierung GPIO-Pins
    GPIO.setmode(GPIO.BCM)                    # GPIO Modus (BOARD / BCM)
    GPIO.setup(US_SENSOR_TRIGGER, GPIO.OUT)   # Trigger-Pin = Raspberry Pi Output
    GPIO.setup(US_SENSOR_ECHO, GPIO.IN)       # Echo-Pin = raspberry Pi Input

    GPIO.add_event_detect(US_SENSOR_ECHO, GPIO.BOTH, callback = US_SENSOR_EchoInterrupt)
                      
    try:
        while True:
            Abstand = US_SENSOR_GetDistance()
            
            if Abstand >= Abstand_Max:
                # Ausgabe Text
                print ("Kein Objekt gefunden")
            else:
                # Ausgabe Text
                print ("Gemessene Entfernung = %i mm" % Abstand)
            
            time.sleep(Messung_Pause)
 
    # Beim Abbruch durch STRG+C: GPIO Port freigeben
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
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
