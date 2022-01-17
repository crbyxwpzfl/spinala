#import privates variable
import sys

characteristic = sys.argv[3].strip("''")

Statuspath = "/home/pi/spinala/Status.txt"

if sys.argv[1] == "Get":

    if characteristic == "Name":
        print("raspberry")
        sys.exit()

    if characteristic == "TemperatureDisplayUnits":
        print("CELSIUS")
        sys.exit()

    if characteristic == "HeatingThresholdTemperature":
        print("0")
        sys.exit()

    if  characteristic == "TargetTemperature" or characteristic == "CoolingThresholdTemperature":
        print("10")
        sys.exit()
    
    if characteristic == "CurrentHeatingCoolingState" or characteristic == "TargetHeatingCoolingState":
        f = open(Statuspath, 'r')
        status = f.read()
        f.close()
        
        import RPi.GPIO as GPIO
        GPIO.setwarnings(False)
        fan = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(fan,GPIO.OUT)
        
        #cool
        if int(status) == 2:
            GPIO.output(fan,1)
            
        #heat
        if int(status) == 1:
            GPIO.output(fan,0)
            
        print(status)
        sys.exit()

    if characteristic == "CurrentTemperature":
        
        #read cpu temp
        from gpiozero import CPUTemperature
        cpu = CPUTemperature()
        cputemp = round(cpu.temperature)
        
        #set status to cooling
        if cputemp > 40:
            f = open(Statuspath, 'w')
            f.write("2") #status cool
            f.close

    
        #set status to heating
        if cputemp < 30:
            f = open(Statuspath, 'w')
            f.write("1") #status heat
            f.close


        print(cputemp)
        sys.exit() 

if sys.argv[1] == "Set":

    if characteristic == "TargetHeatingCoolingState":
        value = sys.argv[4].strip("''")
        value = int(value)
            
        import RPi.GPIO as GPIO
        GPIO.setwarnings(False)
        fan = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(fan,GPIO.OUT)

        #off
        if int(value) == 0 or int(value) == 3:
            #not handled on purpose
            sys.exit()

        #heat
        if int(value) == 1:
            GPIO.output(fan,0)
            f = open(Statuspath, 'w')
            f.write(value)
            f.close
            sys.exit()

        #cool
        if int(value) == 2:
            GPIO.output(fan,1)
            f = open(Statuspath, 'w')
            f.write(value)
            f.close
            sys.exit()
