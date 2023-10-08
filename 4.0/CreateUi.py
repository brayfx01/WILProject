import tkinter as tk
from tkinter import filedialog
import os
import tkinter as tk
import csv
import subprocess
import time
from AddUi import AddUi
class CreateUi:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Create")
        self.root.grab_set()
        
        self.conditionsEntries = []
        self.conditionNames =[]
        
        self.textFile = ""
        self.tankWidget = ""
        self.containerWidget = ""
        # this is used fo rthe left text to save into the file
        self.containerOnOff = tk.StringVar()
        self.roundTripEfficency = tk.StringVar()
        self.tankMaxVolume = tk.StringVar()
        self.tankMinVolume = tk.StringVar()
        self.tankMaxSoc = tk.StringVar()
        self.TankMinSoc = tk.StringVar()
        self.containerMaxCharge = tk.StringVar()
        self.containerMinCharge = tk.StringVar()
        
        
    def save(self):
        # getting all the user inputs and putting them into user Inputs
        userInputs = [self.conditionNames[i] + self.conditionsEntries[i].get() for i in range(8)] 

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
                content =  + content[previousNewlinePosition + 1:]
            updateContent =  "\n".join(userInputs) + "\n" + content
            
          
            with open(self.textFile, "w")as file:
                file.write(updateContent)

        # we are going to check for the Tanks key word as this is where we will start
    def getNumTanksCont(self, textFile, operation):
        # get numTanks
        count = 0
        found = False
        if operation == 0 :
            start = "Tanks:"
            end = "Containers:"
            # now going through and checking when the Tanks: shows up
            with open(textFile, "r") as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    if(end in line):
                        break
                    elif(found == True and "Tank" in line):
                        count = count + 1
                    elif(start in line):
                        foune = True
        return count       
    def update_widget(self,file,widget,start,end):
        
        # Open the file and read its contents
        with open(file, "r") as f:
            textdata = f.readlines()

        # Clear the current content of the widget
        widget.config(state=tk.NORMAL)
        widget.delete(1.0, tk.END)

        # Initialize variables for capturing and displaying text
        displayinfo = []
        capturing = False

        for line in textdata:
            if capturing:
                if end in line:
                    capturing = False
                    break
                else:
                    displayinfo.append(line)
            elif start in line:
                displayinfo.append(line)
                capturing = True

        # Insert the updated content into the widget
        widget.insert(tk.END, "".join(displayinfo))
        widget.config(state=tk.DISABLED)
                  
    def createWindow(self):
        self.root.geometry("500x600")
        # creating rows 
        self.root.grid_rowconfigure(0, weight = 1, minsize= 100)
        self.root.grid_rowconfigure(1, weight = 1, minsize= 100)
        # column 
        self.root.grid_columnconfigure(0, weight=1, minsize= 100)

    def addPressed(self, operation):

        # number of tanks
        numberOfTanks = 0
        numberofContainers = 0
       
        print(numberOfTanks)
        addUi = AddUi(operation,self.textFile, self.root, numberOfTanks,numberofContainers)
       
        addUi.createUi()
        # wait untill the create ui window is closed before continuing
        self.root.wait_window(addUi.root)
        if operation == 0 :
            self.update_widget(self.textFile, self.tankWidget,"Tanks", "Containers")
        elif operation == 1:
            self.update_widget(self.textFile, self.containerWidget,"Containers", "END")
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
      
    def displayFile(self,file,widget,start,end):
        
        with open(file, "r")as f:
            textdata = f.readlines()
        widget.config(state = tk.NORMAL)
        # this holds everything to be dispalyed
        displayinfo = []
        # when we start capturing and when we end capturing
        startKeyWord = start
        endKeyWord = end
        # when we start capturing
        capturing = False
    
        for line in textdata:
            if capturing:
                if endKeyWord in line:
                    capturing = False
                    break
                else:
                    displayinfo.append(line)
            elif startKeyWord in line:
                displayinfo.append(line)
                capturing = True
                
        widget.insert(tk.END, "".join(displayinfo))
        widget.config(state=tk.DISABLED)
    
    def addContent(self, frame, operation):
        if operation == 0:
            # Add title to the top left of the frame
            title = tk.Label(frame, text="Tanks:")
            title.grid(row=0, column=0, sticky="n")

            # Current Tanks
            currentTanks = tk.Label(frame, text="Current Tanks")
            currentTanks.grid(row=1, column=0, sticky="w", padx= 5)

            # Now adding in the widget to display the text file
            configWidget = tk.Text(frame, wrap=tk.NONE, state=tk.DISABLED, height=10, width=40, highlightbackground="light grey", highlightthickness=2)
            configWidget.grid(row=2, column=0, sticky="w", padx= 5)
            self.tankWidget = configWidget
                # Create a vertical scrollbar for the Text widget
            scrollbar = tk.Scrollbar(frame, command=configWidget.yview)
            scrollbar.grid(row = 2,rowspan = 1, column=1, sticky="nswe")
            
            # Configure the Text widget to use the scrollbar
            configWidget.config(yscrollcommand=scrollbar.set)
            
            self.displayFile(self.textFile,configWidget, "Tanks", "Containers")
            # Now adding buttons to the end of this
            # Need a new frame to hold them so that they can be done horizontally
            buttonFrame = tk.Frame(frame, bg="White")
            buttonFrame.grid(row=3, column=0, sticky="w")
            addButton = tk.Button(buttonFrame, text="Add", command= lambda: self.addPressed(0))
            addButton.pack(side=tk.LEFT, padx= 5)
            
            editButton = tk.Button(buttonFrame, text="Edit", command= lambda: self.editText(self.textFile,0))
            editButton.pack(side=tk.LEFT, padx= 5)

        elif operation == 1:
            # Add title to the top left of the frame
            title = tk.Label(frame, text="Containers:")
            title.grid(row=0, column=0, sticky="n")

            # Current Containers
            currentContainers = tk.Label(frame, text="Current Containers")
            currentContainers.grid(row=1, column=0, sticky="w", padx= 5)

            # Now adding in the widget to display the text file
            configWidget = tk.Text(frame, wrap=tk.NONE, state=tk.DISABLED, height=10, width=40, highlightbackground="light grey", highlightthickness=2)
            configWidget.grid(row=2, column=0, sticky="w",padx= 5)
            self.containerWidget = configWidget
            
             # Create a vertical scrollbar for the Text widget
            scrollbar = tk.Scrollbar(frame, command=configWidget.yview)
            scrollbar.grid(row = 2,rowspan = 1, column=1, sticky="nsew")
            
            # Configure the Text widget to use the scrollbar
            configWidget.config(yscrollcommand=scrollbar.set)
            
            self.displayFile(self.textFile,configWidget, "Containers", "END")
            
            buttonFrame = tk.Frame(frame, bg="White")
            buttonFrame.grid(row=3, column=0, sticky="w")
            addButton = tk.Button(buttonFrame, text="Add",command= lambda: self.addPressed(1))
            addButton.pack(side=tk.LEFT, padx= 5)
            
            editButton = tk.Button(buttonFrame, text="Edit", command= lambda: self.editText(self.textFile,1))
            editButton.pack(side=tk.LEFT, padx= 5)

    def rightText(self):
        # top frame background
        topFrameBackground = tk.Frame(self.root, bg = "black")
        topFrameBackground.grid(row = 0 , column= 0, sticky= "ns", padx=10,pady=10)
        
        textFrameBackground = tk.Frame(topFrameBackground, bg = "white")
        textFrameBackground.pack(fill = tk.BOTH, expand= True, padx = 1, pady =1)
        # add content to textFrameBackgournd
        self.addContent(textFrameBackground,0)
        
        bottomFrameBackground = tk.Frame(self.root, bg=  "black")
        bottomFrameBackground.grid(row = 1, column= 0, sticky= "ns", padx=10,pady=10)
        
        bottomTextFrameBackground = tk.Frame(bottomFrameBackground, bg = "white")
        bottomTextFrameBackground.pack(fill = tk.BOTH, expand= True, padx = 1, pady= 1)

        self.addContent(bottomTextFrameBackground,1)
    def createUi(self):
    
        self.textFile = "createdConfig.txt"
        # just writing the default sections
        with open(self.textFile, "w") as file:
            # Step 2: Write data to the file
            file.write("Tanks:\n")
            file.write("Containers:\n")
            file.write("END")
        self.createWindow()
        self.rightText()
    
        


      
