"""

Othello is a turn-based two-player strategy board game.

-----------------------------------------------------------------------------
Board representation

We represent the board as a flat-list of 100 elements, which includes each square on
the board as well as the outside edge. Each consecutive sublist of ten
elements represents a single row, and each list element stores a piece. 
An initial board contains four pieces in the center:

    ? ? ? ? ? ? ? ? ? ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . o @ . . . ?
    ? . . . @ o . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? ? ? ? ? ? ? ? ? ?

The outside edge is marked ?, empty squares are ., black is @, and white is o.

This representation has two useful properties:

1. Square (m,n) can be accessed as `board[mn]`, and m,n means m*10 + n. This avoids conversion
   between square locations and list indexes.
2. Operations involving bounds checking are slightly simpler.
"""
import random
import math
import time

# The black and white pieces represent the two players.
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
# in total 8 directions.
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)
# search constants
MAX_DEPTH = 4
WEIGHTS = [
    [20, -3, 11, 8, 8, 11, -3, 20],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [20, -3, 11, 8, 8, 11, -3, 20],
]

def squares():
    # list all the valid squares on the board.
    # returns a list of valid integers [11, 12, ...]; e.g. 19,20,21 are invalid
    # 11 means first row, first col, because the board size is 10x10
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

def initial_board():
    # create a new board with the initial black and white positions filled
    # returns a list ['?', '?', '?', ..., '?', '?', '?', '.', '.', '.', ...]
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # the middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board

def print_board(board):
    # get a string representation of the board
    # heading '  1 2 3 4 5 6 7 8\n'
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    # begin,end = 11,19 21,29 31,39 ..
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))

    rep = rep.replace(" o", "⚪")
    rep = rep.replace(" @", "⚫")

    return rep

# -----------------------------------------------------------------------------
# Playing the game

# We need functions to get moves from players, check to make sure that the moves
# are legal, apply the moves to the board, and detect when the game is over.

# Checking moves. A move must be both valid and legal: it must refer to a real square,
# and it must form a bracket with another piece of the same color with pieces of the
# opposite color in between.

def is_valid(move):
    # is move a square on the board?
    # move must be an int, and must refer to a real square
    return isinstance(move, int) and move in squares()

def opponent(player):
    # get player's opponent piece
    return BLACK if player is WHITE else WHITE

def find_bracket(square, player, board, direction):
    # find and return the square that forms a bracket with square for player in the given
    # direction; returns None if no such square exists
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    # if last square board[bracket] not in (EMPTY, OUTER, opp) then it is player
    return None if board[bracket] in (OUTER, EMPTY) else bracket

def is_legal(move, player, board):
    # is this a legal move for the player?
    # move must be an empty square and there has to be a bracket in some direction
    # note: any(iterable) will return True if any element of the iterable is true
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(hasbracket(x) for x in DIRECTIONS)

def make_move(move, player, board):
    # when the player makes a valid move, we need to update the board and flip all the
    # bracketed pieces.
    board[move] = player
    # look for a bracket in any direction
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board

def make_flips(move, player, board, direction):
    # flip pieces in the given direction as a result of the move by player
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    # found a bracket in this direction
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction

# Monitoring players

# define an exception
class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board
    
    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

def legal_moves(player, board):
    # get a list of all legal moves for player
    # legal means: move must be an empty square and there has to be is an occupied line in some direction
    return [sq for sq in squares() if is_legal(sq, player, board)]

def any_legal_move(player, board):
    # can player make any moves?
    return any(is_legal(sq, player, board) for sq in squares())

# Putting it all together. Each round consists of:
# - Get a move from the current player.
# - Apply it to the board.
# - Switch players. If the game is over, get the final score.

def play(black_strategy, white_strategy, logging=True):
    # play a game of Othello and return the final board and score
    board = initial_board()
    prev_player = current_player = BLACK
    strategies = {BLACK: black_strategy, WHITE: white_strategy}
    while current_player := next_player(board, prev_player):
        if logging:
            tic = time.perf_counter()
            print(print_board(board))
            print("CALCULATED SCORE FOR BLACK:", score(BLACK, board) - score(WHITE, board))
        move = get_move(strategies[current_player], current_player, board)
        if logging:
            toc = time.perf_counter()
            print("PLAYER", PLAYERS[current_player].upper() + "'S TURN. CHOOSES:", move, f"in {toc - tic:0.4f} seconds")
        board = make_move(move, current_player, board)
        prev_player = current_player

    if logging:
        print("\n")
        print("\n")
        print(print_board(board))
    winner = prev_player
    if score(prev_player, board) < score(opponent(prev_player), board):
        winner = opponent(prev_player)
    
    if logging:
        print("POINTS:", score(winner, board) - score(opponent(winner), board))
        print("GAME FINISHED!", PLAYERS[winner].upper(), "WINS")
    return PLAYERS[winner]
        

