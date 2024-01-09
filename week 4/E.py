
def count(n, stay=True):
    if n == 0:
        return 1
    if stay:
        return 4 * count(n - 1, False)
    return count(n - 1, True)

steps = 10
paths = count(steps)

print(paths)