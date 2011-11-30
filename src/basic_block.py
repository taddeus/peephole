# TODO: Get all jump commands
JUMP_COMMANDS = ['j', 'jal']

def is_jump(line):
    '''Check if a statement is a jump command.'''
    return line[0] == 'command' and line[1] in JUMP_COMMANDS

def find_leaders(lines):
    '''Determine the leaders, which are:
       1. The first statement.
       2. Any statement that is the target of a jump.
       3. Any statement that follows directly follows a jump.'''
    leaders = [0]
    jump_target_labels = []

    # Append statements following jumps and save jump target labels
    for i, line in enumerate(lines[1:]):
        if is_jump(line):
            leaders.append(i + 2)
            jump_target_labels.append(line[2]['args'][0])
            #print 'found jump:', i, line

    #print 'target labels:', jump_target_labels

    # Append jump targets
    for i, line in enumerate(lines[1:]):
        if i + 1 not in leaders \
                and line[0] == 'label' \
                and line[1] in jump_target_labels:
            leaders.append(i + 1)
            #print 'target:', i + 1, lines[i + 1]

    return leaders

def find_basic_blocks(lines):
    '''Divide a statement list into basic blocks. Returns a list of basic
    blocks, which are also statement lists.'''
    leaders = find_leaders(lines)
    blocks = []

    for i in range(len(leaders) - 1):
        blocks.append(lines[leaders[i]:leaders[i + 1]])

    return blocks
