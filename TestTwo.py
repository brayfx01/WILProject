import tkinter as tk

def highlight_rows():
    keyword = keyword_entry.get()
    text_content = text_widget.get("1.0", "end-1c")
    rows = text_content.split('\n')
    
    for i, row in enumerate(rows):
        if keyword not in row:
            text_widget.tag_add("highlight", f"{i + 1}.0", f"{i + 1}.end")
    
    text_widget.tag_config("highlight", background="red")

# Create the main window
root = tk.Tk()
root.title("Text Widget Highlighter")

# Create an entry widget for the keyword
keyword_label = tk.Label(root, text="Keyword:")
keyword_label.pack()
keyword_entry = tk.Entry(root)
keyword_entry.pack()

# Create a Text widget
text_widget = tk.Text(root, height=10, width=40)
text_widget.pack()

# Create a button to highlight rows
highlight_button = tk.Button(root, text="Highlight Rows", command=highlight_rows)
highlight_button.pack()

root.mainloop()
