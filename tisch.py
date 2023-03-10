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
    writer.write(bytes(d.get('transpos', "error"), "utf-8"))  # write to client to responde to get
    r = (await reader.read(255));    d['dsrd'] = int(r.decode('utf8')) if r else d['dsrd']  # read from client to change 'dsrd'

async def serve():  # initiates listening for client connections and calls move
    print("here")
    d['dsrd'] = int(sys.argv[2]);    await asyncio.start_server(whenclient, 'localhost', 2222);    await move()

async def move():  # for positive moves wihle dsrd is above rawpos's or for negative moves while dsrd is belwo rawpos's  # inital negative move and dsrd not bigger than dsrd then   # this server respondes to 'Set/Get whatever whatever int' and drives tisch to int. int can be 'R+\{1}'
    import os;    os.environ["BLINKA_MCP2221"] = "1";    
    import board
    import digitalio, adafruit_vl53l1x;    d['vl53'] = adafruit_vl53l1x.VL53L1X(board.I2C());    d['vl53'].start_ranging()  # configure sense some how eventough this takes 1sec no client connections are lost in the mean time
    print(board.G0)
    print("done import")

    # TODO rethink imports especially pay attention to name is not defined error and make sure tryrecv can range for it self alswell!!!
    


    while ( not d.get('transpos-prev') > d['dsrd'] < d['transpos-curr']) if d.get('move+-') else ( not d.get('transpos-prev', d['dsrd']) < d['dsrd'] > d.get('transpos-curr', d['dsrd'])) :
        await asyncio.sleep(0.5)  # to just read sensor spawn serve instance via 'python3 ....py serve 101' so pins dont get pulled high or low
        d['rawpos'] = d['range']();    d['transpos-prev'] = d.get('transpos-curr', d['dsrd']);    d['transpos-curr'] = d['translate'](d['rawpos'])
        print(d['lineup'], end=d['lineclear']);    print(f"rawpos-{d['rawpos']} transpos-prev-{d['transpos-prev']} transpos-curr-{d['transpos-curr']} desired-{d['dsrd']} move-{d.get('move+-')}")  # pretty print
        if  -1 < d['dsrd'] < 101 and not 'move+-' in d: d['move+-'] = True if d['dsrd'] > d['transpos-curr'] else False;    d['drivepin'](eval(d['pindw']) if d['move+-'] else eval(d['pinup']) , False); d['drivepin'](eval(d['pinup']) if d['move+-'] else eval(d['pindw']) , True)
    if -1 < d['dsrd'] < 101 and 'move+-' in d: d['drivepin']( eval(d['pinup']) if d['move+-'] else eval(d['pindw']) , False)

async def trysend():  # 1 will be ignored since for every 'Set tisch Brightness int' homebridge also does 'Set tisch On 1' wich would overwrite brightness int
    try: socket.create_connection(('localhost', 2222)).sendall(bytes(sys.argv[4], "utf-8")) if sys.argv[4] != '1' else sys.exit()  # try to connect to serve() socket instance and send desired pos 
    except: sub(f'screen -S tisch -d -m python3 "{pathlib.Path(__file__)}" serve "{sys.argv[4]}"', False) if sys.argv[4] != '1' else sys.exit() # no connection possible spawn serve() instance

async def tryrecv():  # try to asks serve instance for 'int' except ranges int
    try: d['transpos'] = socket.create_connection(('localhost', 2222)).recv(255).decode();    print( max( min(d['transpos'],1), 0) ) if sys.argv[3] == 'On' else print(d['transpos'])  # TODO peraps change this to raw pos and round or do max(d['rawpos'],0) to report correct hight and off state
    except: await setupvl53();    d['rawpos'] = d['range']();    d['transpos'] = d['translate'](d['rawpos']);    print( max( min(d['transpos'],1), 0) ) if sys.argv[3] == 'On' else print(d['transpos'])

    # TODO perhaps prematurly return 0 when server not found


d = {'Set': trysend, 'Get': tryrecv,'serve': serve, 'pinup': "board.G1", 'pindw': "board.G0",
     'drivepin': lambda pin, val: digitalio.DigitalInOut(pin).switch_to_output(value=val),
     'translate': lambda h: max( round( ( h - 71 )*100/(115-71) ), 0),  # TODO put round() here somewhere
     'range': lambda: d['vl53'].distance if d['vl53'].data_ready and d['vl53'].distance else 1111,  # vl53.clear_interrupt() is missing but thoretically interrupt is not relevant
     'lineup': '\033[1A', 'lineclear': '\x1b[2K'}

asyncio.run( d.get(sys.argv[1])() )  # call move

#    d['h'] = (d['range']*d['dsrd']/100) + d['down']  # translating 'desired' into hight 79 to 140
#    d['h'] = int( (d['h']-d['down'])*100/d['range'] )  # translating 'h' into 1 to 100 vlaue
