# TODO: JALR & JR
JUMP_COMMANDS = ['j', 'jal', 'beq', 'bne', 'blez', 'bgtz', 'bltz', 'bgez', \
                 'bc1f', 'bc1t']

def is_jump(statement):
    '''Check if a statement is a jump command.'''
    return statement[0] == 'command' and statement[1] in JUMP_COMMANDS

def find_leaders(statements):
    '''Determine the leaders, which are:
       1. The first statement.
       2. Any statement that is the target of a jump.
       3. Any statement that follows directly follows a jump.'''
    leaders = [0]
    jump_target_labels = []

    # Append statements following jumps and save jump target labels
    for i, statement in enumerate(statements[1:]):
        if is_jump(statement):
            leaders.append(i + 2)
            print statement[2]['args'][-1]
            jump_target_labels.append(statement[2]['args'][-1])
            #print 'found jump:', i, statement

    print 'target labels:', jump_target_labels
    print 'leaders:', leaders

    # Append jump targets
    for i, statement in enumerate(statements[1:]):
        if i + 1 not in leaders \
                and statement[0] == 'label' \
                and statement[1] in jump_target_labels:
            leaders.append(i + 1)
            #print 'target:', i + 1, statements[i + 1]

    return leaders

def find_basic_blocks(statements):
    '''Divide a statement list into basic blocks. Returns a list of basic
    blocks, which are also statement lists.'''
    leaders = find_leaders(statements)
    blocks = []

    for i in range(len(leaders) - 1):
        blocks.append(statements[leaders[i]:leaders[i + 1]])

    blocks.append(statements[leaders[-1]:])

    return blocks
