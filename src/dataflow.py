from copy import copy

from statement import Block


class BasicBlock(Block):
    edges_to = []
    edges_from = []

    dominates = []
    dominated_by = []

    def add_edge_to(self, block):
        self.edges_to.append(block)
        block.edges_from.append(self)

    def set_dominates(self, block):
        self.dominates.append(block)
        block.dominated_by.append(self)

    def get_gen(self):
        pass

    def get_kill(self):
        pass

    def get_in(self):
        pass

    def get_out(self):
        pass


def find_leaders(statements):
    """Determine the leaders, which are:
       1. The first statement.
       2. Any statement that is the target of a jump.
       3. Any statement that follows directly follows a jump."""
    leaders = [0]
    jump_target_labels = []

    # Append statements following jumps and save jump target labels
    for i, statement in enumerate(statements[1:]):
        if statement.is_jump():
            leaders.append(i + 2)
            jump_target_labels.append(statement[-1])

    # Append jump targets
    for i, statement in enumerate(statements[1:]):
        if i + 1 not in leaders \
                and statement.is_label() \
                and statement.name in jump_target_labels:
            leaders.append(i + 1)

    leaders.sort()

    return leaders


def find_basic_blocks(statements):
    """Divide a statement list into basic blocks. Returns a list of basic
    blocks, which are also statement lists."""
    leaders = find_leaders(statements)
    blocks = []

    for i in range(len(leaders) - 1):
        blocks.append(BasicBlock(statements[leaders[i]:leaders[i + 1]]))

    blocks.append(BasicBlock(statements[leaders[-1]:]))

    return blocks


def generate_flow_graph(blocks):
    """Add flow graph edge administration of an ordered sequence of basic
    blocks."""
    for b in blocks:
        last_statement = b[-1]

        if last_statement.is_jump():
            target = last_statement.jump_target()

            # Compare the target to all leading labels, add an edge if the
            # label matches the jump target
            for other in blocks:
                if other[0].is_label(target):
                    b.add_edge_to(other)


def generate_dominator_tree(nodes):
    """Add dominator administration to the given flow graph nodes."""
    # Dominator of the start node is the start itself
    nodes[0].dom = set([nodes[0]])

    # For all other nodes, set all nodes as the dominators
    for n in nodes[1:]:
        n.dom = set(copy(nodes))

    def pred(n, known=[]):
        """Recursively find all predecessors of a node."""
        direct = filter(lambda x: x not in known, n.edges_from)
        p = copy(direct)

        for ancestor in direct:
            p += pred(ancestor, direct)

        return p

    # Iteratively eliminate nodes that are not dominators
    changed = True

    while changed:
        changed = False

        for n in nodes[1:]:
            old_dom = n.dom
            intersection = lambda p1, p2: p1.dom & p2.dom
            n.dom = set([n]) | reduce(intersection, pred(n), set([]))

            if n.dom != old_dom:
                changed = True

    def idom(d, n):
        """Check if d immediately dominates n."""
        for b in n.dom:
            if b != d and b != n and b in n.dom:
                return False

        return True

    # Build tree using immediate dominators
    for n in nodes:
        for d in n.dom:
            if idom(d, n):
                d.set_dominates(n)
                break

# statements = parse_file(...)
# b = find_basic_blocks(statements)
# generate_flow_graph(b)  # nodes now have edges
# generate_dominator_tree(b)  # nodes now have dominators
