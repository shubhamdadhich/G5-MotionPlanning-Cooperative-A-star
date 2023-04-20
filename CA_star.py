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
def CA_star_search(init_state, f, is_goal, actions, actions_goal_reached, h, res_table, robot_id, diagonalf, time_cap, costDict):
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
        
        # check if state has not been visited (by current robot)
        if n_i.state not in visited:
            visited.append(n_i.state)
            if is_goal(n_i.state):
                path, action_path = backpath(n_i)
                if len(path) < time_cap:
                    # import pdb;pdb.set_trace()
                    for a in (actions[:-1] + actions_goal_reached):
                        # print(a)
                        s_prime = f(n_i.state, a)
                        n_prime = SearchNode(s_prime, actions[:-1] + actions_goal_reached, n_i, a)
                        # only add node and its cost if not in p-queue yet
                        # f = g + h
                        
                        n_prime.cost = costpath(n_prime, actions, costDict, goalAction=actions_goal_reached) + h(n_prime.state)

                        # if n_prime isn't in the queue and has not been visited by previous robot
                        if frontier.get_cost(n_prime) is None and n_prime.state not in res_table:

                            # check for robots jumping over each other in x direction in space-time
                            diagonal_top, diagonal_bot = diagonalf(n_prime.state, a)
                            if diagonal_top not in res_table and diagonal_bot not in res_table:
                                frontier.push(n_prime, n_prime.cost)
                if len(path) >= time_cap:
                    # make robot path 'reserved' in space-time
                    for state in path:
                        res_table.add(tuple(state), robot_id)
                    return (path, visited, res_table)
            else:

                for a in actions:
                    s_prime = f(n_i.state, a)
                    n_prime = SearchNode(s_prime, actions, n_i, a)
                    # only add node and its cost if not in p-queue yet
                    # f = g + h
                    
                    n_prime.cost = costpath(n_prime, actions, costDict) + h(n_prime.state)

                    # if n_prime isn't in the queue and has not been visited by previous robot
                    if frontier.get_cost(n_prime) is None and n_prime.state not in res_table:
                        # check for robots jumping over each other in x direction in space-time
                        # if n_i.state[:-1] == (7, 5) and a == 'r':
                        #     import pdb;pdb.set_trace()
                        diagonal_top, diagonal_bot = diagonalf(n_prime.state, a)
                        if diagonal_top and diagonal_bot:
                            if diagonal_top not in res_table and diagonal_bot not in res_table:
                                frontier.push(n_prime, n_prime.cost)

                    # NOTE may need to add this back in later, took out because causing errors
                    #elif n_prime.cost < frontier.get_cost(n_prime):
                    #    frontier.push(n_prime, n_prime.cost)
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

def costpath(node, actions, costDict, goalAction=None):
    '''
    Function to backtrack the cost of the node
    '''
    cost = 0
    # run until start node is hit
    while node.parent is not None:
        if node.parent_action in actions:
            cost = cost + costDict[node.parent_action]
            node = node.parent
        elif goalAction and node.parent_action in goalAction:
            cost = cost + costDict[node.parent_action]
            node = node.parent
        else:
            raise Exception("Invalid action")
        
    return (cost)