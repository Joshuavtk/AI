import os
from collections import deque
from copy import deepcopy

# kruiswoord puzzel

def make_domain():
    # domain is a dict var:value and value is a set of words with correct length
    domain = dict()

    size_domain = dict()
    for i in [4,5,6,7,11]:
        size_domain[i] = set() 

    words = open("words_NL.txt").read().splitlines()

    for word in words:
        index = len(word)
        if index in size_domain:
            size_domain[index].add(word)

    for i, var in enumerate([4,11,5,5,6,5,5,4,5,6,7]):
        domain[i + 1] = deepcopy(size_domain[var])
    
    return domain


def valid(X, word, assign, unassigned_vars):
    for Y, intersection in unassigned_vars[X]['intersects'].items():
        if Y in assign:
            i, j = intersection
            if word[i] != assign[Y][j]:
                return False
    return True

def make_arc_consistent(domain, X, assign, unassigned_vars):
    # var : word
    new_domain = deepcopy(domain)
    stack = []
    for p in unassigned_vars[X]['intersects'].keys():
        changed = False
        for word in domain[p]:
            if not valid(p, word, assign, unassigned_vars):
                new_domain[p].remove(word)
                changed = True

        if len(new_domain[p]) == 0:
            return False, new_domain
        
        if changed:
            stack.append(p)

    while stack:
        current = stack.pop()

        if len(new_domain[current]) != 1:
            continue

        for p in unassigned_vars[current]['intersects'].keys():
            success, new_domain = make_arc_consistent(new_domain, p, assign, unassigned_vars)
            if not success:
                return False, new_domain

    return True, new_domain
    

def solve(domain, assign, unassigned_vars):
    if len(unassigned_vars) == len(assign):
        return True

    min_var = None
    for var in unassigned_vars.keys():
        if var in assign:
            continue
        
        if min_var == None:
            min_var = var
        else:
            min_var = max(min_var, var, key=lambda x: len(unassigned_vars[x]['intersects']))
    
    for word in domain[min_var]:
        if not valid(min_var, word, assign, unassigned_vars):
            continue

        assign[min_var] = word

        # make arc consistent here ~
        success, new_domain = make_arc_consistent(domain, min_var, assign, unassigned_vars)

        if not success:
            continue

        if solve(new_domain, assign, unassigned_vars):
            return True
        
        del assign[min_var]
        
    return False

domain = make_domain()
unassigned_vars_2 = {
    3: {'length': 5, 'intersects': { 9: (2, 0), 10: (4, 0) }},
    6: {'length': 5, 'intersects': { 9: (1, 3), 10: (3, 3) }},
    9: {'length': 5, 'intersects': { 3: (0, 2), 6: (3, 1) }},
    10: {'length': 6, 'intersects': { 3: (0, 4), 6: (3, 3) }},
}

unassigned_vars = {
    1: {'length': 4, 'intersects': { 2: (1, 6), 4: (3, 4) }},
    2: {'length': 11, 'intersects': { 1: (6, 1) }},
    4: {'length': 5, 'intersects': { 1: (4, 3), 5: (3, 0) }},
    5: {'length': 6, 'intersects': { 4: (0, 3), 11: (4, 0) }},
    7: {'length': 5, 'intersects': { 11: (3, 3) }},
    8: {'length': 4, 'intersects': { 11: (3, 6) }},
    11: {'length': 7, 'intersects': { 5: (0, 4), 7: (3, 3), 8: (6, 3) }},
}
assign = dict()
solution_found = solve(domain, assign, unassigned_vars)
print(assign)


assign = dict()
solution_found = solve(domain, assign, unassigned_vars_2)
print(assign)

# Vragen:
# 1:
#  a: 11 velden
#  b: alle woorden in het woordenboek
#  c: met een getal
#  d: meeste kruizingen, tiebreaker op woordlengte
# 2: 
#  a: 
#   - Het woord moet even lang zijn als het veld.
#   - Als het veld kruist met een veld wat al is ingevuld moet de letter op de positie overeenkomen
#  b: Als een crossing waarde waarin de positie van de crossing op beide velden staat. 
#     De lengte constraint wordt gerepresenteerd door de lengte van het veld op te slaan
#  c: Er bestaan één of meer waardes voor het kruisende veld
#  d: Het helpt met het tijdig stoppen van een search als er geen geldige mogelijkheden zijn voor een kruisend woord, het is dus zinvol.
# 3: Realistisch gezien is het onmogelijk omdat er zoveel combinaties zijn.   