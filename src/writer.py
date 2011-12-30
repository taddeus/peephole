from math import ceil


TABSIZE = 4                 # Size in spaces of a single tab
INLINE_COMMENT_LEVEL = 6    # Number of tabs to inline commment level
COMMAND_SIZE = 8            # Default length of a command name, used for
                            # indenting
ADD_COMMENT_BLOCKS = True   # Wether to add newlines before and after
                            # non-inline comment
ADD_ARGUMENT_SPACE = False  # Wether to add a space between command arguments
                            # and the previous comma


def write_statements(statements):
    """Write a list of statements to valid assembly code."""
    out = ''
    indent_level = 0
    prev_comment = False

    for i, s in enumerate(statements):
        current_comment = False

        if s.is_label():
            line = s.name + ':'
            indent_level = 1
        elif s.is_comment():
            line = '\t' * indent_level + '#' + s.name
            current_comment = True
        elif s.is_directive():
            line = '\t' + s.name
        elif s.is_command():
            line = '\t' + s.name

            # If there are arguments, add tabs until the 8 character limit has
            # been reached. If the command name is 8 or more characers long,
            # add a single space
            if len(s):
                l = len(s.name)

                if l < COMMAND_SIZE:
                    line += '\t' * int(ceil((COMMAND_SIZE - l)
                                       / float(TABSIZE)))
                else:
                    line += ' '

                delim = ', ' if ADD_ARGUMENT_SPACE else ','
                line += delim.join(map(str, s))
        else:
            raise Exception('Unsupported statement type "%s"' % s.stype)

        # Add the inline comment, if there is any
        if s.has_inline_comment():
            start = INLINE_COMMENT_LEVEL * TABSIZE
            diff = start - len(line.expandtabs(TABSIZE))

            # The comment must not be directly adjacent to the command itself
            tabs = int(ceil(diff / float(TABSIZE))) + 1 if diff > 0 else  1

            line += '\t' * tabs + '#' + s.options['comment']

        # Add newline at end of command
        line += '\n'

        if ADD_COMMENT_BLOCKS:
            if prev_comment ^ current_comment:
                out += '\n'

        out += line
        prev_comment = current_comment

    return out


def write_to_file(filename, statements):
    """Convert a list of statements to valid assembly code and write it to a
    file."""
    s = write_statements(statements)
    f = open(filename, 'w+')
    f.write(s)
    f.close()
