s = """0  0  0  0  0  0  0  0 81 
0  0 46 45  0 55 74  0  0 
0 38  0  0 43  0  0 78  0 
0 35  0  0  0  0  0 71  0 
0  0 33  0  0  0 59  0  0 
0 17  0  0  0  0  0 67  0 
0 18  0  0 11  0  0 64  0 
0  0 24 21  0  1  2  0  0 
0  0  0  0  0  0  0  0  0 """

class Board:
    def __init__(self, s):
        self.clues = []
        self.board, self.start_index, self.N = self.decode_board(s)
        self.final_value = self.N ** 2

    def decode_board(self, s: str) -> tuple[list[list], tuple, int]:
        board = []
        start_index = (-1, -1)
        for i, row in enumerate(s.splitlines()):
            filled_row = []
            j = 0
            for col in row.split(" "):
                if col != '':
                    number = int(col)
                    filled_row.append(number)
                    if number == 1:
                        start_index = (j, i)
                    if number != 0:
                        self.clues.append(number)
                    j += 1
            board.append(filled_row)

        N = len(board)
        self.clues = sorted(self.clues)[1:]
        return board, start_index, N
    
    def get_neighbours(self, x, y) -> list[int]:
        
        neighbours = []
        for i in range(-1,2,2):
            neighbour = self.get_value(x + i, y)
            if neighbour != -1:
                neighbours.append((x + i, y))
        
        for i in range(-1,2,2):
            neighbour = self.get_value(x, y + i)
            if neighbour != -1:
                neighbours.append((x, y + i))

        return neighbours
    
    def solve(self, position, stepcount, current_clue):
        '''
            branching factor is 4
            depth = N*N

            er vallen veel paden weg door de gegeven clues

            op het moment dat je alleen een 1 en N*N hebt heb je de worst case

            tijdscomplexiteit, worst case: O(b^d)
        '''
        x, y = position
        value = self.get_value(x, y)
        clue = self.clues[current_clue]

        if stepcount != value and value != 0:
            return
        
        if clue < stepcount:
            return

        if stepcount == self.final_value == clue:
            print("path found.")
            print(self)
            return   
        
        if value == clue:
            current_clue += 1
        else:
            self.board[y][x] = stepcount
        
        neighbours = self.get_neighbours(x,y)
        
        for neighbour in neighbours:
            self.solve(neighbour, stepcount+1, current_clue)

        self.board[y][x] = value

    def start_solve(self):
        self.solve(self.start_index, 1, 0)
                
    def get_value(self,x,y):
        if (x >= 0 and x < self.N) and (y >= 0 and y < self.N):
            return self.board[y][x]
        return -1

    def __repr__(self) -> str:
        repr_str = ""
        for row in self.board:
            s = '|'.join([str(col).rjust(2) for col in row])
            repr_str += s + '\n'
            repr_str += '-' * (len(s)) + '\n'
        return repr_str.rstrip()

board = Board(s)
board.start_solve()