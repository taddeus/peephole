from copy import copy


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

        b.live_in = b.use_set
        b.live_out = set()

    change = True

    while change:
        change = False

        for b in blocks:
            # in[B] = use[B] | (out[B] - def[B])
            new_in = b.use_set | (b.live_out - b.def_set)

            # out[B] = union of in[S] for S in succ(B)
            new_out = set()

            for s in succ(b):
                new_out |= s.live_in

            # Check if either `in' or `out' changed
            if new_in != b.live_in:
                b.live_in = new_in
                change = True

            if new_out != b.live_out:
                b.live_out = new_out
                change = True
