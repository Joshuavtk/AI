import itertools

floors = [1, 2, 3, 4, 5]

for (L, M, N, E, J) in list(itertools.permutations(floors)):
    if E > M and abs(J - N) != 1 and abs(M - N) != 1 and L != 5 and N != 5 and N != 1 and M != 1:
        print("Loes:", L, ", Marja:", M, ", Niels:", N,", Erik:", E,", Joep:", J)
