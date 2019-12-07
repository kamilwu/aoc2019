from typing import Optional, List, Set, Dict


class Node:
    def __init__(self, label: str):
        self.label: str = label
        self.master: Optional[Node] = None
        self.slaves: List[Node] = []

    def add_slave(self, label: str):
        node = Node(label)
        node.master = self
        self.slaves.append(node)

    def add_master(self, master):
        assert self.master is None
        master.slaves.append(self)
        self.master = master

    def traverse(self, label: str):
        if label == self.label:
            return self
        for slave in self.slaves:
            n = slave.traverse(label)
            if n:
                return n

    def lenghts_sum(self, level: int = 0) -> int:
        result = level
        for slave in self.slaves:
            result += slave.lenghts_sum(level + 1)
        return result


def build_tree(orbits: List[str]) -> Node:
    def find(label: str) -> Optional[Node]:
        for root in trees:
            n = root.traverse(label)
            if n:
                return n

    trees: List[Node] = []
    inserted: Set[str] = set()

    for orbit in orbits:
        master, slave = orbit.split(')')

        if master in inserted and slave in inserted:
            slave_node = find(slave)
            master_node = find(master)
            slave_node.parent = master_node
            master_node.slaves.append(slave_node)
            trees.remove(slave_node)
        elif master in inserted:
            node = find(master)
            node.add_slave(slave)
            inserted.add(slave)
        elif slave in inserted:
            node = find(slave)
            trees.remove(node)
            master_node = Node(master)
            node.add_master(master_node)
            trees.append(master_node)
            inserted.add(master)
        else:
            node = Node(master)
            trees.append(node)
            node.add_slave(slave)
            inserted.add(master)
            inserted.add(slave)

    assert len(trees) == 1
    return trees[0]


def get_puzzle(filename: str) -> List[str]:
    with open(filename) as file:
        return [x.rstrip() for x in file.readlines()]


if __name__ == '__main__':
    test = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L']
    tree = build_tree(test)
    lenghts = tree.lenghts_sum()
    assert lenghts == 42, 'actual: %s' % lenghts

    puzzle = get_puzzle('day6.txt')
    tree = build_tree(puzzle)
    print(tree.lenghts_sum())
