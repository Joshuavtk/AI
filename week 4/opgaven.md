### Opgave 1: 

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

e) 4^10 = 1048576 mogelijke paden als stay overgeslagen word als stap (zie [E.py](E.py))

f) de branching factor is: 4

g) in totaal zijn er 20 mogelijke paden van 6 stappen lang (zie [g.png](g.png))

h) Zie [h.py](h.py)

Formule
(Waarbij x = abs(x1 - x2) en y = abs(y1 - y2)): 

$ F(x, y) = 1 + F(x-1, y) + F(x, y-1) $

i) $ 1 \over 5 $

j) 