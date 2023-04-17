## Code to read in maps
from actions import *
from robots import *
import re
import numpy as np

DEFAULT_OBSTACLE_VALUE = -1

class MapReader(object):

    def __init__(self, mapFile):
        self.mapFile = mapFile
        self.robotType = None
        self.dof = None
        self.mapDim = None
        # self.actions = None
        self.robotCount = None
        self.goalSet = None
        self.initMap = None
        self.obstacleList = []
        self.readMapContents()

    def lookup(self, reg, data):
        for item in data:
            mobj = re.search(reg, item)
            if(mobj):
                return mobj
        return None
    
    def getGoals(self, data):
        goalFound = False
        for i, item in enumerate(data):
            mobj = re.search(r'GOAL_SET\:\n', item)
            if mobj:
                goalFound = True
                break
        if goalFound:
            self.goalSet = []
            for j in range(i+1, i + self.robotCount + 1):
                glsettxt = data[j].strip().split(':')
                glset = []
                for cdstxt in glsettxt:
                    coords = []
                    mobj1 = re.search(r'\[(.*)\]', cdstxt)
                    if mobj1 is None:
                        print("Coordinate not found for index: {}".format(j))
                        return
                    cdslist = mobj1.group(1).strip('').split(',')
                    for cd in cdslist:
                        coords.append(int(cd.strip()))
                    glset.append(coords)
                self.goalSet.append(glset)
            return True
        else:
            return False
    
    def printMap(self, map):
        for item in map:
            print(item)
        
    def getMap(self, data):
        mapFound = False
        for i, item in enumerate(data):
            mobj = re.search(r'MAP\:\n', item)
            if mobj:
                mapFound = True
                break
        if mapFound:
            self.initMap = np.zeros(self.mapDim, dtype=np.int32)
            for j in range(i+1, i + self.mapDim[1] +1):
                line = data[j].strip()
                # print(line, j)
                for k in range(len(line)):
                    if line[k] == "x":
                        self.initMap[j-(i+1)][k] = DEFAULT_OBSTACLE_VALUE
                        self.obstacleList.append((j-(i+1), k))
            return True
        else:
            return False

    def readMapContents(self):
        with open(self.mapFile) as f:
            data = f.readlines()

        mobj = self.lookup(r'ROBOT_TYPE\: (.*)', data)
        if mobj:
            self.robotType = getRobotClass(mobj.group(1).strip())
            if self.robotType is None:
                print("No robot found for {}".format(mobj.group(1).strip()))
                return None
            print("Robot Type: {}".format(self.robotType))
        else:
            print("Error: No match for Robot Type found")

        mobj = self.lookup(r'MAP_DIMENSIONS\: \[(.*)\]', data)
        if mobj:
            l = mobj.group(1).strip().split(',')
            self.mapDim = []
            for item in l:
                self.mapDim.append(int(item.strip()))
            print("Map Dimensions: {}".format(self.mapDim))
        else:
            print("Error: No match for Map Dimensions found")

        mobj = self.lookup(r'ROBOT_COUNT\: ([0-9]*)', data)
        if mobj:
            self.robotCount = int(mobj.group(1).strip())
            print("Robot Count: {}".format(self.robotCount))
        else:
            print("Error: No match for Robot Count found")

        self.getGoals(data)
        print("Goal Set: {}".format(self.goalSet))

        self.getMap(data)
        self.printMap(self.initMap)

if __name__ == "__main__":
    m = MapReader('maps/testmap0.txt')
    r = m.robotType(1)
    print(r.actionSet.actions)
