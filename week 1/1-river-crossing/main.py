def is_illegal(state):
    return (not "F" in state) and "G" in state and ("W" in state or "C" in state)
    
def get_moves(left_state, right_state):
    state = left_state if "F" in left_state else right_state
    moves = []
    if "W" in state:
        moves.append("FW")
    if "C" in state:
        moves.append("FC")
    if "G" in state:
        moves.append("FG")
    moves.append("F")
    return moves

def make_move(left_state, right_state, move):
    if "F" in left_state:
        new_left_state = [c for c in left_state if c not in move]
        new_right_state = right_state + list(move)
    if "F" in right_state:
        new_right_state = [c for c in right_state if c not in move]
        new_left_state = left_state + list(move)

    return new_right_state, new_left_state


def river_crossing(left_state = ['F', 'G', 'W', 'C'], right_state = [], moves = [], visited = set()):
    '''
        herhalingen worden niet verder gecheckt
        het maximum aantal states, en dus de diepte van de search is 7 omdat er geen herhaalde states mogen zijn
        de branching factor is afhankelijk van het aantal mogelijke zetten van een state

        O(b^d)
    '''
    if is_illegal(left_state) or is_illegal(right_state): # loss
        return

    if len(left_state) == 0: # win
        print("WINNER!:", moves)
        return

    possible_moves = get_moves(left_state, right_state)
    for move in possible_moves:
        moves.append(move)
        new_right_state, new_left_state = make_move(left_state, right_state, move)

        key = "".join(sorted(new_left_state)) + "|" + "".join(sorted(new_right_state))
        if key not in visited:
            visited.add(key)
            river_crossing(new_left_state, new_right_state, moves, visited)
            visited.remove(key)

        moves.pop()

river_crossing()