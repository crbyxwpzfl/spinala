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
    d['h'] = int( ( (d['echo']-d['pulse']-d['down']) / (d['up']-d['down']) )*100 - d['downshift'] ) # 'echo' 'pulse' time delta translated into 1 to 100 hight including slight down bias
    time.sleep(0.2) # pause for when called via while in 'Set' no good but one line shorter
    return d['h'] if sys.argv[4:] else print(d['echo']-d['pulse']) if sys.argv[2] == 'cali' else print( max( min(d['h'],1), 0) ) if sys.argv[3] == 'On' else print(max(d['h'],0)) # return for 'Set' else print 1/0 for 'Get' 'On' else print hight for 'Get' 'Rotspeed' else print raw hight for 'Get' 'cali' to calibarate up/down

def head(): # just when 'Set' and vlaue not 1 so Set On 0 works but Set On 1 does not
    while int(sub('pgrep -lfc move', True).strip('\n')) > 1 and sys.argv[4:] != ['1']: sub('pkill -of move', True) # kill oldest move as long as more than 1 is running so paralell gets are responsive and all sets exit cleanly and ocasional double moves get reduced to one
    sub(f'python3 {pathlib.Path(__file__).resolve()} move to height {sys.argv[4]} & disown', False)

d = {'move': move, 'Set': head, 'Get': sense, 'triggerpin': 17, 'echopin': 27, 'uppin': 14, 'downpin': 15, 'up': 0.006590, 'down': 0.004060, 'downshift': 2} # set 'pins' set 'up'/'down' to 'Get' 'cali' at position top/bottom

if sys.argv[4:] != ['1']: GPIO.setwarnings(False)
if sys.argv[4:] != ['1']: GPIO.setmode(GPIO.BCM) # gpio Modus BOARD or BCM

if sys.argv[4:] != ['1']: GPIO.setup(d['echopin'], GPIO.IN) # 'echopin' input
if sys.argv[4:] != ['1']: GPIO.setup(d['triggerpin'], GPIO.OUT) # 'triggerpin' output

if sys.argv[4:] != ['1']: d.get(sys.argv[1].strip("''"))() # call 'Get' or 'Set' ignoring set on/rotspeed 1

if sys.argv[4:] != ['1']: GPIO.cleanup() # lots of warnings with conurrent calls because previous script doesnt reach cleanup dont know how to fix perhaps with spawning seperate move instance and here just telling it where to go
