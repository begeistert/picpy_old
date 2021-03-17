from picpy.utils.base import PortList, TrisList

config = "CONFIG"
fuses_asm = {
    "wdt": "WDTEN",
    "mclr": "MCLRE",
    "debug": "DEBUG",
    "lvp": "LVP",
    "fosc": "FOSC"
}


def fuses(**kwargs):
    """
    Función que define las configuraciones del PIC seleccionado

    Las configuraciones disponibles son:

    wdt: Watchdog \n
    mclr: MCLR \n
    debug: Debug enable \n
    lvp: \n
    fosc: Oscilador

    :return: None
    """
    if "build" in kwargs.keys():
        if kwargs["build"]:
            del kwargs["build"]
            code = ""
            for key, value in kwargs.items():
                code += f"   {config} {fuses_asm[key]} = {value}\n"
            return code
    else:
        pass
