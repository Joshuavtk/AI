import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')

def calculate_slope(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else float('inf')

def lines_intersect(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    slope1 = calculate_slope(x1, y1, x2, y2)
    slope2 = calculate_slope(x3, y3, x4, y4)

    if slope1 != slope2:  # Lines have different slopes, so they intersect
        return True
    elif slope1 == slope2 == float('inf'):  # Vertical lines with the same x-coordinate
        print("Test1")
        return True
    elif slope1 == slope2 == 0:  # Horizontal lines with the same y-coordinate
        print("Test2")
        return True
    return False

def check_line_intersection_with_orientation_test(line1, line2):
    a,b = line1
    c,d = line2
    orientation1 = orientation(a, b, c)
    orientation2 = orientation(a, b, d)
    orientation3 = orientation(c, d, a)
    orientation4 = orientation(c, d, b)

    return (orientation1 != orientation2) and (orientation3 != orientation4)

def orientation(x,y,z):
    crossProduct = (y.y - x.y) * (z.x - x.x) - (y.x - x.x) * (z.y - x.y)

    if crossProduct == 0:
        return 0  # Collinear
    elif crossProduct > 0:
        return 1  # Clockwise
    else:
        return -1  # Counterclockwise

def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def NN(cities):
    cities = set(cities)
    current = next(iter(cities))
    cities.remove(current)

    tour = [current]
    while len(cities) > 0:
        closest = None
        for city in cities:
            if not closest:
                closest = city
            elif distance(current, city) < distance(current, closest):
                closest = city
        tour.append(closest)
        current = closest
        cities.remove(current)

    return tour

def two_opt(cities):
    tour = NN(cities)
    N = len(tour)
    
    for i in range(0, N):
        line1_revised = [tour[i-1], tour[i]]
        for j in range(0, N):
            if tour[j] not in line1_revised and tour[j - 1] not in line1_revised and check_line_intersection_with_orientation_test((tour[i - 1], tour[i]), (tour[j - 1], tour[j])):

                start = i
                end = j
                if i > j:
                    start = j 
                    end = i
                
                tour[start:end] = tour[start:end][::-1]

    return tour


def try_all_tours(cities):
    print(cities)
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)

def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # note: cities is a set, sets don't support indexing
    start = next(iter(cities)) 
    return [[start] + list(rest) for rest in itertools.permutations(cities - {start})]

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1]) for i in range(len(tour)))

def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed(42) # the current system time is used as a seed
                  # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height)) for c in range(n))

def plot_tour(tour): 
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-') # blue circle markers, solid line style
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()

def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    tour = algorithm(cities)
    t1 = time.process_time()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)

# give a demo with 10 cities using brute force
# plot_tsp(try_all_tours, make_cities(10))
cities = make_cities(500)
# plot_tsp(try_all_tours, cities)
plot_tsp(NN, cities)
plot_tsp(two_opt, cities)

# Vragen:
# a: Met seed 42 zit het 1.1% van de optimale route af
#   na het een paar keer te draaien zie je vaak wel een verschil van 5 tot 15%
#
# b: 0.072 seconden met een i7 4600U, totale lengte: 20914.6
#
# c: 
# for i in range(1, N):
#     line1 = (tour[i - 1], tour[i])
#     for j in range(1, N):
#         line2 = (tour[j - 1], tour[j])
#         if line1 != line2:
#             calculate the slope of both lines
#             
#             if the slopes are not parallel, they intersect
#             if the slopes approach infinity, they intersect
#             if the slopes are 0, they intersect
#             
#             return false
#
# d:
# NN-algoritme 500 steden lengte: 20914.6
# NN-algoritme met 2-opt lengte: 19106.4 
# Ongeveer 9,4% beter in 0.1 tot 0.2 sec (runtime verschilt nog wel eens)
#
# e: (1) N^2 tijdscomplexiteit
# (2) het zou dan 40 seconden lang duren