import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create the main application window
root = tk.Tk()
root.title("Tabbed Interface with FigureCanvas")

# Create a ttk.Notebook widget
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Create a frame for the first tab
frame1 = tk.Frame(notebook)
notebook.add(frame1, text='Tab 1')

# Create a Figure and a FigureCanvas for Matplotlib
fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame1)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Now you can use the 'fig' to create plots and add them to the canvas
# Example: Create a simple plot
ax = fig.add_subplot(111)
ax.plot([1, 2, 3, 4, 5], [2, 3, 5, 7, 11])

# Create a frame for the second tab
frame2 = tk.Frame(notebook)
notebook.add(frame2, text='Tab 2')

# Add content to the second tab
label2 = tk.Label(frame2, text='This is Tab 2')
label2.pack(padx=20, pady=20)

# Start the main tkinter event loop
root.mainloop()
