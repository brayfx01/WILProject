import tkinter as tk

root = tk.Tk()
root.title("Main Window")
root.grid_rowconfigure(0, weight=0, minsize=200)
root.grid_rowconfigure(1, weight=0, minsize=200)

root.grid_columnconfigure(0, weight=0 , minsize= 200)
root.grid_columnconfigure(1, weight= 0, minsize= 100)


column1_frame = tk.Frame(root, bg = "black", width= 11 , height= 1)
# Place the frames in the grid layout
column1_frame.grid(row=0, column=0, sticky="nsew", padx = 0 , pady = 0)

column2_frame = tk.Frame(column1_frame, bg='White', width=5, height= 5)
column2_frame.pack(expand= True, fill = "both",padx = 1, pady=1)



root.mainloop()
