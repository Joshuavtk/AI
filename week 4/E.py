def count(n, stay=True):
    if n == 0:
        return 1
    if stay:
        return 4 * count(n - 1, False)
    return count(n, True)

def count2(n, stay=True):
    if n == 0:
        return 1
    
    if stay:
        if n == 10: # only first step has 4 new directions (paths) otherwise add 3 new paths
            return 4 * count2(n - 1, False)
        return 3 * count2(n - 1, False)
    else:
        possible_routes = count2(n-1, True)

        sum = 1 + count2(n - 1, False) + possible_routes

        return sum


def count3(n, just_stood_still = True):
    if n <= 0:
        return 1
    
    if just_stood_still:
        return 4 * count3(n - 1, False)

    # sum = count3(n-1, False) # repeat
    sum = count3(n-1, False) # repeat
    sum += count3(n-1, True) # stay
    return sum


steps = 10

print("Function 1")
paths = count(steps)
print("Total paths:", paths)
print("Branching factor:", sum([count(x) / count(x - 1) for x in range(2,10)]) / 8)

print("---------------------")

print("Function 2")
paths = count2(steps)
print("Total paths:", paths)
print("Branching factor:", sum([count2(x) / count2(x - 1) for x in range(2,10)]) / 8)

print("---------------------")

print("Function 3")
paths = count3(steps)
print("Total paths:", paths)
print("Branching factor:", sum([count3(x) / count3(x - 1) for x in range(2,10)]) / 8)