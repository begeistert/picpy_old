import importlib, os
from picpy.parsers.utils.asm import *
from ast import *

instances = {}
n_loop = 0
user_functions = []
asm = ASM('temp_picpy')


def get_asm(script, name):
    main_code = ''
    asm.filename = name
    for line in script:
        if isinstance(line, ImportFrom):
            if 'picpy.devices' in line.module:
                get_pic_instance(line.module)
            elif '.utils.' in line.module:
                instances["utils"] = importlib.import_module(line.module)
            else:
                instances[line.module] = importlib.import_module(line.module)
        elif isinstance(line, Expr):
            if isinstance(line.value, Call):
                if line.value.func.id in dir(instances['processor']):
                    # print(f"{line.value.func.id} is a proc function")
                    if line.value.func.id in ['fuses', 'build', 'delay']:
                        kwargs = keywords_to_dict(line.value.keywords)
                        code = getattr(instances['processor'], line.value.func.id)(**kwargs)
                        if line.value.func.id == 'fuses':
                            asm.config_zone = code
                        elif line.value.func.id == 'build':
                            asm.code_zone['Pre-Main'] = code
                        else:
                            main_code += code
                    if line.value.func.id == 'org':
                        pass
                elif line.value.func.id in user_functions:
                    # print(f"{line.value.func.id} is a user function")
                    main_code += f'   CALL {line.value.func.id}\n'
                else:
                    # print(f'Function {line.value.func.id} not defined')
                    pass
            pass
        elif isinstance(line, FunctionDef):
            set_function(line)
        elif isinstance(line, Assign):
            pass
        elif isinstance(line, While):
            main_code += make_while(line)
    asm.set_main_code(main_code)
    asm.build_asm_file()
    output = os.popen(f'gpdasm -p{instances["processor"].pic} -i {asm.filename}.hex').readlines()
    for out in output:
        if 'number of bytes' in out:
            out = out.strip()
            print(f'Memory used: {out.replace("number of bytes -> ", "")} bytes')
            break


def make_while(loop):
    name = f'Loop_{n_loop}'
    code = ''
    inf = False
    if isinstance(loop.test, Compare):
        pass
    if isinstance(loop.test, NameConstant):
        if isinstance(loop.test.value, bool):
            inf = loop.test.value
    for line in loop.body:
        if isinstance(line, For):
            pass
        elif isinstance(line, Assign):
            for target in line.targets:
                if isinstance(target, Attribute):
                    # print(f'{line.value.n} is assigned to the attribute {line.targets[0].attr} of variable {
                    # line.targets[0].value.id} in function {name}')
                    if line.targets[0].value.id in dir(instances["processor"]):
                        # print(f'{line.targets[0].value.id} is a proc attribute')
                        code += assign_proc_prop(line.targets[0],
                                                 line.value.n)  # Esto debe hacerse para todas las propiedades
                elif isinstance(target, Name):
                    # print(f'{line.value.n} is assigned to {line.targets[0].id} in function {name}')
                    if line.targets[0].id in dir(instances["processor"]):
                       # print(f'{line.targets[0].id} is a proc attribute')
                        pass
                    else:
                        # print(f'{line.targets[0].id} is not a proc attribute')
                        pass
    if inf:
        code += f'   GOTO {name}'
    asm.define_function(name, None, code)
    return f'   GOTO {name}'


def keywords_to_dict(keywords):
    new_keywords = {
        'build': True
    }
    for keyword in keywords:
        if isinstance(keyword.value, Name):
            if keyword.value.id in dir(instances['processor']):
                new_keywords[keyword.arg] = getattr(instances['processor'], keyword.value.id)
            else:
                new_keywords[keyword.arg] = keyword.value.id
        elif isinstance(keyword.value, Num):
            new_keywords[keyword.arg] = keyword.value.n

    return new_keywords


def get_pic_instance(processor):
    instances["processor"] = importlib.import_module(processor)
    asm.proc(instances["processor"].pic)


def set_function(function):
    name = function.name
    user_functions.append(name)
    args = function.args.args
    defaults = function.args.defaults
    code = ''
    for line in function.body:
        if isinstance(line, Expr):
            if isinstance(line.value, Call):
                if line.value.func.id in dir(instances['processor']):
                    # print(f"{line.value.func.id} is a proc function")
                    pass
            pass
        elif isinstance(line, FunctionDef):
            set_function(line)
        elif isinstance(line, Assign):
            for target in line.targets:
                if isinstance(target, Attribute):
                    # print(f'{line.value.n} is assigned to the attribute {line.targets[0].attr} of variable {
                    # line.targets[0].value.id} in function {name}')
                    if line.targets[0].value.id in dir(instances["processor"]):
                        # print(f'{line.targets[0].value.id} is a proc attribute')
                        code += assign_proc_prop(line.targets[0], line.value.n)  # Esto debe hacerse para todas las propiedades
                elif isinstance(target, Name):
                    # print(f'{line.value.n} is assigned to {line.targets[0].id} in function {name}')
                    if line.targets[0].id in dir(instances["processor"]):
                        # print(f'{line.targets[0].id} is a proc attribute')
                        pass
                    else:
                        # print(f'{line.targets[0].id} is not a proc attribute')
                        pass
    code += '   RETURN\n'
    asm.define_function(name, args, code)


def assign_proc_prop(target, value):
    line = ''
    if target.value.id in ('TRIS', 'PORT', 'LAT'):
        if value > 0:
            line = f'   MOVLW   {hex(value)}\n' \
                   f'   MOVWF   {target.value.id}{target.attr}\n'
        else:
            line = f'   CLRF    {target.value.id}{target.attr}\n'

    return line

