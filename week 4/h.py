def calculate_amount_of_manhattan_paths(x,y):
    paths = 0
    if x > 0:
        paths += calculate_amount_of_manhattan_paths(x-1, y)
    if y > 0:
        paths += calculate_amount_of_manhattan_paths(x, y-1)
    if x == 0 and y == 0:
        return 1

    return paths


print(calculate_amount_of_manhattan_paths(3,3))
print(calculate_amount_of_manhattan_paths(2,3))
print(calculate_amount_of_manhattan_paths(3,2))
print(calculate_amount_of_manhattan_paths(2,2))

# first do |x1 - x2| and |y1 - y2|
# e.g. x1 = 14, y1 = 9, x2 = 3, y2 = 5
x1 = 14
y1 = 9
x2 = 3
y2 = 5
paths = calculate_amount_of_manhattan_paths(abs(x1-x2), abs(y1-y2))
print(paths)