import sys
import RPi.GPIO as GPIO
import os


def Get():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(d['fanpin'],GPIO.OUT)
    GPIO.output(d['fanpin'], True) if d['CurrentTemperature'] > 30 else GPIO.output(d['fanpin'], False) # default case run fan 
    print(d.get(sys.argv[3].strip("''") , GPIO.input(d['fanpin']) + 1 )) # prints 'CurrentHeatingCoolingState' 'TargetHeatingCoolingState' states 1 heat or 2 cool or from dict

GPIO.setwarnings(False)
d = {'Get': Get, 'fanpin': 21, 'CurrentTemperature': int(os.popen('vcgencmd measure_temp').readline()[5:-5]),'TemperatureDisplayUnits': 'CELSIUS', 'HeatingThresholdTemperature': 0, 'TargetTemperature': 10, 'CoolingThresholdTemperature': 10} # set 'pin'
d.get(sys.argv[1].strip("''"), sys.exit)() # call 'Get' or 'Set'
#GPIO.cleanup() # lots of warnings with out cleanup but clenup doesnt keep fan running