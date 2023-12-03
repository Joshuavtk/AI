import tkinter as tk
import model

# global gui vars
SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10
BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", 32:"#f67c5f", 64:"#f65e3b",
                       128:"#edcf72", 256:"#edcc61", 512:"#edc850", 1024:"#edc53f", 2048:"#edc22e", 4096: "#3c3a32",
                     8192 : "#3c3a32", 16384: "#3c3a32", 32768: "#3c3a32", 65536: "#3c3a32"}

FOREGROUND_COLOR_DICT = {2:"#776e65", 4:"#776e65"}
DEFAULT_FOREGROUND_COLOR = "#f9f6f2"

FONT = ("Verdana", 40, "bold")

class MainApp(tk.Frame):
    # frame for the grid (subclass of tk.Frame)
    def __init__(self, root):
        tk.Frame.__init__(self)
        self.root = root
        self.grid() # tk layout manager grid
        self.grid_cells = [] # GUI grid
        self.init_grid()
        self.board = model.start()    # init model (& add 2 values)
        self.update_grid_cells()      # redraw grid
        
    def init_grid(self):
        background = tk.Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid() # tk layout manager grid
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = tk.Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/GRID_LEN, height=SIZE/GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                t = tk.Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=tk.CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row) # append values to list

    def update_grid_cells(self):
        # redraw grid
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.board[i][j] # get value from model
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number],
                                                 fg=FOREGROUND_COLOR_DICT.get(new_number, DEFAULT_FOREGROUND_COLOR))
        self.update_idletasks() # redraw widgets
        
    def do_move(self):
        # direction = model.get_random_move()
        direction = model.get_expectimax_move(self.board)
        if direction:
            self.board = model.play_move(self.board, direction)
            self.update_grid_cells()            # redraw grid
            self.root.after(100, self.do_move)  # reschedule do_move in 100 msec

        # else: game over, no reschedule

# create and start GUI
root = tk.Tk()  # create root window
root.title("2048")

app = MainApp(root)
root.after(1000, app.do_move)
root.mainloop()
