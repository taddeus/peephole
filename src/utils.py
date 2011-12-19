import re

class Statement:
    def __init__(self, stype, name, *args, **kwargs):
        self.stype = stype
        self.name = name
        self.args = args
        self.options = kwargs

    def __getitem__(self, n):
        """Get an argument."""
        return self.args[n]

    def __eq__(self, other):
        """Check if two statements are equal by comparing their type, name and
        arguments."""
        return self.stype == other.stype and self.name == other.name \
                and self.args == other.args

    def is_comment(self):
        return self.stype == 'comment'

    def is_inline_comment(self):
        return self.is_comment() and self.options['inline']

    def is_directive(self):
        return self.stype == 'directive'

    def is_label(self):
        return self.stype == 'label'

    def is_command(self):
        return self.stype == 'command'

    def is_jump(self):
        """Check if the statement is a jump."""
        return self.is_command() \
               and re.match('^j|jal|beq|bne|blez|bgtz|bltz|bgez|bct|bcf$', \
                            self.name)

    def is_shift(self):
        """Check if the statement is a shift operation."""
        return self.is_command() and re.match('^s(ll|la|rl|ra)$', self.name)

    def is_load(self):
        """Check if the statement is a load instruction."""
        return self.is_command() and self.name in ['lw', 'dlw', 'l.s', 'l.d']

    def is_arith(self):
        """Check if the statement is an arithmetic operation."""
        return self.is_command() \
               and re.match('^(add|sub|mult|div|abs|neg)(u|\.d)?$', self.name)

    def jump_target(self):
        """Get the jump target of this statement."""
        if self.is_jump():
            return self[-1]
        else:
            raise Exception('Command "%s" has no jump target' % self.name)

    def get_def(self):
        """Get the def[S] of this statement."""
        if not self.is_command():
            return []

        if self.is_load() or self.is_arith():
            return [self[0]]

    def get_use(self):
        """Get the use[S] of this statement."""
        return []

    def defines(self, var):
        """Check if a variable is defined by this statement."""
        return var in self.get_def()

    def uses(self, var):
        """Check if a variable is used by this statement."""
        return var in self.get_use()


class Block:
    def __init__(self, statements=[]):
        self.statements = statements
        self.pointer = 0

    def __iter__(self):
        return iter(self.statements)

    def __len__(self):
        return len(self.statements)

    def replace(self, start, end, replacement):
        """Replace the given range start-end with the given statement list, and
        move the pointer to the first statement after the replacement."""
        before = self.statements[:start]
        after = self.statements[end:]
        self.statements = before + replacement + after
        self.pointer = start + len(replacement)

    def read(self, count=1):
        """Read the statement at the current pointer position and move the
        pointer one position to the right."""
        s = statements[self.pointer]
        self.pointer += 1

        return s

    def peek(self, count=1):
        """Read the statements until an offset from the current pointer
        position."""
        i = self.pointer + offset

        if i < len(self.statements):
            return self.statements[self.pointer:i]

    def end(self):
        """Check if the pointer is at the end of the statement list."""
        return self.pointer == len(self.statements) - 1


def find_leaders(statements):
    """Determine the leaders, which are:
       1. The first statement.
       2. Any statement that is the target of a jump.
       3. Any statement that follows directly follows a jump."""
    leaders = [0]
    jump_target_labels = []

    # Append statements following jumps and save jump target labels
    for i, statement in enumerate(statements[1:]):
        if statement.is_jump():
            leaders.append(i + 2)
            jump_target_labels.append(statement[-1])

    # Append jump targets
    for i, statement in enumerate(statements[1:]):
        if i + 1 not in leaders \
                and statement.is_label() \
                and statement.name in jump_target_labels:
            leaders.append(i + 1)

    leaders.sort()

    return leaders


def find_basic_blocks(statements):
    """Divide a statement list into basic blocks. Returns a list of basic
    blocks, which are also statement lists."""
    leaders = find_leaders(statements)
    blocks = []

    for i in range(len(leaders) - 1):
        blocks.append(Block(statements[leaders[i]:leaders[i + 1]]))

    blocks.append(Block(statements[leaders[-1]:]))

    return blocks
