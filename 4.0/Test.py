import tkinter as tk
from tkinter import ttk

def switch_tab(event):
    current_tab = notebook.index(notebook.select())
    for tab, label in tabs.items():
        if tab == current_tab:
            label.grid()
        else:
            label.grid_remove()

root = tk.Tk()
root.title("Tabbed Window")

notebook = ttk.Notebook(root)

tab_labels = ["Tab 1", "Tab 2", "Tab 3"]
tabs = {}

frameOne = tk.Frame(notebook, bg = "light grey")
notebook.add(frameOne, text = "tab 1")
label  = tk.Label(frameOne, text = "content For Label 1", padx= 10, pady=10)
label.grid(row = 0 , column= 0)

frameTwo = tk.Frame(notebook)
notebook.add(frameTwo, text = "tab 2")
label  = tk.Label(frameTwo, text = "content For Label 2", padx= 10, pady=10)
label.grid(row = 0 , column= 0)

frameThree = tk.Frame(notebook)
notebook.add(frameThree, text = "tab 3")
label  = tk.Label(frameThree, text = "content For Label 3", padx= 10, pady=10)
label.grid(row = 0 , column= 0)
notebook.pack(expand=1, fill="both")
ttk.Style().configure("TNotebook.Tab", background="grey")

# Bind the tab switching function to the tab change event
notebook.bind("<<NotebookTabChanged>>", switch_tab)

root.mainloop()
