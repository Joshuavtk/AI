steps_per_step = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0}

def count(n, stay=True):
    if n == 0:
        return 1
    if stay:
        return 4 * count(n - 1, False)
    return count(n - 1, True)

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
        
        steps_per_step[n] = sum

        return sum



steps = 10
paths = count2(steps)

print(paths)

print(steps_per_step)