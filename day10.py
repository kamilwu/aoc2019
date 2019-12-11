import math
from collections import defaultdict
from functools import partial
from operator import itemgetter


def visible(angles):
    return len(angles)


def get_angles(asteroids, starting_point):

    def full_360(degrees):
        degrees += 90
        return degrees + 360 if degrees < 0 else degrees

    angles = defaultdict(list)
    for y, row in enumerate(asteroids):
        for x, cell in enumerate(row):
            if x == starting_point[0] and y == starting_point[1]:
                continue

            if cell == '#':
                a, b = x - starting_point[0], y - starting_point[1]
                angle = full_360(math.degrees(math.atan2(b, a)))
                angles[angle].append((x, y))
    return angles


def find_best_place(asteroids):
    width, height = len(asteroids[0]), len(asteroids)
    max_visible = 0
    place = None

    for x in range(width):
        for y in range(height):
            if asteroids[y][x] == '#':
                v = visible(get_angles(asteroids, (x, y)))
                if v > max_visible:
                    max_visible = v
                    place = x, y
    return max_visible, place


def launch_laser(angles, station, stops_at):

    def length(x, y):
        x1, y1 = x
        x2, y2 = y
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    targets = sorted(angles.items(), key=itemgetter(0))
    length_from_station = partial(length, station)
    targets = [(x, sorted(y, key=length_from_station)) for x, y in targets]
    return targets[stops_at - 1][1][0]


if __name__ == '__main__':
    with open('day10.txt') as file:
        asteroids = [x.rstrip() for x in file.readlines()]

    test = ['.#..#', '.....', '#####', '....#', '...##']
    result, _ = find_best_place(test)
    assert result == 8, 'actual: %s' % result

    test = ['.#..#..###',
            '####.###.#',
            '....###.#.',
            '..###.##.#',
            '##.##.#.#.',
            '....###..#',
            '..#.#..#.#',
            '#..#.#.###',
            '.##...##.#',
            '.....#.#..']
    result, _ = find_best_place(test)
    assert result == 41, 'actual: %s' % result

    test = ['.#..##.###...#######',
            '##.############..##.',
            '.#.######.########.#',
            '.###.#######.####.#.',
            '#####.##.#.##.###.##',
            '..#####..#.#########',
            '####################',
            '#.####....###.#.#.##',
            '##.#################',
            '#####.##.###..####..',
            '..######..##.#######',
            '####.##.####...##..#',
            '.#####..#.######.###',
            '##...#.##########...',
            '#.##########.#######',
            '.####.#.###.###.#.##',
            '....##.##.###..#####',
            '.#.#.###########.###',
            '#.#.#.#####.####.###',
            '###.##.####.##.#..##']

    result, best_place = find_best_place(test)
    assert result == 210, 'actual: %s' % result
    assert best_place == (11, 13), 'actual: %s' % best_place
    last_to_be_vaporized = launch_laser(get_angles(test, best_place),
                                        best_place, stops_at=200)
    assert last_to_be_vaporized == (8, 2)

    max_visible, best_place = find_best_place(asteroids)
    print(max_visible)

    last_to_be_vaporized = launch_laser(get_angles(asteroids, best_place),
                                        best_place, stops_at=200)
    print(last_to_be_vaporized)
