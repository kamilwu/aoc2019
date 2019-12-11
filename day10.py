import math


def visible(asteroids, starting_x, starting_y):
    angles = set()
    visible_asteroids = 0

    for y, row in enumerate(asteroids):
        for x, cell in enumerate(row):
            a, b = x - starting_x, y - starting_y
            angle = math.degrees(math.atan2(b, a))
            if angle not in angles and cell == '#':
                angles.add(angle)
                visible_asteroids += 1
    return visible_asteroids


def most_visible(asteroids):
    width, height = len(asteroids[0]), len(asteroids)
    maximum_visible = 0

    for x in range(width):
        for y in range(height):
            if asteroids[y][x] == '#':
                maximum_visible = max(visible(asteroids, x, y),
                                      maximum_visible)
    return maximum_visible


if __name__ == '__main__':
    with open('day10.txt') as file:
        asteroids = [x.rstrip() for x in file.readlines()]

    test = ['.#..#', '.....', '#####', '....#', '...##']
    result = most_visible(test)
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
    result = most_visible(test)
    assert result == 41, 'actual: %s' % result

    print(most_visible(asteroids))
