import tkinter as tk
from tkinter import filedialog
import os
import tkinter as tk
import csv
import subprocess
import time
# add back in the previousWindo 
class AddUi:
    def __init__(self,operation, file, previousWindow ,tankNum, contNum):
        self.root = tk.Toplevel(previousWindow)
        self.root.title("Add")
        self.root.grab_set()
        self.textFile = file

        self.tankNum = tankNum
        self.contNum = contNum
        # 0 create tank 
        # 1 create container
        self.operation = operation
        #input these
        self.tankName = ""
        self.containerName = ""
        
        
        self.contWidget = None
        self.tankWidget = None
        
        self.soc = tk.StringVar() 
        self.volume = tk.StringVar()
        
        self.sectionName = tk.StringVar()
        self.charge = tk.StringVar()
        self.CorrespondingTanks = tk.StringVar()
        # used to add in new sections 
        self.currnetSectionName = ""
        
        # Bind the close event to a method
        self.root.protocol("WM_DELETE_WINDOW", self.closeWindow)
       
    def closeWindow(self):
       # self.root.grab_release()
        print("Close")
        self.root.destroy()
    
    def getWindow(self):
        return self.root
    def updateTankNameDisplay(self):
        self.label_text.set(f"Tank {self.tankNum + 1}")
    def updateContainerNameDisplay(self):
        self.label_text.set(f"Container {self.contNum + 1}")
        
    def addValues(self):
        #reading the file first
        with open(self.textFile, "r") as file:
            lines = file.readlines()
     
        # the target we want to insert after or before
        # we are inserting above the target word
        if(self.operation == 0):
            target_word = "Containers:"
        elif(self.operation==1):
            target_word = "END"
   
        for i, line in enumerate(lines):
            if target_word in line:
                if(self.operation==0):
                   
                    # Step 4: Insert text above the target word
                    new_line = "        SOC " + str(self.soc.get()) + "\n"
                    lines.insert(i, new_line)  # Insert above the target line
                                        
                    new_line = "        Volume = " + str(self.volume.get()) + "\n"
                    lines.insert(i, new_line)  # Insert above the target line
                                        # Step 4: Insert text above the target word
                    new_line = f"    Tank {self.tankNum + 1}" + "\n"
                    self.tankNum = self.tankNum + 1
                    lines.insert(i, new_line)  # Insert above the target line
                elif(self.operation == 1):
                   
                    new_line = "        corresponding Tanks:" + str(self.CorrespondingTanks.get()) + "\n"
                    lines.insert(i, new_line)
                    
                    new_line = "        Charge: " + str(self.charge.get()) + "\n"
                    lines.insert(i , new_line)
                    
                    
                    new_line =f"    container {self.contNum + 1} :" + "\n"
                    self.contNum = self.contNum + 1
                    lines.insert(i, new_line)
                    
                    new_line = str(self.sectionName.get()) + "\n"
                    
                    # only add a new section if the section name is different 
                    # to the current section name
                    if(self.currnetSectionName == ""):
                        
                        self.currnetSectionName = new_line
                        lines.insert(i , new_line)
                    else:
                        if self.currnetSectionName != new_line:
                            lines.insert(i, new_line)
                            self.currnetSectionName = new_line
                break  # Stop searching after the first occurrence

        # Step 5: Open the file again in write mode to overwrite its content
        with open(self.textFile, "w") as file:
            file.writelines(lines)
        if(self.operation == 0):
            self.updateTankNameDisplay()
        elif(self.operation == 1):
            self.updateContainerNameDisplay()
    def createWindow(self):
    
        # rows and columns
        self.root.grid_rowconfigure(0, weight = 1)
        self.root.grid_rowconfigure(1, weight = 1)
        self.root.grid_rowconfigure(2, weight = 1)
        self.root.grid_rowconfigure(3, weight = 1)
      
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_columnconfigure(1,weight=1)
        #backgorund colour goes accross the columns
        background = tk.Frame(self.root,bg = "Light Grey")
        background.grid(rowspan= 5,  columnspan= 2,sticky= "nsew")
    def createTextTanks(self):
        # the title of this window
        title = tk.Label(self.root, text= "Adding Tank")
        title.grid(row = 0,columnspan=2, sticky="n")
        # Tank Name 
        tankName = tk.Label(self.root, text = "Tank Name:")
        tankName.grid(row =1 ,column=0, sticky="ne", pady= 5, padx= 5)
        
        
        print(f"Tank {self.tankNum + 1}")
        self.label_text = tk.StringVar()
        self.label_text.set(f"Tank {self.tankNum + 1}")
        print(self.label_text)
        nameOfTank = tk.Label(self.root, textvariable =  self.label_text)
        nameOfTank.grid(row = 1, column=1, sticky="nw", pady = 5, padx= 5)
        
        #Tank Volume
        tankVolume = tk.Label(self.root, text = "Volume:")
        tankVolume.grid(row =2 ,column=0, sticky="ne", pady = 5, padx= 5)
        
        volumeEntry = tk.Entry(self.root, textvariable= self.volume, width= 10)
        volumeEntry.grid(row =2 ,column=1, sticky="nw", pady = 5, padx= 5)

        #Tank Soc
        tankSoc = tk.Label(self.root, text = "Soc:")
        tankSoc.grid(row =3 ,column=0, sticky="ne", pady = 5, padx= 5)
        
        socValue = tk.Entry(self.root, textvariable= self.soc, width= 10)
        socValue.grid(row =3 ,column=1, sticky="nw", pady = 5, padx= 5)
        
    
    def createTextContainers(self):
        # the title of this window
        title = tk.Label(self.root, text= "Adding Container")
        title.grid(row = 0,columnspan=2, sticky="n")
        
        sectionName = tk.Label(self.root, text = "Section Name:")
        sectionName.grid(row =1 ,column=0, sticky="ne", pady= 5, padx= 5)

        nameOfSection = tk.Entry(self.root, textvariable= self.sectionName,width= 10)
        nameOfSection.grid(row = 1, column= 1, sticky= "nw", pady = 5, padx= 5)
   
        # cont Name 
        containerName = tk.Label(self.root, text = "Container Name:")
        containerName.grid(row =2 ,column=0, sticky="ne", pady= 5, padx= 5)
        
        # this allows the name to be updated when adding 
        self.label_text = tk.StringVar()
        self.label_text.set(f"Container {self.contNum + 1}")
        
        nameOfContainer = tk.Label(self.root, textvariable= self.label_text)
        nameOfContainer.grid(row = 2, column=1, sticky="nw", pady = 5, padx= 5)
        #cont charge
        containerCharge = tk.Label(self.root, text = "Charge:")
        containerCharge.grid(row =3 ,column=0, sticky="ne", pady = 5, padx= 5)
        
        chargeEntry = tk.Entry(self.root, textvariable= self.charge, width= 10)
        chargeEntry.grid(row =3 ,column=1, sticky="nw", pady = 5, padx= 5)
        
        # corresponding tanks
        CorrespondingTanks = tk.Label(self.root, text = "Corresponding Tanks")
        CorrespondingTanks.grid(row =4 ,column=0, sticky="ne", pady = 5, padx= 5)
        
        tanks = tk.Entry(self.root, textvariable= self.CorrespondingTanks, width= 10)
        tanks.grid(row =4 ,column=1, sticky="nw", pady = 5, padx= 5)
        
       
        
    def createUi(self):
  
      
        self.createWindow()
        if(self.operation == 0):
            self.createTextTanks()
        elif(self.operation == 1):
            self.createTextContainers()
       
        totalRows = self.root.grid_size()[1]
      
        # adding buttons to the end of the window 
        backButton = tk.Button(self.root, text="Back", command= self.closeWindow)
        backButton.grid(row = totalRows, column=0, sticky="sw", padx= 5, pady=5)

        # adding buttons to the end of the window 
        addButton = tk.Button(self.root, text="ADD", command=self.addValues)
        addButton.grid(row = totalRows, column=1, sticky="se", padx= 5, pady=5)
    