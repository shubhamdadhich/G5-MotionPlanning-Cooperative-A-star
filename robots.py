## Code to create various types of robots, e.g. (non) holonomic.
import sys, inspect
from actions import *
from mapObj import *
from CA_star import *

class Robot(object):

    def __init__(self, id, currPos=None) -> None:
        self.id = id
        self.currPos=currPos
        self.path = None
        self.visited = None
        self.mapObj = None
        self.path = None

class FourDirectionHolonomic(Robot):
    
    actionSet = CooperativeFourDirection()

    def __init__(self, Id) -> None:
        super().__init__(Id)
        self.name = "FourDirectionHolonomic"
    
    def getPath(self, mapDim, camap, res_table, start, goal):
        self.mapObj = MapObj2D(mapDim, camap, start, goal, __class__.actionSet)
        self.path, self.visited, res_table = CA_star_search(self.mapObj.initPos, self.mapObj.transition, self.mapObj.is_goal, self.mapObj.actionSet.actions, self.mapObj.actionSet.goalReachedAction,
                                                            self.mapObj.manhattan_heuristic, res_table, self.id, self.mapObj.check_diagonal, 200, self.actionSet.costDict)
        return self.path, self.visited, res_table


def getRobotClass(robotString):
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for item in clsmembers:
        if robotString == item[0]:
            if item[1]:
                return item[1]
            else:
                print("Error: no Robot class defined for: {}".format(robotString))
    print("Error: no Robot class found for: {}".format(robotString))
    return None