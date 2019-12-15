import day9


class Screen(day9.OutDevice):
    def __init__(self):
        self._width = 100
        self._height = 30
        self._screen = [0] * self._width * self._height
        self._x = None
        self._y = None

    def _reset(self):
        self._x = None
        self._y = None

    def out(self, item):
        if self._x is None:
            self._x = item
        elif self._y is None:
            self._y = item
        else:
            index = self._y * self._width + self._x
            self._screen[index] = item
            self._reset()

    def show(self):
        charmap = {
            0: ' ',
            1: 'X',
            2: '*',
            3: '_',
            4: 'O',
        }
        for i in range(self._height):
            line = self._screen[i * self._width: (i + 1) * self._width]
            [print(charmap[ch], end='') for ch in line]


def part1(program):
    screen = Screen()
    day9.program_loop(program, None, screen)
    return sum(1 for x in screen._screen if x == 2)


def part2(program):
    screen = Screen()
    program[0] = 2

    def input_gen():
        while True:
            yield 0

    day9.program_loop(program, input_gen(), screen)
    screen.show()


if __name__ == '__main__':
    program = day9.get_puzzle('day13.txt')
    print(part1(program))
    part2(program)

