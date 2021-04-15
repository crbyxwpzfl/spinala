TEST


import sys
characteristic = sys.argv[3].strip("''")

if sys.argv[1] == "Get":

    if characteristic == "Name":
        print("raspberry")
        sys.exit()

    if characteristic == "CurrentHeatingCoolingState":
        f = open("/home/pi/Desktop/CHCStatus.txt", 'r')
        status = f.read()
        f.close()
        print(status)
        sys.exit()

    if characteristic == "TargetHeatingCoolingState":
        f = open("/home/pi/Desktop/THCStatus.txt", 'r')
        status = f.read()
        f.close()
        print(status)
        sys.exit()

    if characteristic == "CurrentTemperature":
        from gpiozero import CPUTemperature
        cpu = CPUTemperature()
        print(round(cpu.temperature))
        sys.exit() 

    if characteristic == "TargetTemperature":
        f = open("/home/pi/Desktop/TTemp.txt", 'r')
        status = f.read()
        f.close()
        print(status)
        sys.exit() 

    if characteristic == "TemperatureDisplayUnits":
        print("CELSIUS")
        sys.exit()

    if characteristic == "CoolingThresholdTemperature":
        f = open("/home/pi/Desktop/CTTemp.txt", 'r')
        status = f.read()
        f.close()
        print(status)
        sys.exit() 

    if characteristic == "HeatingThresholdTemperature":
        f = open("/home/pi/Desktop/HTTemp.txt", 'r')
        status = f.read()
        f.close()
        print(status)
        sys.exit() 


if sys.argv[1] == "Set":

    if characteristic == "TargetHeatingCoolingState":
        value = sys.argv[4].strip("''")
        value = str(value)
            
        import RPi.GPIO as GPIO
        GPIO.setwarnings(False)
        fan = 40
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(fan,GPIO.OUT)

        #off
        if value == "0":
            GPIO.output(fan,0)

        #heat
        if value == "1":
            GPIO.output(fan,0)

        #cool
        if value == "2":
            GPIO.output(fan,1)

        #auto
        if value == "3":
            GPIO.output(fan,0)

        f = open("/home/pi/Desktop/THCStatus.txt", 'w')
        f.write(value)
        f.close

        f = open("/home/pi/Desktop/CHCStatus.txt", 'w')
        f.write(value)
        f.close
        sys.exit()

    if characteristic == "TargetTemperature":
        value = sys.argv[4].strip("''")
        value = str(float(value))

        f = open("/home/pi/Desktop/TTemp.txt", 'w')
        f.write(value)
        f.close
        sys.exit()
        
    if characteristic == "CoolingThresholdTemperature":
        value = sys.argv[4].strip("''")
        value = str(float(value))

        f = open("/home/pi/Desktop/CTTemp.txt", 'w')
        f.write(value)
        f.close
        sys.exit()

    if characteristic == "HeatingThresholdTemperature":
       value = sys.argv[4].strip("''")
       value = str(float(value))

       f = open("/home/pi/Desktop/HTTemp.txt", 'w')
       f.write(value)
       f.close
       sys.exit()
