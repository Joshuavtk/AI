# kruiswoord puzzel

def make_domain():
    # domain is a dict var:value and value is a set of words with correct length
    domain = dict()

    domain_size = dict()
    for i in [4,5,6,7,8,11]:
        domain_size[i] = set()    


def valid(key, a):
# key = variable, a is a dict var:value, where value is a word but can be None
    match key:
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
        case 6:
        case 7:
        case 8:
        case 9:
        case 10:
        case 11:
    return False

def make_arc_consistent(domain, a, key):
    # make variable x arc consistent with variable y
    # meaning: if words x and y overlap, and if word x = a[key] has no match in y.domain, 

# dict represents a tree: a dictionary variable:value
def solve(domain, assign, unassigned_vars):

