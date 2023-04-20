# main running code of CA* will be implemented here

import argparse
from server import RobotServer

if __name__ == "__main__":
    parser = argparse.ArgumentParser("CA Star", "Plan motion for multiple robots")
    parser.add_argument('-f', '--fileName', dest='fileName', default='maps/testmap0.txt', help="File Path")
    parser.add_argument('-o', '--outputFile', dest='outputFile', default='video_1')
    args = parser.parse_args()
    server = RobotServer(args.fileName)
    paths = server.startPlanning()
    server.animatePath(args.outputFile)
    