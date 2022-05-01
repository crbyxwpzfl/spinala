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
    while Get() < int( sys.argv[4].strip("''") - 3) and GPIO.input(d['downpin']) == 0 : # lift when position delta pos and 'downpin' off
        GPIO.output(d['uppin'], True)

    while Get() + 10 > int( sys.argv[4].strip("''") + 3 ) and GPIO.input(d['uppin']) == 0 : # lowwer when position delta neg and 'uppin' off
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