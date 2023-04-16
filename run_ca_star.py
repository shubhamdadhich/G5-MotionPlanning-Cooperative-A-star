# main running code of CA* will be implemented here

from server import RobotServer

if __name__ == "__main__":
    server = RobotServer('maps/testmap0.txt')
    server.startPlanning()