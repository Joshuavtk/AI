import heapq

"""
a board (=state) is represented as a list of integers where 0 is the hole
note: a list is an ordered sequence, so [0,1,2] is not the same as [1,0,2]
note: lists are mutable, tuples are not
"""

class PriorityQueue:
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list.
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

def swap(state, hole, neighbor):
    # input is a board (list), returns a board where hole and neighbor are swapped
    s = state[:] # make a local copy
    s[hole], s[neighbor] = s[neighbor], s[hole]
    return s

def neighbors(state):
    # input is a board (flat list), returns a tuple of 2..4 neighboring states, depending on the hole
    n = () # tuple with neighboring states
    # find index of hole in s
    i = state.index(0)
    row = i//N # [0..N-1]
    # up or down: neighbor in [0..N*N]? then add to tuple
    if i-N >= 0: n = n + (swap(state, i, i-N),)
    if i+N < SIZE: n = n + (swap(state, i, i+N),)
    # left or right: neigbor in current row? then add to tuple
    if i-1 >= row*N: n = n + (swap(state, i, i-1),)
    if i+1 < (row+1)*N: n = n + (swap(state, i, i+1),)
    return n

def heuristic(state):
    # input is a board (list), returns an (optimistic) estimate of cost to reach the goal state.
    N = len(state) ** 0.5
    total_distance = 0
    for i, e in enumerate(state):
        if e != 0:
            current_row, current_col = divmod(i, N)
            target_row, target_col = divmod(e - 1, N)
            distance = int(abs(current_row - target_row) + abs(current_col - target_col))
            total_distance += distance
    return total_distance


def astar(start, goal):
    # input is a start state (list), returns the path to the goal state
    # path is a dictionary tuple_state => tuple_parent_state
    heap = PriorityQueue()
    path = dict()
    cost = dict()
    visited = set() 

    path[tuple(start)] = None
    cost[tuple(start)] = 0
    heap.put(start, 0)

    count = 0
    while not heap.empty():
        count += 1
        current = heap.get()

        if tuple(current) == goal:
            break
        
        visited.add(tuple(current))
        succesors = neighbors(current)
        for s in succesors:
            new_cost = cost[tuple(current)] + 1
            if tuple(s) not in visited or new_cost < cost[tuple(s)]:
                priority = new_cost + heuristic(s)
                heap.put(s, priority)
                path[tuple(s)] = tuple(current)
                cost[tuple(s)] = new_cost
                visited.add(tuple(s))

    print("total iterations:", count)
    print("puzzles in memory:", count + len(heap.elements))

    return path, cost[tuple(goal)]

def display(state):
    # input is state (tuple), returns a string representation for printing
    s = "".join(str(x) for x in state)
    return ' '.join(s[i:i+N] for i in range(0, SIZE, N))

def print_path(path):
    # input is a dict tuple_state => tuple_parent_state
    # print the path from start to goal
    state_list = []
    s = tuple_goal
    # put all states as strings in a list
    while s:    # an empty tuple is False
        state_list.append(display(s))
        s = path[s]
    # print states from start to goal
    for x in state_list[::-1]:
        print(x[0:3] + '\n' + x[4:7] + '\n' + x[8:11] + '\n')

def to_list(s):
    # input is a string of space-separated rows filled with N numbers, where 
    # 0 represents the hole; returns a list of size N^2
    s = s.replace(" ", "")
    return [int(x) for x in s]

# ------ main part --------------------

# start state, 0 is the hole
s = "867 254 301"
g = "123 456 780"

print("the start> ", s)
print("the goal > ", g)
print()

start = to_list(s) # convert to board as a list
SIZE = len(start)  # the total size, e.g. 9 or 16
N = int(SIZE**0.5) # size of row or column, e.g. 3 or 4

tuple_goal = tuple(to_list(g))  # goal state as a tuple, to to check if we're done

path, cost = astar(start, tuple_goal)
print("nr states visited:", cost)
print_path(path)
