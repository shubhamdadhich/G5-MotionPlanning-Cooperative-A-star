# Central server class will be implemented here

from map_reader import MapReader
from res_table import Reservation_table
from visualization_multiple import *

_buffer=10

class RobotServer(object):

    def __init__(self, mapFile) -> None:
        self.mapFile = mapFile
        self.mapReader = MapReader(mapFile=self.mapFile)
        self.robotList = []
        self.resTable = Reservation_table()
        self.paths = []

    def startPlanning(self):

        for id, goalSet in zip(range(self.mapReader.robotCount), self.mapReader.goalSet):
            robotObj = self.mapReader.robotType(id+_buffer)
            self.robotList = [id+_buffer, robotObj]
            path, visited, self.resTable = robotObj.getPath(self.mapReader.mapDim, self.mapReader.initMap, self.resTable, goalSet[0], goalSet[1])
            self.paths.append(path)
            print(path)
        # print(self.paths)
        return self.paths
    
    def animatePath(self):
        animate_paths(self.paths, self.mapReader.mapDim, self.mapReader.goalSet, self.mapReader.obstacleList, "video_1", show_goals=True)
