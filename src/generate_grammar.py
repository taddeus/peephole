#!/usr/bin/python
argmap ={'REG': 'WORD'}

def command(name, args):
    """Generate grammar code to be pasted in grammar.y for a sinle MIPS
    command."""
    argc = len(args)
    mapped_args = [argmap[arg] if arg in argmap else arg for arg in args]
    code = '"%s" %s {\n' % (name, ' COMMA '.join(mapped_args))
    code += '\t\tchar **argv = (char **)malloc(%d * sizeof(char *));\n' % argc
    code += '\t\tint *argt = (int *)malloc(%d * sizeof(int));\n' % argc

    for i, argtype in enumerate(args):
        code += '\t\targv[%d] = $%d;\n' % (i, i * 2 + 2)
        code += '\t\targt[%d] = ARG_%s;\n' % (i, argtype)

    code += '\t\tadd_line(TYPE_CMD, %s, %d, argv, argt);\n' % (name, argc)
    code += '\t}\n'

    return code

# Define commands
commands = [ \
            (['add', 'sub'], ['REG'] * 3), \
            (['addi', 'subi'], ['REG', 'REG', 'INT']), \
        ]

# Generate 'command' grammar
cmd = []

for names, args in commands:
    for name in names:
        cmd.append(command(name, args))

code = 'commands:\n\t%s\t;\n' % '\t| '.join(cmd)

print code
