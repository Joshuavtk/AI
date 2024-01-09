### Opgave 1: mars MARS ROBOT

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

e) 1024

f) de branching factor is: $  b^{\lfloor {d/2}  \rfloor} $

g) 0, je hebt minimaal 7 stappen nodig.

 - right -> (8,7) 
 - right -> (9,7)
 - right -> (10,7)
 - stay -> (10,7)
 - up -> (10,8)
 - up -> (10,9)
 - up -> (10,10)

