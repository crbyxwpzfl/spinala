import RPi.GPIO as GPIO
import time
import sys
import subprocess
import pathlib # for calling itself

def sub(cmdstring, waitforcompletion): # string here because shell true because only way of chaning commands
     p = subprocess.Popen(cmdstring , text=False, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
     if waitforcompletion: return p.communicate()[0].decode() # this will wait for subprocess to finisih

def move(): # in the right direction
    GPIO.setup(d['uppin'], GPIO.OUT) # init move pins just on set so that set can run while get senses pos
    GPIO.setup(d['downpin'], GPIO.OUT)

    while sense() not in range( int(sys.argv[4]) - 10 , int(sys.argv[4]) ): # some fine tuning is to be done to reach true zero every time here
        if d['h'] > int(sys.argv[4]): GPIO.output(d['uppin'], False); GPIO.output(d['downpin'], True)
        if d['h'] < int(sys.argv[4]): GPIO.output(d['uppin'], True); GPIO.output(d['downpin'], False)

    GPIO.output(d['downpin'], False) # stop driving
    GPIO.output(d['uppin'], False)

def sense(): # current pos via sensor
    GPIO.output(d['triggerpin'], True)
    time.sleep(0.00001) # see spec sheet trigger pin high for 0.01ms to init pulse
    GPIO.output(d['triggerpin'], False)
    while GPIO.input(d['echopin']) == 0: d['pulse'] = time.time() # time when pulse is out
    while GPIO.input(d['echopin']) == 1: d['echo'] = time.time() # time when echo returns
    d['h'] = int(( (d['echo']-(d['pulse']) -d['down'])/(d['up']-d['down']))*100 ) # 'echo' 'pulse' time delta translated into 1 to 100
    time.sleep(0.2) # pause for when called via while in 'Set' no good but one line shorter
    return d['h'] if sys.argv[4:] else print(int(d['h']/d['h'])) if sys.argv[3].strip("'") == 'On' and d['h'] else print(int(d['h'])) # return for 'Set' and print 1 for 'Get' 'On' else print h

def head(): # just when 'Set' and vlaue not 1 so Set On 0 works but Set On 1 does not
    if sub('pgrep -lfc tisch.py', True).strip('\n') > 1 and sys.argv[4:] != ['1']: sub('pkill -of tisch.py', True) # kill oldest tisch.py when more than 2 are running
    sub(f'python3 {pathlib.Path(__file__).resolve()} move to height {sys.argv[4]} & disown', False)


d = {'move': move, 'Set': head, 'Get': sense, 'triggerpin': 17, 'echopin': 27, 'uppin': 14, 'downpin': 15, 'up': 0.003370, 'down': 0.000545} # set 'pins' set 'up' 'down' to 'echo' - 'pulse' at position max min

if sys.argv[4:] != ['1']: GPIO.setwarnings(False)
if sys.argv[4:] != ['1']: GPIO.setmode(GPIO.BCM) # gpio Modus BOARD or BCM

if sys.argv[4:] != ['1']: GPIO.setup(d['echopin'], GPIO.IN) # 'echopin' input
if sys.argv[4:] != ['1']: GPIO.setup(d['triggerpin'], GPIO.OUT) # 'triggerpin' output

if sys.argv[4:] != ['1']: d.get(sys.argv[1].strip("''"))() # call 'Get' or 'Set' ignoring set on/rotspeed 1

if sys.argv[4:] != ['1']: GPIO.cleanup() # lots of warnings with conurrent calls because previous script doesnt reach cleanup dont know how to fix perhaps with spawning seperate move instance and here just telling it where to go
