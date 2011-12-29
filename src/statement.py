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

    def __len__(self):
        return len(self.args)

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

    def is_command(self, *args):
        return self.stype == 'command' and (not len(args) or self.name in args)

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
        return self.is_command() and re.match('^s(ll|rl|ra)$', self.name)

    def is_load(self):
        """Check if the statement is a load instruction."""
        return self.is_command() and self.name in ['lw', 'dlw', 'l.s', 'l.d']

    def is_arith(self):
        """Check if the statement is an arithmetic operation."""
        return self.is_command() \
               and re.match('^s(ll|rl|ra)'
                            + '|(mfhi|mflo|abs|neg|and|[xn]?or)'
                            + '|(add|sub|slt)u?'
                            + '|(add|sub|mult|div|abs|neg|sqrt|c)\.[sd]$', \
                            self.name)

    def is_monop(self):
        """Check if the statement is an unary operation."""
        return len(self) == 2 and self.is_arith()

    def is_binop(self):
        """Check if the statement is an binary operation."""
        return self.is_command() and len(self) == 3 and not self.is_jump()

    def jump_target(self):
        """Get the jump target of this statement."""
        if not self.is_jump():
            raise Exception('Command "%s" has no jump target' % self.name)

        return self[-1]

    def get_def(self):
        # TODO: Finish
        if self.is_load() or self.is_arith():
            return self[:1]

        return []

    def get_use(self):
        # TODO: Finish with ALL the available commands!
        use = []

        if self.is_binop():
            use += self[1:]
        elif self.is_command('move'):
            use.append(self[1])
        elif self.is_command('lw', 'sb', 'sw', 'dsw', 's.s', 's.d'):
            m = re.match('^\d+\(([^)]+)\)$', self[1])

            if m:
                use.append(m.group(1))

            # 'sw' also uses its first argument
            if self.name in ['sw', 'dsw']:
                use.append(self[0])
        elif len(self) == 2:  # FIXME: temporary fix, manually add all commands
            use.append(self[1])

        return use

    def defines(self, reg):
        """Check if this statement defines the given register."""
        return reg in self.get_def()

    def uses(self, reg):
        """Check if this statement uses the given register."""
        return reg in self.get_use()


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
        if self.end():
            return Statement('empty', '') if count == 1 else []

        return self.statements[self.pointer] if count == 1 \
               else self.statements[self.pointer:self.pointer + count]

    def replace(self, count, replacement, start=None):
        """Replace the given range start-(start + count) with the given
        statement list, and move the pointer to the first statement after the
        replacement."""
        if self.pointer == 0:
            raise Exception('No statement have been read yet.')

        if start == None:
            start = self.pointer - 1

        before = self.statements[:start]
        after = self.statements[start + count:]
        self.statements = before + replacement + after
        self.pointer = start + len(replacement)

    def insert(self, statement, index=None):
        if index == None:
            index = self.pointer

        self.statements.insert(index, statement)

    def apply_filter(self, callback):
        """Apply a filter to the statement list. If the callback returns True,
        the statement will remain in the list.."""
        self.statements = filter(callback, self.statements)

    def reverse_statements(self):
        """Reverse the statement list and reset the pointer."""
        self.statements = self.statements[::-1]
        self.pointer = 0
