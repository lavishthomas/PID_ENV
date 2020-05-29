eq = [5, 6, 7]

# 5 x 2 ^ 2 + 6 x 2 + 7
# 20 + 12 + 7
# 39

x_value = 2


def eq_evaluator(eq, x_value):
    total = 0
    for index, coefficient in enumerate(reversed(eq)):
        print(index, '  ', coefficient)
        total = total + (coefficient * (x_value ** (index)))

    print(total)


eq_evaluator(eq, x_value)
