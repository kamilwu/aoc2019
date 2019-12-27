from itertools import cycle, repeat
import operator


def fft(signal, base_pattern):
    result = []
    for i in range(len(signal)):
        pattern = cycle(val for val in base_pattern for _ in range(i + 1))
        next(pattern)  # skip the very first value
        result.append(abs(sum(map(operator.mul, signal, pattern))) % 10)
    return result


def repeated_fft(input_signal, base_pattern, phases):
    signal = list(input_signal)
    for _ in range(phases):
        signal = fft(signal, base_pattern)
    return signal


def get_puzzle(filename):
    with open(filename) as file:
        return [int(x) for x in file.read().rstrip()]


if __name__ == '__main__':
    test = [1, 2, 3, 4, 5, 6, 7, 8]
    result = repeated_fft(test, [0, 1, 0, -1], phases=4)
    assert result == [0, 1, 0, 2, 9, 4, 9, 8], 'actual: %s' % result

    input_signal = get_puzzle('data/day16.txt')
    result = repeated_fft(input_signal, [0, 1, 0, -1], phases=100)
    print(result[:8])
