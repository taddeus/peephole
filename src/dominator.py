from copy import copy


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
