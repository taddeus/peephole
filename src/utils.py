import re

class Statement:
    def __init__(self, stype, name, *args):
        self.stype = stype
        self.name = name
        self.args = args

    def __getitem__(self, n):
        """Get an argument."""
        return self.args[n]

    def jump_target(self, arg):
        """Get the use[S] of this statement."""
        if self.name in ['beq', 'bne', 'blez', 'bgtz', 'bltz', 'bgez', \
                         'bct', 'bcf']:
            return self[1]
        else:
            raise Exception('"%s" command has no jump target' % self.name)

    def is_command(self):
        """Check if the statement is a command."""
        return self.stype == 'command'

    def is_jump(self):
        """Check if the statement is a jump."""
        return self.is_command() and re.match('j|jal|jr|jalr', self.name)

    def is_shift(self):
        """Check if the statement is a shift operation."""
        return self.is_command() and re.match('s(ll|la|rl|ra)', self.name

    def is_load(self):
        """Check if the statement is a load instruction."""
        return self.is_command() and self.name in ['lw', 'dlw', 'l.s', 'l.d']

    def is_arith(self):
        """Check if the statement is an arithmetic operation."""
        return self.is_command() \
               and re.match('(add|sub|mult|div|abs|neg)(u|\.d)?', self.name)

    def get_def(self):
        """Get the def[S] of this statement."""
        if not self.is_command():
            return []

        if self.is_load() or self.is_arith():
            return [self[0]]

        if self.arith():
            return [self[0]]

    def get_use(self, arg):
        """Get the use[S] of this statement."""
        return []

    def defines(self, var):
        """Check if a variable is defined by this statement."""
        return var in self.get_def()

    def uses(self, var):
        """Check if a variable is used by this statement."""
        return var in self.get_use()

class StatementList:
    def __init__(self, statement_list):
        self.statement_list = statement_list
        self.pointer = 0

    def __getitem__(self, n):
        return self.statement_list[n]

    def __iter__(self):
        return iter(self.statement_list)

    def __len__(self):
        return len(self.statement_list)

    def get_range(self, start, end):
        return self.statement_list[start:end]

    def replace(self, start, end, replacement):
        before = self.statement_list[:start]
        after = self.statement_list[end:]
        self.statement_list = before + replacement + after

    def move_pointer(self, steps=1):
        self.pointer += steps

    def liveness(self, stype):
        """Check if the statement is of a given type."""
        return self.stype == stype


while not block.end():
    if (...):
        i = block.current()
        block.replace(i, i + 3, [nieuwe statements])
        block.move_pointer(3)
    else:
        block.move_pointer(1)
