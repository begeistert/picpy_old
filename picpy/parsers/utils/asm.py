import os

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
        self.cblock = []
        self.variables = {}
        self.var_alloc = 0x00
        self.config_zone = ''
        self.mask_zone = ''
        self.variables = {}
        self.code_zone = {
            "Pre-Main": '',
            "Main": '',
            'main': [],
            "functions": {},
            "footers": ''
        }
        self.tables = {}
        self.foo = {}
        self.n_loop = 0

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

    def delete_dependencies(self):
        dependencies = self.code_zone['footers'].strip('\n')
        if isinstance(dependencies, list):
            for dependency in dependencies:
                dependency = dependency.strip()
                dependency = dependency.replace("INCLUDE <", '')
                dependency = dependency.replace(">", '')
                os.remove(f'{os.path.dirname(self.filename)}/{dependency}')
        else:
            dependencies = dependencies.strip()
            dependencies = dependencies.replace("INCLUDE <", '')
            dependencies = dependencies.replace(">", '')
            os.remove(f'{os.path.dirname(self.filename)}/{dependencies}')

    def build_asm_file(self):
        code = ''
        code += self.header
        code += self.config_zone + '\n'
        cblock = "".join(self.cblock)
        code += f'   CBLOCK  0x0C\n{cblock}   ENDC\n\n'
        code += self.mask_zone + '\n'
        code += self.code_zone['Pre-Main']
        code += f'Main: \n{self.code_zone["Main"]}\n'
        for key, value in self.code_zone['functions'].items():
            code += f'{key}:\n{value["code"]}'
        for key, value in self.tables.items():
            code += f'{key}:\n{value["code"]}'
        code += self.code_zone['footers']
        code += '\n   END'
        asm_file = open(f'{self.filename}.asm', 'w')
        asm_file.write(code)
        asm_file.close()
        # self.delete_dependencies()

    def call(self, subroutine, context):
        _call = f'   CALL {subroutine}'
        self.code_zone[context].append(_call)

    def bra(self, subroutine, context):
        _bra = f'   BRA {subroutine}'
        self.code_zone[context].append(_bra)

    def goto(self, destiny, context):
        _goto = f'   GOTO {destiny}'
        self.code_zone[context].append(_goto)
