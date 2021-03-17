from .parsers import *
from ast import parse
import os


def build(path):
    script = parse(open(path).read()).body
    get_asm(script, os.path.basename(path).replace('.py', ''))


def gpasm_swd(path):
    pass

