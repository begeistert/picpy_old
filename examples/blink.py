from picpy.devices.p18f45k50 import *

fuses(wdt=off, mclr=on, debug=off, lvp=off, fosc=intoscio)
build(reset=0x02000, interrupt=0x02008)
delay(internal=INT_4M)


def init():
    TRIS.A = 0xFE


init()
LED = PORT.A[0]

while True:
    toggle(LED)
    delay_ms(500)

