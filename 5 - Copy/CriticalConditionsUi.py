import tkinter as tk
from tkinter import filedialog
import os
import tkinter as tk
from tkinter import ttk
import csv
import subprocess
import time


class CriticalConditions:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.grab_set()
        self.root.title("Critical Conditions")
        # this is going to be passed to the review and CreateUi
        self.textFile = ""
        self.conditionEntries = []
        self.conditionNames = []
         # These are the conditions
        self.containerOnOff = tk.StringVar()
        self.roundTripEfficency = tk.StringVar()
        self.tankMaxVolume = tk.StringVar()
        self.tankMinVolume = tk.StringVar()
        self.tankMaxSoc = tk.StringVar()
        self.TankMinSoc = tk.StringVar()
        self.containerMaxCharge = tk.StringVar()
        self.containerMinCharge = tk.StringVar()
    def editText(self,fileName,operation):
        # getting the last saved time
        currentSavedTime = os.path.getatime(fileName)
        try:
           process = subprocess.Popen(["notepad.exe", fileName])  # Opens the file in Notepad (Windows)
        except FileNotFoundError:
            print("Text editor not found or file does not exist.")
        #wait until the editor is closeed
        # and make sure the window cannot be used while wainting
        self.root.grab_set()
        process.wait()
        self.root.grab_release()

        if(operation == 0):
            self.update_widget( fileName,self.tankWidget,"Tanks:", "Containers:")
        elif(operation == 1):
            self.update_widget( fileName,self.containerWidget,"Containers:", "End")
    
        # Function to periodically check for changes in the text file and update the widget
      
    def next(self):
        # getting all the user inputs and putting them into user Inputs
        userInputs = [self.conditionNames[i] + self.conditionEntries[i].get() for i in range(8)] 

        targetWord = "Tanks:"
        
        try:
            # reading the existed file
            with open(self.textFile, "r") as file:
                content = file.read()
        except FileNotFoundError:
            content = ""
        
        #now finding th eposition of the specified word
        wordPosition = content.find(targetWord)
        
        if wordPosition != -1:
            previousNewlinePosition = content.rfind('\n', 0, wordPosition)
            if previousNewlinePosition != -1:
                # remove everthing above the key word
                content =   content[previousNewlinePosition + 1:]
            updateContent =  "\n".join(userInputs) + "\n" + content
            
          
            with open(self.textFile, "w")as file:
                file.write(updateContent)
                

        review.createWindow()
        self.root.wait_window(review.root)
        self.root.grab_set()
        #open up the review window for this
    def uiElements(self):

        # array of label names
        self.conditionNames = ["Container On Off Efficency: ", "Round Trip Efficency: ", 
                      "tank Max Volume: ", "tank Min Volume: ", "Tank Max Soc: ", "Tank Min Soc: "
                      ,"container Max Charge: ", "container Min Charge: "]
        entryTextVariables = [self.containerOnOff, self.roundTripEfficency, 
                              self.tankMaxVolume,self.tankMinVolume,self.tankMaxSoc,self.TankMinSoc,
                              self.containerMaxCharge,self.containerMinCharge]

        self.root.grid_rowconfigure(0, weight = 1, minsize = 200)
        # creaing column
        self.root.grid_columnconfigure(0,weight= 1, minsize =200)
            
        # now we are going to create a frame in the first one
        # this will help to determine how it looks 
        backgroundFrame = tk.Frame(self.root,bg="light grey",width = 10, height=10)
        backgroundFrame.grid(rowspan=2 , column= 0,sticky="nsew")
        
        innerFrame= tk.Frame(backgroundFrame, bg= "white",width = 5, height=5)
        innerFrame.pack(expand= True, fill = "both",padx=1,pady=1)
        # put this into a loop in anouther function 
        # this is the title of the frame 
        title = tk.Label(innerFrame, text= "Critical Conditions:",bg = "white",)
        title.grid(row = 0, columnspan= 2, sticky="nswe")
        #creating 8 labels and entries
        for i in range(8):
            # create a label at row 1 + i and labelName i 
            label = tk.Label(innerFrame, text = self.conditionNames[i])
            label.grid(row = 1 + i, column=0)
            # do the same with the entry
            entry = tk.Entry(innerFrame, textvariable= entryTextVariables[i])
            entry.grid(row = 1 + i , column= 1, padx = 10)
            # now appending these to the entry widgets 
            self.conditionEntries.append(entry)
        editButton = ttk.Button(innerFrame, text = "Edit", command= lambda: self.editText(self.textFile,2))
        editButton.grid(row = 9, column=0, sticky="w")
        # this is the save button bottom right of the frame
        nextButton = ttk.Button(innerFrame, text = "Next", command= self.next)
        nextButton.grid(row = 9,column=1 , sticky="e",padx= 20)  
    def createWindow(self):
    
        self.textFile = "createdConfig.txt"
        # just writing the default sections
        with open(self.textFile, "w") as file:
            # Step 2: Write data to the file
            file.write("Tanks:\n")
            file.write("Containers:\n")
            file.write("END")
            self.root.geometry("300x250")
        # creating rows 
        self.root.grid_rowconfigure(0, weight = 1, minsize= 100)
   
        # column 
        self.root.grid_columnconfigure(0, weight=1, minsize= 100)

     
        #ading the UI elements
        self.uiElements()

