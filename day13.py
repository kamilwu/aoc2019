from collections import deque

import day9


class Screen(day9.OutDevice):
    def __init__(self, joystick=None):
        self._width = 50
        self._height = 25
        self.screen = [0] * self._width * self._height
        self._x = None
        self._y = None
        self._charmap = {0: ' ', 1: 'X', 2: '*', 3: '_', 4: 'O'}
        self.score = 0
        self._paddle_x_pos = None
        self._joystick = joystick

    def _reset(self):
        self._x = None
        self._y = None

    def out(self, item):
        if self._x is None:
            self._x = item
        elif self._y is None:
            self._y = item
        elif self._x == -1 and self._y == 0:
            self.score = item
            self._reset()
        else:
            index = self._y * self._width + self._x
            self.screen[index] = item

            if item == 3:  # is paddle
                self._paddle_x_pos = self._x
            if item == 4 and self._paddle_x_pos:  # is ball
                self._tilt_joystick_if_needed()

            self._reset()

    def _tilt_joystick_if_needed(self):
        if self._paddle_x_pos > self._x:
            self._joystick.tilt(-1)
        elif self._paddle_x_pos < self._x:
            self._joystick.tilt(1)

    def show(self):
        for i in range(self._height):
            line = [self._charmap[ch] for ch in
                    self.screen[i * self._width: (i + 1) * self._width]]
            print(''.join(line))


class Joystick:
    def __init__(self):
        self._buffer = deque()

    def tilt(self, signal):
        self._buffer.append(signal)

    def get_input(self):
        return self._buffer.popleft()

    def input_available(self):
        return len(self._buffer) != 0


def part1(program):
    screen = Screen()
    day9.program_loop(program, None, screen)
    return sum(1 for x in screen.screen if x == 2)


def part2(program):
    joystick = Joystick()
    screen = Screen(joystick)
    program[0] = 2

    def input_gen():
        while True:
            yield joystick.get_input() if joystick.input_available() else 0

    day9.program_loop(program, input_gen(), screen)
    return screen.score


if __name__ == '__main__':
    program = day9.get_puzzle('day13.txt')
    print(part1(program))
    print('Total score:', part2(program))
