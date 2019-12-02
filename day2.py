from operator import add, mul


def run_part1(program):
    program = list(program)
    cir = 0  # current instruction register
    while cir < len(program):
        opcode = program[cir]
        if opcode == 1:
            operation = add
        elif opcode == 2:
            operation = mul
        elif opcode == 99:
            return program

        inputs = program[program[cir + 1]], program[program[cir + 2]]
        program[program[cir + 3]] = operation(*inputs)
        cir += 4


def run_part2(program, output_to_find):
    return 0, 0


def get_puzzle(filename):
    with open(filename) as file:
        return list(map(int, file.read().rstrip().split(',')))


def init_1202_program():
    program[1] = 12
    program[2] = 2
    return program


if __name__ == '__main__':
    result = run_part1([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    assert result == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50], 'actual: %s' % result

    program = get_puzzle('day2.txt')
    init_1202_program()
    result = run_part1(program)
    print(result)

    noun, verb = run_part2(program, 19690720)
    print(noun, verb * 100)
