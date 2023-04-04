## Code to create various types of robots, e.g. (non) holonomic.
from actions import *
import sys, inspect

class Robot(object):

    def __init__(self, Id) -> None:
        self.Id = Id

class FourDirectionHolonomic(Robot):

    def __init__(self, Id) -> None:
        super().__init__(Id)
        self.name = "FourDirectionHolonomic"
        self.actionSet = CooperativeFourDirection()
        # self


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