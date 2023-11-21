# assuming a resulution of 1920 x 1080 = 16 : 9

# color scheme
BG_C    = '#FDF6E3'
GRID_C  = '#542437'
BLOCK_C = 'red'
PATH_C  = 'lightblue'
FINAL_C = 'blue'
START_C = '#C7F464'
GOAL_C  = 'yellow'

# grid size
START = (0, 0) # try to modify the start position!
SIZE  = 25     # the nr of nodes=grid crossings in a row (or column)
GOAL  = (SIZE-1, SIZE-1)

# pixel sizes
CELL  = 35           # size of cell in pixels
W  = (SIZE-1) * CELL # width of grid in pixels
H  = W               # height of grid
TR = 10              # translate/move the grid, upper left is TR,TR


