# main running code of CA* will be implemented here

from server import RobotServer

if __name__ == "__main__":
    server = RobotServer('maps/testmap1.txt')
    paths = server.startPlanning()
    server.animatePath()
    