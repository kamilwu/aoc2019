from operator import add, mul


BUFFER = []


def program_loop(program, input_value):
    cir = 0  # current instruction register

    while cir < len(program):
        value = program[cir]
        offset = 1

        def parameter_modes():
            modes = str(int(value / 100)).zfill(3)
            for mode in modes[::-1]:
                # nonlocal offset
                # offset += 1
                yield mode

        opcode = value % 100
        parameter_modes_gen = parameter_modes()

        def address(param):
            mode = next(parameter_modes_gen)
            idx = cir + param
            return program[idx] if mode == '0' else idx

        if opcode == 1:
            inputs = program[address(1)], program[address(2)]
            program[address(3)] = add(*inputs)
            offset = 3
        elif opcode == 2:
            inputs = program[address(1)], program[address(2)]
            program[address(3)] = mul(*inputs)
            offset = 3
        elif opcode == 3:
            inputs = program[address(1)]
            program[inputs] = input_value
        elif opcode == 4:
            inputs = program[address(1)]
            BUFFER.append(inputs)
        elif opcode == 5:
            cond = program[address(1)]
            ptr = program[address(2)]
            if cond:
                offset = ptr - cir - 1
            else:
                offset = 2
        elif opcode == 6:
            cond = program[address(1)]
            ptr = program[address(2)]
            if not cond:
                offset = ptr - cir - 1
            else:
                offset = 2
        elif opcode == 7:
            program[address(3)] = 1 if program[address(1)] < program[
                address(2)] else 0
            offset = 3
        elif opcode == 8:
            program[address(3)] = 1 if program[address(1)] == program[
                address(2)] else 0
            offset = 3
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
    result = BUFFER.pop()
    assert result == 999, 'actual %s' % result

    program_loop(test_input, 8)
    result = BUFFER.pop()
    assert result == 1000, 'actual %s' % result

    program_loop(test_input, 9)
    result = BUFFER.pop()
    assert result == 1001, 'actual %s' % result

    program_loop(puzzle, 5)
    buf_print()
