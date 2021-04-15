import os
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

characteristic = sys.argv[3].strip("''")
if charcacteristic == "name":
    print("aptv")
    sys.exit()

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)

wert = chan0.value

if wert < 40000:
    print("OCCUPANCY_DETECTED")
    
if wert > 40000:
    print("OCCUPANCY_NOT_DETECTED")

sys.exit()
