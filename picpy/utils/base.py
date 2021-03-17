

def build(reset=0x02000, interrupt=0x02008, **kwargs):
    if "build" in kwargs.keys():
        if kwargs["build"]:
            return f"\n   ORG     {hex(reset)}\n" \
                    f"   GOTO    {hex(interrupt)}\n" \
                    f"   ORG     {hex(interrupt)}\n\n"


def org(vectors: list):
    for vector in vectors:
        print(vector)


class TrisList(dict):
    def __init__(self, limit: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        j = 0
        for i in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
            self.setdefault(i, 0xff)
            j += 1
            if i == limit:
                break
        self.__dict__ = self


class PortList(dict):

    def __init__(self, limit: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        j = 0
        for i in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
            self.setdefault(i, 0xff)
            j += 1
            if i == limit:
                break
        self.__dict__ = self
