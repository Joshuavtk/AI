import tkinter as tk
from tkinter import ttk
import model as mo
import config as cf

# global var
START_FLAG = True # do not redraw grid when pressing start the first time

class MainApp(tk.Frame):
    # view + controller
    # frame for the grid (subclass of tk.Frame)
    def __init__(self, root):
        tk.Frame.__init__(self)
        # save root window
        self.root = root
        # save user values
        self.delay = tk.StringVar()
        # create grid and control frame
        self.make_grid_panel()
        self.make_control_panel()
        # plot grid and nodes in grid frame
        self.re_plot()

    def pause(self):
        self.root.after(int(self.delay.get()) * cf.DELAY) # pause in msec
        self.root.update_idletasks() # redraw widgets

    def make_grid_panel(self):
        # init grid frame (and canvas)
        left_frame = tk.Frame(self.root)
        left_frame.grid(column=0, row=0, padx=12, pady=12)
        self.canvas = tk.Canvas(left_frame, height=cf.H+4*cf.TR, width=cf.W+4*cf.TR, borderwidth=-cf.TR, bg = cf.BG_C)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def make_grid(self):
        # vertical lines
        for i in range(0, cf.W+1, cf.CELL):
            self.canvas.create_line(i+cf.TR, 0+cf.TR, i+cf.TR, cf.H+cf.TR, fill = cf.GRID_C)
        # horizontal lines
        for i in range(0, cf.H+1, cf.CELL):
            self.canvas.create_line(0+cf.TR, i+cf.TR, cf.W+cf.TR, i+cf.TR, fill = cf.GRID_C)

    def plot_line_segment(self, x0, y0, x1, y1, color):
        self.canvas.create_line(x0*cf.CELL+cf.TR, y0*cf.CELL+cf.TR, x1*cf.CELL+cf.TR, y1*cf.CELL+cf.TR, fill = color, width = 2)

    def plot_node(self, node, color):
        # size of (red) square is 8 by 8
        x0 = node[0]*cf.CELL - (cf.BLOCK_SIZE/2)
        y0 = node[1]*cf.CELL - (cf.BLOCK_SIZE/2)
        x1 = x0 + cf.BLOCK_SIZE + 1
        y1 = y0 + cf.BLOCK_SIZE + 1
        self.canvas.create_rectangle(x0+cf.TR, y0+cf.TR, x1+cf.TR, y1+cf.TR, fill = color)

    def make_control_panel(self):
        # note: self.alg is an instance variable, and lf1 is a local variable
        # note: make_control_panel is an instance function and start_search is a local function

        right_frame = tk.Frame(self.root)
        right_frame.grid(column=1, row=0, padx=12, pady=12)

        # LabelFrame 1 to group start button and algorithm select button
        lf1 = tk.LabelFrame(right_frame)
        lf1.grid(column=0, row=0, padx=8, pady=4)
        lf1.grid_rowconfigure(2, minsize=10)

        def start():
            # do not redraw grid when pressing start the first time
            global START_FLAG
            if not START_FLAG:
                self.re_plot()
            START_FLAG = False
            #mo.move_robot(self, cf.START_POS)
            # this will start the main program
            mo.move_robot(self, cf.START_POS)

        start_button = tk.Button(lf1, text="Start", command=start, width=10)
        start_button.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        def box_update1(event):
            # print selected delay
            print('delay is set to:', box1.get())

        # LabelFrame 2 to group delay and probability buttons
        lf2 = tk.LabelFrame(right_frame, relief="sunken")
        lf2.grid(column=0, row=1, padx=5, pady=5)

        # within lf2, create label and combobox for delay value
        tk.Label(lf2, text="Delay").grid(column=1, row=1, sticky='w')
        box1 = ttk.Combobox(lf2, textvariable=self.delay, state='readonly', width=6)
        box1.grid(column=1, row=2, sticky='w')
        box1['values'] = tuple(str(i) for i in range(5)) # can select 0..4
        box1.current(1) # set to 1
        box1.bind("<<ComboboxSelected>>", box_update1)

    def re_plot(self):
        # (re)paint grid and nodes
        self.canvas.delete("all")
        self.make_grid()
        # show start and goal nodes
        self.plot_node(cf.START_POS, color=cf.START_C)

# create and start GUI
root = tk.Tk()
root.title('Mars robot')

app = MainApp(root)
root.mainloop()
