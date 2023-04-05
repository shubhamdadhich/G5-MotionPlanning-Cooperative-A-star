import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

path = [(4, 0, 0), (4, 1, 1), (4, 2, 2), (4, 3, 3), (4, 4, 4), (3, 4, 5), (2, 4, 6), (1, 4, 7), (0, 4, 8)]
path_new = []
for tup in path:
    new_tup = (tup[0],tup[1])
    path_new.append(new_tup)
print(path_new)

points = [(0.1, 0.5), (0.5, 0.5), (0.9, 0.5)]
points = path_new

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(5,5)
 
def animate(i):
    ax.clear()
    # Get the point from the points list at index i
    point = points[i]
    # Plot that point using the x and y coordinates
    ax.plot(point[0], point[1], color='green', 
            label='original', marker='o')
    # Set the x and y axis to display a fixed range
    ax.set_xlim([0, 6])
    ax.set_ylim([0, 6])
ani = FuncAnimation(fig, animate, frames=len(points),
                    interval=500, repeat=False)
plt.close()

from matplotlib.animation import PillowWriter
# Save the animation as an animated GIF
ani.save("simple_animation.gif", dpi=300,
         writer=PillowWriter(fps=1))