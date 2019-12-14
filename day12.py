from itertools import combinations


def apply_gravity(positions, velocities):
    per = list(combinations(zip(positions, velocities), 2))
    for first, second in per:
        factors = []
        for i in range(3):
            if first[0][i] > second[0][i]:
                factors.append(-1)
            elif first[0][i] < second[0][i]:
                factors.append(1)
            else:
                factors.append(0)

        vec = first[1]
        for i in range(3):
            vec[i] += factors[i]
        vec = second[1]
        for i in range(3):
            vec[i] += factors[i] * -1


def run(positions, steps):
    velocities = [[0] * 3 for _ in range(4)]

    for _ in range(steps):
        apply_gravity(positions, velocities)

        for pos, vel in zip(positions, velocities):
            for i in range(3):
                pos[i] += vel[i]
    return positions, velocities


def calculate_energy(positions, velocities):
    return sum([sum(map(abs, x)) * sum(map(abs, y))
                for x, y in zip(positions, velocities)])


if __name__ == '__main__':
    positions, velocities = run([[-1, 0, 2], [2, -10, -7], [4, -8, 8],
                                 [3, 5, -1]], steps=10)
    assert positions == [[2, 1, -3], [1, -8, 0], [3, -6, 1], [2, 0, 4]], \
        'actual: {}'.format(positions)
    energy = calculate_energy(positions, velocities)
    assert energy == 179, 'actual: {}'.format(energy)

    positions = [[3, 2, -6], [-13, 18, 10], [-8, -1, 13], [5, 10, 4]]
    positions, velocities = run(positions, steps=1000)
    energy = calculate_energy(positions, velocities)
    print(energy)
