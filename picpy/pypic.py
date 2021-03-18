from .parsers import *
from ast import parse
import os


def build(path):
    script = parse(open(path).read()).body
    get_asm(script, path)


def gpasm_swd(path):
    pass

