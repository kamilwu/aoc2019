import math


def formula(mass):
    return math.floor(mass / 3) - 2


def calc_fuel_requirements():
    with open('data/day1.txt') as file:
        return [formula(int(x)) for x in file.readlines()]


def calc_extra_fuel(fuel):
    extra = formula(fuel)
    return extra + calc_extra_fuel(extra) if extra > 0 else 0


if __name__ == '__main__':
    fuel_per_module = calc_fuel_requirements()
    print(sum(fuel_per_module))

    extra_fuel = [calc_extra_fuel(x) for x in fuel_per_module]
    print(sum(fuel_per_module) + sum(extra_fuel))
