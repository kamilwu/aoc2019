from random import randint
from queue import SimpleQueue

import day9
from day11 import Direction


class ResultsReady(Exception):
    pass


class RepairRobot(day9.OutDevice):
    def __init__(self):
        self.position = complex(0, 0)
        self.maze = {self.position: 'S'}
        self.moves_required = {self.position: 0}
        self.next_direction = None

    def out(self, item):
        position = self.position + self.next_direction.value
        if item == 0:
            self.maze[position] = '#'
        elif item == 1 or item == 2:
            if position not in self.moves_required:
                self.moves_required[position] = self.moves_required[
                                                    self.position] + 1
            self.position = position

            if item == 1:
                self.maze[position] = '.'
            elif item == 2:
                self.maze[position] = 'O'
                raise ResultsReady(self.moves_required[position])

    def move(self):
        directions = [Direction.DOWN, Direction.UP, Direction.LEFT,
                      Direction.RIGHT]
        self.next_direction = directions[randint(0, 3)]
        return self._get_command(self.next_direction)

    @staticmethod
    def _get_command(direction):
        mapping = {
            Direction.UP: 1,
            Direction.DOWN: 2,
            Direction.LEFT: 3,
            Direction.RIGHT: 4,
        }
        return mapping[direction]


def get_time_needed_to_fill_area_with_oxygen(maze):

    def get_neighbours(position):
        return [x.value + position for x in [Direction.DOWN, Direction.UP,
                                             Direction.LEFT, Direction.RIGHT]]

    oxygen_system = next(k for k, v in maze.items() if v == 'O')
    queue = SimpleQueue()
    queue.put([oxygen_system])
    discovered = set()
    discovered.add(oxygen_system)

    time = 0

    while not queue.empty():
        chunk = queue.get()
        new_chunk = []
        for elem in chunk:
            neighbours = [x for x in get_neighbours(elem) if x not in
                          discovered and maze.get(x, '#') != '#']
            new_chunk.extend(neighbours)
            discovered.update(neighbours)
        if new_chunk:
            queue.put(new_chunk)
        time += 1

    return time


if __name__ == '__main__':
    program = day9.get_puzzle('data/day15.txt')
    robot = RepairRobot()

    def input_gen():
        while True:
            yield robot.move()

    try:
        day9.program_loop(program, input_gen(), robot)
    except ResultsReady as e:
        distance_from_starting_point = e.args[0]
        print(distance_from_starting_point)

    print(get_time_needed_to_fill_area_with_oxygen(robot.maze))
