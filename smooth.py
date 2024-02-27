
import array
import board
import time
import rp2pio
import adafruit_pioasm
import digitalio
import math
import ulab
import supervisor


stepdir = adafruit_pioasm.assemble( """
.program stepdir
.side_set 1 opt

loop:                ; requires 18delaybits 14endbits in this order
    pull block         ; 1 pull waits on fresh tx fifo, also here init populates inital y/curpos
    out x 18           ; 2 afterwards osr/14endbits-18bufferzeros, x/14bufferzeros-18delaybits

pause:               ; pause for bussy cycles of delay count                  
    jmp x-- pause  [7]  ; 3 x/delay non zero stay in pause and decr x/delay otherwise continue

prepfinddir:         ; prep x/endpos for comparison, y/curpos already preped since init or later since finddir
    out x 14           ; 4 afterwards osr/32bufferzeros, x/18bufferzeros-14endposbits

    mov osr x          ; 5 afterwards osr/endpos, also no race condition here since no auto pull
    mov isr y  side 0  ; 6 afterwards isr/curpos so y/curpos stays persistant while finddir, also side/setppin alias enter lowtime for >100ns

    jmp x!=y finddir   ; 7 y/curpos not x/endpos finddir otherwise nofinddir alias re loop
    jmp preploop       ; 8 


finddir:
    mov x osr      ; 1 cycle osr/endpos isr/curpos with x/interim save
    mov osr isr    ; 2 shift msb bit of here osr/curpos out
    mov isr x      ; 3 either write carrypin 1 for curpos 0 alias perhaps posdir
    out x 1        ; 4     or write carrypin 0 for curpos 1 alias perhaps negdir
    mov pins ~x    ; 5

    mov x osr      ; 6 cycle x/osr/isr
    mov osr isr    ; 7 shift msb bit of here osr/endpos out
    mov isr x      ; 8 and verifiy possible dir
    out x 1        ; 9

    jmp pin pssblposdir    ; 10 curpos1 alias verify possible negdir
        jmp x-- finddir    ; 11 but endpos1 re finddir    !!! x0 -> xfffff , x1 -> x0    

        jmp y-- goon  [1]  ; 12 but endpos0 found dir so decrement y/peristant curpos       !!! if scratch Y non-zero, prior to decrement
        goon:
        set pins 0         ; 13 setpin/dirpin to negdir, also dirpin to steppin time > 20ns tmc2209 13.1
        jmp compensate     ; 14 nops for same time as posdir case

    pssblposdir:           ; curpos0 alias verify possible posdir   
        jmp !x finddir     ; 15 but endpos0 re findir

        mov y ~y           ; 16 but endpos1 found dir so increment y/persitant curpos
        jmp y-- pers       ; 17                                                         !!! if scratch Y non-zero, prior to decrement
        pers:
        mov y ~y           ; 18 
        set pins 1         ; 19 setpin/dirpin to posdir, also dirpin to steppin time > 20ns tmc2209 13.1

compensate:             ; per leftover bit in osr/endpos do nothing for 11instr, alos only odd endposses valid
    out x 1          [4]  ; 20 deplete osr/endpos bit after bit
    mov x osr        [4]  ; 21 until osr/endpos zero alias depleted last odd bit then proceede
    jmp x-- compensate    ; 22 else x non zero stay in compensate

    in y 32       side 1  ; 23 this stalls on full rx fifo, also y persists, also enter side/setppin alias enter hightime

preploop:
    push noblock  ; 9 explicit push solves auto push stall aboveus, also clears isr

""" )


pwmin = adafruit_pioasm.assemble( """
.program PwmIn

init:
    mov y ~null         ; start with the value 0xFFFFFFFF
    mov x ~null         ; start with the value 0xFFFFFFFF
    wait 0 pin 0        ; wait for a 0
    wait 1 pin 0        ; wait for a 1, now we really have the rising edge
hightime:               ; loop for high period
    jmp y-- stillhigh   ; count down for pulse width
    jmp init            ; timer has reached 0, stop count down of pulse, restart
stillhigh:
    jmp pin hightime    ; test if the pin is still 1, if so, continue counting down
lowtime:                ; loop for low period
    jmp pin stop        ; if the pin has become 1, the period is over, stop count down
    jmp x-- lowtime     ; if not: count down
    jmp init            ; timer has reached 0, stop count down of low period, restart
stop:
    mov isr ~y          ; move the value ~y to the ISR: the high period (pulsewidth) (0xFFFFFFFF-y)
    push noblock        ; push the ISR into the Rx FIFO
    mov isr ~x          ; move the value ~x to the ISR: the low period (0xFFFFFFFF-x)
    push noblock        ; push the ISR into the Rx FIFO
""" )




