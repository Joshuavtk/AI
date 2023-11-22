import random
import time


test_bord = [
    ["P", "I", "E", "T"],
    ["G", "A", "A", "T"],
    ["A", "T", "M", "S"],
    ["H", "U", "I", "S"]
]

def generate_board(n):
    return [[chr(97 + random.randint(0,25)) for j in range(n)] for i in range(n)]

f = open("words_EN.txt", "r")
dictionary = [row[:-1] for row in f]
total_letter_count = sum([len(word) for word in dictionary])
print(total_letter_count/len(dictionary))

board = generate_board(100)

class Tree(object):
    "Generic tree node."
    def __init__(self, name='root', children=None, is_word=False):
        self.name = name
        self.children = []
        self.is_word = is_word
        if children is not None:
            for child in children:
                self.add_child(child)

    def __contains__(self, item):
        if len(item) == 0:
            return True
        first = item[0]
        if first not in self.children:
            return False
        index = self.children.index(first)
        child = self.children[index]
        if child.name != first:
            return False
        return item[1::] in child

    def __eq__(self, item):
        return self.name == item

    def __repr__(self):
        return self.name
    
    def __getitem__(self, character):
        if character in self.children:
            idx = self.children.index(character)
            return self.children[idx]
        else:
            return False
    
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

def make_tree():
    count = 0
    f = open("words_EN.txt", "r")
    dictionary = [row[:-1] for row in f]
    root = Tree('$')
    for word in dictionary:
        current = root
        N = len(word)
        for i, character in enumerate(word):
            new_tree = current[character]
            if new_tree:
                current = new_tree
            else:
                child = Tree(character, is_word=i + 1 == N)
                current.add_child(child)
                count += 1
                current = child
    print(f"count1:{count}")
    return root


start = time.time()
print("start making tree")
root = make_tree()
print("finish making tree")

end = time.time()

print(end - start)


start = time.time()

def check_if_in_dictionary(word):
    '''
        Returns (boolean) is_word, (boolean) is_prefix
    '''
    global root
    current = root
    for character in word:
        new_tree = current[character]
        if new_tree:
            current = new_tree
        # if character in current.children:
        #     idx = current.children.index(character)
        #     current = current.children[idx]
        else:
            return False, False
        
    return current.is_word, 0 < len(current.children)

# assert check_if_in_dictionary("xyzs") == (False, False)
# assert check_if_in_dictionary("huis") == (True, True)
# assert check_if_in_dictionary("aardi") == (False, True)
# assert check_if_in_dictionary("aardige") == (True, False)


def walk_through_board(board):
    height, width = len(board), len(board[0])
    
    global root

    for y in range(height):
        for x in range(width):
            visited = set()
            stack = list()

            stack.append((x, y))
            # current_letter = board[y][x]
            # current_tree = root[current_letter]

            while len(stack) > 0:
                x, y = stack.pop()
                
                neighbours = get_neighbours(board, x, y)
                for neighbour in neighbours:
                    stack.append(neighbour)

            print(visited)
            
def get_neighbours(board, x, y):
    height, width = len(board), len(board[0]) 
    return [
        (x - 1 if x - 1 >= 0 else width - 1, y),
        (x, y - 1 if y - 1 >= 0 else height - 1),
        (x + 1 if x + 1 < width else 0, y),
        (x, y + 1 if y + 1 < height else 0),
    ]

found_words = set()

def get_letter_from_board(x,y, board):
    return board[y][x].lower()    

def walk_through_board_recursive(board, tree, x, y, word = "", visited = set()):
    if tree.is_word:
        global found_words
        found_words.add(word)
    
    neighbours = get_neighbours(board, x, y)
    for neighbour in neighbours:
        x, y = neighbour
        new_tree = tree[get_letter_from_board(x,y,board)]
        key = f"{x}:{y}"
        if new_tree and key not in visited:
            visited.add(key)
            walk_through_board_recursive(board, new_tree, x, y, word + get_letter_from_board(x,y,board), visited)
            visited.remove(key)
    
            

# board = test_bord

# print(root['a'])
            
height, width = len(board), len(board[0])
for y in range(height):
    for x in range(width):
        current_letter = get_letter_from_board(x,y,board)
        current_tree = root[current_letter]
        # print(current_letter)
        # print(current_tree)
        if current_tree:
            walk_through_board_recursive(board, current_tree, x, y, word=current_letter)
    
            

# print(get_letter_from_board(1,2,test_bord))
    
end = time.time()

print(end - start)

print(found_words)
