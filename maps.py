import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, MultipleLocator
import re

map_root = "maps/"
map_list = [
            "testmap1.txt", # 5x5, 4 robots
            "bug_map.txt",  # 5x5, 4 robots
            "vdberg1a.txt", # 5x5, 3 robots
            "vdberg1b.txt", # 6x5, 3 robots
            "vdberg1c.txt", # 6x5, 4 robots
            "plus.txt",     # 7x7, 2 robots
            "choke.txt",    # 7x7, 2 robots
            "testmap0.txt", # 10x10, 4 robots
            "testmap2.txt", # 10x10, 4 robots
            "vdberg3c.txt", # 32x22, 10 robots
            "quad.txt",     # 32x22, 4 robots
            "gauntlet.txt" # 32x21, 19 robots
]

palette = np.array([[255, 255, 255],   # white, empty
                    [128, 128, 128],   # grey, blocked
                    [  0, 255,   0],   # green, start
                    [255,   0,   0],   # red, end
                    ])

def get_map(map_num=None, DEBUG=False):
    if map_num is None:
        rand = np.random.Generator
        map_num = rand.integers(low=0, high=len(map_list))
    if DEBUG:
        print("Returning map: " + map_list[map_num])

    return map_list[map_num]

def show_map(mapFile):
    ## reading in map
    map_start = None
    robot_count = None
    robot_coords = None
    with open(map_root + mapFile) as f:
        data = f.readlines()
    for i, line in enumerate(data):
        if re.search("MAP", line):
            map_start = i + 1

        search = re.search("MAP_DIMENSIONS", line)
        if search:
            (y_dim, x_dim) = tuple(int(num) for num in re.findall(r"\d+", line)) # https://stackoverflow.com/a/30933281

        search = re.search("ROBOT_COUNT", line)
        if search:
            robot_count = int(re.findall(r"\d+", line)[0])

        search = re.search("GOAL_SET", line)
        if search is not None and robot_count is not None:
            robot_coords = np.zeros([robot_count,4], dtype=int)
            for r in range(robot_count):
                robot_coords[r] = re.findall(r"\d+", data[i + 1 + r])

    map_array = np.zeros([x_dim,y_dim],dtype=int)
    if map_start is not None:
        for l in range((map_start),(map_start+y_dim)):
            line = data[l]
            for x in range(x_dim):
                if (line[x] == "x"):
                    val = 1
                elif (line[x] == "i"):
                    val = 2
                elif (line[x] == "g"):
                    val = 3
                else:
                    val = 0
                map_array[x][l - map_start] = val

    ## plotting
    plt.close("all")
    plt.figure(figsize=(0.3*x_dim+1,0.3*y_dim+1))
    ax = plt.imshow(palette[map_array.T], aspect="equal").axes # https://stackoverflow.com/a/37720602, https://stackoverflow.com/a/8280500
    plt.xlim([-1, x_dim])
    plt.ylim([-1, y_dim])
    #ax.invert_yaxis() # https://stackoverflow.com/a/8280500
    ax.xaxis.set_major_locator(MultipleLocator(base=5)) # https://stackoverflow.com/a/34880501
    ax.yaxis.set_major_locator(MultipleLocator(base=5)) # https://stackoverflow.com/a/34880501
    for i, coord in enumerate(robot_coords):
        plt.annotate(str(i), xy=(coord[1], coord[0]), va="center", ha="center")
        plt.annotate(str(i), xy=(coord[3], coord[2]), va="center", ha="center")
    name = mapFile.split(".")[0] + ".png"
    plt.savefig(fname=map_root + "images/" + name, dpi=300)
    return

if __name__ == '__main__':
    for i in range(len(map_list)):
        print("Starting" + map_list[i])
        show_map(map_list[i])
        #plt.pause(3)