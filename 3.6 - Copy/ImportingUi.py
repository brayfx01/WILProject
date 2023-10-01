import tkinter as tk
from ReviewUI import Review
from tkinter import filedialog
import os

class Importing:
    def __init__(self,windowName,rootWindow,windowsArray):
        #stop the previous window form operating
        self.windowsArray = windowsArray
        self.window = tk.Toplevel()
        self.windowsArray.append(self.window)
        
        self.rootWindow = rootWindow
        self.rootWindow.withdraw()
        self.window.grab_set()
        self.window.title("Importing")
        # the size of the window
        self.window_width = 300
        self.window_height = 300
        self.label = tk.Label(self.window,text= "")

        

        self.window.title(windowName)
       
        
        self.textFileName = ""
        self.csvName = ""

    # Function to be called when Button 1 is clicked
    def button1_click(self):
    
        
        # now we are going to associate importingUI with this
        self.label.config(text="Button 1 Clicked!")
    # returns the txt file 
    def getConfigFile(self):
        print(self.textFileName)
        return self.textFileName   
    def getCsvFile(self):
        return self.csvName
    def next(self, textFileName,csvName):
        #release the grab before creation of new window
        self.window.grab_release()
        ReviewUi = Review("Review",textFileName,csvName,self.window,self.windowsArray)
        ReviewUi.createWindow()
        self.textFileName = ReviewUi.getConfigFile()
        print("after pressing next in importing",self.textFileName)
    # Function to be called when Button 2 is clicked
    def CloseWindow(self):
        self.rootWindow.deiconify()
        self.window.destroy()
      # Function to be called when Button 1 is clicked
    # Function to open a file dialog and update the text label
    def browse_file1(self, textFileName):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            file_name = os.path.basename(file_path)
            # sets the config file name as thiss
            self.textFileName = file_name
            textFileName.config(text=f"File Name: {file_name}")

    def browse_file2(self,textFileName):
        # get 
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            file_name = os.path.basename(file_path)
            #set the dataset name to this
            self.csvName = file_name
            textFileName.config(text=f"File Name: {file_name}")
# Create the main window
    def createWindow(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.window.geometry(f"300x200+{x}+{y}")
        
        # create a top frame with a title label
        topFrame =tk.Frame(self.window)
        titleLabel = tk.Label(topFrame, text = "Choose Files")
        titleLabel.place(relx=0.5, rely= 0.1, anchor = tk.CENTER)
        topFrame.pack(fill= tk.BOTH, expand= True)
        
        # now creating the middle frame and text buttons ect 
        middleFrame = tk.Frame(self.window)
        
        # dispaly this as default
        textFileLabelOne = tk.Label(middleFrame, text = "FileName: None")
        textFileLabelTwo = tk.Label(middleFrame, text = "FileName: None")
        
        browsTextButton = tk.Button(middleFrame, text = "Brose Test File:", command =lambda:self.browse_file1(textFileLabelOne))
      
        browsCsvButton = tk.Button(middleFrame, text = "Brosw CSV FILE:", command= lambda: self.browse_file2(textFileLabelTwo))
        
        browsTextButton.grid(row = 0, column= 0 , padx = 10 , pady = 10 )
        textFileLabelOne.grid(row = 0 , column= 1, padx = 10, pady= 10)
        
        browsCsvButton.grid(row = 1, column = 0, padx = 10 , pady = 10)
        textFileLabelTwo.grid(row = 1, column = 1 , padx = 10 , pady = 10)
        
        # placeing the midelf frame 
        middleFrame.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)
        
        # close and nect buttons 
        
        CloseButton = tk.Button(self.window, text = "CLOSE", command= self.CloseWindow)
        NextButton = tk.Button(self.window, text = "Next", command= lambda: self.next(self.textFileName,self.csvName))
     
        CloseButton.place(relx= 0.1, rely = 0.9, anchor=tk.W)
        NextButton.place(relx = 0.9 , rely = 0.9, anchor=tk.E)
        
        # Bind the closing event to the custom function
        self.window.protocol("WM_DELETE_WINDOW", self.CloseWindow)
        # Start the main event loop
        self.window.mainloop()
        