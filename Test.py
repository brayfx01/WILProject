import tkinter as tk

root = tk.Tk()
root.title("Nested Frames in a Column Example")

# Create a grid layout with two columns
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create the outer frame and place it in the first column
outer_frame = tk.Frame(root, bg="lightblue", width=400, height=300)
outer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Create the inner frame and place it inside the outer frame
inner_frame = tk.Frame(outer_frame, bg="lightgreen", width=200, height=150)
inner_frame.pack(padx=10, pady=10)

# Add labels to both frames for demonstration
label_outer = tk.Label(outer_frame, text="Outer Frame", bg="lightblue")
label_outer.pack()

label_inner = tk.Label(inner_frame, text="Inner Frame", bg="lightgreen")
label_inner.pack()

root.mainloop()
