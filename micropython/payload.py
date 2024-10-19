import math
import time
import neopixel
import machine
from machine import Pin, SoftI2C
import ssd1306

i2c = SoftI2C(scl=Pin(25), sda=Pin(21), freq=100000)

# using default address 0x3C
display = ssd1306.SSD1306_I2C(128, 64, i2c)


p = machine.Pin(27, machine.Pin.OUT)
n = neopixel.NeoPixel(p, 1)

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5008))
   

def loop():

    data, source = sock.recvfrom(1025)
    
    display.buffer[:] = data[1:]
    display.mirror()
    display.show()
    display.contrast(data[0])  # bright
    
    time.sleep(0.1)

try:
    display.poweron()      # power on the display, pixels redrawn
    display.contrast(255)  # bright
    while True:
        loop()
except Exception as e:
    print(e)
    with open('exception.txt', 'w') as f:
        f.write(str(e))
        f.write("\n")
