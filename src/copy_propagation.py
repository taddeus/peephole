from dataflow import pred
from liveness import RESERVED_REGISTERS


def create_gen_kill(block):
    block.c_gen = set()
    block.c_kill = set()

    for s in block:
        if s.is_command('move'):
            # An occurrence of a copy statement generates this statement
            x, y = s

            if x not in RESERVED_REGISTERS and y not in RESERVED_REGISTERS:
                block.c_gen.add((x, y))
        else:
            # An assignment to x or y kills the copy statement x = y
            block.c_kill |= set(s.get_def())
            #for reg in s.get_def():
            #    block.c_kill.add(reg)
            #    print 'kill of %s' % reg


def create_in_out(blocks):
    """Generate the `in' and `out' sets of the given blocks using the iterative
    algorithm from the lecture slides."""
    # Create gen/kill sets
    for b in blocks:
        create_gen_kill(b)
        b.copy_in = set()
        b.copy_out = set()

    # in[B1] = {} where B1 is the initial block
    blocks[0].copy_in = set()

    #def create_sets(b, first=False):
    for i, b in enumerate(blocks):
        # in[B1] = {} where B1 is the initial block
        # in[B] = intersection of out[P] for P in pred(B) for B not initial
        if i:
            b.copy_in = set()

            for p in pred(b):
                b.copy_in &= p.copy_out

        # out[B] = c_gen[B] | (in[B] - c_kill[B])
        in_minus_kill = set()

        for x, y in b.copy_in:
            if x not in b.c_kill and y not in b.c_kill:
                print '%s, %s not in c_kill' % (x, y)
                in_minus_kill.add((x, y))

        b.copy_out = b.c_gen | in_minus_kill

        #for successor in b.edges_to:
        #    create_sets(successor)

    #create_sets(blocks[0], True)


#def propagate_copies(block):
#    changed = False
#
#    # For each copy statement s: x = y do
#    for s in block:
#        if s.is_command('move'):
#            x, y = s
#
#            # Determine the uses of x reached by this definition of x
#            uses = filter(lambda suc: s.sid in suc.reach_in, block.edges_to)
#
#            # Determine if for each of those uses this is the only
#            # definition reaching it -> s in in[B_use]
#            only_def = True
#
#            for b_use in uses:
#                if (x, y) not in b_use.copy_in:
#                    only_def = False
#
#            # If so, remove s and replace the uses of x by uses of y
#            if only_def:
#                for use in uses:
#                    print 'use:', use
#                    for statement in use:
#                        if statement.uses(x):
#                            statement.replace_usage(x, y)
#                            message = ' Replaced %s with %s' % (x, y)
#                            print message
#                            statement.set_inline_comment(message)
#                            changed = True
#
#    return changed
