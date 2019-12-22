import math
from queue import SimpleQueue
from collections import defaultdict, namedtuple


Order = namedtuple('Ingredient', 'ingredient amount')


def get_recipes(input):
    recipes = {}

    for line in input:
        ingredients, result = line.split(' => ')
        r_amount, r_label = result.split(' ')
        ingredients_list = []
        for ingredient in ingredients.split(', '):
            amount, label = ingredient.split(' ')
            ingredients_list.append(Order(label, int(amount)))
        recipes[r_label] = {'ingredients': ingredients_list,
                            'amount': int(r_amount)}
    return recipes


def get_fuel_cost(recipes, fuel_units=1):
    orders = SimpleQueue()
    orders.put(Order('FUEL', fuel_units))
    supply = defaultdict(int)
    ore_needed = 0

    while not orders.empty():
        order = orders.get()
        if order.ingredient == 'ORE':
            ore_needed += order.amount
        elif order.amount <= supply[order.ingredient]:
            supply[order.ingredient] -= order.amount
        else:
            recipe = recipes[order.ingredient]
            order = Order(order.ingredient, order.amount - supply[
                order.ingredient])
            factor = math.ceil(order.amount / recipe['amount'])
            supply[order.ingredient] = factor * recipe['amount'] - \
                                       order.amount
            for x in recipe['ingredients']:
                orders.put(Order(x.ingredient, factor * x.amount))
    return ore_needed


def make_fuel(recipes, ore_available):
    start = 1
    end = 10000000

    while end - start > 1:
        pivot = (end + start) // 2
        usage = get_fuel_cost(recipes, pivot)
        if usage > ore_available:
            end = pivot
        else:
            start = pivot
    return start


def get_puzzle(filename):
    with open(filename) as file:
        return [x.rstrip() for x in file.readlines()]


if __name__ == '__main__':
    test = ['9 ORE => 2 A', '8 ORE => 3 B', '7 ORE => 5 C', '3 A, 4 B => 1 AB',
            '5 B, 7 C => 1 BC', '4 C, 1 A => 1 CA',
            '2 AB, 3 BC, 4 CA => 1 FUEL']
    fuel_cost = get_fuel_cost(get_recipes(test))
    assert fuel_cost == 165, 'actual: %s' % fuel_cost

    test = ['157 ORE => 5 NZVS', '165 ORE => 6 DCFZ',
            '44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL',
            '12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ', '179 ORE => 7 PSHF',
            '177 ORE => 5 HKGWZ', '7 DCFZ, 7 PSHF => 2 XJWVT',
            '165 ORE => 2 GPVTF',
            '3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT']
    fuel_cost = get_fuel_cost(get_recipes(test))
    assert fuel_cost == 13312, 'actual: %s' % fuel_cost

    test = ['171 ORE => 8 CNZTR',
            '7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL',
            '114 ORE => 4 BHXH', '14 VRPVC => 6 BMBT',
            '6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL',
            '6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT',
            '15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW',
            '13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW',
            '5 BMBT => 4 WPTQ', '189 ORE => 9 KTJDG',
            '1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP',
            '12 VRPVC, 27 CNZTR => 2 XDBXC', '15 KTJDG, 12 BHXH => 5 XCVML',
            '3 BHXH, 2 VRPVC => 7 MZWV', '121 ORE => 7 VRPVC',
            '7 XCVML => 6 RJRHP', '5 BHXH, 4 VRPVC => 5 LTCX']
    fuel_cost = get_fuel_cost(get_recipes(test))
    assert fuel_cost == 2210736, 'actual: %s' % fuel_cost

    recipes = get_recipes(get_puzzle('day14.txt'))
    fuel_cost = get_fuel_cost(recipes)
    print(fuel_cost)
    print(make_fuel(recipes, 1000000000000))
