from copy import copy

from statement import Block


class BasicBlock(Block):
    def __init__(self, statements=[], dummy=False):
        Block.__init__(self, statements)
        self.edges_to = []
        self.edges_from = []

        self.dominates = []
        self.dominated_by = []

        self.dummy = dummy

    def add_edge_to(self, block):
        if block not in self.edges_to:
            self.edges_to.append(block)
            block.edges_from.append(self)

    def set_dominates(self, block):
        if block not in self.dominates:
            self.dominates.append(block)
            block.dominated_by.append(self)


def find_leaders(statements, return_jump_targets=False):
    """
    - Determine the leaders, which are:
      1. The first statement.
      2. Any statement that is the target of a jump.
      3. Any statement that follows directly follows a jump.
    - To determine the leaders, a list of known jump targets is created. This
      list can also be returned for later use.
    """
    leaders = [0]
    jump_targets = []

    # Append statements following jumps and save jump target labels
    for i, statement in enumerate(statements[1:]):
        if statement.is_jump():
            leaders.append(i + 2)
            jump_targets.append(statement[-1])

    # Append jump targets
    for i, statement in enumerate(statements[1:]):
        if i + 1 not in leaders \
                and statement.is_label() \
                and statement.name in jump_targets:
            leaders.append(i + 1)

    leaders.sort()

    return (leaders, jump_targets) if return_jump_targets else leaders


def find_basic_blocks(statements, return_jump_targets=False):
    """Divide a statement list into basic blocks. Returns a list of basic
    blocks, which are also statement lists."""
    leaders, jump_targets = find_leaders(statements, True)
    blocks = []

    for i in xrange(len(leaders) - 1):
        blocks.append(BasicBlock(statements[leaders[i]:leaders[i + 1]]))

    blocks.append(BasicBlock(statements[leaders[-1]:]))

    # Add a target block for unknown jump targets
    #blocks.append(BasicBlock([], dummy=True))

    return (blocks, jump_targets) if return_jump_targets else blocks


def generate_flow_graph(blocks):
    """Add flow graph edge administration of an ordered sequence of basic
    blocks."""
    #dummy_block = blocks[-1]

    for i, b in enumerate(blocks):
        last_statement = b[-1]

        if last_statement.is_jump():
            target = last_statement.jump_target()

            # Compare the target to all leading labels, add an edge if the
            # label matches the jump target
            #target_found = False

            for other in blocks:
                if other[0].is_label(target):
                    b.add_edge_to(other)
                    #target_found = True

            # If the jump target is outside the program, add an edge to the
            # dummy block
            #if not target_found:
            #    b.add_edge_to(dummy_block)

            # A branch and jump-and-line instruction also creates an edge to
            # the next block
            if (last_statement.is_branch() or last_statement.name == 'jal') \
                    and i < len(blocks) - 1:
                b.add_edge_to(blocks[i + 1])
        elif i < len(blocks) - 1:
            b.add_edge_to(blocks[i + 1])


def pred(block, known=[]):
    """Recursively find all predecessors of a node."""
    direct = filter(lambda b: b != block and b not in known, block.edges_from)
    p = copy(direct)

    for predecessor in direct:
        p += pred(predecessor, known + direct)
        return p

    return p


def succ(block, known=[]):
    """Recursively find all successors of a node."""
    direct = filter(lambda b: b != block and b not in known, block.edges_to)
    s = copy(direct)

    for successor in direct:
        s += succ(successor, known + direct)
        return s

    return s
