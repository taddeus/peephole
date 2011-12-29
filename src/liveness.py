def create_gen_kill(block):
    # Get the last of each definition series and put in in the `def' set
    block.live_gen = set()
    block.live_kill = set()
    print 'block:', block

    for s in block:
        # If a register is used without having been defined in this block,
        # yet, put it in the `gen' set
        for reg in s.get_use():
            if reg not in block.live_kill:
                print '  add:', reg
                block.live_gen.add(reg)

        for reg in s.get_def():
            block.live_kill.add(reg)


def create_in_out(blocks):
    pass
