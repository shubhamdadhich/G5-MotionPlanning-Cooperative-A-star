# actions class will be implemented here
import numpy as np


class ActionSet(object):

    def __init__(self) -> None:
        pass


class CooperativeFourDirection(ActionSet):

    _T = 2
    _X = 1 
    _Y = 0

    def __init__(self) -> None:
        super().__init__()
        self.actions = ['r', 'l', 'u', 'd', 'wait']
        self.goalReachedAction = ['pgoal']
        self.actionsDict = {'r': [0, 1, 1],
                        'l': [0, -1, 1],
                        'u': [-1, 0, 1],
                        'd': [+1, 0, 1],
                        'wait': [0, 0, 0.25]}
        self.costDict = {'r':1, 'l':1, 'u':1, 'd':1, 'wait': 0.25, 'pgoal': 0}
        self.xdirs = ['r', 'l']
        self.ydirs = ['u', 'd']

    def isgoal(self, s, goal):
        # if(s[:-1]==(5,5)):
        #     import pdb;pdb.set_trace()
        return (s[self._X] == goal[self._X] and s[self._Y] == goal[self._Y])
        
    def move(self, s, a, rows, cols):
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
            if s[self._Y] > 0:
                new_pos[self._Y] -= 1
                new_pos[self._T] += 1
        elif a == 'd':
            if s[self._Y] < rows - 1:
                new_pos[self._Y] += 1
                new_pos[self._T] += 1
        elif a == 'l':
            if s[self._X] > 0:
                new_pos[self._X] -= 1
                new_pos[self._T] += 1
        elif a == 'r':
            if s[self._X] < cols - 1:
                new_pos[self._X] += 1
                new_pos[self._T] += 1
        elif a == 'wait':   # ADD Pause Action
            new_pos[self._T] += 1
        elif a == 'pgoal':   # ADD Pause Action
            new_pos[self._T] += 1

        else:
            print('Unknown action:', str(a))

        return new_pos
    
    
    def checkDiagonal(self, s, a):
        if a in self.xdirs:
            diagonal_top_x = tuple(np.subtract(s,(0,0,1)))
            if a == 'r':
                diagonal_bottom_x = tuple(np.subtract(s,(1,0,0)))
            elif a == 'l':
                diagonal_bottom_x = tuple(np.add(s,(1,0,0)))
            return diagonal_top_x, diagonal_bottom_x
        elif a in self.ydirs:
            diagonal_top_y = tuple(np.subtract(s,(0,0,1)))
            if a == 'u':
                diagonal_bottom_y = tuple(np.add(s,(0,1,0)))
            elif a == 'd':
                diagonal_bottom_y = tuple(np.subtract(s,(0,1,0)))
            return diagonal_top_y, diagonal_bottom_y
        return None, None