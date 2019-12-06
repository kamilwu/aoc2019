from operator import add, mul


BUFFER = []


def program_loop(program, input_value):
    program = list(program)
    cir = 0  # current instruction register

    while cir < len(program):
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
                yield program[idx] if mode == '0' else idx

        opcode = value % 100
        addr = address_gen()

        if opcode == 1:
            inputs = program[next(addr)], program[next(addr)]
            program[next(addr)] = add(*inputs)
        elif opcode == 2:
            inputs = program[next(addr)], program[next(addr)]
            program[next(addr)] = mul(*inputs)
        elif opcode == 3:
            program[next(addr)] = input_value
        elif opcode == 4:
            inputs = program[next(addr)]
            BUFFER.append(inputs)
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
        elif opcode == 99:
            return program

        cir += offset + 1


def get_puzzle(filename):
    with open(filename) as file:
        return list(map(int, file.read().rstrip().split(',')))


def buf_print():
    global BUFFER
    BUFFER.reverse()
    while BUFFER:
        print(BUFFER.pop())


if __name__ == '__main__':
    puzzle = get_puzzle('day5.txt')
    program_loop(puzzle, 1)
    buf_print()

    test_input = [
        3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
        1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
        999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99
    ]
    program_loop(test_input, 7)
    assert len(BUFFER) == 1
    result = BUFFER.pop()
    assert result == 999, 'actual %s' % result

    program_loop(test_input, 8)
    assert len(BUFFER) == 1
    result = BUFFER.pop()
    assert result == 1000, 'actual %s' % result

    program_loop(test_input, 9)
    assert len(BUFFER) == 1
    result = BUFFER.pop()
    assert result == 1001, 'actual %s' % result

    program_loop(puzzle, 5)
    buf_print()
