import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

path = [(4, 0, 0), (4, 1, 1), (4, 2, 2), (4, 3, 3), (4, 4, 4), (3, 4, 5), (2, 4, 6), (1, 4, 7), (0, 4, 8)]
points = []

# take time out of path
for tup in path:
    new_tup = (tup[0],tup[1])
    points.append(new_tup)
print(points)

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(5,5)
 
def animate(i):
    ax.clear()
    # Get the point from the points list at index i
    point = points[i]
    # Plot that point using the x and y coordinates
    ax.plot(point[0], point[1], color='black', label='original', marker='o')
    # Set the x and y axis to display a fixed range
    ax.set_xlim([0, 6])
    ax.set_ylim([0, 6])

# run animation
ani = FuncAnimation(fig, animate, frames=len(points),
                    interval=500, repeat=False)
plt.close()

# Save the animation as an animated GIF
ani.save("simple_animation.gif", dpi=300, writer=PillowWriter(fps=1))