def initsmout(initpos):  # smout waitis for tx fifo so this init has time to prefill y/curpos
    for bit in range(initpos.bit_length() - 1, -1, -1):
        smout.run(adafruit_pioasm.assemble(f"set y {(initpos >> bit) & 1}"))  # form msb to lsb shift bit per bit of initpos into isr
        smout.run(adafruit_pioasm.assemble("in y 1"))   # requires left in shift

    smout.run(adafruit_pioasm.assemble("mov y isr"))  # init y/curpos with isr
    send(initpos, 60000)  # kickoff alias release smout with first backgroundwrite

def dm2282(bool):
    enablepin.switch_to_output(value= not bool ); enabsign.switch_to_output(value= bool )  # dm2282 enable low is on wich is default on reboot enable high is off

def send(endpos, pause):  # send delay and endpos to smout
    smout.background_write(loop=array.array( 'L', [((pause<<14)+endpos)] ))  # 18bit pause shifted 14bits to the left to leave room for endpos

def curpos():
    curposbuff = array.array('L', [32]); smout.clear_rxfifo();  # prep buff and clear rx fifo

    while smout.in_waiting < 1:  # wait until words in in rx fifo
        pass

    smout.readinto(curposbuff)
    return curposbuff[0]





""" hue procentages are not linerar to pwm hightime so fit a curve to it

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def polynomial_func(x, f, a, b, c, d):  # Define the polynomial function
    return f * np.log(x)**2 + a * x**3 + b * x**2 + c * x + d

y_data = np.array([100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 0])  # ydata is hue setting
x_data = np.array([62498, 56458, 51167, 45740, 40633, 36199, 31705, 27529, 23956, 20390, 17384, 14432, 11798, 9650, 7630, 5926, 4637, 3546, 2776, 2345, 2195])  # xdata is hightime

params, covariance = curve_fit(polynomial_func, x_data, y_data)  # Fit the polynomial function to the data

f, a, b, c, d = params  # extract the coefficients (f, a, b, c, d)

fitted_curve = polynomial_func(x_data, f, a, b, c, d)  # generate the fitted curve

# Plot the data and the fitted curve
plt.scatter(x_data, y_data, label="Data")
plt.plot(x_data, fitted_curve, color='red', label="Polynomial Fit")
plt.xlabel("hue %"); plt.ylabel("hightime of pwm"); plt.legend(); plt.show()

"""

def logpoly(x):  # translate hightimte into procentage 0 to 100 on it ab 20 bad at <5 found via look up
    f= 22.566232819279517; a= -1.7203472030903148e-13; b= 2.095672920474736e-08; c= -0.000310573490816624; d= -170.03832854916905
    return f * math.log(x) + a * x**3 + b * x**2 + c * x + d

def mess():
    while ttointerval() < 1:  # stay here and watch for emergancy stop until min one ms has passed so T>0 for simulation
    
        hightimebuff = array.array("L", [0]); lowtimebuff = array.array("L", [0]); smin.clear_rxfifo()  # clear rx fifo to do messurement

        while smin.in_waiting < 2:  # wait until 2 words in in rx fifo so when hue off then loop is stuck here so emergancy stop after a waittime
            if ttointerval() > 4: dm2282(True); supervisor.reload()  # emergancy stop after 4ms no reading  # reload alias ctrl d is save since dm2282 stayes enabled plus this is called upon reload first so hangs here until readings are available

    smin.readinto(hightimebuff); smin.readinto(lowtimebuff)

    highns = hightimebuff[0]*2*8; lowns = lowtimebuff[0]*2*8; periodns = highns+lowns; pwminfreq = int(1e+9/periodns); endpospercentage = int(logpoly(hightimebuff[0])); k = -0.4;
    
    endposshifted = ( ((k-1)*(2*(endpospercentage/100)-1)) / (2*( 4k*abs((endpospercentage/100)-0,5) -k -1)) )+0.5  # shift values form 0 to 1 along a sigmoid curve so that fine control near end positions and rough fast contorll in between
    endpossteps = int(ulab.numpy.interp(endposshifted,[0,1],[11,16001])[0]);  # than convert sigmoid shaped endposition into endpossteps

    endposodd = 2*math.floor(endpossteps/2)+1  # translate endpos to step position 11 to 15001 and ensure odd endpos

    return endposodd, endpossteps, endpospercentage, pwminfreq

