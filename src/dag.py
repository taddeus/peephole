class Dag:
    def __init__(self, block):
        """Create the Directed Acyclic Graph of all binary operations in a
        basic block."""
        self.nodes = []

        for s in block:
            if s.is_command('move') or s.is_monop():
                rd, rs = s
                y = self.find_reg_node(rs)
                self.find_op_node(s.name, rd, y)
            elif s.is_binop():
                rd, rs, rt = s
                y = self.find_reg_node(rs)
                z = self.find_reg_node(rt)
                self.find_op_node(s.name, rd, y, z)

    def find_reg_node(self, reg):
        for n in self.nodes:
            if reg in n.reg:
                return n

        node = DagLeaf(reg)
        self.nodes.append(node)

        return node

    def find_op_node(self, op, rd, *args):
        for n in self.nodes:
            if not isinstance(n, DagLeaf) and n.op == op and n.nodes == args:
                n.labels.append(rd)

                return n

        node = DagNode(op, rd, *args)
        self.nodes.append(node)

        return node


class DagNode:
    def __init__(self, op, label, *args):
        self.op = op
        self.labels = [label]
        self.nodes = args


class DagLeaf:
    def __init__(self, reg):
        self.reg = reg
