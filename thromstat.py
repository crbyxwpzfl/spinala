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
        from gpiozero import CPUTemperature
        cpu = CPUTemperature()
        print(round(cpu.temperature))
        sys.exit()

    if characteristic == "TemperatureDisplayUnits":
        print("CELSIUS")
        sys.exit()

    if characteristic == "CoolingThresholdTemperature":
        from gpiozero import CPUTemperature
        cpu = CPUTemperature()
        print(round(cpu.temperature))
        sys.exit()

    if characteristic == "HeatingThresholdTemperature":
        print("0")
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
                #not handled on purpose
                sys.exit()
        #heat
        if value == "1":
                GPIO.output(fan,0)
                f = open("/home/pi/Desktop/THCStatus.txt", 'w')
                f.write(value)
                f.close
                
                f = open("/home/pi/Desktop/CHCStatus.txt", 'w')
                f.write(value)
                f.close
                sys.exit()

        #cool
        if value == "2":
                GPIO.output(fan,1)
                f = open("/home/pi/Desktop/THCStatus.txt", 'w')
                f.write(value)
                f.close
                
                f = open("/home/pi/Desktop/CHCStatus.txt", 'w')
                f.write(value)
                f.close
                sys.exit()

        #auto
        if value == "3":
                #not handled on purpose
                sys.exit()
