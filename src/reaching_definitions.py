from dataflow import BasicBlock as B


def get_defs(blocks):
    """Collect definitions of all registers."""
    defs = {}

    for b in blocks:
        for s in b:
            for reg in s.get_def():
                if reg not in defs:
                    defs[reg] = set([s.sid])
                else:
                    defs[reg].add(s.sid)

    return defs


def create_gen_kill(block, global_defs):
    block_defs = {}

    # Get the last of each definition series and put in in the `def' set
    block.gen_set = set()

    for s in reversed(block):
        for reg in s.get_def():
            if reg not in block_defs:
                block_defs[reg] = s.sid
                block.gen_set.add(s.sid)

    # Generate kill set
    block.kill_set = set()

    for reg, statement_ids in global_defs.iteritems():
        if reg in block_defs:
            block.kill_set |= statement_ids - set([block_defs[reg]])


def create_in_out(blocks):
    """Generate the `in' and `out' sets of the given blocks using the iterative
    algorithm from the lecture slides."""
    # Create gen/kill sets
    defs = get_defs(blocks)

    for b in blocks:
        create_gen_kill(b, defs)
        b.reach_out = b.gen_set

    change = True

    while change:
        change = False

        for b in blocks:
            b.reach_in = set()

            for pred in b.edges_from:
                b.reach_in |= pred.reach_out

            new_out = b.gen_set | (b.reach_in - b.kill_set)

            if new_out != b.reach_out:
                b.reach_out = new_out
                change = True
