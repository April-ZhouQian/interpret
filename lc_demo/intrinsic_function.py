def sub(S, x):
    return x[0]- x[1], S
def add(S, x):
    return x[0] + x[1], S
def div(S, x):
    return x[0] / x[1], S
def mul(S, x):
    return x[0] * x[1], S
def mod(S, x):
    return x[0] % x[1], S
def lt(S, x):
    return x[0] < x[1], S
def gt(S, x):
    return x[0] > x[1], S
def ge(S, x):
    return x[0] >= x[1], S
def le(S, x):
    return x[0] <= x[1], S
def eq(S, x):
    return x[0] == x[1], S
def logic_and(S, x):
    return x[0] and x[1], S
def logic_or(S, x):
    return x[0] or x[1], S
def logic_not(S, x):
    return not x, S