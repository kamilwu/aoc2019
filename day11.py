from enum import Enum, IntEnum, unique
from operator import attrgetter

import day9


@unique
class Color(IntEnum):
    BLACK = 0
    WHITE = 1


@unique
class Direction(Enum):
    UP = complex(-1, 0)
    DOWN = complex(1, 0)
    LEFT = complex(0, -1)
    RIGHT = complex(0, 1)


class Robot:
    def __init__(self, default_color):
        self.default_color = default_color
        self.panels = {}
        self._current_pos = complex(0, 0)
        self._facing_at = Direction.UP

    def get_color(self, at_position=None):
        if not at_position:
            at_position = self._current_pos
        try:
            return self.panels[at_position]
        except KeyError:
            return self.default_color

    def paint_and_move(self, color, direction):
        self._paint(color)
        self._rotate(direction)
        self._move()

    def _paint(self, color):
        self.panels[self._current_pos] = Color(color)

    def _rotate(self, direction):
        factor = complex(0, 1) if direction == 0 else complex(0, -1)
        self._facing_at = Direction(self._facing_at.value * factor)

    def _move(self):
        self._current_pos += self._facing_at.value


class Controller:
    def __init__(self, robot):
        self.robot = robot
        self.signals = []

    def out(self, item):
        self.signals.append(item)
        if len(self.signals) == 2:
            self.robot.paint_and_move(self.signals[0], self.signals[1])
            self.signals.clear()


def run(robot, program):
    def input_gen():
        while True:
            yield robot.get_color()

    day9.program_loop(program, input_gen(), Controller(robot))
    return len(robot.panels)


if __name__ == '__main__':
    program = day9.get_puzzle('data/day11.txt')
    robot = Robot(Color.BLACK)
    print(run(robot, program))

    robot = Robot(Color.WHITE)
    run(robot, program)

    max_width = int(max(robot.panels, key=attrgetter('imag')).imag)
    max_height = int(max(robot.panels, key=attrgetter('real')).real)
    output = [[' '] * (max_width + 1) for _ in range(max_height + 1)]
    for k, v in robot.panels.items():
        x = int(k.real)
        y = int(k.imag)
        output[x][y] = '█' if v else ' '
    [print(' '.join(x)) for x in output]


