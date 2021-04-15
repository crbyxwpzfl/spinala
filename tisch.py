#PROBLEM tisch färht langsam an daraus folgt abweichung zu durchgehender fahrzeit0-100 
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

    if characteristic == "On":
        if value == "0":
            #fahr tisch auf 0 wenn
            
            f = open("/home/pi/Desktop/git/height.txt", 'w')
            f.write(value) #schrieb höhe null in height.txt
            f.close

    sys.exit() #wenn value 1 also anschalten tu nichts


    if characteristic == "Brightness":
          f = open("/home/pi/Desktop/git/height.txt", 'r')
          status = f.read() #lies alten höhen wert
          f.close()
          
          totaltime = 10 #fahrzeit von 0-100 von unten bis ganz oben
          onesteptime = totaltime/100

          diff = value - status
          
          #fahr runter
          if diff < 0:
              diff = abs(diff)
              ontime = diff*onesteptime
              
              print("runter")
              print(ontime)

          #fahr hocch
          if diff > 0:
              ontime = diff*onesteptime
              
              print("hoch")
              print(ontime)

          f = open("/home/pi/Desktop/git/height.txt", 'w')
          f.write(value) #schrib neuen höhen wert
          f.close


          
