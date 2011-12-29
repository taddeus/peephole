from dataflow import BasicBlock as B, generate_flow_graph


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
    block.reach_gen = set()

    for s in reversed(block):
        for reg in s.get_def():
            if reg not in block_defs:
                block_defs[reg] = s.sid
                block.reach_gen.add(s.sid)

    # Generate kill set
    block.reach_kill = set()

    for reg, statement_ids in global_defs.iteritems():
        if reg in block_defs:
            block.reach_kill |= statement_ids - set([block_defs[reg]])


def create_in_out(blocks):
    """Generate the `in' and `out' sets of the given blocks using the iterative
    algorithm from the lecture slides."""
    # Generate flow graph
    generate_flow_graph(blocks)

    # Create gen/kill sets
    defs = get_defs(blocks)
    print 'defs:', defs

    for b in blocks:
        create_gen_kill(b, defs)
        b.reach_out = b.reach_gen

    change = True

    while change:
        change = False

        for b in blocks:
            print 'block:', b
            b.reach_in = set()

            for pred in b.edges_from:
                print 'pred:      ', pred
                b.reach_in |= pred.reach_out

            print 'b.reach_in:  ', b.reach_in
            print 'b.reach_out: ', b.reach_out
            new_out = b.reach_gen | (b.reach_in - b.reach_kill)
            print 'new_out:   ', new_out

            if new_out != b.reach_out:
                print 'changed'
                b.reach_out = new_out
                change = True
