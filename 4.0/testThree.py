import tkinter as tk
from tkinter import ttk

root = tk.Tk()
s = ttk.Style()
backgroundFrame = tk.Frame(root, bg = "light grey")
backgroundFrame.pack(fill="both", expand=True)
s.configure("TNotebook.Tab", background="black", foreground="black", font=("Helvetica", 12))
notebook = ttk.Notebook(backgroundFrame)

# Create and add tabs
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
notebook.add(tab1, text="Tab 1")
notebook.add(tab2, text="Tab 2")

notebook.pack(side= "left", anchor="n")

root.mainloop()
