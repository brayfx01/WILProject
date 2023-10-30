import tkinter as tk
from tkinter import ttk

from ReviewUI import Review
from tkinter import filedialog
import os

class InitialUI:
    def __init__(self):
        # will hold all winows
       
     
        self.windowsArray = []
        self.window = tk.Tk()
        self.windowsArray.append(self.window)
        
        self.window_width = 300
        self.window_height = 200

     
        # Create a label to display messagesgeta
        self.label = tk.Label(self.window, text="")
        
        self.textFrame = None
        self.generatedDataFrame = None
        self.loadDataFrame = None
        # means we have an error somewhere 
        self.errorState = True
        
        self.textErrorMessage = None
        self.genErrorMessage = None
        self.loadErrorMessage = None
        # holdds their absolue paths 
        self.configAbsolutePath = ""
        self.generatedAbsolutePath = ""
        self.loadAbsolutePath = ""
            

    def checkEmpty(self,textWidget,generatedWidget,loadWidget,importFrame):

        self.errorState = False
        # just do this once
        if(self.textErrorMessage== None):
            self.textErrorMessage = tk.Label(self.textFrame,text ="Cannot Leave Text File empty")
            self.genErrorMessage = tk.Label(self.generatedDataFrame,text ="Cannot Leave Generated File empty")
            self.loadErrorMessage = tk.Label(self.loadDataFrame,text ="Cannot leave Load File empty")
        
        if(textWidget.get("1.0","end-1c") == ""):# dispaly a red boarder around the widget
          
            textWidget.config(highlightbackground = "red")
           
            # get rid of and replace the error text with same one
            self.textErrorMessage.config(text = "File Name Cannot Be Empty")
            self.textErrorMessage.grid(row = 2, column= 1)
    
            
            self.errorState = True
        elif(os.path.exists(self.configAbsolutePath)== False):
            textWidget.config(highlightbackground = "red")
             
            self.textErrorMessage.configure(text = "ERROR: FILE NOT FOUND")
            self.textErrorMessage.grid(row = 2, column= 1)
            self.errorState = True
        elif(os.path.exists(textWidget.get("1.0", "end-1c")) == False and textWidget.get("1.0", "end-1c") != os.path.basename(self.configAbsolutePath)):
            textWidget.config(highlightbackground = "red")

            self.textErrorMessage.configure(text = "ERROR: FILE NOT FOUND")
            self.textErrorMessage.grid(row = 2, column= 1)
            self.errorState = True
        else:# otherwise set it back to normal and get rid of the error message
            textWidget.config(highlightbackground = "light grey")
            self.textErrorMessage.grid_remove()
            
           
        
        # empty file name
        if(generatedWidget.get("1.0","end-1c")  == ""):
            
            generatedWidget.config(highlightbackground = "red")
           
            self.genErrorMessage.config(text = "File Name Cannot Be Empty")
            self.genErrorMessage.grid(row = 2, column= 1)
          
            self.errorState = True
        elif(os.path.exists(self.generatedAbsolutePath)== False): #cannot find file name
            generatedWidget.config(highlightbackground = "red")
             
            self.genErrorMessage.configure(text = "ERROR: FILE NOT FOUND")
            self.genErrorMessage.grid(row = 2, column= 1)
            self.errorState = True
        elif(os.path.exists(generatedWidget.get("1.0", "end-1c")) == False and generatedWidget.get("1.0", "end-1c") != os.path.basename(self.generatedAbsolutePath)):
            generatedWidget.config(highlightbackground = "red")
             
            self.genErrorMessage.configure(text = "ERROR: FILE NOT FOUND")
            self.genErrorMessage.grid(row = 2, column= 1)
            self.errorState = True
        else:#normal
            generatedWidget.config(highlightbackground = "light grey")
            self.genErrorMessage.grid_remove()
            
            
        if(loadWidget.get("1.0","end-1c") == ""):
            
            loadWidget.config(highlightbackground = "red")
            
            self.loadErrorMessage.config(text = "File Name Cannot Be Empty")
            
            self.loadErrorMessage.grid(row = 2, column= 1)
            empty = True
            
            self.errorState = True
        elif(os.path.exists(self.loadAbsolutePath)== False):
            loadWidget.config(highlightbackground = "red")
             
            self.loadErrorMessage.configure(text = "ERROR: FILE NOT FOUND")
            self.loadErrorMessage.grid(row =2, column= 1)
            self.errorState = True
        elif(os.path.exists(loadWidget.get("1.0", "end-1c")) == False and loadWidget.get("1.0", "end-1c") != os.path.basename(self.loadAbsolutePath)):
            loadWidget.config(highlightbackground = "red")
             
            self.loadErrorMessage.configure(text = "ERROR: FILE NOT FOUND")
            self.loadErrorMessage.grid(row =2, column= 1)
            self.errorState = True
        else:
            loadWidget.config(highlightbackground = "light grey")
            self.loadErrorMessage.grid_remove()
            
      
        return self.errorState

    def importPressed(self, textWidget,generatedWidget,loadWidget,importingFrame):
        
        # check if any of the inputs were left empty
        if self.checkEmpty(textWidget,generatedWidget,loadWidget, importingFrame) == False :
            # textWiget.get() just getting the inputs of the widgets and passing them into the next window
            ReviewUi = Review("Review",self.configAbsolutePath,self.generatedAbsolutePath,self.loadAbsolutePath,self.windowsArray,self)
            ReviewUi.createWindow()
            self.textFileName = ReviewUi.getConfigFile()
       
           
    def getConfigFile(self):
        return self.textFileName   
    def getGenFile(self):
        return self.genFile
    def getLoadFile(self):
        return self.loadFile
    def browseTextFile(self, textFileWidget):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.configAbsolutePath = os.path.abspath(file_path);
            file_name = os.path.basename(file_path)
            # sets the config file name as thiss
            self.configFile = file_name
            #delete the current text 
            textFileWidget.delete("1.0","end")
            textFileWidget.insert("1.0", file_name)
    def browseDataSet(self,csvWidget, operation):
        # get 
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            # this just gets the name of the file
            file_name = os.path.basename(file_path)
            #set the dataset name to this
            if operation == 0:
                # sets the absolute path for checking
                self.generatedAbsolutePath = os.path.abspath(file_path)
                self.generatedFile = file_name
            else: 
                self.loadAbsolutePath = os.path.abspath(file_path)
                self.loadFile = file_name
                
            #delet the current text 
            csvWidget.delete("1.0", "end")
            csvWidget.insert("1.0", file_name)

    def finish(self):
        self.window.quit()
        return self.configFile, self.csvFile
    

    def getConfigFile(self):
        return self.configFile
    def getCsvFile(self):
        return self.csvFile
    def undo(self,textWidget):
        textWidget.edit_undo()

    def redo(self,textWidget):
        textWidget.edit_redo()
    # this is used to pass the final config file back to the main so 
    # that it can be passed as a variable into the system
    def setConfigFile(self, configFile):
        self.configFile = configFile
    def setGenFile(self, genFile):
        self.genFile = genFile
    def setLoadFile(self,loadFile):
        self.loadFile = loadFile
    # this will exit out of the system
    def closeWindow(self):
        quit()
    def createWidgets(self,importFrame):
        # create the first frame and its contents
        textFileFrame = tk.Frame(importFrame, bg = "white")
        textFileFrame.pack()
        # this will be used in the error handling
        self.textFrame = textFileFrame
        
        textWidgetname = tk.Label(textFileFrame,text = "Configuration File:", bg = "white")
        textWidgetname.grid(row = 0, columnspan= 2, sticky= "w")
       
        # add in the button and the widget
        textFileWidget = tk.Text(textFileFrame, width = 20 , height= 1, wrap="word",highlightbackground="light grey", highlightthickness=1)
        
        textFileWidget.grid(row = 1 , column=1 , pady= 5, padx= 5, sticky="ew")
        
        textBrowsButton = ttk.Button(textFileFrame, text = "BROWSE", command=lambda: self.browseTextFile(textFileWidget))
        textBrowsButton.grid(row = 1, column=0, padx= 5)
      
        # create the second frame and its contents
        generatedDataFrame = tk.Frame(importFrame, bg = "white")
        generatedDataFrame.pack()
        
          
        genWidgetname = tk.Label(generatedDataFrame,text = "Generation Dataset File:", bg = "white")
        genWidgetname.grid(row = 0, columnspan= 2, sticky= "w")
       
        #for error handling
        self.generatedDataFrame = generatedDataFrame
        # add in the button and the widget
        generatedDatsetWidget = tk.Text(generatedDataFrame, width = 20 , height= 1, wrap="word",highlightbackground="light grey", highlightthickness=1)
        generatedDatsetWidget.grid(row = 1 , column=1 , pady= 5, padx= 5, sticky="ew")
        
        generatedBrowsButton = ttk.Button(generatedDataFrame, text = "BROWSE", command=lambda: self.browseDataSet(generatedDatsetWidget,0))
        generatedBrowsButton.grid(row = 1, column=0, padx= 5)
        
        # create the third frame and its contents
        loadDataFrame = tk.Frame(importFrame, bg = "white")
        loadDataFrame.pack()
        # for error handling
        genWidgetname = tk.Label(loadDataFrame,text = "Load Dataset File:", bg = "white")
        genWidgetname.grid(row = 0, columnspan= 2, sticky= "w")
       
        self.loadDataFrame = loadDataFrame
        # add in the button and the widget
        loadDatasetWidget = tk.Text(loadDataFrame, width = 20 , height= 1, wrap="word",highlightbackground="light grey", highlightthickness=1)
        loadDatasetWidget.grid(row = 1 , column=1 , pady= 5, padx= 5, sticky="ew")
        
        loadBrowseButton = ttk.Button(loadDataFrame, text = "BROWSE", command=lambda: self.browseDataSet(loadDatasetWidget,1))
        loadBrowseButton.grid(row = 1, column=0, padx= 5)
        
          
        #inserting the default tex for the widgets 
        textFileWidget.insert("1.0", "ConfigExample.txt")
        generatedDatsetWidget.insert("1.0", "GeneratedExample.csv")
        loadDatasetWidget.insert("1.0", "LoadExample.csv")



        # enabling the ctrl z and y undo an redo functionality  for the widgets

        # Bind Ctrl+Z to undo for text_widget1
        self.window.bind("<Control-z>", lambda event: self.undo(textFileWidget))

        # Bind Ctrl+Y to redo for text_widget1
        self.window.bind("<Control-y>", lambda event: self.redo(textFileWidget))

        # Bind Ctrl+Shift+Z to undo for text_widget2
        self.window.bind("<Control-Shift-Z>", lambda event: self.undo(generatedDatsetWidget))

        # Bind Ctrl+Shift+Y to redo for text_widget2
        self.window.bind("<Control-Shift-Y>", lambda event: self.redo(generatedDatsetWidget))
                
        
        return textFileWidget, generatedDatsetWidget, loadDatasetWidget
     # Create the main window

    def createWindow(self):
       
        #window is not resizeable
        self.window.resizable(False,False)
        self.window.title("Battery Management System")

        # Calculate the center of the screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 300
        window_height = 350
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the window size and position it in the center
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")


        outlineFrame =tk.Frame(self.window,  width=200, height=100, highlightbackground="grey", highlightthickness=2)
        outlineFrame.pack(expand=True)
        
        Title = tk.Label(outlineFrame, text="BMS: IMPORTING", bg ="white", font=("Arial", 10))
        Title.pack(fill= "both", expand=True)
        
        importingFrame = tk.Frame(outlineFrame, width= 10, height=100, bg= "white")
        importingFrame.pack( fill= 'x')
        
        textFileWidget, generatedDatsetWidget, loadDatasetWidget  =self.createWidgets(importingFrame)
      
        # Create a frame to hold the buttons
        button_frame = tk.Frame(outlineFrame, bg= "white")
        button_frame.pack(fill="x")
     
        
        # Create two buttons and add them to the frame
        ImportButton = ttk.Button(button_frame, text="IMPORT", command=lambda: self.importPressed(textFileWidget,generatedDatsetWidget,loadDatasetWidget,importingFrame))
       
        ImportButton.pack(side=tk.BOTTOM, padx=10, pady =20)
    
        CloseButton = ttk.Button(self.window, text = "CLOSE",command = self.closeWindow )
        CloseButton.pack(side = "bottom", anchor= "w")
        
       

      
        self.label.pack()
        # Bind the closing event to the custom function
        self.window.protocol("WM_DELETE_WINDOW", self.closeWindow)
        # Start the main event loop
        self.window.mainloop()
        
        self.window.destroy()
