import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
import numpy as np

def animate_paths(all_paths, all_ends, obstacles, file_name, show_goals = False):
    ''' 
    function that plots paths over time and saves it as a gif
    '''

    # find max path length
    max_len = 0
    for path in all_paths:
        if len(path) > max_len:
            max_len = len(path)

    # # need this because one path will be shorter
    # for path in all_paths:
    #     while len(path) != max_len:
    #         path.append(path[-1])

    all_points = []
    # take time out of paths so they are just lists of points to plot
    for path in all_paths:
        temp_points = []
        for tup in path:
            new_tup = (tup[0],tup[1])
            temp_points.append(new_tup)
        all_points.append(temp_points)

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(5,5)
    
    def animate(i):
        ax.clear()
        # Get the point from the points list at index i
        current_points = []
        for points in all_points:
            current_points.append(points[i])

        color_map = ['black', 'gray', 'tan', 'steelblue']

        # plot obstacles
        for obstacle in obstacles:
            ax.plot(obstacle[0],obstacle[1],color = 'black', marker = 'x', markersize = 20)

        if show_goals == True:
            for j,coord in enumerate(all_ends):
                ax.plot(coord[0],coord[1],color = color_map[j], marker = 'o')

        # Plot that point using the x and y coordinates
        for x, point in enumerate(current_points):
            ax.plot(point[0], point[1], color=color_map[x], label='original', marker='o',markersize=40)

        # Set the x and y axis to display a fixed range
        ax.set_xlim([-1, 5])
        ax.set_ylim([-1, 5])
        ax.grid(True)

    # run animation
    ani = FuncAnimation(fig, animate, frames=max_len,
                        interval=500, repeat=False)
    plt.close()

    # Save the animation as an animated GIF
    ani.save(file_name + ".gif", dpi=300, writer=PillowWriter(fps=1.5))
    print(f"Saved video: {file_name}.gif")