def ttointerval():
    return (supervisor.ticks_ms() - interval) & tmax; T = ( ((T + thalfperiod) & tmax) - thalfperiod )  # wrap save interval calc see docs super ticks ms plus convert superticks ms interval into s




def colored(char, color):  # github.com/kroitor/asciichart/
    return color + char + "\033[0m"

red = "\033[31m"; green = "\033[32m"; yellow = "\033[33m"; blue = "\033[34m"; magenta = "\033[35m"; cyan = "\033[36m"; default = "\033[39m"; lightred = "\033[91m"; lightgreen = "\033[92m"; lightyellow = "\033[93m"; lightblue = "\033[94m"; lightmagenta = "\033[95m"; lightcyan = "\033[96m"

def plot(series, cfg={}, colors=[lightmagenta, blue], symbols=['┼', '┤', '╶', '╴', '─', '╰', '╭', '╮', '╯', '│']):  # current asumption is two series in nested list
    minimum = cfg.get('min', min(filter(math.isfinite, [j for i in series for j in i])))
    maximum = cfg.get('max', max(filter(math.isfinite, [j for i in series for j in i])))

    interval = maximum - minimum
    offset = cfg.get('offset', 3)
    height = cfg.get('height', interval)
    ratio = height / interval if interval > 0 else 1

    min2 = int(math.floor(minimum * ratio))
    max2 = int(math.ceil(maximum * ratio))

    def clamp(n):
        return min(max(n, minimum), maximum)

    def scaled(y):
        return int(round(clamp(y) * ratio) - min2)

    rows = max2 - min2

    width = 0
    for i in range(0, len(series)):
        width = max(width, len(series[i]))
    width += offset

    result = [[' '] * width for i in range(rows + 1)]

    # axis and labels
    for y in range(min2, max2 + 1):
        label = '{:8.0f} '.format(maximum - ((y - min2) * interval / (rows if rows else 1)))
        result[y - min2][max(offset - len(label), 0)] = label
        result[y - min2][offset - 1] = symbols[0] if y == 0 else symbols[1]  # zero tick mark

    # first value is a tick mark across the y-axis
    d0 = series[0][0]
    if math.isfinite(d0):
        result[rows - scaled(d0)][offset - 1] = symbols[0]

    for i in range(0, len(series)):

        color = colors[i % len(colors)]

        # plot the line
        for x in range(0, len(series[i]) - 1):
            d0 = series[i][x + 0]
            d1 = series[i][x + 1]

            if math.isnan(d0) and math.isnan(d1):
                continue

            if math.isnan(d0) and math.isfinite(d1):
                result[rows - scaled(d1)][x + offset] = colored(symbols[2], color)
                continue

            if math.isfinite(d0) and math.isnan(d1):
                result[rows - scaled(d0)][x + offset] = colored(symbols[3], color)
                continue

            y0 = scaled(d0)
            y1 = scaled(d1)
            if y0 == y1:
                result[rows - y0][x + offset] = colored(symbols[4], color)
                continue

            result[rows - y1][x + offset] = colored(symbols[5], color) if y0 > y1 else colored(symbols[6], color)
            result[rows - y0][x + offset] = colored(symbols[7], color) if y0 > y1 else colored(symbols[8], color)

            start = min(y0, y1) + 1
            end = max(y0, y1)
            for y in range(start, end):
                result[rows - y][x + offset] = colored(symbols[9], color)

    result.append([f"{round(minimum,5)}min/{round(maximum,5)}max clamp, {round(width,5)}x/{round(height,5)}y scale, { ', '.join( map(colored, [str(x[-1])[:5] + n for x in series for n in cfg.get('names', [''])] , colors ) ) }"])

    # whipe lines
    for i in range(0,len(result)):  # plus -1 to scroll plot to the top or 0 to keep plot at position
        print('\033[1A', end='\x1b[2K')

    print(f"{chr(10).join([''.join(row).rstrip() for row in result])}")  # chr(10) is \n





huepin = board.A0; carrypin = board.D24; setppin = board.NEOPIXEL0; dirpin = board.NEOPIXEL1; enablepin = digitalio.DigitalInOut(board.NEOPIXEL2); enabsign = digitalio.DigitalInOut(board.LED);

