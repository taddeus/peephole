from math import ceil


def write_statements(statements):
    """Write a list of statements to valid assembly code."""
    out = ''
    indent_level = 0
    prevline = ''

    for i, s in enumerate(statements):
        newline = '\n' if i else ''

        if s.is_label():
            line = s.name + ':'
            indent_level = 1
        elif s.is_comment():
            line = '#' + s.name

            if s.is_inline_comment():
                l = len(prevline.expandtabs(4))
                tabs = int(ceil((24 - l) / 4.)) + 1
                newline = '\t' * tabs
            else:
                line = '\t' * indent_level + line
        elif s.is_directive():
            line = '\t' + s.name
        elif s.is_command():
            line = '\t' + s.name

            if len(s):
                if len(s.name) < 8:
                    line += '\t'
                else:
                    line += ' '

                line += ','.join(s.args)
        else:
            raise Exception('Unsupported statement type "%s"' % s.stype)

        out += newline + line
        prevline = line

    # Add newline at end of file
    out += '\n'

    return out

def write_to_file(filename, statements):
    """Convert a list of statements to valid assembly code and write it to a
    file."""
    s = write_statements(statements)
    f = open(filename, 'w+')
    f.write(s)
    f.close()
