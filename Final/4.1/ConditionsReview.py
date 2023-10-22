import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import tkinter as tk
import csv
import subprocess
import time
from AddUi import AddUi

from CreateUi import CreateUi
class ConditionReview:
    def __init__(self,textFile):
        self.root = tk.Toplevel()
        self.root.title("CriticalConditions:Review")
        self.textFile = textFile
        self.textFileWidget = ""
        self.root.grab_set()
       
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
    def confirm(self):
        create = CreateUi()
        create.createUi()
        # only allow this window to be acive
        self.root.wait_window(create.root)
        self.root.grab_set()
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
         
    def edit(self,fileName,operation):
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
        self.update_widget(self.textFile, self.textFileWidget,"Container On Off Efficency:","Tanks:")
        # Function to periodically check for changes in the text file and update the widget
      
    def close(self): 
        self.root.destroy()
    def createWindow(self):
        self.root.geometry("300x350")

        widgetFrame = tk.Frame(self.root, background= "white", width= 10 ,height=10, highlightbackground= "grey", highlightthickness=1)
        widgetFrame.pack(fill = "both", expand=True, padx=10, pady=10)
        
        title = tk.Label(widgetFrame, text = "Critical Conditions Review", bg = "light grey")
        title.pack(pady = 10)
        
        textWidget = tk.Text(widgetFrame, wrap = tk.NONE, state= tk.DISABLED, width= 20, height= 10, highlightbackground= "grey", highlightthickness=0.5)
        textWidget.pack(fill = "both", expand= True, padx= 10, pady=10)
        self.textFileWidget = textWidget
        self.displayFile(self.textFile, textWidget, "Container On Off Efficency:", "Tanks:")
        buttonFrame = ttk.Frame(self.root, height= 10 , width=10)
        buttonFrame.pack(fill= "both")
        
        BackButton = ttk.Button(buttonFrame, text ="Back", command= self.close)
        BackButton.pack(side= "left", padx= 10, pady= 5)
        
        EditButton = ttk.Button(buttonFrame, text = "Edit", command= lambda: self.edit(self.textFile,0))
        EditButton.pack(side= "left", pady= 5)
        
        ConfirmButton = ttk.Button(buttonFrame, text = "Confirm",command= self.confirm)
        ConfirmButton.pack(side = "right", pady = 5)



        
        