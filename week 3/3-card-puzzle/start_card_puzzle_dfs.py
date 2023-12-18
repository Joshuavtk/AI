'''Constraints:
    1 every Ace borders a King
    2 every King borders a Queen
    3 every Queen borders a Jack
    4 no Ace borders a Queen
    5 no two of the same cards border each other

'''
import itertools
from math import factorial as fact

# the board has 8 cells, let’s represent the board with a list [0..7]
start_board = ['.'] * 8
cards = ['K', 'K', 'Q', 'Q', 'J', 'J', 'A', 'A']
neighbors = {0:[3], 1:[2], 2:[1,4,3], 3:[0,2,5], 4:[2,5], 5:[3,4,6,7], 6:[5], 7:[5]}

def is_valid(board):
    valid = True
    for idx, card in board.items():
        has_prerequisite = card == "J" or card == "."
        
        for neighbor_idx in neighbors[idx]:
            neighbor_card = board[neighbor_idx]
            valid &= check_if_valid_combination(card, neighbor_card)
            if check_if_prerequisite(card, neighbor_card):
                has_prerequisite = True
            
        valid &= has_prerequisite

    return valid
        
def check_if_valid_combination(card_1, card_2):
    if '.' in [card_1, card_2]:
        return True
    if card_1 == card_2:
        return False
    if card_1 in ['Q', 'A'] and card_2 in ['A', 'Q']:
        return False
    return True

def check_if_prerequisite(card_1, card_2):
    return card_2 == "." or card_1 == 'A' and card_2 == 'K' or card_1 == 'K' and card_2 == 'Q' or card_1 == 'Q' and card_2 == 'J'

assert not is_valid({0: 'J', 1: 'K', 2: 'Q', 3: 'Q', 4: 'J', 5: 'K', 6: 'A', 7: 'A'})
assert not is_valid({0: 'J', 1: 'J', 2: 'Q', 3: 'Q', 4: 'K', 5: 'K', 6: 'A', 7: 'A'})
assert is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'})
assert is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'})
assert not is_valid({0: '.', 1: '.', 2: '.', 3: 'J', 4: 'J', 5: 'A', 6: 'J', 7: 'J'}) # [1]
assert not is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'K', 6: 'J', 7: 'Q'}) # [3]
assert is_valid({0: '.', 1: 'Q', 2: '.', 3: '.', 4: 'Q', 5: 'J', 6: '.', 7: '.'}) # [3] 
assert not is_valid({0: 'Q', 1: '.', 2: '.', 3: 'K', 4: '.', 5: '.', 6: '.', 7: '.'}) # [3]
assert not is_valid({0: '.', 1: 'A', 2: 'Q', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: '.'}) # [4]
assert not is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'J', 6: '.', 7: '.'}) # [5]
assert not is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: 'Q'}) # [5]
assert is_valid({0: 'Q', 1: 'Q', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'})
assert is_valid({0: 'K', 1: 'Q', 2: 'J', 3: 'Q', 4: 'A', 5: 'K', 6: 'J', 7: 'A'}) # Solution


counter = 0

def dfs(board, cards, i=7, visited=set()):
    global counter
    counter += 1
    setup = tuple(board.values())

    if setup in visited:
        return False

    visited.add(setup)

    if is_valid(board) and "." not in setup:
        print("Oplossing gevonden:", board)
        return
    
    if not is_valid(board):
        return
    
    for card in cards:
        board[i] = card
        cards_copy = cards[::]
        cards_copy.remove(card)
        dfs(board, cards_copy, i-1, visited)
        board[i] = '.'

def brute_force(cards):
    i = 0
    visited = set()
    for setup in itertools.permutations(cards):
        if setup in visited:
            continue
        visited.add(setup)
        i += 1
        board_state = {i: x for i,x in enumerate(setup)}
        if is_valid(board_state):
            print("Oplossing gevonden:", board_state)     

    print("Aantal permutaties getest:", i, "(Moet overeen komen met):", int(fact(8) / (fact(2) * fact(2) * fact(2) * fact(2))))


print("Start brute force")
brute_force(cards)

print("\n")
print("Start DFS")
dfs({i: x for i,x in enumerate(start_board)}, cards)
print("Aantal permutaties getest:", counter)

# Vragen:
#     
# a
#  1: het aantal permutaties is 8! = 40320, het aantal unieke permutaties is 2520
#     De uiteindelijke formule voor permutaties met herhaalde waarden is n! / (n1! * n2! * n3! * n4! ... * nk!) 
#       waarbij n1 ... nk de hoeveelheid van dezelfde waarde zijn voor elke waarde
#     Dus dan is de formule 8! / (2! * 2! * 2! * 2!) = 40320 / 16 = 2520
#  2: 2520
#
# b (geimplementeerd) iets meer dan 404 iteraties
# 
# c (afbeelding)
# c5_vrouw:
# - 3,4,6,7 kunnen geen aas of vrouw zijn vanwege [4] en [5]
# - 0,1,2 moeten een aas of vrouw zijn
# - als 1 of 2 een A is kan er geen V meer naast komen te staan vanwege [4]
# - als 0 een A is moeten er op 1 en 2 een V en dat kan niet vanwege [5]

# c5_boer:
# - 3,4,6,7 kunnen geen B zijn vanwege [5]
# - 3 moet V zijn vanwege [2]
# - 0 en 2 moeten heer zijn vanwege [2]
# - 1 moet B zijn want er is geen andere mogelijke positie voor de tweede B
# - nu is er geen plek om aan regel [1] te voldoen omdat maar een aas naast een H kan staan

# c5_aas:
# - 3,4,6,7 kunnen geen A zijn vanwege [5] 
# - 3,4,6,7 kunnen geen V zijn vanwege [4] 
# - dus 3,4,6,7 moet een H of B zijn 
# - er zijn maar 2xH en 2xB kaarten, dus 0,1,2 moet een A of V zijn
# - als 1 of 2 een V is kan er geen A meer naast komen te staan vanwege [4]
# - als 0 een V is moeten er op 1 en 2 een A en dat kan niet vanwege [5]