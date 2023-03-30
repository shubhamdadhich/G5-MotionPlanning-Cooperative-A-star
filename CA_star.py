# original 'graph_search.py' script converted to include
# time dimension and corresponding actions
#.!/usr/bin/env python

import sys
import numpy as np
import heapq
import matplotlib.pyplot as plotter
from math import hypot, sqrt

_DEBUG = False
_DEBUG_END = True
_ACTIONS = ['u','d','l','r','p']  # p for pause
_T = 2
_X = 1 
_Y = 0
_GOAL_COLOR = 0.75
_INIT_COLOR = 0.25
_PATH_COLOR_RANGE = _GOAL_COLOR-_INIT_COLOR
_VISITED_COLOR = 0.9

class GridMap:
    '''
    Class to hold a grid map for navigation. Reads in a map.txt file of the format
    0 - free cell, x - occupied cell, g - goal location, i - initial location.
    Additionally provides a simple transition model for grid maps and a convience function
    for displaying maps.
    '''
    def __init__(self, map_path=None):
        '''
        Constructor. Makes the necessary class variables. Optionally reads in a provided map
        file given by map_path.

        map_path (optional) - a string of the path to the file on disk
        '''
        self.rows = None
        self.cols = None
        self.goal = None
        self.init_pos = None
        self.occupancy_grid = None
        if map_path is not None:
            self.read_map(map_path)

# edit
    def read_map(self, map_path):
        '''
        Read in a specified map file of the format described in the class doc string.

        map_path - a string of the path to the file on disk
        '''
        map_file = open(map_path,'r')
        lines = [l.rstrip().lower() for l in map_file.readlines()]
        map_file.close()
        self.rows = len(lines)
        self.cols = max([len(l) for l in lines])
        if _DEBUG:
            print('rows', self.rows)
            print('cols', self.cols)
            print(lines)
        self.occupancy_grid = np.zeros((self.rows, self.cols), dtype=np.bool)
        for r in range(self.rows):
            for c in range(self.cols):
                if lines[r][c] == 'x':
                    self.occupancy_grid[r][c] = True
                if lines[r][c] == 'g':
                    self.goal = (r,c)
                elif lines[r][c] == 'i':
                    self.init_pos = (r,c,0)

    def is_goal(self,s):
        '''
        Test if a specifid state is the goal state

        s - tuple describing the state as (row, col) position on the grid.

        Returns - True if s is the goal. False otherwise.
        '''
        return (s[_X] == self.goal[_X] and
                s[_Y] == self.goal[_Y])

    def transition(self, s, a):
        '''
        Transition function for the current grid map.

        s - tuple describing the state as (row, col) position on the grid.
        a - the action to be performed from state s

        returns - s_prime, the state transitioned to by taking action a in state s.
        If the action is not valid (e.g. moves off the grid or into an obstacle)
        returns the current state.
        '''
        new_pos = list(s[:])
        # Ensure action stays on the board
        if a == 'u':
            # if not at top edge
            if s[_Y] > 0:
                new_pos[_Y] -= 1
                new_pos[_T] += 1
        elif a == 'd':
            if s[_Y] < self.rows - 1:
                new_pos[_Y] += 1
                new_pos[_T] += 1
        elif a == 'l':
            if s[_X] > 0:
                new_pos[_X] -= 1
                new_pos[_T] += 1
        elif a == 'r':
            if s[_X] < self.cols - 1:
                new_pos[_X] += 1
                new_pos[_T] += 1
        elif a == 'p':   # ADD Pause Action
            new_pos[_T] += 1

        else:
            print('Unknown action:', str(a))

        # Test if new position is clear
        if self.occupancy_grid[new_pos[0], new_pos[1]]:
            s_prime = tuple(s)
        else:
            s_prime = tuple(new_pos)
        return s_prime

# edit
    def display_map(self, path=[], visited={}, filename=None):
        '''
        Visualize the map read in. Optionally display the resulting plan and visisted nodes

        path - a list of tuples describing the path take from init to goal
        visited - a set of tuples describing the states visited during a search
        filename - relative path to file where image will be saved
        '''
        display_grid = np.array(self.occupancy_grid, dtype=np.float32)

        # Color all visited nodes if requested
        for v in visited:
            display_grid[v[0],v[1]] = _VISITED_COLOR
        # Color path in increasing color from init to goal
        for i, p in enumerate(path):
            disp_col = _INIT_COLOR + _PATH_COLOR_RANGE*(i+1)/len(path)
            display_grid[p[0],p[1]] = disp_col

        display_grid[self.init_pos[0],self.init_pos[1]] = _INIT_COLOR
        display_grid[self.goal] = _GOAL_COLOR

        # Plot display grid for visualization
        imgplot = plotter.imshow(display_grid)
        # Set interpolation to nearest to create sharp boundaries
        imgplot.set_interpolation('nearest')
        # Set color map to diverging style for contrast
        imgplot.set_cmap('Spectral')
        if filename is not None:
            plotter.savefig(filename)
        plotter.show()
        
    def uninformed_heuristic(self, s):
        '''
        Example of how a heuristic may be provided. This one is admissable, but dumb.

        s - tuple describing the state as (row, col) position on the grid.

        returns - floating point estimate of the cost to the goal from state s
        '''
        return 0.0
    
    def euclidean_heuristic(self, s):
        '''
        Euclidian distance heuristic
        '''
        a = abs(s[0]-self.goal[0])
        b = abs(s[1]-self.goal[1])
        dist = sqrt((a**2)+(b**2))
        return dist
    
    def manhattan_heuristic(self, s):
        '''
        Manhattan distance heuristic
        '''
        a = abs(s[0]-self.goal[0])
        b = abs(s[1]-self.goal[1])
        dist = a + b
        return dist

