from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
from matplotlib.widgets import CheckButtons
class ExpandedGraphs:
    def __init__(self, difference, totalTank, individualTank, totalSoc, IndividualSoc, totalContainer, individualContainer):
        self.root = tk.Toplevel()
        self.differnece = difference
        self.totalTank = totalTank
        self.individualTank = individualTank
        self.totalSoc = totalSoc
        self.individualSoc = IndividualSoc
        self.totalContainer = totalContainer
        self.individualContainerData = individualContainer
        self.timeArray = []
        self.finisehd = False
    def closeWindow(self):

        self.root.destroy()
    # type indicates whether it is figure 1, 2,3,4, which will require 
    # differing models
    # Function to toggle line visibility
    def toggle_line(self,line,figure,name,ax1,lineHolder):

        if(line.get_visible() == True):
            line.set_visible(False)
        else:
            line.set_visible(True)
        # only display the active labels in the legend
        activeLabels = [line.get_label() for line in lineHolder if line.get_visible()]
        lineColors = [line.get_color() for line in lineHolder if line.get_visible()]
        
        custom_legend = [Line2D([0], [0], color=color, lw=2, label=label) for color, label in zip(lineColors, activeLabels)]
        
        ax1.legend(handles=custom_legend)
        figure.canvas.draw()
    
    def isActiveLine(self,name, graph):
        
        for lines in graph.get_lines():
            if(lines.get_label() == name):
          
                return lines.get_visible()
    def selectDESelect(self, operation, lineHolder,figure,checkBoxArray,ax1):
        if(operation == 0): # selecting all 
            for line in lineHolder:
                line.set_visible(True)
            for box in checkBoxArray:
                box.select()
        else:# deselecting all
            for line in lineHolder:
                line.set_visible(False)
                for box in checkBoxArray:
                    box.deselect()
        # only display the active labels in the legend
        activeLabels = [line.get_label() for line in lineHolder if line.get_visible()]
        lineColors = [line.get_color() for line in lineHolder if line.get_visible()]
        
        custom_legend = [Line2D([0], [0], color=color, lw=2, label=label) for color, label in zip(lineColors, activeLabels)]
        
        ax1.legend(handles=custom_legend)
        figure.canvas.draw()
    
        
    def activeWidgets(self, frame,name_data,lineHolder, operation,ax1,figure):
        
  
        # creating the widget
        background = tk.LabelFrame(frame, bg = "white")
        background.pack(fill = "both", expand= True)

        # title 
     
        # going through and name data and for each createa a frame with two columns
        # first column has button for on off the second the name of the line
        # Create an empty dictionary to store dynamic variables
        
        #holds all the checkBoxes creates so that they can all be turned on and off witht eh
        # all buttons
        checkBoxArray =[]
        for name in name_data:
            for line in lineHolder:
                if(line.get_label() == name):
                    nameofgraph = line.get_label()
                    correspondingLine = line
            
            listFrame = tk.Frame(background)
            listFrame.pack(side = "top", anchor="n")
         
       
            
            # need ot ahve disticnt button names 
           
            buttonName = tk.Checkbutton(listFrame, text= name,  command=lambda line = correspondingLine, graph = nameofgraph: self.toggle_line(line,figure, graph,ax1,lineHolder))
            checkBoxArray.append(buttonName)
            if(self.isActiveLine(name,ax1)):
                buttonName.select()
            buttonName.grid(row=0, column= 0, sticky= "w", padx= 2, pady=1)
         
        selectDeSelectFrame = tk.Frame(background)
        selectDeSelectFrame.pack(pady = 10, side="bottom")

        selectAll = ttk.Button(selectDeSelectFrame, text= "SELECT ALL", command= lambda: self.selectDESelect(0, lineHolder,figure,checkBoxArray,ax1))
        selectAll.pack(side= "left")

        deSelectAll = ttk.Button(selectDeSelectFrame, text= "DESELECT ALL", command= lambda: self.selectDESelect(1, lineHolder,figure,checkBoxArray,ax1))
        deSelectAll.pack(side= "left")
 
        
           
    def plotIndividual(self , data,tab, operation,yAxisName,graphName ):
        # Separate the data by names
        # we are dealing with tank individual volume
        name_data = {}
        if(operation == 1):
            for name, volume,soc, time in data:
                if name in name_data:
                    name_data[name].append(volume)
                else:
                    name_data[name] = [volume]
          
        elif(operation == 2):
            for section,name, charge in data:
                if name in name_data:
                    name_data[name].append(charge)
                else:
                    name_data[name] = [charge]
        elif(operation == 3):
            for name, volume,soc, time in data:
                if name in name_data:
                    name_data[name].append(soc)
                else:
                    name_data[name] = [soc]
         
 
        # Create a figure and axis
        fig, ax = plt.subplots()
        array = []
      
        time = 0
        for i in range(len(name_data[name])):
            time += 5
            array.append(time)
        # for now just do this
        if(operation == 2):
            array = self.timeArray
        # Plot each individual name's values on the same graph
        figure = Figure(figsize=(7, 4))
        backgroundFrame = tk.Frame(tab)
        backgroundFrame.grid(row = 1, column=0)
        # this contains the buttons to activate and deactivate the lines
        leftFrame = tk.Frame(backgroundFrame, bg = "light Grey", width = 100 ,height= 100)
        leftFrame.grid(row = 0, column= 0, sticky= "ns")


        rightFrame = tk.Frame(backgroundFrame)
        rightFrame.grid(row = 0, column= 1)

        canvas = FigureCanvasTkAgg(figure, master=rightFrame)
        canvasWidget = canvas.get_tk_widget()
        canvasWidget.grid(row=1, column=1)

    
        # button frames
        figTwoButtonFrame = tk.Frame(self.root, bg= "light Grey")
        figTwoButtonFrame.grid(row = 2, column= 0, sticky= "nsew")

         # creating the buttons
        CloseButton = ttk.Button(figTwoButtonFrame, text = "CLOSE", command= self.closeWindow)
        CloseButton.pack(side = "left", anchor="n", padx= 80)

        SaveButton = ttk.Button(figTwoButtonFrame, text = "SAVE" , command= lambda: self.saveGraph(figure))
        SaveButton.pack(side = "right", anchor="n", padx= 60)

        ax1 = figure.add_subplot(111)   

                  # Set labels and titles for each subplot
        ax1.set_xlabel('Time minutes')
        ax1.set_ylabel(yAxisName)
        ax1.set_title(graphName) 

        plt.title("Change of " + graphName + " over Time")
        plt.xlabel("Time")
        plt.ylabel(yAxisName)
        # how many are shown on the graph
        numberShown = 0
        # holds the lines that are created so they can be set as visible or invisible
        lineHolder = []
      
        for name, values in name_data.items():
            line , = ax1.plot(array, values, marker='o', label=name)
            lineHolder.append(line)
            numberShown += 1
            if(numberShown >= 4):
                line.set_visible(False)
            
      
        # now go and create the elements for the left frame 
        self.activeWidgets(leftFrame, name_data,lineHolder,operation,ax1,figure)
        activeLabels =[line.get_label() for line in lineHolder if line.get_visible()]
        ax1.legend(lineHolder,activeLabels)

      
    def saveGraph(self, figure):
        # Save the figure as an image (e.g., PNG)
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if(file_path):
            figure.savefig(file_path)
    def createCanvas(self,figure, type):
         # Create Canvas widgets for Matplotlib figures

        if(type == 0):
            canvas1 = FigureCanvasTkAgg(figure, master=self.root)
             # Add Canvas widgets to the grid
            canvas1_widget = canvas1.get_tk_widget()
            canvas1_widget.grid(row=1, column=0)
             # creating frames to house  buttons
            figOneButtonFrame = tk.Frame(self.root, bg= "light Grey")
            figOneButtonFrame.grid(row = 2, column= 0, sticky= "NSEW")
            # creating the buttons
            CloseButton = ttk.Button(figOneButtonFrame, text = "CLOSE", command= self.closeWindow)
            CloseButton.pack(side = "left", anchor="n", padx= 80)

            SaveButton = ttk.Button(figOneButtonFrame, text = "SAVE" , command= lambda: self.saveGraph(figure))
            SaveButton.pack(side = "right", anchor="n", padx= 60)
        elif(type == 1): # this is the total volume over time
            notebook = ttk.Notebook(self.root)
            # Create the four tabs
            tab1 = ttk.Frame(notebook)
            tab2 = ttk.Frame(notebook)
            notebook.add(tab1, text="Total Volume of Tanks")
            notebook.add(tab2,text = "Individual Tank Volume")
           

            notebook.grid(row = 0 ,column=0, sticky="w")
            notebook.grid(row  =0 , column= 0, sticky = "w")
            # this is tab one 
            canvas2 = FigureCanvasTkAgg(figure, master=tab1)
            canvas2_widget = canvas2.get_tk_widget()
            canvas2_widget.grid(row=1, column=0)
            # button frames
            figTwoButtonFrame = tk.Frame(self.root, bg= "light Grey")
            figTwoButtonFrame.grid(row = 2, column= 0, sticky= "nsew")

             # creating the buttons
            CloseButton = ttk.Button(figTwoButtonFrame, text = "CLOSE")
            CloseButton.pack(side = "left", anchor="n", padx= 80)

            SaveButton = ttk.Button(figTwoButtonFrame, text = "SAVE" , command= lambda: self.saveGraph(figure))
            SaveButton.pack(side = "right", anchor="n", padx= 60)

            # this is tab 2
            self.plotIndividual(self.individualTank,tab2, type,"Liters","Individual Tank Volume")
      
            
        elif(type == 2): # containers
            notebook = ttk.Notebook(self.root)
            # Create the four tabs
            tab1 = ttk.Frame(notebook)
            tab2 = ttk.Frame(notebook)
            notebook.add(tab1, text="Total Charge of Containers")
            notebook.add(tab2,text = "Individual Charge of Containers")
            
            notebook.grid(row = 0 ,column=0, sticky="w")
            notebook.grid(row  =0 , column= 0, sticky = "w")

            canvas3 = FigureCanvasTkAgg(figure, master=tab1)
            canvas3_widget = canvas3.get_tk_widget()
            canvas3_widget.grid(row=1, column=0)
            # button frames
            figTwoButtonFrame = tk.Frame(self.root, bg= "light Grey")
            figTwoButtonFrame.grid(row = 2, column= 0, sticky= "nsew")

             # creating the buttons
            CloseButton = ttk.Button(figTwoButtonFrame, text = "CLOSE")
            CloseButton.pack(side = "left", anchor="n", padx= 80)

            SaveButton = ttk.Button(figTwoButtonFrame, text = "SAVE" , command= lambda: self.saveGraph(figure))
            SaveButton.pack(side = "right", anchor="n", padx= 60)
        
            self.plotIndividual(self.individualContainerData,tab2, type, "MW","Individual Container Volume")
        elif(type == 3):# SOC
            notebook = ttk.Notebook(self.root)
            # Create the four tabs
            tab1 = ttk.Frame(notebook)
            tab2 = ttk.Frame(notebook)
            notebook.add(tab1, text="Total SOC of Tanks")
            notebook.add(tab2,text = "Individual SOC of Tanks")
            
            notebook.grid(row = 0 ,column=0, sticky="w")
            notebook.grid(row  =0 , column= 0, sticky = "w")

            canvas4 = FigureCanvasTkAgg(figure, master=tab1)
            canvas4_widget = canvas4.get_tk_widget()
            canvas4_widget.grid(row=1, column=0)
            # button frames
            figTwoButtonFrame = tk.Frame(self.root, bg= "light Grey")
            figTwoButtonFrame.grid(row = 2, column= 0, sticky= "nsew")

             # creating the buttons
            CloseButton = ttk.Button(figTwoButtonFrame, text = "CLOSE")
            CloseButton.pack(side = "left", anchor="n", padx= 80)

            SaveButton = ttk.Button(figTwoButtonFrame, text = "SAVE" , command= lambda: self.saveGraph(figure))
            SaveButton.pack(side = "right", anchor="n", padx= 60)
            
            self.plotIndividual(self.individualSoc,tab2, type, "Percentage(%)","Individual SOC of Tank")


        
    def graph(self, type):
        # this is the difference graph
        if type == 0:
           
            self.root.title("Difference Graph over time")
            time = 0
            timestamps = []
            for element in self.differnece:
                time = time +  5
                timestamps.append(time)
              # Create a label for the title at the top
            title_label = tk.Label(self.root, text="Optimal Statistics")
            title_label.grid(row=0, column=0, columnspan=3)  # Span all columns

            # Create a Matplotlib figure
            fig1 = Figure(figsize=(7, 4))
            self.createCanvas(fig1, type)
            # Create subplots for each figure
            ax1 = fig1.add_subplot(111)
                
            # Set labels and titles for each subplot
            ax1.set_xlabel('Time minute')
            ax1.set_ylabel('MW')
            ax1.set_title('Difference')

            differenceGraph, = ax1.plot(timestamps, self.differnece, marker='o', linestyle='-', label='Difference')
        elif type == 1: # this is the total volume
           
            self.root.title("Total Tank Volume Over Time")
            time = 0
            timestamps = []
            for element in self.totalTank:
                time = time +  5
                timestamps.append(time)
              # Create a label for the title at the top
            title_label = tk.Label(self.root, text="Optimal Statistics")
            title_label.grid(row=0, column=0, columnspan=3)  # Span all columns

            # Create a Matplotlib figure
            fig1 = Figure(figsize=(7, 4))
            self.createCanvas(fig1, type)
            # Create subplots for each figure
            ax1 = fig1.add_subplot(111)
                
            # Set labels and titles for each subplot
            ax1.set_xlabel('Time minute')
            ax1.set_ylabel('Liters')
            ax1.set_title('Total Volume over Time')

            totalVolumeGraph, = ax1.plot(timestamps, self.totalTank, marker='o', linestyle='-', label='total tank')
        elif type == 2:
           
            self.root.title("Total Charge of container over time")
            time = 0
            timestamps = []
            
            for element in self.totalContainer:
                time = time +  5
                timestamps.append(time)
            self.timeArray = timestamps
              # Create a label for the title at the top
            title_label = tk.Label(self.root, text="Total container Charge over Time")
            title_label.grid(row=0, column=0, columnspan=3)  # Span all columns

            # Create a Matplotlib figure
            fig1 = Figure(figsize=(7, 4))
        
            self.createCanvas(fig1, type)
         
            # Create subplots for each figure
            ax1 = fig1.add_subplot(111)
         
            # Set labels and titles for each subplot
            ax1.set_xlabel('Time minute')
            ax1.set_ylabel('MW')
            ax1.set_title('Total container Charge over Time')
            totalVolumeGraph, = ax1.plot(timestamps, self.totalContainer, marker='o', linestyle='-', label='total tank')

        elif(type == 3):
           
            self.root.title("Total SOC over time")
            time = 0
            timestamps = []
            for element in self.totalSoc:
                time = time +  5
                timestamps.append(time)
              # Create a label for the title at the top
            title_label = tk.Label(self.root, text="Total SOC over Time")
            title_label.grid(row=0, column=0, columnspan=3)  # Span all columns

            # Create a Matplotlib figure
            fig1 = Figure(figsize=(7, 4))
            self.createCanvas(fig1, type)
            # Create subplots for each figure
            ax1 = fig1.add_subplot(111)
                
            # Set labels and titles for each subplot
            ax1.set_xlabel('Time minute')
            ax1.set_ylabel('percent(%)')
            ax1.set_title('Total SOC over Time')

            totalVolumeGraph, = ax1.plot(timestamps, self.totalSoc, marker='o', linestyle='-', label='total tank')

        
  