# actions class will be implemented here


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
        self.actionsDict = {'r': [0, 1, 1],
                        'l': [0, -1, 1],
                        'u': [-1, 0, 1],
                        'd': [+1, 0, 1],
                        'wait': [0, 0, 0.25]}
        self.costDict = {'r':1, 'l':1, 'u':1, 'd':1, 'wait': 0.25}

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

        else:
            print('Unknown action:', str(a))

        return new_pos