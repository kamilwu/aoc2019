def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def get_points(wire):
    vect = {
        'U': (0, 1),
        'D': (0, -1),
        'L': (-1, 0),
        'R': (1, 0)
    }
    points = {}
    pos = 0, 0
    step = 0

    for point in wire:
        direction = point[0]
        n = int(point[1:])
        for _ in range(n):
            pos = add(pos, vect[direction])
            step += 1
            if pos not in points:
                points[pos] = step
    return points


def run(path1, path2):
    path1, path2 = [x.rstrip().split(',') for x in [path1, path2]]
    first_wire = get_points(path1)
    second_wire = get_points(path2)
    intersections = set(first_wire.keys()) & set(second_wire.keys())

    def closest_intersection():
        return min(map(lambda x: abs(x[0]) + abs(x[1]), list(intersections)))

    def fewest_steps_required():
        return min(map(lambda x: first_wire[x] + second_wire[x],
                       list(intersections)))

    return closest_intersection(), fewest_steps_required()


if __name__ == '__main__':
    result = run('R8,U5,L5,D3', 'U7,R6,D4,L4')
    assert result == (6, 30), 'actual: {}'.format(result)

    result = run('R75,D30,R83,U83,L12,D49,R71,U7,L72',
                 'U62,R66,U55,R34,D71,R55,D58,R83')
    assert result == (159, 610), 'actual: {}'.format(result)

    result = run('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
                 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7')
    assert result == (135, 410), 'actual: {}'.format(result)

    with open('day3.txt') as file:
        first_path, second_path = file.readlines()
        result = run(first_path, second_path)
        print(result)
