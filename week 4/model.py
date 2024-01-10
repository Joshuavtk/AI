import random
import math
import config as cf

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

#-----------------------------------------------------------------------------
# (x, y) = (0, 0) is the top left of the grid
#
# a state (x, y, action) is a combination of current position (x,y) and last/previous action
# where: 0 <= x,y <= cf.SIZE - 1 and action is one of {'L', 'R', 'U', 'D', 'S'}
#
#-----------------------------------------------------------------------------

class Distribution(dict):
    # the Distribution class extends a Python dictionary
    def __missing__(self, key):
        # if the key is missing, return probability 0
        return 0

    def renormalize(self):
        # scale all the probabilities so that they sum up to 1
        # renormalization is necessary for positions at borders/in corners

        normalization_constant = sum(self.values())
        for key in self.keys():
            self[key] /= normalization_constant

def get_all_states():
    # returns a (long) list of all possible states (position and previous action) ex. (7, 7, 'S')
    # we need this in Viterbi (1065 states)
    all_states = []
    for x in range(cf.SIZE):
        for y in range(cf.SIZE):
            possible_prev_actions = ['L', 'R', 'U', 'D', 'S']

            if x == 0: # previous action could not have been to go right
                possible_prev_actions.remove('R')
            if x == cf.SIZE - 1: # could not have gone left
                possible_prev_actions.remove('L')
            if y == 0: # could not have gone down
                possible_prev_actions.remove('D')
            if y == cf.SIZE - 1: # could not have gone up
                possible_prev_actions.remove('U')

            for action in possible_prev_actions:
                all_states.append((x, y, action))
    return all_states

def transition_model(state):
    # given a state (position and previous action), 
    # return a dict with keys = possible next states and values = probabilities
    # example output: {(7, 7, 'S'): 0.2, (7, 6, 'U'): 0.2, (7, 8, 'D'): 0.2, (6, 7, 'L'): 0.2, (8, 7, 'R'): 0.2}
    # note: top left position is (0,0)
    x, y, action = state
    distr_next_states = Distribution()
    possible_moves=[('S',0,0),('L',-1,0),('R',1,0),('U',0,-1),('D',0,1)]

    for move, hor_mov, vert_move in possible_moves:
        next_x = x + hor_mov
        next_y = y + vert_move
        # if the move remains on the grid (0..cf.SIZE-1), get the distribution for this move
        if (next_x >= 0) and (next_x < cf.SIZE) and (next_y >= 0) and (next_y < cf.SIZE):
            if action == 'S': # previous move was stay, 0.2 prob for all possible moves/stay
                distr_next_states[(next_x, next_y, move)] = .2
            elif move == 'S': # previous move was a displacement, so prob for stay = 0.1
                distr_next_states[(next_x, next_y, move)] = .1
            elif action == move: # previous move is same as next move, prob = 0.9
                distr_next_states[(next_x, next_y, move)] = .9

    # if were at border or in corner then renormalize
    distr_next_states.renormalize()
    return distr_next_states

def get_next_state(distr_next_states):
    # Sample the next state based on the probability distribution
    return max(distr_next_states.keys(), key=lambda k: distr_next_states[k])

def observation_model(state):
    # given a state, return the distribution for its observations = positions
    # example: state=(5, 4, 'S') returns {(5, 4): 0.2, (4, 4): 0.2, (6, 4): 0.2, (5, 3): 0.2, (5, 5): 0.2}
    x, y, action    = state
    observed_states = Distribution()
    observation_probs = [(0, 0, 0.2), (-1, 0, 0.2), (1, 0, 0.2), (0, -1, 0.2), (0, 1, 0.2)]

    for dx, dy, prob in observation_probs:
        # position is on the grid (0..cf.SIZE-1), get the observation prob for this position
        if (x + dx >= 0) and (x + dx < cf.SIZE) and (y + dy >= 0) and (y + dy < cf.SIZE):
            observed_states[(x + dx, y + dy)] = prob

    observed_states.renormalize()
    return observed_states

def Viterbi(all_possible_states, observations):
    viterbi = [{}]
    backpointer = [{}]

    o = observations[0]
    for s in all_possible_states:
        viterbi[0][s] = observation_model(s)[o]
        backpointer[0][s] = None
    
    for t in range(1, len(observations)):
        print(t)
        viterbi.append({})
        backpointer.append({})
        for s in all_possible_states:
            viterbi[t][s] = -1
            o = observations[t]
            for S in all_possible_states:
                prob = viterbi[t-1][S] * transition_model(S)[s] * observation_model(s)[o]
                if prob > viterbi[t][s]:
                    viterbi[t][s] = prob
                    backpointer[t][s] = S

    path = []
    bestpathprob = -1
    bestpathpointer = None
    for s in all_possible_states:
        prob = viterbi[-1][s]
        if prob > bestpathprob:
            bestpathprob = prob
            bestpathpointer = s

    path.append(bestpathpointer)
    previous = bestpathpointer 

    for t in range(len(viterbi) - 2, -1, -1):
        s = backpointer[t+1][previous]
        path.insert(0, s)
        previous = s

    return path

def load_data(filename):
    states = []
    observed_path = []

    with open(filename, 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            line = line.strip()
            parts = line.split()

            prev_action = parts[0]

            # get real position
            string_xy = parts[1].split(',')
            real_x = int(string_xy[0])
            real_y = int(string_xy[1])
            states.append((real_x, real_y, prev_action))

            # get observed position
            if parts[2] == 'missing':
                observed_path.append(None)
            else:
                string_xy = parts[2].split(',')
                observed_x = int(string_xy[0])
                observed_y = int(string_xy[1])
                observed_path.append((observed_x, observed_y))

    return states, observed_path

def move_robot (app, start):
    # plot a fully random path for demonstration
    # start[0]=x and start[1]=y
    prev = start
    for i in range(100):
        dir = random.choice(['L', 'R', 'U', 'D'])
        match dir:
            case 'L': current = prev[0]-1, prev[1]
            case 'R': current = prev[0]+1, prev[1]
            case 'D': current = prev[0], prev[1]-1
            case 'U': current = prev[0], prev[1]+1

        # check if new position is valid
        if (current[0] >= 0 and current[0] <= cf.SIZE-1 and current[1] >= 0 and current[1] <= cf.SIZE-1):
            app.plot_line_segment(prev[0], prev[1], current[0], current[1], color=cf.ROBOT_C)
            app.pause()
            app.plot_line_segment(prev[0], prev[1], current[0], current[1], color=cf.PATH_C)
            prev = current
            app.pause()

    app.plot_node(current, color=cf.ROBOT_C)

