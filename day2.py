from operator import add, mul


def program_loop(program):
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


def run_part1(program):
    return program_loop(program)


def run_part2(program, output_to_find):
    initial_state = list(program)

    for i in range(100):
        for j in range(100):
            program = init_program(initial_state, noun=i, verb=j)
            results = program_loop(program)
            if results[0] == output_to_find:
                return i, j


def get_puzzle(filename):
    with open(filename) as file:
        return list(map(int, file.read().rstrip().split(',')))


def init_program(program, noun, verb):
    program = list(program)
    program[1] = noun
    program[2] = verb
    return program


if __name__ == '__main__':
    result = run_part1([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    assert result == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50], 'actual: %s' % result

    input_data = get_puzzle('data/day2.txt')

    program = init_program(input_data, noun=12, verb=2)
    print(run_part1(program)[0])

    noun, verb = run_part2(input_data, output_to_find=19690720)
    print(100 * noun + verb)
