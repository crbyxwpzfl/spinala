import RPi.GPIO as GPIO
import time
import sys
import subprocess

def sub(cmdstring, waitforcompletion): # string here because shell true because only way of chaning commands
     p = subprocess.Popen(cmdstring , text=False, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
     if waitforcompletion: return p.communicate()[0].decode() # this will wait for subprocess to finisih

def move(): # in the right direction
    while sense() < int(sys.argv[4]) - 3: # lift when position delta pos and 'downpin' off including some correction values
        GPIO.output(d['downpin'], False) # here incase of changed direction
        GPIO.output(d['uppin'], True)

    while sense() + 10 > int(sys.argv[4]) + 3: # lowwer when position delta neg and 'uppin' off
        GPIO.output(d['uppin'], False) # here incase of changed direction
        GPIO.output(d['downpin'], True)

    GPIO.output(d['downpin'], False) # stop driving
    GPIO.output(d['uppin'], False) # stop driving

def sense(): # current pos via sensor
    GPIO.output(d['triggerpin'], True)
    time.sleep(0.00001) # see spec sheet trigger pin high for 0.01ms to init pulse
    GPIO.output(d['triggerpin'], False)
    while GPIO.input(d['echopin']) == 0: d['pulse'] = time.time() # time when pulse is out
    while GPIO.input(d['echopin']) == 1: d['echo'] = time.time() # time when echo returns
    d['h'] = int(( (d['echo']-(d['pulse']) -d['down'])/(d['up']-d['down']))*100 ) # 'echo' 'pulse' time delta translated into 1 to 100
    time.sleep(0.2) # pause for when called via while in 'Set' no good but one line shorter
    return d['h'] if sys.argv[4:] else print(int(d['h']/d['h'])) if sys.argv[3].strip("'") == 'On' and d['h'] else print(int(d['h'])) # return for 'Set' and print 1 for 'Get' 'On' else print h

d = {'Set': move, 'Get': sense, 'triggerpin': 17, 'echopin': 27, 'uppin': 14, 'downpin': 15, 'up': 0.003370, 'down': 0.000545} # set 'pins' set 'up' 'down' to 'echo' - 'pulse' at position max min

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # gpio Modus BOARD or BCM
GPIO.setup(d['echopin'], GPIO.IN) # 'echopin' input
GPIO.setup(d['triggerpin'], GPIO.OUT) # 'triggerpin' output
GPIO.setup(d['uppin'], GPIO.OUT) # init move pins
GPIO.setup(d['downpin'], GPIO.OUT)


# set move pins to off somwhere here otherwise they keep state and reactivae on new script run



if sub('pgrep -lfc tisch.py', True).strip('\n') > 1: sub('pkill -of tisch.py', True) # kill oldest tisch.py when more than 2 are running

if not sys.argv[4:] or sys.argv[4:] != ['1']: d.get(sys.argv[1].strip("''"))() # call 'Get' or 'Set'

GPIO.cleanup() # lots of warnings with conurrent calls because previous script doesnt reach cleanup dont know how to fix perhaps with checking for running python process
