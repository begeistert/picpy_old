class ASM:
    """
    A class used to represent an asm file

    Attributes
    ----------
    @processor : str
        a formatted string to define the pic to use
    @config_zone : dict
        a dict to define the config directives
    @variables : dict
        a dict to define the variables to use

    The dict variables represent a list of all variables required by the asm program.
    """

    def __init__(self, filename):
        self.success = True
        self.filename = filename
        self.header = ""
        self.variables = {}
        self.var_alloc = 0x00
        self.config_zone = ''
        self.variables = {}
        self.code_zone = {
            "Pre-Main": '',
            "Main": '',
            "functions": {}
        }
        self.foo = {}

    def set_main_code(self, code):
        self.code_zone['Main'] = code

    def proc(self, pic):
        self.header = f'   LIST P = {pic}\n   #include "p{pic}.inc"\n\n'

    def config_directives(self, code):
        self.config_zone = code

    def define_function(self, name, args, code):
        self.code_zone['functions'][name] = {}
        self.code_zone['functions'][name]['args'] = args
        self.code_zone['functions'][name]['code'] = code

    def define_var(self, name):
        self.variables[name] = "{} EQU {}".format(name, hex(self.var_alloc))
        self.var_alloc += 1
        print(self.variables)

    def build_asm_file(self):
        code = ''
        code += self.header
        code += self.config_zone
        code += self.code_zone['Pre-Main']
        code += f'Main\n{self.code_zone["Main"]}\n'
        for key, value in self.code_zone['functions'].items():
            code += f'{key}\n{value["code"]}'
        code += '\n   END'
        asm_file = open(f'{self.filename}.asm', 'w')
        asm_file.write(code)
        asm_file.close()
        print("Finished")
