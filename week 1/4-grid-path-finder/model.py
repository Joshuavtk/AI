import random
import heapq
import math
import config as cf

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

class PriorityQueue:
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[1]

def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10 else 0

def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    return grid[node[0]][node[1]]

def set_grid_value(node, value): 
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    grid[node[0]][node[1]] = value

def get_neighbours(position) -> list[int]:
    x, y = position
    neighbours = []
    for i in range(-1,2,2):
        nx = x + i
        if nx >= 0 and nx <= cf.SIZE - 1:
            neighbours.append((x + i, y))
    
    for i in range(-1,2,2):
        ny = y + i
        if ny >= 0 and ny <= cf.SIZE - 1:
            neighbours.append((x, y + i))

    return neighbours

def manhattan_distance(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

def euclidean_distance(start, goal):
    return math.sqrt((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2)

def octile_heuristic(start, goal):
    dx = abs(start[0] - goal[0])
    dy = abs(start[1] - goal[1])
    return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)

def search(app, start, goal):
    alg = app.alg.get()
    
    frontier = PriorityQueue()
    visited = set()
    cost = dict()
    path = dict()

    frontier.put(start, 0)
    cost[start] = 0
    path[start] = None
    path[goal] = None

    while not frontier.empty():
        current = frontier.get()
        app.plot_node(current, cf.CURRENT_C)
    
        visited.add(current)

        if current == goal:
            break

        successors = get_neighbours(current)
        for s in successors:
            new_cost = cost[current] + 1
            if get_grid_value(s) != 'b' and (s not in visited or new_cost < cost[s]):
                cost[s] = new_cost
                heuristic = 0
                priority = new_cost + heuristic
                if alg == 'A*':
                    heuristic = manhattan_distance(s, goal)
                    priority = new_cost * 0.99 + heuristic
                    
                app.plot_node(s, cf.FRONTIER_C)

                frontier.put(s, priority)
                visited.add(s)
                path[s] = current

        if current != start:
            app.plot_node(current, cf.PATH_C)
        app.pause()

    current = goal
    previous = goal
    while current:
        previous = current
        current = path[current]
        if current != None:
            app.plot_line_segment(previous[0],previous[1], current[0], current[1], color=cf.FINAL_C)
        app.pause()
        previous = current
