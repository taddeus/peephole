from math import ceil

def write_statements(statements):
    '''Write a list of statements to valid assembly code.'''
    s = ''
    indent_level = 0
    prevline = ''

    for i, statement in enumerate(statements):
        statement_type, name, args = statement
        newline = '\n' if i else ''

        if statement_type == 'label':
            line = name + ':'
            indent_level = 1
        elif statement_type == 'comment':
            line = '#' + name

            if args['inline']:
                l = len(prevline.expandtabs(4))
                tabs = int(ceil((24 - l) / 4.)) + 1
                newline = '\t' * tabs
            else:
                line = '\t' * indent_level + line
        elif statement_type == 'directive':
            line = '\t' + name
        elif statement_type == 'command':
            line = '\t' + name

            if len(args['args']):
                l = len(name)

                if l < 8:
                    line += '\t'
                else:
                    line += ' '

                line += ','.join(args['args'])
        else:
            raise Exception('Unsupported statement type "%s"' % statement_type)

        s += newline + line
        prevline = line

    return s

def write_to_file(filename, statements):
    '''Convert a list of statements to valid assembly code and write it to a
    file.'''
    s = write_statements(statements)
    f = open(filename, 'w+')
    f.write(s)
    f.close()
