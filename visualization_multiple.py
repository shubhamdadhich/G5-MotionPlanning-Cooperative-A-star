import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
import numpy as np

palette = np.array([[255, 255, 255],   # white, empty
                    [128, 128, 128],   # grey, blocked
                    [  0, 255,   0],   # green, start
                    [255,   0,   0],   # red, end
                    ])

def animate_paths(paths, mapDim, goalset, obstacleList, file_name, show_goals = False):
    # function that plots two paths over time and saves it as a gif
    # will extend to multiple paths later

    pointList = []

    # find max path length
    list_len = [len(i) for i in paths]
    l_max = max(list_len)

    # if length isn't equal to path length
    # take last element in path and append to array until it is
    # (need this because one path will be shorter)

    for i, path in enumerate(paths):
        while len(path) < l_max:
            path.append(path[-1])

    # while len(path1) != l_max:
    #     path1.append(path1[-1])
    
    # while len(path2) != l_max:
    #     path2.append(path2[-1])


    # take time out of paths

    for path in paths:
        points = []
        for tup in path:
            new_tup = (tup[0],tup[1])
            points.append(new_tup)
        pointList.append(points)

    # for tup in path1:
    #     new_tup = (tup[0],tup[1])
    #     points1.append(new_tup)
    # for tup in path2:
    #     new_tup = (tup[0],tup[1])
    #     points2.append(new_tup)

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(5,5)
    
    def animate(i):
        ax.clear()
        # Get the point from the points list at index i

        colorList = ['red', 'green', 'blue', 'purple', 'yellow', 'gray', 'black', 'cyan', 'magenta', 'brown', 'pink', 'orange', 'olive','red', 'green', 'blue', 'purple', 'yellow', 'gray']

        apointList = []
        for points in pointList:
            apointList.append(points[i])
        # print(apointList)

        # point1 = points1[i]
        # point2 = points2[i]

        # Plot Obstacles
        map_array = np.zeros([mapDim[0],mapDim[1]],dtype=int)
        for point in obstacleList:
            map_array[point[0],point[1]] = 1
            #ax.plot(point[1], point[0], color='black', label='original', marker='s',markersize=5)
        ax.imshow(palette[map_array])

        if show_goals == True:
            # Plot goals

            for ind, setPt in enumerate(goalset):
                ax.plot(setPt[1][1], setPt[1][0], color=colorList[ind], marker='x', markersize=8)
            # ax.plot(2,4,color = 'black', marker = 'o')
            # ax.plot(2,0,color = 'gray', marker = 'o')

        # Plot that point using the x and y coordinates

        for ind, point in enumerate(apointList):
            ax.plot(point[1], point[0], color=colorList[ind], label='original', marker='o',markersize=7)

        # ax.plot(point1[0], point1[1], color='black', label='original', marker='o',markersize=40)
        # ax.plot(point2[0], point2[1], color='gray', label='original', marker='o',markersize=40)

        # Set the x and y axis to display a fixed range
        ax.set_xlim([-1, mapDim[1]])
        ax.set_ylim([-1, mapDim[0]])
        ax.grid(True)

    # run animation
    ani = FuncAnimation(fig, animate, frames=len(pointList[0]),
                        interval=500, repeat=False)
    plt.close()

    # Save the animation as an animated GIF
    ani.save(file_name + ".gif", dpi=300, writer=PillowWriter(fps=2))

    print(f"Saved video: {file_name}.gif")
