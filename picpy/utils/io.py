
def fast_io(ports, **kwargs):
    if "build" in kwargs.keys():
        if kwargs["build"]:
            if ports.isinstance(list):
                pass


def toggle(pin,  **kwargs):
    if "build" in kwargs.keys():
        if kwargs["build"]:
            if isinstance(pin, list):
                return f"   BTG {pin[0]}, {pin[1]}\n"
            if isinstance(pin, str):
                return f"   BTG {pin}\n"