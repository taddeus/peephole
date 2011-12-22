import re


class Statement:
    def __init__(self, stype, name, *args, **kwargs):
        self.stype = stype
        self.name = name
        self.args = list(args)
        self.options = kwargs

    def __getitem__(self, n):
        """Get an argument."""
        return self.args[n]

    def __setitem__(self, n, value):
        """Set an argument."""
        self.args[n] = value

    def __eq__(self, other):
        """Check if two statements are equal by comparing their type, name and
        arguments."""
        return self.stype == other.stype and self.name == other.name \
               and self.args == other.args

    def __str__(self):  # pragma: nocover
        return '<Statement type=%s name=%s args=%s>' \
                % (self.stype, self.name, self.args)

    def __repr__(self):  # pragma: nocover
        return str(self)

    def is_comment(self):
        return self.stype == 'comment'

    def is_inline_comment(self):
        return self.is_comment() and self.options['inline']

    def is_directive(self):
        return self.stype == 'directive'

    def is_label(self, name=None):
        return self.stype == 'label' if name == None \
               else self.stype == 'label' and self.name == name

    def is_command(self, name=None):
        return self.stype == 'command' if name == None \
               else self.stype == 'command' and self.name == name

    def is_jump(self):
        """Check if the statement is a jump."""
        return self.is_command() \
               and re.match('^j|jal|beq|bne|blez|bgtz|bltz|bgez|bct|bcf$', \
                            self.name)

    def is_branch(self):
        """Check if the statement is a branch."""
        return self.is_command() \
               and re.match('^beq|bne|blez|bgtz|bltz|bgez|bct|bcf$', \
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
        if not self.is_jump():
            raise Exception('Command "%s" has no jump target' % self.name)

        return self[-1]


class Block:
    def __init__(self, statements=[]):
        self.statements = statements
        self.pointer = 0

    def __iter__(self):
        return iter(self.statements)

    def __getitem__(self, n):
        return self.statements[n]

    def __len__(self):
        return len(self.statements)

    def read(self, count=1):
        """Read the statement at the current pointer position and move the
        pointer one position to the right."""
        s = self.statements[self.pointer]
        self.pointer += 1

        return s

    def end(self):
        """Check if the pointer is at the end of the statement list."""
        return self.pointer == len(self)

    def peek(self, count=1):
        """Read the statements until an offset from the current pointer
        position."""
        return self.statements[self.pointer] if count == 1 \
               else self.statements[self.pointer:self.pointer + count]

    def replace(self, count, replacement, start=None):
        """Replace the given range start-(start + count) with the given
        statement list, and move the pointer to the first statement after the
        replacement."""
        if start == None:
            start = self.pointer

        before = self.statements[:start]
        after = self.statements[start + count:]
        self.statements = before + replacement + after
        self.pointer = start + len(replacement)

    def apply_filter(self, callback):
        """Apply a filter to the statement list. If the callback returns True,
        the statement will remain in the list.."""
        self.statements = filter(callback, self.statements)
