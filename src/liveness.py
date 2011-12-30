from copy import copy


RESERVED_REGISTERS = ['$fp', '$sp', '$31']


def is_reg_dead_after(reg, block, index):
    """Check if a register is dead after a certain point in a basic block."""
    if reg in RESERVED_REGISTERS:
        return False

    if index < len(block) - 1:
        for s in block[index + 1:]:
            # If used, the previous definition is live
            if s.uses(reg):
                return False

            # If redefined, the previous definition is dead
            if s.defines(reg):
                return True

    # If dead within the same block, check if the register is in the block's
    # live_out set
    return reg not in block.live_out


def create_use_def(block):
    used = set()
    defined = set()

    # Get the last of each definition series and put in in the `def' set
    block.use_set = set()
    block.def_set = set()

    for s in block:
        # use[B] is the set of variables whose values may be used in B prior to
        # any definition of the variable
        for reg in s.get_use():
            used.add(reg)

            if reg not in defined:
                block.use_set.add(reg)

        # def[B] is the set of variables assigned values in B prior to any use
        # of that variable in B
        for reg in s.get_def():
            defined.add(reg)

            if reg not in used:
                block.def_set.add(reg)


def succ(block, known=[]):
    """Recursively find all successors of a node."""
    direct = filter(lambda b: b != block and b not in known, block.edges_to)
    s = copy(direct)

    for successor in direct:
        s += succ(successor, known + direct)
        return s

    return s


def create_in_out(blocks):
    for b in blocks:
        create_use_def(b)

        b.live_in = set()
        b.live_out = set()

    # Start by analyzing the exit points
    work_list = set()

    if len(blocks) == 1:
        work_list.add(blocks[0])
    else:
        for b in blocks:
            if b.edges_from and not b.edges_to:
                work_list.add(b)

    while len(work_list):
        b = work_list.pop()

        # out[B] = union of in[S] for S in succ(B)
        b.live_out = set()

        for s in succ(b):
            b.live_out |= s.live_in

        # in[B] = use[B] | (out[B] - def[B])
        new_in = b.use_set | (b.live_out - b.def_set)

        # Check if the out set has changed. If so, add all predecessors to the
        # work list
        if new_in != b.live_in:
            b.live_in = new_in
            work_list |= set(b.edges_from)
