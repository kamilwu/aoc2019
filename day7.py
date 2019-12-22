from queue import Queue
from itertools import permutations
import threading

import day5


class SynchronizedQueue(Queue):
    def append(self, item):
        self.put(item)


def amplify(program, phase_setting):
    output = 0
    for phase in phase_setting:

        def input_gen():
            yield phase
            yield output
        output = day5.program_loop(program, input_gen())[0]
    return output


def amplify_with_loop(program, phase_setting):
    buffers = [SynchronizedQueue() for _ in range(len(phase_setting))]
    threads = []

    def input_gen(i, phase):
        yield phase
        if i == 0:
            yield 0
        while True:
            yield buffers[i - 1].get()

    for i, phase in enumerate(phase_setting):
        thread = threading.Thread(target=day5.program_loop,
                                  args=(program, input_gen(i, phase),
                                        buffers[i]))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    return buffers[-1].get()


def largest_amplification(program, phase_setting, feedback_loop=False):
    max_output = 0
    for setting in permutations(phase_setting):
        if feedback_loop:
            output = amplify_with_loop(program, setting)
        else:
            output = amplify(program, setting)
        max_output = max(max_output, output)
    return max_output


if __name__ == '__main__':
    # part 1
    program = day5.get_puzzle('data/day7.txt')
    print(largest_amplification(program, range(5)))

    # part 2
    test = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
            27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
    result = amplify_with_loop(test, [9, 8, 7, 6, 5])
    assert result == 139629729, 'actual %s' % result

    test2 = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55,
             1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53, 54, 53,
             1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001,
             56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]
    result = amplify_with_loop(test2, [9, 7, 8, 5, 6])
    assert result == 18216, 'actual %s' % result

    print(largest_amplification(program, range(5, 10), feedback_loop=True))
