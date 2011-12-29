import re


class Statement:
    sid = 1

    def __init__(self, stype, name, *args, **kwargs):
        self.stype = stype
        self.name = name
        self.args = list(args)
        self.options = kwargs

        # Assign a unique ID to each statement
        self.sid = Statement.sid
        Statement.sid += 1

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
        return '<Statement sid=%d type=%s name=%s args=%s>' \
                % (self.sid, self.stype, self.name, self.args)

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

    def is_branch_zero(self):
        """Check if statement is a branch that compares with zero."""
        return self.is_command() \
               and re.match('^blez|bgtz|bltz|bgez$', self.name)

    def is_shift(self):
        """Check if the statement is a shift operation."""
        return self.is_command() and re.match('^s(ll|rl|ra)$', self.name)

    def is_load(self):
        """Check if the statement is a load instruction."""
        return self.is_command() and self.name in ['lw', 'li', 'dlw', 'l.s', \
                                                   'l.d']

    def is_store(self):
        """Check if the statement is a store instruction."""
        return self.is_command() and self.name in ['sw', 'sb', 's.d', 'dsw', \
                                                   's.s', 's.b']

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

    def is_load_non_immediate(self):
        """Check if the statement is a load statement."""
        return self.is_command() \
               and re.match('^l(w|a|b|bu|\.d|\.s)|dlw$', \
                            self.name)

    def is_logical(self):
        """Check if the statement is a logical operator."""
        return self.is_command() and re.match('^(xor|or|and)i?$', self.name)

    def is_double_arithmetic(self):
        """Check if the statement is a arithmetic .d operator."""
        return self.is_command() and \
                re.match('^(add|sub|div|mul)\.d$', self.name)

    def is_double_unary(self):
        """Check if the statement is a unary .d operator."""
        return self.is_command() and \
                re.match('^(abs|neg|mov)\.d$', self.name)

    def is_move_from_spec(self):
        """Check if the statement is a move from the result register."""
        return self.is_command() and self.name in ['mflo', 'mthi']

    def is_set_if_less(self):
        """Check if the statement is a shift if less then."""
        return self.is_command() and self.name in ['slt', 'sltu']

    def is_convert(self):
        """Check if the statement is a convert operator."""
        return self.is_command() and re.match('^cvt\.[a-z\.]*$', self.name)

    def is_truncate(self):
        """Check if the statement is a convert operator."""
        return self.is_command() and re.match('^trunc\.[a-z\.]*$', self.name)

    def is_compare(self):
        """Check if the statement is a comparison."""
        return self.is_command() and re.match('^c\.[a-z\.]*$', self.name)

    def jump_target(self):
        """Get the jump target of this statement."""
        if not self.is_jump():
            raise Exception('Command "%s" has no jump target' % self.name)

        return self[-1]

    def get_def(self):
        """Get the variable that this statement defines, if any."""
        instr = ['move', 'addu', 'subu', 'li', 'dmfc1', 'mov.d']
        
        if self.is_command('mtc1'):
            return [self[1]]
        if self.is_load_non_immediate() or self.is_arith() \
                or self.is_logical() or self.is_double_arithmetic() \
                or self.is_move_from_spec() or self.is_double_unary() \
                or self.is_set_if_less() or self.is_convert() \
                or self.is_truncate() or self.is_load() \
                or self.is_command(*instr):
            return self[:1]

        return []

    def get_use(self):
        """Get the variables that this statement uses, if any."""
        instr = ['addu', 'subu', 'mult', 'div', 'move', 'mov.d', \
            'dmfc1']
        use = []

        # Case arg0
        if self.is_branch() or self.is_store() or self.is_compare() \
                or self.is_command(*['mult', 'div', 'dsz', 'mtc1']):
            if self.name == 'dsz':
                m = re.match('^[^(]+\(([^)]+)\)$', self[0])

                if m:
                    use.append(m.group(1))
            else:
                use.append(self[0])
        # Case arg1 direct adressing
        if (self.is_branch() and not self.is_branch_zero()) or self.is_shift()\
                or self.is_double_arithmetic() or self.is_double_unary() \
                or self.is_logical() or self.is_convert() \
                or self.is_truncate() or self.is_set_if_less() \
                or self.is_compare() or self.is_command(*instr):
            use.append(self[1])
        # Case arg1 relative adressing
        if self.is_load_non_immediate() or self.is_store():
            m = re.match('^[^(]+\(([^)]+)\)$', self[1])

            if m:
                use.append(m.group(1))
            else:
                use.append(self[1])
        # Case arg2
        if self.is_double_arithmetic() or self.is_set_if_less() \
                or self.is_logical() or self.is_truncate() \
                or self.is_command(*['addu', 'subu']):
            if not isinstance(self[2], int):
                    use.append(self[2])

        return use

    def defines(self, reg):
        """Check if this statement defines the given register."""
        return reg in self.get_def()

    def uses(self, reg):
        """Check if this statement uses the given register."""
        return reg in self.get_use()


class Block:
    bid = 1

    def __init__(self, statements=[]):
        self.statements = statements
        self.pointer = 0

        # Assign a unique ID to each block for printing purposes
        self.bid = Block.bid
        Block.bid += 1

    def __str__(self):
        return '<Block bid=%d statements=%d>' % (self.bid, len(self))

    def __repr__(self):
        return str(self)

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
        return self.pointer >= len(self)

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
        self.reset()

    def reset(self):
        """Reset the internal pointer."""
        self.pointer = 0
