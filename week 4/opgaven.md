### Opgave 1:

$P(Blauw) = 0.15$

$P(Groen) = 0.85$

$P(Juist) = 0.8$

$P(Onjuist) = 0.2$

$ P(H) = P(Blauw) * P(Juist) + P(Groen) * P(Onjuist) = 0.29$

$ P(E) = P(E|H) * P(E|-H) = 0.12$

$ P(E) = P(Juist) * P(Onjuist) = 0.12$

$ P(H|E) = P(E) / P(H) = 0.4137 $

De kans is 41.37%


### Opgave 2: MARS ROBOT

a) 

b) De kans dat een willekeurige move 'left' is hangt af van de vorige toestand, maar in het geval dat de vorige toestand 'stay' is, is de kans $1 \over 5$ Hetzelfde geldt voor 'stay'.

c) Een kans van $1 \over 125$.

d) ${3 \over 25}$, dus als de robot oneindig lang door zou lopen zou de robot gemiddeld ${3 \over 25}t$ in de toestand 'stay' zitten.


|   |$S$       |$L$       |$U$       |$R$       |$D$       |$\sum$     |
|---|----------|----------|----------|----------|----------|-----------|
|$S$|$2\over10$|$2\over10$|$2\over10$|$2\over10$|$2\over10$|$10\over10$|
|$L$|$1\over10$|$9\over10$|$0\over10$|$0\over10$|$0\over10$|$10\over10$|
|$U$|$1\over10$|$0\over10$|$9\over10$|$0\over10$|$0\over10$|$10\over10$|
|$R$|$1\over10$|$0\over10$|$0\over10$|$9\over10$|$0\over10$|$10\over10$|
|$D$|$1\over10$|$0\over10$|$0\over10$|$0\over10$|$9\over10$|$10\over10$|

e) $ 4^{10} = 1048576 $ mogelijke paden als stay overgeslagen word als stap (zie [E.py](E.py))

f) de branching factor is: $4$

g) in totaal zijn er 20 mogelijke paden van 6 stappen lang (zie [g.png](g.png))

h) Zie [h.py](h.py)

Formule waarbij $ x = abs(x1 - x2)$ en $y = abs(y1 - y2)$: 

$ F(x, y) = 1 + F(x-1, y) + F(x, y-1) $

i) $ 1 \over 5 $

j) Ons Viterbi algoritme gaf dit als meest waarschijnlijkste pad (wat overeenkomt met het daadwerkelijke pad): [(5, 5, 'R'), (6, 5, 'R'), (6, 5, 'S'), (5, 5, 'L'), (4, 5, 'L'), (3, 5, 'L'), (3, 5, 'S'), (4, 5, 'R'), (5, 5, 'R'), (6, 5, 'R'), (7, 5, 'R'), (8, 5, 'R'), (9, 5, 'R'), (10, 5, 'R'), (11, 5, 'R'), (11, 5, 'S'), (10, 5, 'L'), (10, 5, 'S'), (11, 5, 'R'), (11, 5, 'S'), (10, 5, 'L'), (9, 5, 'L'), (8, 5, 'L'), (7, 5, 'L'), (6, 5, 'L')]

k) regel 110, 114 en 118 in model.py

l) Pruning zou mogelijk zijn maar er komen wat lastige dingen bij kijken zoals de cutoff bepalen. Daarnaast zou je met pruning het goede pad weg kunnen knippen met pruning omdat het aan het begin misschien nog een lage kans had.

m) Bij observations_v2 heeft ons algoritme als meest waarschijnlijkste pad dit gegeven (wat ook overeenkomt met het daadwerkelijke pad): [(5, 5, 'R'), (6, 5, 'R'), (6, 5, 'S'), (5, 5, 'L'), (4, 5, 'L'), (3, 5, 'L'), (3, 5, 'S'), (4, 5, 'R'), (5, 5, 'R'), (6, 5, 'R'), (7, 5, 'R'), (8, 5, 'R'), (9, 5, 'R'), (10, 5, 'R'), (11, 5, 'R'), (11, 5, 'S'), (10, 5, 'L'), (10, 5, 'S'), (11, 5, 'R'), (11, 5, 'S'), (10, 5, 'L'), (9, 5, 'L'), (8, 5, 'L'), (7, 5, 'L'), (6, 5, 'L')]

n) 0 fouten!

o) De tijdcomplexiteit is: $ O(TN^2) $. Het hangt af van de gekozen datastructuur. Als dijkstra ook gebruikmaakt van een trellis graph dan is de tijdcomplexiteit vergelijkbaar met viterbi.

p) paralleliseren, beam search, precomputed probability tables