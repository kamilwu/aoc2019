from collections import Counter


def password_gen(start, stop, any_num_repeated_twice):
    i = start
    while i <= stop:
        password = str(i)
        never_decrease = True

        counts = Counter(password).values()
        if any_num_repeated_twice:  # part 2
            has_adjacent = 2 in counts
        else:  # part 1
            has_adjacent = max(counts) > 1

        # The digits never decrease
        for index in range(len(password) - 1):
            if int(password[index]) > int(password[index + 1]):
                never_decrease = False
                break

        if has_adjacent and never_decrease:
            yield i
        i += 1


def possible_passwords(start, stop):
    return len(list(password_gen(start, stop, any_num_repeated_twice=False))), \
           len(list(password_gen(start, stop, any_num_repeated_twice=True)))


if __name__ == '__main__':
    print(possible_passwords(134564, 585159))
