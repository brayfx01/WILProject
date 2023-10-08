import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mpldatacursor
import numpy as np


class Graphs:
    def __init__(self,optimalContainers, optimalTanks,difference):
        self.data = difference
        self.optimalTanks = optimalTanks
        self.optimalContainers = optimalContainers
        self.root = tk.Tk()
        self.root.title("Matplotlib Graphs in Tkinter")
        
    def createCanvas(self,fig1,fig2,fig3):
         # Create Canvas widgets for Matplotlib figures
        canvas1 = FigureCanvasTkAgg(fig1, master=self.root)
        canvas2 = FigureCanvasTkAgg(fig2, master=self.root)
        canvas3 = FigureCanvasTkAgg(fig3, master=self.root)

        # Add Canvas widgets to the grid
        canvas1_widget = canvas1.get_tk_widget()
        canvas2_widget = canvas2.get_tk_widget()
        canvas3_widget = canvas3.get_tk_widget()

        canvas1_widget.grid(row=1, column=0)
        canvas2_widget.grid(row=1, column=1)
        canvas3_widget.grid(row=1, column=2)
        
        # creating a frame in canvas1_widget or figure 1 
        buttonFrameFigureOne = tk.Frame(self.root, bg= "light grey",width=10,height=10)
        buttonFrameFigureOne.grid(row = 2, column=0, sticky="nswe")
        
        buttonFrameFigureTwo = tk.Frame(self.root, bg= "light grey",width=10,height=10)
        buttonFrameFigureTwo.grid(row = 2, column=1, sticky="nswe")
        
        buttonFrameFigureThree = tk.Frame(self.root, bg= "light grey",width=10,height=10)
        buttonFrameFigureThree.grid(row = 2, column=2, sticky="nswe")
        
        
        padding = 70
        #adding View Buttons
        figOneViewButton = tk.Button(buttonFrameFigureOne, text = "View")
        figOneViewButton.grid(row =0, column= 0 , sticky= "w", padx= padding)
        
        #adding figure 1 view button 
        figTwoViewButton = tk.Button(buttonFrameFigureTwo, text = "View")
        figTwoViewButton.grid(row =0, column= 0 , sticky= "w", padx= padding)
        
        #adding figure 1 view button 
        figThreeViewButton = tk.Button(buttonFrameFigureThree, text = "View")
        figThreeViewButton.grid(row =0, column= 0 , sticky= "w", padx= padding)

    def graph(self):
        # this is for difference
        time = 0
        timestamps = []
        for element in self.data:
            time = time +  5
            timestamps.append(time)
            
           # this is for the optimal tanks
        tankVolume = [entry[0] for entry in self.optimalTanks]
        tankSoc = [entry[1] for entry in self.optimalTanks]
        tankTime = [entry[2] for entry in self.optimalTanks]
     
        # these are for containers 
        
        ContCharg = [entry[0] for entry in self.optimalContainers]
        contTime = [entry[1] for entry in self.optimalContainers]
        


        # Create a Tkinter window


        # Create a label for the title at the top
        title_label = tk.Label(self.root, text="Optimal Tanks Statistics")
        title_label.grid(row=0, column=0, columnspan=3)  # Span all columns

        # Create a Matplotlib figure
        fig1 = Figure(figsize=(6, 4))
        fig2 = Figure(figsize=(6, 4))
        fig3 = Figure(figsize=(6, 4))
        self.createCanvas(fig1,fig2,fig3)
       
        # Create subplots for each figure
        ax1 = fig1.add_subplot(111)
        ax2 = fig2.add_subplot(111)
        ax3 = fig3.add_subplot(111)

        # Plot data on each subplot
        line1, = ax1.plot(timestamps, self.data, marker='o', linestyle='-', label='Difference')
        # volume and SOC of optimal Tanks over time
        line2, = ax2.plot(tankTime, tankVolume, marker='o', linestyle='-', label='TankVolumes')
        line3, = ax2.plot(tankTime, tankSoc, marker='o', linestyle='-', label='TankSoc 3')
        differenceLineTwo = ax2.plot(timestamps, self.data, marker='o', linestyle='-', label='Difference')
        
        line4, = ax3.plot(contTime, ContCharg, marker='o', linestyle='-', label='Container Charge')

        # Set labels and titles for each subplot
        ax1.set_xlabel('X-axis')
        ax1.set_ylabel('Y-axis')
        ax1.set_title('Difference')

        ax2.set_xlabel('X-axis')
        ax2.set_ylabel('Y-axis')
        ax2.set_title('Tanks volume and soc over time')

        ax3.set_xlabel('X-axis')
        ax3.set_ylabel('Y-axis')
        ax3.set_title('containers over time')

        # Enable data cursor for each subplot
        mpldatacursor.datacursor(line1, hover=True, formatter='{x:.2f}, {y:.2f}'.format)
        mpldatacursor.datacursor(line2, hover=True, formatter='{x:.2f}, {y:.2f}'.format)
        mpldatacursor.datacursor(line3, hover=True, formatter='{x:.2f}, {y:.2f}'.format)
        mpldatacursor.datacursor(line4, hover=True, formatter='{x:.2f}, {y:.2f}'.format)
        mpldatacursor.datacursor(differenceLineTwo, hover=True, formatter='{x:.2f}, {y:.2f}'.format)
        # Run the Tkinter main loop
        self.root.mainloop()
