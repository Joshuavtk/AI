import random
import itertools
import math

MAX_DEPTH = 6
CHANCE = 1
MAX = 2

def merge_left(b):
    # merge the board left
    # this is the function that is reused in the other merges
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]    
    def merge(row, acc):
        # recursive helper for merge_left

        # if len row == 0, return accumulator
        if not row:
            return acc

        x = row[0]
        # if len(row) == 1, add element to accumulator
        if len(row) == 1:
            return acc + [x]

        # if len(row) >= 2
        if x == row[1]:
            # add row[0] + row[1] to accumulator, continue with row[2:]
            return merge(row[2:], acc + [2 * x])
        else:
            # add row[0] to accumulator, continue with row[1:]
            return merge(row[1:], acc + [x])

    new_b = []
    for row in b:
        # merge row, skip the [0]'s
        merged = merge([x for x in row if x != 0], [])
        # shift left: add zeros to the right if necessary
        merged = merged + [0] * (len(row) - len(merged))
        new_b.append(merged)
    # return [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    return new_b

def merge_right(b):
    # merge the board right
    # strategy: is like merge_left with all rows reversed
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def reverse(x):
        return list(reversed(x))

    rev = [reverse(x) for x in b]
    ml = merge_left(rev)
    # return [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    return [reverse(x) for x in ml]


def merge_up(b):
    # merge the board upward
    # note that zip(*b) is the transpose of b
    trans = merge_left(zip(*b))
    return [list(x) for x in zip(*trans)]


def merge_down(b):
    # merge the board downward
    # note that zip(*b) is the transpose of b
    trans = merge_right(zip(*b))
    return [list(x) for x in zip(*trans)]


# translate directions to functions
MERGE_FUNCTIONS = {
    'L': merge_left,
    'R': merge_right,
    'U': merge_up,
    'D': merge_down
}

def give_moves(b):
    # a move is legal if (1) at least one tile can be shifted to an empty place or
    # (2) if two adjacent tiles have the same value != 0
    # return all possible moves for board b as a list with values L, R, U, D
    # if no move is possible an empty list is returned

    # note: in the original js-code the strategy is: try to do a move, only if move was possible
    # then add random tiles: if (moved) {this.addRandomTile(); ...}. Here we could call all four
    # merge-functions and then check, but this no so good performance-wise

    def inner(b, left, right):
        rlis = []
        flag = False
        for row in b:
            # special case where row contains only zeros
            if not all(val == 0 for val in row):
                # evaluate all pairs of adjacent tiles
                for x, y in zip(row[:-1], row[1:]):
                    # check if they are equal
                    if x == y and x != 0:
                        rlis = [left, right]
                        flag = True # no need to continue
                        break
                    # check first if shift left is possible
                    if x == 0 and y != 0:
                        rlis.append(left) if left not in rlis else rlis
                    # then check if shift right is possible
                    if x != 0 and y == 0:
                        rlis.append(right) if right not in rlis else rlis
            if flag:
                break

        return rlis

    res1 = inner(b, 'L', 'R')
    # check columns: zip(*b) is the transpose of b
    trans = [list(x) for x in zip(*b)]
    res2 = inner(trans, 'U', 'D')

    return res1 + res2

def start():
    # make initial board
    b = [[0] * 4 for _ in range(4)]
    add_two_four(b)
    add_two_four(b)
    return b


def play_move(b, direction):
    # get merge function and apply it to board
    b = MERGE_FUNCTIONS[direction](b)
    add_two_four(b)
    return b


def add_two_four(b):
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
    rows, cols = list(range(4)), list(range(4))
    random.shuffle(rows)
    random.shuffle(cols)
    distribution = [2] * 9 + [4]
    for i, j in itertools.product(rows, cols):
        if b[i][j] == 0:
            b[i][j] = random.sample(distribution, 1)[0]
            return (b)
        else:
            continue

