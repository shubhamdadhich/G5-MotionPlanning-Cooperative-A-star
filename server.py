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
            
            #print(goalSet,"khkajBDFk")
            #print(jdbn)
            #tpath, tvisited, tresTable,mreqtime = robotObj.getPath(self.mapReader.mapDim, self.mapReader.initMap, self.resTable, goalSet[0], goalSet[1],200)
            path, visited, self.resTable = robotObj.getPath(self.mapReader.mapDim, self.mapReader.initMap, self.resTable, goalSet[0], goalSet[1],100)
            self.paths.append(path)
            print("Done")
        
        fh=open("output.txt",'w')
        time=dict()
        for pos in self.resTable:
            if pos[2] in time:
                time[pos[2]].append([self.resTable[pos],pos[0],pos[1]])
            else:
                time[pos[2]]=[]
                time[pos[2]].append([self.resTable[pos],pos[0],pos[1]])

        print(time,file=fh)
        fh.close()
        return self.paths
    
    def animatePath(self, outPath):
        animate_paths(self.paths, self.mapReader.mapDim, self.mapReader.goalSet, self.mapReader.obstacleList, outPath, show_goals=True)
