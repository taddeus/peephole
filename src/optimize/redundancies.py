import re


def remove_redundancies(block):
    """Execute all functions that remove redundant statements."""
    callbacks = [move_aa, move_inst, instr_move_jal, move_move, sw_ld, shift, 
                 add_lw]
    old_len = -1
    changed = False

    while old_len != len(block):
        old_len = len(block)

        block.reset()

        while not block.end():
            s = block.read()

            for callback in callbacks:
                if callback(s, block):
                    changed = True
                    break

    return changed


def move_aa(mov, statements):
    """
    move $regA, $regA          ->  --- remove it
    """
    if mov.is_command('move') and mov[0] == mov[1]:
        statements.replace(1, [])

        return True


def move_inst(mov, statements):
    """
    move $regA, $regB          ->  instr $regA, $regB, ...
    instr $regA, $regA, ...
    """
    if mov.is_command('move'):
        ins = statements.peek()

        if ins and len(ins) >= 2 and ins[0] == mov[0] and ins[1] == mov[0]:
            ins[1] = mov[1]
            statements.replace(2, [ins])

            return True


def instr_move_jal(ins, statements):
    """
    instr $regA, ...          ->  instr $4, ...
    move $4, $regA                 jal XX
    jal XX
    """
    if ins.is_command() and len(ins):
        following = statements.peek(2)

        if len(following) == 2:
            mov, jal = following

            if mov.is_command('move') and mov[1] == ins[0] \
                    and re.match('^\$[4-7]$', mov[0]) \
                    and jal.is_command('jal'):
                ins[0] = mov[0]
                statements.replace(2, [ins])

                return True


def move_move(mov1, statements):
    """
    move $RegA, $RegB         ->  move $RegA, $RegB
    move $RegB, $RegA
    """
    if mov1.is_command('move'):
        mov2 = statements.peek()

        if mov2.is_command('move') and mov2[0] == mov1[1] and \
                mov2[1] == mov1[0]:
            statements.replace(2, [mov1])

            return True


def sw_ld(sw, statements):
    """
    sw $regA, XX              ->  sw $regA, XX
    ld $regA, XX
    """
    if sw.is_command('sw'):
        ld = statements.peek()

        if ld.is_command('lw') and ld.args == sw.args:
            statements.replace(2, [sw])

            return True


def shift(shift, statements):
    """
    shift $regA, $regA, 0     ->  --- remove it
    """
    if shift.is_shift() and shift[0] == shift[1] and shift[2] == 0:
        statements.replace(1, [])

        return True


def add_lw(add, statements):
    """
    add $regA, $regA, X       ->  lw ..., X($regA)
    lw ..., 0($regA)
    """
    if add.is_command('addu') and add[0] == add[1] and isinstance(add[2], int):
        lw = statements.peek()

        if lw.is_load() and lw[-1] == '0(%s)' % add[0]:
            lw[-1] = '%s(%s)' % (add[2], add[0])
            statements.replace(2, [lw])

            return True

def remove_redundant_jumps(statements):
    """Remove jump if label follows immediatly."""
    old_len = -1

    while old_len != len(statements):
        old_len = len(statements)
        
        while not statements.end():
            s = statements.read()

            #     j $Lx     ->             $Lx:
            # $Lx:
            if s.is_command('j'):
                following = statements.peek(2)

                if following.is_label(s[0]):
                    statements.replace(1, [])
                        
def remove_redundant_branch_jumps(statements):
    """Optimize statement sequences on a global level."""
    old_len = -1

    while old_len != len(statements):
        old_len = len(statements)

        while not statements.end():
            s = statements.read()

            #     beq/bne ..., $Lx      ->      bne/beq ..., $Ly
            #     j $Ly                     $Lx:
            # $Lx:
            if s.is_command('beq', 'bne'):
                following = statements.peek(2)

                if len(following) == 2:
                    j, label = following

                    if j.is_command('j') and label.is_label(s[2]):
                        s.name = 'bne' if s.is_command('beq') else 'beq'
                        s[2] = j[0]
                        statements.replace(3, [s, label])

    statements.reset()
