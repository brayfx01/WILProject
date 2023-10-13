import tkinter as tk
from tkinter import ttk
class AnimatedHoverButton:
    def __init__(self, root):
        self.root = root
        self.buttons = []
        self.style = ttk.Style()
        self.style.configure("TButton", background="blue")  # Set an initial background color

    def add_button(self, button):
        button.bind("<Enter>", self.hover)
        button.bind("<Leave>", self.unhover)
        self.buttons.append(button)

    def hover(self, event):
        self.animate_color(event.widget, "lightblue")

    def unhover(self, event):
        self.animate_color(event.widget, "lightgray")

    def animate_color(self, button, target_color):
        
        current_color = button.cget("background")
      
        if current_color != target_color:
            r, g, b = self.root.winfo_rgb(current_color)
            r_target, g_target, b_target = self.root.winfo_rgb(target_color)
            r_step = (r_target - r) / 10
            g_step = (g_target - g) / 10
            b_step = (b_target - b) / 10

            def update_color(step):
                new_color = "#%02x%02x%02x" % (int(r + r_step * step), int(g + g_step * step), int(b + b_step * step))
                button.configure(bg=new_color)
                if step < 10:
                    button.after(20, update_color, step + 1)

            update_color(1)

