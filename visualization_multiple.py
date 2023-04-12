import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
import numpy as np

def animate_paths(path1,path2, file_name, show_goals = False):
    # function that plots two paths over time and saves it as a gif
    # will extend to multiple paths later

    points1 = []
    points2 = []

    # find max path length
    x = [len(path1),len(path2)]
    l_max = max(x)

    # if length isn't equal to path length
    # take last element in path and append to array until it is
    # (need this because one path will be shorter)
    while len(path1) != l_max:
        path1.append(path1[-1])
    
    while len(path2) != l_max:
        path2.append(path2[-1])


    # take time out of paths
    for tup in path1:
        new_tup = (tup[0],tup[1])
        points1.append(new_tup)
    for tup in path2:
        new_tup = (tup[0],tup[1])
        points2.append(new_tup)

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(5,5)
    
    def animate(i):
        ax.clear()
        # Get the point from the points list at index i
        point1 = points1[i]
        point2 = points2[i]

        if show_goals == True:
            # Plot goals
            ax.plot(2,4,color = 'black', marker = 'o')
            ax.plot(2,0,color = 'gray', marker = 'o')

        # Plot that point using the x and y coordinates
        ax.plot(point1[0], point1[1], color='black', label='original', marker='o',markersize=40)
        ax.plot(point2[0], point2[1], color='gray', label='original', marker='o',markersize=40)

        # Set the x and y axis to display a fixed range
        ax.set_xlim([-1, 5])
        ax.set_ylim([-1, 5])
        ax.grid(True)

    # run animation
    ani = FuncAnimation(fig, animate, frames=len(points2),
                        interval=500, repeat=False)
    plt.close()

    # Save the animation as an animated GIF
    ani.save(file_name + ".gif", dpi=300, writer=PillowWriter(fps=.8))

    print(f"Saved video: {file_name}.gif")