def run(first_path, second_path):
    first_path, second_path = [x.rstrip().split(',') for x in [first_path, second_path]]

    def add(a, b):
        return tuple(x + y for x, y in zip(a, b))

    def get_points(wire):
        vect = {
            'U': (0, 1),
            'D': (0, -1),
            'L': (-1, 0),
            'R': (1, 0)
        }
        coords = {}
        pos = 0, 0
        step = 0

        for point in wire:
            direction = point[0]
            n = int(point[1:])
            for _ in range(n):
                pos = add(pos, vect[direction])
                if pos not in coords:
                    coords[pos] = step
                step += 1
        return coords

    def closest_intersection(first_wire, second_wire):
        intersections = set(first_wire.keys()) & set(second_wire.keys())
        return min(map(lambda x: abs(x[0]) + abs(x[1]), list(intersections)))

    return closest_intersection(get_points(first_path), get_points(second_path))


if __name__ == '__main__':
    assert run('R8,U5,L5,D3', 'U7,R6,D4,L4') == 6
    assert run('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83') == 159
    assert run('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,'
                                                              'U6,R7') == 135

    with open('day3.txt') as file:
        first_path, second_path = file.readlines()
        result = run(first_path, second_path)
        print(result)
