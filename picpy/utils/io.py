
def fast_io(ports, **kwargs):
    if "build" in kwargs.keys():
        if kwargs["build"]:
            if ports.isinstance(list()):
                pass