def test():
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert merge_left(b) == [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    assert merge_right(b) == [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    assert merge_up(b) == [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert merge_down(b) == [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    b = [[2, 8, 4, 0], [16, 0, 0, 0], [2, 0, 2, 0], [2, 0, 0, 0]]
    assert (merge_left(b)) == [[2, 8, 4, 0], [16, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]]
    assert (merge_right(b)) == [[0, 2, 8, 4], [0, 0, 0, 16], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert (merge_up(b)) == [[2, 8, 4, 0], [16, 0, 2, 0], [4, 0, 0, 0], [0, 0, 0, 0]]
    assert (merge_down(b)) == [[0, 0, 0, 0], [2, 0, 0, 0], [16, 0, 4, 0], [4, 8, 2, 0]]

    b = [[0, 1, 2, 3], [0, 4, 5, 6], [0, 1, 2, 3], [0, 4, 5, 6]]
    assert (give_moves(b)) == ['L']
    b = [[0, 0, 0, 0], [1, 2, 3, 4], [5, 6, 7, 8], [1, 2, 3, 4]]
    assert (give_moves(b)) == ['U']
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert (give_moves(b)) == ['L','R','U','D']
    b = [[2, 8, 4, 2], [16, 0, 0, 0], [2, 4, 2, 8], [8, 0, 0, 0]]
    assert give_moves(b) == ['R','D','U']
    b = [[32, 64, 2, 16], [8, 32, 8, 2], [4, 16, 8, 4], [2, 8, 4, 2]]
    assert (give_moves(b)) == ['U','D']

    # no left 
    b = [[4, 0, 0, 0], [8, 2, 0, 0], [8, 4, 0, 0], [8, 16, 2, 0]]
    assert (give_moves(b)) == ['R','U','D']
    # no right
    b = [[2, 4, 2, 16], [0, 0, 16, 8], [0, 8, 16, 2], [0, 0, 4, 2]]
    assert (give_moves(b)) == ['L','U','D']
    # no up
    b = [[4, 4, 4, 8], [0, 2, 2, 4], [0, 0, 0, 16], [0, 0, 0, 0]]
    assert (give_moves(b)) == ['L','R','D']
    # no down
    b = [[0, 0, 0, 2], [0, 0, 2, 16], [0, 4, 32, 8], [4, 8, 4, 4]]
    assert (give_moves(b)) == ['L','R','U']
    
    #for i in range(11):
    #    add_two_four(b)
    #    print(b)

def get_random_move():
    return random.choice(list(MERGE_FUNCTIONS.keys()))

def get_expectimax_move(b):
    moves = give_moves(b)

    if len(moves) == 0:
        return False
    
    bestMove = moves[0]
    bestScore = 0
    for move in moves:
        new_b = MERGE_FUNCTIONS[move](b)
        score = expectimax(new_b, 1, MAX_DEPTH, False)
        if score > bestScore:
            bestScore = score
            bestMove = move
    return bestMove

weights = [[32768,16384,8192,4096],[256,512,1024,2048],[128,64,32,16],[1,2,4,8]]

def evaluate_board(b):
    return sum([math.log2((b[y][x]) - 1) * b[y][x] * weights[y][x] for y, x in itertools.product(range(4), range(4)) if b[y][x] != 0])

def key(b):
    b = tuple([tuple(row) for row in b])
    return hash(b) % 1_000_000, b

def expectimax(b, P, depth, player, table=[(None, -1) for _ in range(1_000_000)]):
    k, tb = key(b)

    entry_board, entry_score = table[k]

    if entry_score != -1 and entry_board == tb:
        return entry_score

    moves = give_moves(b)
    zeros = count_zeros(b)

    if depth == 0 or P < 0.0001:
        return evaluate_board(b)
    
    score = 0
    if player:
        for move in moves:
            new_b = MERGE_FUNCTIONS[move](b)
            score = max(score, expectimax(new_b, P, depth - 1, False, table))
    else:
        P2 = (0.9 / zeros)
        P4 = (0.1 / zeros)
        for y, x in itertools.product(range(4), range(4)):
            if b[y][x] != 0:
                continue
            b[y][x] = 2
            score += P2 * expectimax(b, P2 * P, depth - 1, True, table)
            b[y][x] = 4
            score += P4 * expectimax(b, P4 * P, depth - 1, True, table)
            b[y][x] = 0

    table[k] = (tb, score)

    return score


def count_zeros(b):
    zeros = 0
    for y, x in itertools.product(range(4), range(4)):
        if b[y][x] != 0:
            continue
        zeros += 1
    return zeros
    



#test()

# Vraag B:
# Met een probability pruning van 0.01% dan heeft de depth niet zo'n grote impact meer hoger dan 8 omdat de probability van alle zetten die dieper dan 8 zijn bijna altijd lager dan 0.01% ligt.
# Qua acceptabele snelheid zouden we zelf zeggen een depth van 6 is de max. 
# De transpositie tabel voorkomt dat eerder bezochte posities opnieuw worden gevalueerd.
# bitboards, iterative deepening, betere heuristiek