import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mpldatacursor
import numpy as np
from ExpandedGraphs import ExpandedGraphs
from tkinter import filedialog


class Graphs:
    def __init__(self,optimalContainers, optimalTanks,difference,tankData,totalSoc):
        self.data = difference
        self.optimalTanks = optimalTanks
        self.optimalContainers = optimalContainers
        self.tankData = tankData
        self.totalSoc = totalSoc
        self.root = tk.Tk()
        self.root.title("BMS: Results ")
    def closeWindow(self):
        self.root.quit()
    def expandGraph(self,opearation):
         expandWindow = ExpandedGraphs(self.data, self.optimalTanks,self.tankData,self.totalSoc,self.tankData,self.optimalContainers,self.optimalContainers)
         expandWindow.graph(opearation)
    def saveGraphs(self,figure):
        # Save the figure as an image (e.g., PNG)
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if(file_path):
            figure.savefig(file_path)
    def createCanvas(self,fig1,fig2,fig3, fig4):
         # Create Canvas widgets for Matplotlib figures
        canvas1 = FigureCanvasTkAgg(fig1, master=self.root)
        canvas2 = FigureCanvasTkAgg(fig2, master=self.root)
        canvas3 = FigureCanvasTkAgg(fig3, master=self.root)
        canvas4 = FigureCanvasTkAgg(fig4, master=self.root)

        # Add Canvas widgets to the grid
        canvas1_widget = canvas1.get_tk_widget()
        canvas2_widget = canvas2.get_tk_widget()
        canvas3_widget = canvas3.get_tk_widget()
        canvas4_widget = canvas4.get_tk_widget()

        canvas1_widget.grid(row=1, column=0)
        canvas2_widget.grid(row=1, column=1)
        canvas3_widget.grid(row=3, column=0)
        canvas4_widget.grid(row=3, column=1)
        # creating frames to house  buttons
        figOneButtonFrame = tk.Frame(self.root, bg= "light Grey")
        figOneButtonFrame.grid(row = 2, column= 0, sticky= "NSEW")

        figTwoButtonFrame = tk.Frame(self.root, bg= "light Grey")
        figTwoButtonFrame.grid(row = 2, column= 1, sticky= "nsew")

        figThreeButtonFrame = tk.Frame(self.root, bg= "light Grey")
        figThreeButtonFrame.grid(row = 4, column= 0, sticky= "nsew")

        figFourButtonFrame = tk.Frame(self.root, bg= "light Grey")
        figFourButtonFrame.grid(row = 4, column= 1, sticky= "nsew")

        # creating the buttons
        differenceViewButton = ttk.Button(figOneButtonFrame, text = "VIEW", command= lambda: self.expandGraph(0))
        differenceViewButton.pack(side = "left", anchor="n", padx= 80)

        differenceSaveButton = ttk.Button(figOneButtonFrame, text = "SAVE", command=lambda: self.saveGraphs(fig1))
        differenceSaveButton.pack(side = "right", anchor="n", padx= 65)

        
        totalVolumeViewButton = ttk.Button(figTwoButtonFrame, text = "VIEW"  )
        totalVolumeViewButton.pack(side = "left", anchor="n", padx= 80)

        totalSave = ttk.Button(figTwoButtonFrame, text = "SAVE", command=lambda: self.saveGraphs(fig2))
        totalSave.pack(side = "right", anchor="n", padx= 65)
      
        totalContainersViewButton = ttk.Button(figThreeButtonFrame, text = "VIEW")
        totalContainersViewButton.pack(side = "left", anchor="n", padx= 80)

        totalContainerSave = ttk.Button(figThreeButtonFrame, text = "SAVE", command=lambda: self.saveGraphs(fig3))
        totalContainerSave.pack(side = "right", anchor="n", padx= 65)
     
        totalSocViewButton = ttk.Button(figFourButtonFrame, text = "VIEW")
        totalSocViewButton.pack(side = "left", anchor="n", padx= 80)

        totalSocViewButton = ttk.Button(figFourButtonFrame, text = "SAVE",  command=lambda: self.saveGraphs(fig4))
        totalSocViewButton.pack(side = "right", anchor="n", padx= 65)


    def graph(self):
        # this is for difference
        time = 0
        timestamps = []
        for element in self.data:
            time = time +  5
            timestamps.append(time)
        time = 0 
        tankTime = []
        for element in self.optimalTanks:
            time  += 5
            tankTime.append(time)
     
        # these are for containers 
        
        time = 0
        contTime = []
        for element in self.optimalContainers:
            time += 5
            contTime.append(time)
        time =0
        socTime = []

        for element in self.totalSoc:
            time += 5
            socTime.append(time)


        # Create a Tkinter window


        # Create a label for the title at the top
        title_label = tk.Label(self.root, text="Results ",font=("Helvetica", 16) )
        title_label.grid(row=0, column=0, columnspan=3)  # Span all columns

        # Create a Matplotlib figure
        fig1 = Figure(figsize=(7, 4))
        fig2 = Figure(figsize=(7, 4))
        fig3 = Figure(figsize=(7, 4))
        fig4 = Figure(figsize=(7,4))
        self.createCanvas(fig1,fig2,fig3,fig4)
       
        # Create subplots for each figure
        ax1 = fig1.add_subplot(111)
        ax2 = fig2.add_subplot(111)
        ax3 = fig3.add_subplot(111)
        ax4 = fig4.add_subplot(111)

        # Plot data on each subplot
        line1, = ax1.plot(timestamps, self.data, marker='o', linestyle='-', label='Difference')
        # volume and SOC of optimal Tanks over time
        line2, = ax2.plot(tankTime, self.optimalTanks, marker='o', linestyle='-', label='Total tank Volume Over Time')
     
        line3, = ax3.plot(contTime, self.optimalContainers, marker='o', linestyle='-', label='Total Container Charge Over Time')

        line4, =  ax4.plot(socTime, self.totalSoc, marker='o', linestyle='-', label='Total Soc Over Time')

        # Set labels and titles for each subplot
        ax1.set_xlabel('Time minute')
        ax1.set_ylabel('MW')
        ax1.set_title('Difference')

        ax2.set_xlabel('Time(minute)')
        ax2.set_ylabel('MW')
        ax2.set_title('Total tank Volume Over Time')

        ax3.set_xlabel('Time(minute)')
        ax3.set_ylabel('MW')
        ax3.set_title('Total Container Charge Over Time')

        ax4.set_xlabel('Time(minute)')
        ax4.set_ylabel('Percentage(%)')
        ax4.set_title('SOC over time')


        # Enable data cursor for each subplot
        """
        mpldatacursor.datacursor(line1, hover=True, formatter='{x:.2f}, {y:.2f}'.format)
        mpldatacursor.datacursor(line2, hover=True, formatter='{x:.2f}, {y:.2f}'.format)
        mpldatacursor.datacursor(line3, hover=True, formatter='{x:.2f}, {y:.2f}'.format)
        mpldatacursor.datacursor(line4, hover=True, formatter='{x:.2f}, {y:.2f}'.format)
        mpldatacursor.datacursor(differenceLineTwo, hover=True, formatter='{x:.2f}, {y:.2f}'.format)
        """
        self.root.protocol("WM_DELETE_WINDOW", self.closeWindow)
       # Run the Tkinter main loop
        self.root.mainloop()
