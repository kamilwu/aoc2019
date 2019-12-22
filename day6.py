from typing import Optional, List, Set, Dict
from operator import itemgetter
import math


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

    def find(self, label: str):
        if label == self.label:
            return self
        for slave in self.slaves:
            n = slave.find(label)
            if n:
                return n

    def lengths_sum(self, level: int = 0) -> int:
        result = level
        for slave in self.slaves:
            result += slave.lengths_sum(level + 1)
        return result


def dijkstra(start: Node, goal: Node, all_nodes: Set[Node]) -> int:
    not_visited: Set[Node] = set(all_nodes)
    distances: Dict[Node, int] = {k: math.inf for k in all_nodes}
    distances[start] = 0

    while not_visited:
        neighbours = start.slaves
        if start.master is not None:
            neighbours += [start.master]

        for n in neighbours:
            if n in not_visited:
                if distances[n] > distances[start] + 1:
                    distances[n] = distances[start] + 1
        not_visited.remove(start)
        if goal not in not_visited:
            return distances[goal]
        d = {k: v for (k, v) in distances.items() if k in not_visited}
        start = min(d.items(), key=itemgetter(1))[0]


def build_tree(orbits: List[str]) -> Node:
    def find(label: str) -> Optional[Node]:
        for root in trees:
            n = root.find(label)
            if n:
                return n

    trees: List[Node] = []
    inserted: Set[str] = set()

    for orbit in orbits:
        master, slave = orbit.split(')')

        if master in inserted and slave in inserted:
            slave_node = find(slave)
            master_node = find(master)
            slave_node.master = master_node
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


def get_set_of_nodes(node: Node) -> Set[Node]:
    result = set(node.slaves) | {node}
    for slave in node.slaves:
        result |= get_set_of_nodes(slave)
    return result


if __name__ == '__main__':
    test = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J',
            'J)K', 'K)L']
    tree = build_tree(test)
    lengths = tree.lengths_sum()
    assert lengths == 42, 'actual: %s' % lengths

    test = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J',
            'J)K', 'K)L', 'K)YOU', 'I)SAN']
    tree = build_tree(test)
    result = dijkstra(tree.find('YOU'), tree.find('SAN'),
                      get_set_of_nodes(tree)) - 2
    assert result == 4, 'actual: %s' % result

    puzzle = get_puzzle('data/day6.txt')
    tree = build_tree(puzzle)
    print(tree.lengths_sum())
    print(dijkstra(tree.find('YOU'), tree.find('SAN'),
                   get_set_of_nodes(tree)) - 2)
