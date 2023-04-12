import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
import numpy as np

# Robot 1
# [(2, 0, 0), (2, 1, 1), (2, 2, 2), (2, 3, 3), (2, 4, 4)]
# Robot 2
# [(2, 4, 0), (2, 3, 1), (3, 3, 2), (3, 2, 3), (3, 1, 4), (3, 0, 5), (2, 0, 6)]

path1 = [(2, 0, 0), (2, 1, 1), (2, 2, 2), (2, 3, 3), (2, 4, 4)]
# fill in end states when stopped
path1 = [(2, 0, 0), (2, 1, 1), (2, 2, 2), (2, 3, 3), (2, 4, 4), (2, 4, 4), (2, 4, 4)]
points1 = []

path2 = [(2, 4, 0), (2, 3, 1), (3, 3, 2), (3, 2, 3), (3, 1, 4), (3, 0, 5), (2, 0, 6)]
points2 = []

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
ani.save("basic_animation_1.gif", dpi=300, writer=PillowWriter(fps=.8))