import numpy as np
import matplotlib.pyplot as plt
import re

map_root = "maps/"
map_list = ["vdberg1a.txt", # 5x5, 3 robots
        "vdberg1b.txt", # 6x5, 3 robots
        "vdberg1c.txt", # 6x5, 4 robots
        "vdberg3c.txt", # 32x22, 10 robots
        "gauntlet.txt"] # 32x21, 19 robots

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
    map_start = None
    with open(map_root + mapFile) as f:
        data = f.readlines()
    for i, line in enumerate(data):
        if re.search("MAP", line):
            map_start = i + 1
        search = re.search("MAP_DIMENSIONS", line)
        if search:
            (x_dim,y_dim) = tuple(int(num) for num in filter(None,re.split(r"[\b\W\b]", line[search.span()[1]+1:-1]))) # https://stackoverflow.com/a/30933281
    map_array = np.zeros([y_dim,x_dim],dtype=int)
    if map_start is not None:
        for l in range((map_start),(map_start+y_dim)):
            line = data[l]
            for x in range(x_dim):
                if (line[x] == "1"):
                    val = 1
                elif (line[x] == "i"):
                    val = 2
                elif (line[x] == "g"):
                    val = 3
                else:
                    val = 0
                map_array[l - map_start][x] = val
    plt.imshow(palette[map_array]) # https://stackoverflow.com/a/37720602
    return

if __name__ == '__main__':
    for i in range(len(map_list)):
        show_map(map_list[i])
        plt.pause(3)