import numpy as np
import matplotlib.pyplot as plt
import re

map_root = "maps/"
map_list = ["vdberg1a.txt", # 5x5, 3 robots
        "vdberg1b.txt", # 6x5, 3 robots
        "vdberg1c.txt", # 6x5, 4 robots
        "vdberg3c.txt", # 32x22, 10 robots
        "gauntlet.txt"] # 32x21, 19 robots

palette = np.array([[255, 255, 255],   # white
                    [  0,   0,   0],   # black
                    [  0, 255,   0],   # green
                    [255,   0,   0],   # red
                    ])

def get_map(map_num=None, DEBUG=False):
    if map_num is None:
        rand = np.random.Generator
        map_num = rand.integers(low=0, high=len(map_list))
    if DEBUG:
        print("Returning map: " + map_list[map_num])

    return map_list[map_num]

def show_map(mapFile):
    found_map = None
    with open(map_root + mapFile) as f:
        data = f.readlines()
    for i, line in enumerate(data):
        if re.search("MAP", line):
            found_map = i
        search = re.search("MAP_DIMENSIONS", line)
        if search:
            (x,y) = tuple(int(num) for num in filter(None,re.split(r"[\b\W\b]", line[search.span()[1]+1:-1])))
    map_array = np.zeros([y,x],dtype=int)
    if found_map:
        for l in range((found_map+1),(found_map+y+1)):
            line = data[l]
            for c in range(x):
                if (line[c] == "1"):
                    val = 1
                elif (line[c] == "i"):
                    val = 2
                elif (line[c] == "g"):
                    val = 3
                else:
                    val = 0
                map_array[l - found_map-1][c] = val
    plt.imshow(palette[map_array])
    return

if __name__ == '__main__':
    show_map(map_list[0])
    show_map(map_list[1])
    show_map(map_list[2])
    show_map(map_list[3])
    show_map(map_list[4])