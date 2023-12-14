# kruiswoord puzzel
import os

class FieldNode:
    def __init__(self, node_number, length) -> None:
        self.word = ""
        self.node_number = node_number
        self.length = length
        self.crossings = []

    def add(self, field_node, p1, p2):
        self.crossings.append((field_node, p1))
        field_node.crossings.append((self, p2))
        return self
    
    def __str__(self):
        return str(self.node_number)
    
    def __repr__(self):
        return str(self)
    
    # def __repr__(self) -> str:
    #     self_str = f"nodenr. {self.node_number}: "
    #     for field, index in self.crossings:
    #         self_str += f"(Crosses node: {field.node_number} at index: {index}), "
    #     return self_str

nodes_lengths = [4,11,5,5,6,5,5,4,5,6,7]
crossings = [
    {
        "node_a": 1,
        "index_a": 1,
        "node_b": 2,
        "index_b": 6,
        "letter": ''
    },
]
nodes = []

for i, length in enumerate(nodes_lengths):
    nodes.append(FieldNode(i + 1, length))

nodes[0].add(nodes[1], 1, 6).add(nodes[3], 3, 4)
nodes[3].add(nodes[4], 3, 0)
nodes[10].add(nodes[4], 0, 4).add(nodes[6], 3, 3).add(nodes[7], 6, 3)

nodes[2].add(nodes[8], 2, 0).add(nodes[9], 4, 0)
nodes[5].add(nodes[8], 1, 3).add(nodes[9], 3, 3)

for node in nodes:
    print(node)

dictionary = open(os.path.dirname(os.path.abspath(__file__)) + "/words_NL.txt").read().splitlines()
# print(dictionary[-50:])

def make_domain():
    # domain is a dict var:value and value is a set of words with correct length
    domain = dict()
    for i in [4,5,6,7,11]:
        domain[i] = set()

    for word in dictionary:
        index = len(word)
        if index in domain:
            domain[index].add(word)
    
    return domain


def valid(key, a):
# key = variable, a is a dict var:value, where value is a word but can be None
    match key:
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass
        case 5:
            pass
        case 6:
            pass
        case 7:
            pass
        case 8:
            pass
        case 9:
            pass
        case 10:
            pass
        case 11:
            pass
    return False

def make_arc_consistent(domain, a, key):
    # make variable x arc consistent with variable y
    # meaning: if words x and y overlap, and if word x = a[key] has no match in y.domain, 
    pass

# dict represents a tree: a dictionary variable:value
def solve(field, domain=make_domain()):
    words = domain[field.length]

    for child, p1 in field.crossings:
        if child.word != "":
            continue
        
        index = [f[0] for f in child.crossings].index(field)
        parent, p2 = child.crossings[index]

        for word in words:
            if field.word != "" and field.word[p1] != word[p2]:
                continue

            field.word = word
            solve(child, domain)
            field.word = ""

# make_domain()
# print(len(nodes))

solve(nodes[10])

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
#  c: Er bestaat één of meer waardes voor kruisende veld
#  d: lijkt niet zinvol omdat je snel kan berekenen welke waardes wel of niet voldoen aan de constraints
# 3: Realistisch gezien is het onmogelijk omdat er zoveel combinaties zijn.   
