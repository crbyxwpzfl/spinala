#PROBLEM tisch färht in kleinen schritten weiter als in grossen liegt am anfahren 
import sys
import time
characteristic = sys.argv[3].strip("''")


if sys.argv[1] == "Get":
    if characteristic == "On":
        f = open("/home/pi/Desktop/git/height.txt", 'r')
        status = f.read()
        f.close()
        if status != "0":
            print("1") #höhe ungleich 0 heisst an
        if status == "0":
            print("0") #höhe gleich 0 heisst aus
        sys.exit()

    if characteristic == "Brightness":
        f = open("/home/pi/Desktop/git/height.txt", 'r')
        status = f.read()
        f.close()
        print(status)
        sys.exit()


if sys.argv[1] == "Set":
    value = sys.argv[4].strip("''")
    value = str(value)
    
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    runter = 15
    hoch = 14
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(runter,GPIO.OUT)
    GPIO.output(runter,0)
    GPIO.setup(hoch,GPIO.OUT)
    GPIO.output(hoch,0)

    totaltime = 4 #fahrzeit von 0-100 von unten bis ganz oben

    if characteristic == "On":
        if value == "0":
            #fahr tisch auf 0 wenn
            #print("runter")
            #print(totaltime)
            GPIO.output(runter,1)
            time.sleep(totaltime)
            GPIO.cleanup()
            f = open("/home/pi/Desktop/git/height.txt", 'w')
            f.write(value) #schrieb höhe null in height.txt
            f.close
        sys.exit() #wenn value 1 also anschalten tu nichts

    if characteristic == "Brightness":
          f = open("/home/pi/Desktop/git/height.txt", 'r')
          status = f.read() #lies alten höhen wert
          f.close()
          onesteptime = totaltime/100
          diff = int(value) - int(status)
          
          #fahr runter
          if diff < 0:
              diff = abs(diff)
              ontime = diff*onesteptime
              #print("runter")
              #print(ontime)
              GPIO.output(runter,1)
              time.sleep(ontime)
              GPIO.cleanup()

              f = open("/home/pi/Desktop/git/height.txt", 'w')
              f.write(value) #schrib neuen höhen wert
              f.close
              sys.exit()

          #fahr hocch
          if diff > 0:
              ontime = diff*onesteptime
              #print("hoch")
              #print(ontime)
              GPIO.output(hoch,1)
              time.sleep(ontime)
              GPIO.cleanup()

              f = open("/home/pi/Desktop/git/height.txt", 'w')
              f.write(value) #schrib neuen höhen wert
              f.close
              sys.exit()
          
          sys.exit() #wenn diff 0 tu nichts