smout = rp2pio.StateMachine(
    program         = stepdir,
    frequency       = 0,
    out_shift_right = False,  # out shift left for finddir
    in_shift_right  = False,  # in shift left for priming/init y/curpos, i32

    first_in_pin              = carrypin ,  # inpin is carrypin for i5, i10 of finddir
    in_pin_count              = 1,

    jmp_pin                   = carrypin,   # jmppin is carrypin for i10 of finddir

    first_out_pin             = carrypin,   # outpin is carrypin for i5 of finddir
    out_pin_count             = 1,
    initial_out_pin_state     = 0,
    
    first_set_pin             = dirpin,     # setpin is dirpin for i12, i16 of finddir
    set_pin_count             = 1,  
    initial_set_pin_state     = 0,

    first_sideset_pin         = setppin,    # sidepin is setppin
    sideset_pin_count         = 1,
    initial_sideset_pin_state = 0,
    sideset_enable            = True,
)

smin = rp2pio.StateMachine(
    pwmin,                  # load programm
    frequency=0,            # use chip freq 125Mhz
    
    jmp_pin=huepin,         # set the 'jmp' pin
    
    first_in_pin=huepin,    # set the 'wait' pin (uses 'in' pins)

    pull_in_pin_down=1,     # ???? but pull down prolly
    
    in_shift_right=False,   # set shift direction
)




# for testing just import in from repl # from code import initsmout, send, curpos, mess, plot

initsmout(mess()[0])  # init with inital hue reading plus when hue off hangs aka reloads aka ctrlds here this also assumes hue steyes connected while ctrl ds otherwise hue recovery resets hue to arbetrary value miss aligning curpos and endpos

endposlist = curposlist = [mess()[0], mess()[0]]; delaylist = difflist = speedlist = [0, 0]

x = y = mess()[0]; yd = 0; f, z, r = 0.014, 0.8, 0  # constants for sec order dyn system z 1 is critical damp z < 1 is over shoot but pio stops when curpos matches endpos so
k1 = z / (math.pi * f); k2 = 1 / ((2 * math.pi * f) * (2 * math.pi * f)); k3 = r * z / (2 * math.pi *f)

tperiod = 1<<29; tmax = tperiod-1; thalfperiod = tperiod//2; interval = supervisor.ticks_ms()  # timing related consts




while True:
    endposlist.append(mess()[0]); curposlist.append(curpos());

    # FIRST TEST ENDPOSITIONS currently 5% basline at 495 and upper positon 98% at 15517 BUT PAY ATTENTION TO SIGMOID SHAPE !!!!
    # dm2282(False) if endposlist == curposlist and ( all( 475 <= e <= 525 for e in curposlist) or all( 15475 <= e <= 15525 for e in curposlist) ) else dm2282(True)  # determine basline for stable positions also requires hue recovery aligned with stable position 


    # TODO !!!! do sth with diff eg when to high brake brake brake brake 
    difflist.append(abs(y - curposlist[-1]))  # reality gap alias diff between curpos reported of pio and simulated pos since yd can escalate but delay is clamped for safety

    
    T = ttointerval() / 1000; interval = supervisor.ticks_ms()  # T in sec >1 since mess min 1ms plus reset interval
    xd = (endposlist[-1] - endposlist[-2]) / T  # estimate xd this is from t3ssel8r of procedural animation semi implicit euler for y + k1y' + k2y'' = x + k3x' 
    y = y + T * yd  # clac somooth y from yd
    yd = yd + T * (endposlist[-1] + k3*xd   - y - k1*yd ) / k2; speedlist.append(yd)  # clac speed attentione this can escalate  # TODO PERHAPS CLAMP YD HERE SO SIM AND REALWORLD STY IN SYNC PLUS NO NEED TO CLAMP FOR SAFETY LATER PLUS NO NEED TO CHECK FOR DEVISION BY 0 IN CONVERSION FROM YD TO DELAY  but difficulties arrise cause yd can be -600 to 600

    if endposlist[-1] == curposlist[-1]: x = y = endposlist[-1]; yd = 0;  # check curpos endpos match since smout stops on zero delta rehome and reset simulation

    delaylist.append( ((1e+9/abs(yd)) - 1352) / 64 ) if yd > 0 else delaylist.append(150000)  # T is in s, y is in steps so yd is steps/sec so sec/setp is 1/yd is delay so actually 1352ns + (64ns*delay) = 1e9ns/yd

    send(endposlist[-1], max(25000, min(150000, delaylist[-1] )) )  # first 14bitendpos(1-16.383) than 18bitdleay(1-262.143) only odd numbers  # attentione this is clamped so delay does not escalate

    plot([endposlist, curposlist, difflist], {'hue': "on", 'height': 20})

    if len(endposlist) > 50:  # plot length thi is about the limit 
        del curposlist[0]; del endposlist[0]; del delaylist[0]; del difflist[0]; del speedlist[0]






















