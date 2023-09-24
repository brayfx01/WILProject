import tkinter as tk

# Create a list to store references to all the windows
windows = []

# Function to create a new window
def create_window():
    new_window = tk.Toplevel(root)
    windows.append(new_window)
    label = tk.Label(new_window, text="This is a new window")
    label.pack()

# Function to close all windows
def close_all_windows():
    for window in windows:
        window.destroy()
    windows.clear()

# Create the main application window
root = tk.Tk()
root.title("Main Window")

# Create buttons to create new windows and close all windows
create_button = tk.Button(root, text="Create New Window", command=create_window)
create_button.pack()

close_button = tk.Button(root, text="Close All Windows", command=close_all_windows)
close_button.pack()

root.mainloop()
