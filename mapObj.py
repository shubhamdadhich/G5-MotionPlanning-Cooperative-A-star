# Here the map will be stored

from math import hypot, sqrt

class MapObj2D(object):

    def __init__(self, mapDim, initMap, initPos, goal, actionSet) -> None:
        self.mapDim = mapDim
        self.initMap = initMap
        self.actionSet = actionSet
        initPos.append(0)
        self.initPos = tuple(initPos)
        self.goal = tuple(goal)

    def is_goal(self,s):
        '''
        Test if a specifid state is the goal state

        s - tuple describing the state as (row, col) position on the grid.

        Returns - True if s is the goal. False otherwise.
        '''
        return self.actionSet.isgoal(s, self.goal)

    def transition(self, s, a):
        # Test if new position is clear
        new_pos = self.actionSet.move(s, a, self.mapDim[0], self.mapDim[1])
        if self.initMap[new_pos[0], new_pos[1]]:
            s_prime = tuple(s)
        else:
            s_prime = tuple(new_pos)
        return s_prime
    
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