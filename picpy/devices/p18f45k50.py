from picpy.utils import *
from picpy.devices.pic18 import fuses

PORT = PortList("E")
TRIS = TrisList("E")

pic = "18f45k50"

xtal = "XTAL"
intoscio = "INTOSCIO"

INT_16M = 0x09
INT_8M = 0x0
INT_4M = 0x53
INT_2M = 0x0
INT_1M = 0x0
INT_500k = 0x0
INT_250k = 0x0
"""
PORT_A = {
    "value": 0x00,
    0: "PORTA, 0",
    1: "PORTA, 1",
    2: "PORTA, 2",
    3: "PORTA, 3",
    4: "PORTA, 4",
    5: "PORTA, 5",
    6: "PORTA, 6",
    7: "PORTA, 7"
}
"""

LAT_A = 0X00
LAT_B = 0X00
LAT_C = 0X00
LAT_D = 0X00


def delay(**kwargs):
    if "build" in kwargs.keys():
        if kwargs["build"]:
            return "   MOVLW {}\n" \
                   "   MOVWF OSCCON\n".format(hex(kwargs["internal"]))
    else:
        pass

