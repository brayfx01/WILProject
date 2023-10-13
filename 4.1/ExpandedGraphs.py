import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog

class ExpandedGraphs:
    def __init__(self, difference, totalTank, individualTank, totalSoc, IndividualSoc, totalContainer, individualContainer):
        self.differnece = difference
        self.totalTank = totalTank
        self.individualTank = individualTank
        self.totalSoc = totalSoc
        self.individualSoc = IndividualSoc
        self.totalContainer = totalContainer
        self.individualContainer = individualContainer
    def closeWindow(self):
        self.root.quit()  
    # type indicates whether it is figure 1, 2,3,4, which will require 
    # differing models
    def plotIndividual(self , data,tab ):
        # Separate the data by names
        # Separate the data by names
        name_data = {}
        for name, volume,soc, time in data:
            if name in name_data:
                print(name)
                name_data[name].append(volume)
            else:
                name_data[name] = [volume]
   
        # Create a figure and axis
        fig, ax = plt.subplots()
        array = []
        time = 0
        for i in range(276):
            time += 5
            array.append(time)
        # Plot each individual name's values on the same graph
        figure = Figure(figsize=(7, 4))
        
        canvas2 = FigureCanvasTkAgg(figure, master=tab)
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


       
        ax1 = figure.add_subplot(111)   

                  # Set labels and titles for each subplot
        ax1.set_xlabel('Time minute')
        ax1.set_ylabel('MW')
        ax1.set_title('Difference') 

        plt.title("Values for Different Names")
        plt.xlabel("Entry")
        plt.ylabel("Value")
        i = 0
        for name, values in name_data.items():
            ax1.plot(array, values, marker='o', label=name)
            i +=1
            break
        ax1.legend()

      
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
            CloseButton = ttk.Button(figOneButtonFrame, text = "CLOSE")
            CloseButton.pack(side = "left", anchor="n", padx= 80)

            SaveButton = ttk.Button(figOneButtonFrame, text = "SAVE" , command= lambda: self.saveGraph(figure))
            SaveButton.pack(side = "right", anchor="n", padx= 60)
        elif(type == 1): # this is the total volume over time
            notebook = ttk.Notebook(self.root)
            # Create the four tabs
            tab1 = ttk.Frame(notebook)
            tab2 = ttk.Frame(notebook)
            notebook.add(tab1, text="Total Volue")
            notebook.add(tab2,text = "Individual Tanks Volume")
           

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
            self.plotIndividual(self.individualTank,tab2)
      
            
        elif(type == 2):
            canvas3 = FigureCanvasTkAgg(figure, master=self.root)
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
        elif(type == 3):
            canvas4 = FigureCanvasTkAgg(figure, master=self.root)
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


        
    def graph(self, type):
        # this is the difference graph
        if type == 0:
            self.root = tk.Toplevel()
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
            self.root = tk.Toplevel()
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
            ax1.set_ylabel('MW')
            ax1.set_title('Total Volume over Time')

            totalVolumeGraph, = ax1.plot(timestamps, self.totalTank, marker='o', linestyle='-', label='total tank')
        elif type == 2:
            self.root = tk.Toplevel()
            self.root.title("Total Charge of container over time")
            time = 0
            timestamps = []
            for element in self.totalContainer:
                time = time +  5
                timestamps.append(time)
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
            self.root = tk.Toplevel()
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

        
  