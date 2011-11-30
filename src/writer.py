def write_statements(statements):
    s = '';

    for i, statement in enumerate(statements):
        statement_type, name, args = statement
        newline = '\n' if i else ''

        if statement_type == 'label':
            line = name + ':'
        elif statement_type == 'comment':
            line = '#' + name

            if args['inline']:
                newline = '\t\t'
        elif statement_type == 'directive':
            line = '\t' + name
        elif statement_type == 'command':
            line = '\t' + name + '\t' + ','.join(args['args'])
        else:
            raise Exception('Unsupported statement type "%s"' % statement_type)

        s += newline + line

    return s
