from collections import Counter
from operator import itemgetter
from functools import reduce


def get_puzzle(filename):
    with open(filename) as file:
        return file.read().rstrip()


def process_image(width, height, data):
    pixels = width * height
    return [data[x:x + pixels] for x in range(0, len(data), pixels)]


def check_integrity(layers):
    with_fewest_zeroes = min([Counter(x) for x in layers], key=itemgetter('0'))
    return with_fewest_zeroes['1'] * with_fewest_zeroes['2']


def decode_and_print(width, layers):
    def merge(layer1, layer2):
        return [y if x == '2' else x for x, y in zip(layer1, layer2)]
    bytecode = ''.join(reduce(merge, layers))

    lines = ['█' if x == '1' else '' for x in bytecode]
    lines = [lines[x:x + width] for x in range(0, len(lines), width)]
    for line in lines:
        print(line)


if __name__ == '__main__':
    puzzle = get_puzzle('day8.txt')
    layers = process_image(25, 6, puzzle)
    print(check_integrity(layers))
    decode_and_print(25, layers)
