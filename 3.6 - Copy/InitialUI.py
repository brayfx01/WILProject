import tkinter as tk
from ImportingUi import Importing
from CreateUi import CreateUi
class InitialUI:
    def __init__(self):
        # will hold all winows
        
        self.windowsArray = []
        self.window = tk.Tk()
        self.windowsArray.append(self.window)
        
        self.window_width = 300
        self.window_height = 200

     
        # Create a label to display messages
        self.label = tk.Label(self.window, text="")
        
        self.configFile = ""
        self.csvFile = ""


    # Function to be called when Button 1 is clicked
    def button1_click(self):
        
       
        # make this window inoperable untile we are done with the next window
        importingUI = Importing("Importing",self.window,self.windowsArray)
        importingUI.createWindow()
        
        self.configFile = importingUI.getConfigFile()
        print("This is the config file", self.configFile)
        self.csvFile = importingUI.getCsvFile()
        
    # Function to be called when Button 2 is clicked
    def button2_click(self):
        create = CreateUi()
        create.createUi()
    def getConfigFile(self):
        return self.configFile
    def getCsvFile(self):
        return self.csvFile
    # this will exit out of the system
    def closeWindow(self):
        quit()

    def createWindow(self):
        # Create the main window
        
        self.window.title("Centered Buttons")

        # Calculate the center of the screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 300
        window_height = 200
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the window size and position it in the center
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
                
        # Create a frame to hold the buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(expand=True)
     
        
        # Create two buttons and add them to the frame
        button1 = tk.Button(button_frame, text="Import", command=self.button1_click)
        button2 = tk.Button(button_frame, text="Create", command=self.button2_click)
        button1.pack(side=tk.LEFT, padx=10)
        button2.pack(side=tk.LEFT, padx=10)

        
        
      
        self.label.pack()
        # Bind the closing event to the custom function
        self.window.protocol("WM_DELETE_WINDOW", self.closeWindow)
        # Start the main event loop
        self.window.mainloop()


"""
# Create the main window
window = tk.Tk()
window.title("Centered Buttons")

# Calculate the center of the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 300
window_height = 200
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window size and position it in the center
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Function to be called when Button 1 is clicked
def button1_click():
    label.config(text="Button 1 Clicked!")

# Function to be called when Button 2 is clicked
def button2_click():
    label.config(text="Button 2 Clicked!")

# Create a frame to hold the buttons
button_frame = tk.Frame(window)
button_frame.pack(expand=True)

# Create two buttons and add them to the frame
button1 = tk.Button(button_frame, text="Button 1", command=button1_click)
button2 = tk.Button(button_frame, text="Button 2", command=button2_click)
button1.pack(side=tk.LEFT, padx=10)
button2.pack(side=tk.LEFT, padx=10)

# Create a label to display messages
label = tk.Label(window, text="")
label.pack()

# Start the main event loop
window.mainloop()
"""