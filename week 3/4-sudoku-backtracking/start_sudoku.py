import time
from copy import deepcopy
from sudokus import top_95_sudokus, generated_sudokus

#   1 2 3 4 .. 9
# A
# B
# C
# D
# ..
# I

def cross(A, B):
    # concat of chars in string A and chars in string B
    return [a+b for a in A for b in B]

digits = '123456789'
rows   = 'ABCDEFGHI'
cols   = digits
cells  = cross(rows, cols) # 81 cells A1..9, B1..9, C1..9, ... 

# unit = a row, a column, a box; list of all units
unit_list = ([cross(r, cols) for r in rows] +                             # 9 rows 
             [cross(rows, c) for c in cols] +                             # 9 cols
             [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]) # 9 units


units = dict((s, [u for u in unit_list if s in u]) for s in cells)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in cells)

def test():
    # a set of tests that must pass
    assert len(cells) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in cells)
    assert all(len(peers[s]) == 20 for s in cells)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print ('All tests pass.')

def display(grid):
    # grid is a dict of {cell: string}, e.g. grid['A1'] = '1234'
    print()
    for r in rows:
        for c in cols:
            v = grid[r+c]
            # avoid the '123456789'
            if v == '123456789': 
                v = '.'
            print (''.join(v), end=' ')
            if c == '3' or c == '6': print('|', end='')
        print()
        if r == 'C' or r == 'F': 
            print('-------------------')
    print()

def parse_string_to_dict(grid_string):
    # grid_string is a string like '4.....8.5.3..........7......2.....6....   '
    # convert grid_string into a dict of {cell: chars}
    char_list1 = [c for c in grid_string if c in digits or c == '.']
    # char_list1 = ['8', '5', '.', '.', '.', '2', '4', ...  ]
    
    assert len(char_list1) == 81

    # replace '.' with '1234567'
    char_list2 = [s.replace('.', '123456789') for s in char_list1]

    # grid {'A1': '8', 'A2': '5', 'A3': '123456789',  }
    return dict(zip(cells, char_list2))

def no_conflict(grid, c, val):
    # check if assignment is possible: value v not a value of a peer
    for p in peers[c]:
        if grid[p] == val:
           return False # conflict
    return True

def check_if_valid_board(grid):
    no_collusions = True
    for cell in cells:
        value_to_check = grid[cell]
        for p in peers[cell]:
            if grid[p] == value_to_check:
                no_collusions = False
    if not no_collusions:
        print("ILLEGAL BOARD STATE FOUND!")


def solve(grid):
    default_values = [(cell, grid[cell]) for cell in cells if len(grid[cell]) == 1]
    grid = initialize_board(grid, default_values)
    # display(grid)
    solve_recursive(grid)

def solve_recursive(grid):
    if all(len(grid[cell]) == 1 for cell in cells):
        print("SOLUTION FOUND!:")
        display(grid)
        check_if_valid_board(grid)
        return True

    if len([cell for cell in cells if len(grid[cell]) > 1]) == 0:
        return False

    # Find the cell with the minimum number of possibilities
    min_cell = min((cell for cell in cells if len(grid[cell]) > 1), key=lambda cell: len(grid[cell]))

    for number in grid[min_cell]:
        if no_conflict(grid, min_cell, number):
            grid_copy = deepcopy(grid)
            grid_copy[min_cell] = number
            not_illegal, grid_copy = make_arc_consistent(grid_copy, number, min_cell)
            if not not_illegal:
                continue
            if solve_recursive(grid_copy):
                return True

    return False

def initialize_board(grid, default_values):
    for cell, value in default_values:
        for p in peers[cell]:
            
            prev_len = len(grid[p])

            grid[p] = grid[p].replace(value, '')

            if len(grid[p]) == 1 and len(grid[p]) != prev_len:
                number = grid[p]
                _, grid = make_arc_consistent(grid, number, p)

    return grid


def make_arc_consistent(grid, start_value, start_index) -> (bool, dict()):
    queue = [(x, start_value) for x in peers[start_index]]
    while queue:
        x,y = queue.pop(0)

        prev_len = len(grid[x])
        grid[x] = grid[x].replace(y, '')
        
        if len(grid[x]) == 0:
            return False, grid
                
        if len(grid[x]) == 1 and (len(grid[x]) != prev_len):
            number = grid[x]
            for p in peers[x]:
                if number in grid[p]:
                    queue.append((p, number))
        
    return True, grid


# minimum nr of clues for a unique solution is 17
slist = [None for x in range(20)]
slist[0] = '.56.1.3....16....589...7..4.8.1.45..2.......1..42.5.9.1..4...899....16....3.6.41.'
slist[1] = '.6.2.58...1....7..9...7..4..73.4..5....5..2.8.5.6.3....9.73....1.......93......2.'
slist[2] = '.....9.73.2.....569..16.2.........3.....1.56..9....7...6.34....7.3.2....5..6...1.'
slist[3] = '..1.3....5.917....8....57....3.1.....8..6.59..2.9..8.........2......6...315.9...8'
slist[4] = '....6.8748.....6.3.....5.....3.4.2..5.2........72...35.....3..........69....96487'
slist[5] = '.94....5..5...7.6.........71.2.6.........2.19.6...84..98.......51..9..78......5..'
slist[6] = '.5...98..7...6..21..2...6..............4.598.461....5.54.....9.1....87...2..5....'
slist[7] = '...17.69..4....5.........14.....1.....3.5716..9.....353.54.9....6.3....8..4......'
slist[8] = '..6.4.5.......2.3.23.5..8765.3.........8.1.6.......7.1........5.6..3......76...8.'
slist[9] = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[10]= '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
slist[11]= '...5....2...3..85997...83..53...9...19.73...4...84...1.471..6...5...41...1...6247'
slist[12]= '6.3.5....5...7..1...4.2.86.....8..533....61...5...26.4..1........2.........1.8.2.'
# Original 12 puzzle. Takes very long to complete
# slist[12]= '.....6....59.....82....8....45........3........6..3.54...325..6..................'
slist[13]= '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[14]= '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
slist[15]= '6..3.2....5.....1..........7.26............543.........8.15........4.2........7..'
slist[16]= '.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...'
slist[17]= '..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..'
slist[18]= '3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....'
slist[19]= '1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......'

# Use list of 95 difficult sudokus
slist += top_95_sudokus
slist += generated_sudokus

for i,sudo in enumerate(slist):
    print('*** sudoku {0} ***'.format(i))
    print(sudo)
    d = parse_string_to_dict(sudo)
    start_time = time.time()
    solve(d)
    end_time = time.time()
    hours, rem = divmod(end_time-start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print("duration [hh:mm:ss.ddd]: {:0>2}:{:0>2}:{:06.3f}".format(int(hours),int(minutes),seconds))
    print()
