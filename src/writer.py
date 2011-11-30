def write_statements(statements):
    '''Write a list of statements to valid assembly code.'''
    s = '';

    for i, statement in enumerate(statements):
        statement_type, name, args = statement
        newline = '\n' if i else ''

        if statement_type == 'label':
            line = name + ':'
        elif statement_type == 'comment':
            line = '#' + name

            if args['inline']:
                newline = '  '
        elif statement_type == 'directive':
            line = '\t' + name
        elif statement_type == 'command':
            line = '\t' + name + '\t' + ','.join(args['args'])
        else:
            raise Exception('Unsupported statement type "%s"' % statement_type)

        s += newline + line

    return s

def write_to_file(filename, statements):
    '''Convert a list of statements to valid assembly code and write it to a
    file.'''
    s = write_statements(statements)
    f = open(filename, 'w+')
    f.write(s)
    f.close()
