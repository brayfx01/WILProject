import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np

# Create a figure with a white background
fig, ax = plt.subplots()
fig.set_facecolor('white')  # Set the figure background to white

# Define the x values for the sine and cosine graphs
x = np.linspace(0, 2 * np.pi, 100)

# Initialize the line variables for sine and cosine
sine_line, = ax.plot(x, np.sin(x), label='sin(x)')
cosine_line, = ax.plot(x, np.cos(x), label='cos(x')

# Function to update the current tab with the selected graph
def update_tab(selected_function):
    if selected_function == 'sine':
        sine_line.set_visible(True)
        cosine_line.set_visible(False)
        ax.set_title('Sine Graph')
    elif selected_function == 'cosine':
        sine_line.set_visible(False)
        cosine_line.set_visible(True)
        ax.set_title('Cosine Graph')
    ax.legend()
    fig.canvas.draw()

# Create buttons to switch between tabs
btn1 = Button(plt.axes([0.1, 0.95, 0.1, 0.05]), 'Sine')
btn1.on_clicked(lambda event: update_tab('sine'))

btn2 = Button(plt.axes([0.25, 0.95, 0.1, 0.05]), 'Cosine')
btn2.on_clicked(lambda event: update_tab('cosine'))

# Set the background color of the axes to white
ax.set_facecolor('white')

# Set the background color of the legend to white
ax.legend().set_frame_on(False)

# Initialize with the sine graph
update_tab('sine')

plt.show()
