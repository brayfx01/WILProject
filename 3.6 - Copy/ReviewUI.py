import tkinter as tk
from tkinter import filedialog
import os
import tkinter as tk
import csv
import subprocess
class Review:
    def __init__(self, windowName, textFile, csvFile,rootWindow,windowsArray):
        self.windowsArray = windowsArray
        self.window = tk.Toplevel()

        self.window.title("REVIEW")
        self.textFile = textFile
        self.csvFile = csvFile
        # size of the window
        self.windowWidth = 300
        self.windowHeight = 300 
        self.label = tk.Label(self.window,text = "")
        # make the previous window modal /stop 
        self.window.grab_set()
        
        self.window.title(windowName)
        self.textWidget = ""
        self.lastModTime = 0
        

        # Function to open the text file in a text editor
    def open_text_editor(self,fileName):
        try:
            subprocess.Popen(["notepad.exe", fileName])  # Opens the file in Notepad (Windows)
        except FileNotFoundError:
            print("Text editor not found or file does not exist.")

   
    # Function to open the CSV file in a CSV editor (e.g., Microsoft Excel)
    def open_csv_editor(self,fileName):
        
        try:
            # Open the CSV file with the default associated application
            subprocess.Popen([fileName], shell=True)
            print(f"{fileName} opened successfully with the default application.")
        except FileNotFoundError:
            print(f"File not found: {fileName}")
        except Exception as e:
            print(f"An error occurred: {e}")

                
        # Function to periodically check for changes in the text file and update the widget
    def update_text_widget(self,configFileName,text_widget):
        try:
            with open(configFileName, "r") as f:
                new_text_data = f.read()
                if new_text_data != text_widget.get("1.0", "end-1c"):
                    text_widget.config(state=tk.NORMAL)
                    text_widget.delete("1.0", tk.END)
                    text_widget.insert(tk.END, new_text_data)
                    text_widget.config(state=tk.DISABLED)
        except FileNotFoundError:
            pass
    # Function to periodically check for changes in the CSV file and update the widget
    def update_csv_widget(self,csvFileName,csv_widget):
        try:
            with open(csvFileName, "r", newline="") as f:
                new_csv_data = f.read()
                if new_csv_data != csv_widget.get("1.0", "end-1c"):
                    csv_widget.config(state=tk.NORMAL)
                    csv_widget.delete("1.0", tk.END)
                    csv_widget.insert(tk.END, new_csv_data)
                    csv_widget.config(state=tk.DISABLED)
        except FileNotFoundError:
            pass
        except PermissionError as e:
            print(f"PermissionError: {e}")

        
    # Periodically check for changes in the text and CSV files (every 1 second)
    def check_for_changes(self,configFileName, csvFileName, textWidget,csvWidget):
        self.update_text_widget(self.textFile,textWidget)
        self.update_csv_widget(self.csvFile,csvWidget)
        self.window.after(100, self.check_for_changes, configFileName, csvFileName, textWidget, csvWidget)  # Schedule the next check
            # Function to be called when Button 2 is clicked
       
    def ChangeConfig(self,  textWidget):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

        self.textFile = file_path
    def ChangeCsv(self,textFileName):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            file_name = os.path.basename(file_path)
            #set the dataset name to this
            self.csvName = file_name
            #textFileName.config(text=f"File Name: {file_name}") 
        print(file_path == self.textFile)
        print(os.path.basename(file_path), self.csvFile)
        self.csvFile = os.path.basename(file_path) 
    # close all the windows
    def finish(self):
        for window in self.windowsArray:
            window.destroy()
            
    def getConfigFile(self):
        return self.textFile
    def CloseWindow(self):
        self.window.destroy()
    def createWindow(self):
        frame_width = 400  # Adjust as needed
        frame_height = 300  # Adjust as needed
        
        # Set row and column weights to distribute space evenly
        self.window.grid_rowconfigure(0, weight=1)
        #left side
        self.window.grid_columnconfigure(0, weight=1, minsize = 20)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        # right side
        self.window.grid_columnconfigure(3,weight = 1, minsize = 20)

  
        # Increase the minimum height of the empty row (row 2)
        self.window.grid_rowconfigure(1, weight=1, minsize=20)  # Set the minimum height to 20 (adjust as needed)



        # Create a frame for the text file content
        text_frame = tk.Frame(self.window)
        text_frame.grid(row=0 , column=0, sticky="nsew")
        text_frame.config(width=frame_width, height=frame_height)
        
        # Create a Text widget for displaying the text file content (read-only)
        text_widget = tk.Text(text_frame, wrap=tk.NONE, state=tk.DISABLED)
        self.textWidget = text_widget
        text_widget.grid(row= 0, column=0, sticky="nsew")  # Use grid for the widget

        # Create a Scrollbar widget for the text widget
        text_scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview, orient=tk.VERTICAL)
        text_scrollbar.grid(row=0, column=1, sticky="ns")  # Position it to the right
    
        # Configure the Text widget to use the scrollbar
        text_widget.config(yscrollcommand=text_scrollbar.set)

        # Load text data and display it in the Text widget
        text_file = self.textFile
        csv_file = self.csvFile
        # essentially putting he text file in the textWidget
        try:
            with open(text_file, "r") as f:
                text_data = f.read()
                text_widget.config(state=tk.NORMAL)
                text_widget.insert(tk.END, text_data)
                text_widget.config(state=tk.DISABLED)
        except FileNotFoundError:
            text_widget.insert(tk.END, "Error: Text file not found.")
  
                # Create a frame for the CSV file content
        csv_frame = tk.Frame(self.window)
        csv_frame.grid(row=0, column=1, sticky="nsew")
        csv_frame.config(width=frame_width, height=frame_height)
        
        # Create a Text widget for displaying the CSV file content (read-only)
        csv_widget = tk.Text(csv_frame, wrap=tk.NONE, state=tk.DISABLED)
        csv_widget.grid(row=0, column=0, sticky="nsew")  # Use grid for the widget
        
        # Create a Scrollbar widget for the CSV widget
        csv_scrollbar = tk.Scrollbar(csv_frame, command=csv_widget.yview, orient=tk.VERTICAL)
        csv_scrollbar.grid(row=0, column=1, sticky="ns")  # Position it to the right
        
        # Configure the CSV Text widget to use the scrollbar
        csv_widget.config(yscrollcommand=csv_scrollbar.set)
        
        try:
            with open(csv_file, "r", newline="") as f:
                csv_reader = csv.reader(f)
                with open(csv_file, "r", newline="") as f:
                    csv_data = f.read()
                    csv_widget.config(state=tk.NORMAL)
                    csv_widget.insert(tk.END, csv_data)
                    csv_widget.config(state=tk.DISABLED)
        except FileNotFoundError:
            csv_widget.insert(tk.END, "Error: CSV file not found.")
        
            # Create buttons under the config widget
        button_frame_text = tk.Frame(text_frame)
        button_frame_text.grid(row=1, column=0, columnspan=2, sticky="sw")

        button_width = 8  # Set a fixed width for the buttons
        button_height = 1  # Set a fixed height for the buttons
        
        # these are the buttons  
        changeButtonForConfig = tk.Button(button_frame_text, text="Change", width=button_width, height=button_height, command = lambda: self.ChangeConfig(text_widget))
        editButtonForConfig = tk.Button(button_frame_text, text="Edit", width=button_width, height=button_height, command = lambda: self.open_text_editor(self.textFile))
        saveButtonForConfig = tk.Button(button_frame_text, text="Save", width=button_width, height=button_height)

        changeButtonForConfig.grid(row=0, column=0, padx=5, pady=5)
        editButtonForConfig.grid(row=0, column=1, padx=5, pady=5)
        saveButtonForConfig.grid(row=0, column=2, padx=5, pady=5)
        
        
        # Create buttons under the dataset widget aligned to the bottom left
        button_frame_csv = tk.Frame(csv_frame)
        button_frame_csv.grid(row=1, column=0, sticky="sw")

        changeButtonForCsv = tk.Button(button_frame_csv, text="Change", width=button_width, height=button_height, command = lambda: self.ChangeCsv(self.csvFile))
        editButtonForCsv = tk.Button(button_frame_csv, text="Edit", width=button_width, height=button_height, command = lambda: self.open_csv_editor(self.csvFile))
        saveButtonForCsv = tk.Button(button_frame_csv, text="Save", width=button_width, height=button_height)

        changeButtonForCsv.grid(row=0, column=0, padx=5, pady=5, sticky="sw")
        editButtonForCsv.grid(row=0, column=1, padx=5, pady=5, sticky="sw")
        saveButtonForCsv.grid(row=0, column=2, padx=5, pady=5, sticky="sw")
        

         # Create "Close" button at the bottom left of the window
        close_button = tk.Button(self.window, text="Close", width=button_width, height=button_height, command = self.CloseWindow)
        close_button.grid(row=2, column=0, padx=5, pady=5, sticky="sw")

        # Create "Confirm" button at the bottom right of the window
        confirm_button = tk.Button(self.window, text="Confirm", width=button_width, height=button_height, command = self.finish)
        confirm_button.grid(row= 2, column=1, padx=5, pady=5, sticky="se")
      
        # check for updates
        self.window.after(1000, lambda: self.check_for_changes(text_file,csv_file,text_widget,csv_widget))  # Start checking for changes
    
        # Start the tkinter main loop
        self.window.mainloop()

#demoWindo = ReviewUi("Demo", "config.txt", "loadResampled.csv")

                            
        