class SearchNode:
    def __init__(self, s, A, parent=None, parent_action=None, cost=0):
        '''
        s - the state defining the search node (x,y,t)
        A - list of actions
        parent - the parent search node
        parent_action - the action taken from parent to get to s
        '''
        self.parent = parent
        self.cost = cost
        self.parent_action = parent_action
        self.state = s[:]
        self.actions = A[:]

    def __str__(self):
        '''
        Return a human readable description of the node
        '''
        return str(self.state) + ' ' + str(self.actions)+' '+str(self.parent)+' '+str(self.parent_action)
    def __lt__(self, other):
        return self.cost < other.cost

class PriorityQ:
    '''
    Priority queue implementation with quick access for membership testing
    Setup currently to only with the SearchNode class
    '''
    def __init__(self):
        '''
        Initialize an empty priority queue
        '''
        self.l = [] # list storing the priority q
        self.s = set() # set for fast membership testing

    def __contains__(self, x):
        '''
        Test if x is in the queue
        '''
        return x in self.s

    def push(self, x, cost):
        '''
        Adds an element to the priority queue.
        If the state already exists, we update the cost
        '''
        # added "cost < self.get_cost(x)"
        if x.state in self.s:
            return self.replace(x, cost)
        heapq.heappush(self.l, (cost, x))
        self.s.add(x.state)

    def pop(self):
        '''
        Get the value and remove the lowest cost element from the queue
        '''
        x = heapq.heappop(self.l) 
        self.s.remove(x[1].state)
        return x[1]

    def peak(self):
        '''
        Get the value of the lowest cost element in the priority queue
        '''
        x = self.l[0]
        return x[1]

    def __len__(self):
        '''
        Return the number of elements in the queue
        '''
        return len(self.l)

    def replace(self, x, new_cost):
        '''
        Removes element x from the q and replaces it with x with the new_cost
        '''
        for y in self.l:
            if x.state == y[1].state:
                self.l.remove(y)
                self.s.remove(y[1].state)
                break
        heapq.heapify(self.l)
        self.push(x, new_cost)

    def get_cost(self, x):
        '''
        Return the cost for the search node with state x.state
        '''
        for y in self.l:
            if x.state == y[1].state:
                return y[0]

    def __str__(self):
        '''
        Return a string of the contents of the list
        '''
        return str(self.l)

# edit
def CA_star_search(init_state, f, is_goal, actions, h):
    '''
    init_state - value of the initial state
    f - transition function takes input state (s), action (a), returns s_prime = f(s, a)
        returns s if action is not valid
    is_goal - takes state as input returns true if it is a goal state
        actions - list of actions available
    h - heuristic function, takes input s and returns estimated cost to goal
        (note h will also need access to the map, so should be a member function of GridMap)
    '''
    frontier = PriorityQ() # priority queue
    n0 = SearchNode(init_state, actions, cost = 0) 
    visited = []
    frontier.push(n0, n0.cost)
    while len(frontier) > 0:  
        # Expand lowest cost node
        n_i = frontier.pop()
        if n_i.state not in visited:
            visited.append(n_i.state)
            if is_goal(n_i.state):
                path, action_path = backpath(n_i)
                return (path, visited)
            else:
                for a in actions:
                    s_prime = f(n_i.state, a)
                    n_prime = SearchNode(s_prime, actions, n_i, a)
                    # only add node and its cost if not in p-queue yet
                    # f = g + h
                    n_prime.cost = costpath(n_prime) + h(n_prime.state)

                    if frontier.get_cost(n_prime) is None: # if n_prime isn't in the queue
                        frontier.push(n_prime, n_prime.cost)
                    elif n_prime.cost < frontier.get_cost(n_prime):
                        frontier.push(n_prime, n_prime.cost)
    return None

def backpath(node):
    '''
    Function to determine the path that lead to the specified search node

    node - the SearchNode that is the end of the path

    returns - a tuple containing (path, action_path) which are lists respectively of the states
    visited from init to goal (inclusive) and the actions taken to make those transitions.
    '''
    path = []
    action_path = []
    # add goal node to path
    path.append(node.state)
    # run until start node is hit
    while node.parent is not None:
        # add parent node to the path
        node = node.parent
        path.append(node.state)
    # put path in order of start to finish
    path.reverse()
    return (path, action_path)

def costpath(node):
    '''
    Function to backtrack the cost of the node
    '''
    cost = 0
    # run until start node is hit
    while node.parent is not None:
        if node.parent_action in ['u','d','l','r','p']:
            cost = cost + 1
            node = node.parent
        
    return (cost)