def next_player(board, prev_player):
    # which player should move next?  Returns None if no legal moves exist
    current_player = opponent(prev_player)
    if any_legal_move(current_player, board):
        return current_player
    elif any_legal_move(prev_player, board):
        return prev_player
    return None

def get_move(strategy, player, board):
    # call strategy(player, board) to get a move
    return strategy(player, board)

def score(player, board):
    # compute player's score (number of player's pieces minus opponent's)
    player_pieces = 0
    for square in squares():
        if board[square] == player:
            player_pieces += 1
    return player_pieces

# Play strategies

def get_minimax_move(player, board):
    moves = legal_moves(player, board)
    bestMove = moves[0]
    bestScore = -math.inf
    for move in moves:
        new_board = make_move(move, player, board[::])
        score = minimax(new_board, opponent(player), 3, False)
        if score > bestScore:
            bestScore = score
            bestMove = move

    return bestMove

def get_negamax_move(player, board):
    moves = legal_moves(player, board)
    bestMove = moves[0]
    bestScore = -math.inf
    for move in moves:
        new_board = make_move(move, player, board[::])
        score = -negamax(new_board, player, MAX_DEPTH)
        if score > bestScore:
            bestScore = score
            bestMove = move

    return bestMove

def get_random_move(player, board):
    return random.choice(legal_moves(player, board))

# Algorithms

def board_heuristic_value(board, player):
    player_weights = 0
    for square in squares():
        x = square % 10
        y = square // 10
        if board[square] == player:
            player_weights += WEIGHTS[y-1][x-1]

    return player_weights 

def minimax(board, player, depth=4, maximizing=True, alpha=-math.inf, beta=math.inf):
    if depth == 0 or any_legal_move(player, board) == None:
        return board_heuristic_value(board, player) - board_heuristic_value(board, opponent(player))
    
    if maximizing:
        score = -math.inf
        moves = legal_moves(player, board)
        for move in moves:
            new_board = make_move(move, player, board[::])
            score = max(score, minimax(new_board, opponent(player), depth-1, not maximizing, alpha, beta))
            alpha = max(score, alpha)
            if alpha >= beta:
                break
    else: # Minimize
        score = math.inf
        moves = legal_moves(player, board)
        for move in moves:
            new_board = make_move(move, player, board[::])
            score = min(score, minimax(new_board, opponent(player), depth-1, not maximizing, alpha, beta))
            beta = min(score, beta)
            if beta <= alpha:
                break
    return score

def negamax(board, prev_player, depth=4, alpha=-math.inf, beta=math.inf):
    current_player = next_player(board, prev_player)

    if current_player is None:
        return (score(opponent(prev_player), board) - score(prev_player, board)) * 10000

    if depth == 0:
        return board_heuristic_value(board, opponent(prev_player)) - board_heuristic_value(board, prev_player)

    if current_player == prev_player:
        return -negamax(board, current_player, depth - 1, -beta, -alpha)

    moves = legal_moves(current_player, board)
    for move in moves:
        new_board = make_move(move, current_player, board[::])
        alpha = max(alpha, -negamax(new_board, current_player, depth - 1, -beta, -alpha))
        if alpha >= beta:
            break

    return alpha

play(get_negamax_move, get_random_move)

def get_winrate_over_multiple_matches(matches = 100):
    # Helper function to check winrate of algorithm over many matches
    wins = 0

    for i in range(matches):
        # Insert testing algorithms here
        winner = play(get_negamax_move, get_random_move, False)
        if winner == PLAYERS[BLACK]:
            wins += 1
        print("game", i + 1, "won by", winner)
        
    print("wins:", wins, "losses:", matches-wins, "winrate:", (wins / matches) * 100, "%")


# get_winrate_over_multiple_matches(20)

# Vragen:
# C: Het aantal stenen veranderd tijdens het othello spel heel erg, en een zet die veel stenen winst boekt is niet gelijk een goede zet omdat de tegenstander het misschien weer makkelijk terug kan krijgen.
# D: Met een diepte van 4 berekent negamax alle zetten binnen 2 seconden.
# F: Wij vinden, gemiddeld minder dan 3 seconden over een zet nadenken, acceptabel. Hij heeft een acceptabele performance bij een diepte van 4. 
# - Met een transpositietabel zou de performance een stuk beter kunnen zijn omdat dan bepaalde states niet opnieuw bezocht hoeven worden. 
# - Gebruik van bitboards om sneller legale zetten op te sporen. 
# - Matrix-vermenigvuldigingen gebruiken bij het berekenen van heuristics.