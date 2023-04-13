# Central server class will be implemented here

from map_reader import MapReader
from 


class RobotServer(object):

    def __init__(self, mapFile) -> None:
        self.mapFile = mapFile
        self.mapReader = MapReader(mapFile=self.mapFile)


    def startPlanning(self):

        for id in range(self.mapReader.robotCount):
