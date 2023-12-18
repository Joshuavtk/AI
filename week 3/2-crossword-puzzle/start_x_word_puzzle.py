import os
from collections import deque

# kruiswoord puzzel

def make_domain():
    # domain is a dict var:value and value is a set of words with correct length
    domain = dict()
    for i in [4,5,6,7,11]:
        domain[i] = set() 

    words = open("words_NL.txt").read().splitlines()

    for word in words:
        index = len(word)
        if index in domain:
            domain[index].add(word)
    
    return domain


def valid(X, word, assign, unassigned_vars):
    for Y, intersection in unassigned_vars[X]['intersects'].items():
        if Y in assign:
            i, j = intersection
            if word[i] != assign[Y][j]:
                return False
    return True

def make_arc_consistent(domain, X, assign, unassigned_vars):
    pass

runCount = 0

def solve(domain, assign, unassigned_vars):
    global runCount
    runCount += 1
    if runCount % 1000 == 0:
        print(runCount, assign)
    if len(unassigned_vars) == len(assign):
        return True

    min_var = None
    for var, properties in unassigned_vars.items():
        if var in assign:
            continue
        
        if min_var == None:
            min_var = var
        else:
            min_var = max(min_var, var, key=lambda x: len(unassigned_vars[x]['intersects']))
        
    length = unassigned_vars[min_var]['length']

    for word in domain[length]:
        if not valid(min_var, word, assign, unassigned_vars):
            continue

        assign[min_var] = word

        # make arc consistent here ~

        if solve(domain, assign, unassigned_vars):
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
#  d: Lijkt niet zinvol omdat je snel kan berekenen welke waardes wel of niet voldoen aan de constraints
# 3: Realistisch gezien is het onmogelijk omdat er zoveel combinaties zijn.   