# main running code of CA* will be implemented here

import argparse
from server import RobotServer

map_root = "maps/"
map_list = [
            # "testmap1.txt", # 5x5, 4 robots  - works
            # "bug_map.txt",  # 5x5, 4 robots  - works
            # "vdberg1a.txt", # 5x5, 3 robots  - works
            # "vdberg1b.txt", # 6x5, 3 robots  - doesn't work (no solution with our code)
            # "vdberg1c.txt", # 6x5, 4 robots  - works
            # "plus.txt",     # 7x7, 2 robots  - works
            "choke.txt",    # 7x7, 2 robots  - works but shows error of the first robot blocking the path at its goal
            # "testmap0.txt", # 10x10, 4 robots  - works
            # "testmap2.txt", # 10x10, 4 robots  - works
            # "vdberg3c.txt", # 32x22, 10 robots  - works
            "quad.txt",     # 32x22, 4 robots  - works but still throws an error an error
            ##"testmap1_bug.txt",  # 10x10, 4 robots  - grey gets stuck and it throws an error
            "gauntlet.txt"  # 32x21, 19 robots  - doesn't work
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser("CA Star", "Plan motion for multiple robots")
    parser.add_argument('-f', '--fileName', dest='fileName', default='maps/testmap0.txt', help="File Path")
    parser.add_argument('-o', '--outputFile', dest='outputFile', default='video_1')
    args = parser.parse_args()

    for i in range(len(map_list)):
        out_filename = map_list[i].split(".")[0]
        server = RobotServer(map_root + map_list[i])
        paths = server.startPlanning()
        server.animatePath(map_root + "gifs/" + out_filename)
    