from operator import add, mul
from collections import UserList
from itertools import repeat


class ExtendableList(UserList):
    def _extend(self, index):
        self.extend(repeat(0, times=1 + index - len(self)))

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except IndexError:
            if item < 0:
                raise
            self._extend(item)
            return 0

    def __setitem__(self, key, value):
        try:
            super().__setitem__(key, value)
        except IndexError:
            if key < 0:
                raise
            self._extend(key)
            super().__setitem__(key, value)


class OutDevice:
    def out(self, item):
        raise NotImplementedError


def program_loop(program, in_device, out_device):
    program = ExtendableList(program)
    cir = 0  # current instruction register
    relative_base = 0
    opcode = 0

    while opcode != 99:
        value = program[cir]
        offset = 0

        def parameter_modes():
            modes = str(int(value / 100)).zfill(3)
            for mode in modes[::-1]:
                nonlocal offset
                offset += 1
                yield mode

        def address_gen():
            parameter_modes_gen = parameter_modes()
            for i in [1, 2, 3]:
                mode = next(parameter_modes_gen)
                idx = cir + i
                if mode == '0':
                    yield program[idx]
                elif mode == '1':
                    yield idx
                elif mode == '2':
                    yield program[idx] + relative_base

        opcode = value % 100
        addr = address_gen()

        if opcode == 1:
            inputs = program[next(addr)], program[next(addr)]
            program[next(addr)] = add(*inputs)
        elif opcode == 2:
            inputs = program[next(addr)], program[next(addr)]
            program[next(addr)] = mul(*inputs)
        elif opcode == 3:
            program[next(addr)] = next(in_device)
        elif opcode == 4:
            inputs = program[next(addr)]
            out_device.out(inputs)
        elif opcode == 5:
            cond = program[next(addr)]
            ptr = program[next(addr)]
            if cond:
                offset = ptr - cir - 1
        elif opcode == 6:
            cond = program[next(addr)]
            ptr = program[next(addr)]
            if not cond:
                offset = ptr - cir - 1
        elif opcode == 7:
            cond = program[next(addr)] < program[next(addr)]
            program[next(addr)] = 1 if cond else 0
        elif opcode == 8:
            cond = program[next(addr)] == program[next(addr)]
            program[next(addr)] = 1 if cond else 0
        elif opcode == 9:
            param = program[next(addr)]
            relative_base += param

        cir += offset + 1


def get_puzzle(filename):
    with open(filename) as file:
        return list(map(int, file.read().rstrip().split(',')))


def input_gen(number):
    while True:
        yield number


class Buffer(OutDevice, UserList):
    def out(self, item):
        self.append(item)


if __name__ == '__main__':
    test = [109,  1,  204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    result = Buffer()
    program_loop(test, input_gen(1), result)
    assert result == test, 'actual: %s' % result

    puzzle = get_puzzle('day9.txt')
    buffer = Buffer()
    program_loop(puzzle, input_gen(1), buffer)
    print(buffer)

    buffer = Buffer()
    program_loop(puzzle, input_gen(2), buffer)
    print(buffer)
