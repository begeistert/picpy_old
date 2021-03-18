from picpy.devices.p18f45k50 import *

fuses(wdt=off, mclr=on, debug=off, lvp=off, fosc=intoscio)
build(reset=0x02000, interrupt=0x02008)
org([0x0000, 0x1FFF])
delay(internal=INT_4M)
fast_io([PORT.A, PORT.B])
display = (0x3f, 0x06, 0X5b, 0x4f, 0x66,
           0x6d, 0x7d, 0x07, 0x7f, 0x6f)


def init():
    TRIS.A = 0xff
    TRIS.B = 0x00
    PORT.B = 0x00


init()
while True:
    for dec in display:
        for ud in display:
            PORT.A = 2
            PORT.B = ud
            delay_ms(50)
            if dec == 0:
                PORT.A = 3
            else:
                PORT.A = 1
            PORT.B = dec
            delay_ms(50)
