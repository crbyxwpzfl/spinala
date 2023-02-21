import asyncio
import socket
import sys
import pathlib
import subprocess
import math

def sub(cmdstring, silence):  # string here because shell true because only way of chaning commands esp important for tapback()
    if silence: return subprocess.Popen(cmdstring , shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode()  # default universalnewlines/text False is ok because of decode()
    if not silence: subprocess.Popen(cmdstring , shell=True, stdout=sys.stdout, stderr=sys.stderr).wait()  # unlike aboveus this prints output to current stdout not quiet and waits for completion

async def whenclient(reader, writer):  # whan client connects this gets called from serve()
    d['dsrd'] = (await reader.read(255)).decode('utf8')

async def serve():  # initiates listening for client connections and calls move
    await asyncio.start_server(whenclient, 'localhost', 2222); await move()

async def move():  # moves tisch
    import os; os.environ["BLINKA_MCP2221"] = "1"; import board, digitalio, adafruit_vl53l1x; d['vl53'] = adafruit_vl53l1x.VL53L1X(board.I2C()); d['vl53'].start_ranging()  # configure sense some how eventough this takes1 sec no client connections are lost in the mean time
    # pretty print while d.get('desired', sys.argv[2]) != "quit": print(d['lineup'], end=d['lineclear']); print(f" desired: {d.get('desired', sys.argv[2])} measured: {vl53.distance}"); await asyncio.sleep(0.2)  # while sleep serve() has authority to connect to client and call whenclient()

    d['h'] = int( ( (-d['down']) / (d['up']-d['down']) )*100 - d['downshift'] ) # 'echo' 'pulse' time delta translated into 1 to 100 hight including slight down bias
    d['h'] = (d['range']*d['dsrd']/100) + d['down']  # translating 'desired' into hight 79 to 140
    d['h'] = int( (d['h']-d['down'])*100/d['range'] )  # translating 'h' into 1 to 100 vlaue

    digitalio.DigitalInOut(board.G1).switch_to_output(value=False)


    while not math.isclose(d.get('position', 1111) ), d['dsrd'] , abs_tol=5):  # TODO calculate tolerance including round()
        d['position'] = d['translate'](d['range']())
        if d['position'] < d['dsrd'] and not d.get('pinup'): d.pop('pindown');  d['pinup'] = True; d['sendit'](board.pindown, False); d['sendit'](board.pinup, True)
        if d['position'] > d['dsrd'] and not d.get('pindown'): d.pop('pinup'); d['pindown'] = True; digitalio.DigitalInOut(board.up).switch_to_output(value=False); digitalio.DigitalInOut(board.down).switch_to_output(value=True)
        await asyncio.sleep(0.2)

    # TODO check if clauses above

    d['sendit'](board.pindown, False); d['sendit'](board.pinup, False)


def status():
    return d['h'] if sys.argv[4:] else print(d['echo']-d['pulse']) if sys.argv[2] == 'cali' else print( max( min(d['h'],1), 0) ) if sys.argv[3] == 'On' else print(max(d['h'],0)) # return for 'Set' else print 1/0 for 'Get' 'On' else print hight for 'Get' 'Rotspeed' else print raw hight for 'Get' 'cali' to calibarate up/down
    # TODO implement answer to get on off and get hight


async def serveorconnect():
    try: socket.create_connection(('localhost', 2222)).sendall(bytes(sys.argv[2], "utf-8"))  # try to connect to serve() instance and send pos
    except: sub(f'screen -L -S tisch -d -m python3 "{pathlib.Path(__file__)}" serve "{sys.argv[2]}"', False)  # no connection possible spawn serve() instance

d = {'Set': serveorconnect, 'serve': serve, 'pinup': board.G1, 'pindown': board.G0,
     'sendit': lambda pin, state: digitalio.DigitalInOut(pin).switch_to_output(value=state)
     'translate': lambda h: (h - 79 )*100/(140-79),  # TODO put round() here somewhere
     'range': lambda: d['vl53'].distance if d['vl53'].data_ready and d['vl53'].distance else 1111,  # vl53.clear_interrupt() is missing but interrupt is not relevant
     'lineup': '\033[1A', 'lineclear': '\x1b[2K'}


asyncio.run( d.get(sys.argv[1])() )  # call move
