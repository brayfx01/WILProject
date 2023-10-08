import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates  # Import mdates for HourLocator and DateFormatter
import tkinter as tk


class Results:
        def __init__(self,generatedDataset, loadDataset,difference , optimal,manual):
                self.root = tk.Tk()
        def graph(self,frame):
                # Read data from the Excel file
                excel_file_path = 'DataSets/new_data_with_difference.xlsx'
                df = pd.read_excel(excel_file_path)

                # Convert 'Timestamp' column to datetime
                df['Timestamp'] = pd.to_datetime(df['Timestamp'])


                # Create a Matplotlib Figure
                fig, ax = plt.subplots(figsize=(12, 6))

                # Plot the data
                ax.plot(df['Timestamp'], df['Load'], label='Load')
                ax.plot(df['Timestamp'], df['WindGen'], label='WindGen')
                ax.plot(df['Timestamp'], df['Difference'], label='Difference')

                # Configure x-axis ticks to show only the hours
                ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Use mdates.HourLocator
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Use mdates.DateFormatter

                ax.set_xlabel('Time')
                ax.set_ylabel('Values', labelpad=-5)
                ax.set_title('Load, WindGen, and Difference Over Time',fontsize = 14)
                ax.legend()
                ax.grid(True)
                plt.xticks(rotation=45)
                # Create a FigureCanvasTkAgg widget
                canvas = FigureCanvasTkAgg(fig, master=frame)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack()

                # Run the Tkinter main loop





        def createCell(self,rowNum, columnNum, sectionName,graphNum):
        
                self.root.grid_rowconfigure(rowNum, weight= 1, minsize= 300)
                self.root.grid_columnconfigure(columnNum , weight=1 , minsize= 300)
                # now adding frames to the cells

                #empty frame for background
        
                BlackOutline = tk.Frame(self.root, bg = "black", width= 10 , height= 10)
                # Place the frames in the grid layout
                BlackOutline.grid(row=rowNum, column=columnNum, sticky="nsew", padx = 10 , pady = 10)

                background = tk.Frame(BlackOutline, bg='White', width=5, height= 5)
                background.pack(expand= True, fill = "both",padx = 1, pady=1)

                heading = tk.Label(self.root,text =sectionName)
                heading.grid(row= rowNum, column=columnNum,sticky="n",pady=15)
                # now creating anouther frame for the buttons 
                buttonFrame = tk.Frame(background,background="white")
                buttonFrame.pack(side= "bottom", fill = "both")
                # create an eit and view button bottom left of the frame
                EditButton = tk.Button(buttonFrame, text = "Edit Button")
                EditButton.pack(side = "left", padx= 5, pady = 5)
                
                viewButton = tk.Button(buttonFrame, text = "view")
                viewButton.pack(side = "left", padx=5, pady = 5)
                
                saveButton = tk.Button(buttonFrame, text = "Save")
                saveButton.pack(side = "right", padx=5,pady= 5)

                # this means it is the dataset graph
                if graphNum == 0:
                        self.graph(background)
        def Results(self):
              
                self.root.title("Results")
                self.createCell(0,0, "DataSet Graph",0)
                self.createCell(0,1,"Optimal Results",0)
                self.createCell(0,2," Configuration FIle Results",0)



                # this will ensure that the number of columns in this row is the same 
                # as the number of cells created
                rowNum = self.root.grid_size()[0] - 1
                colNum = rowNum

                self.root.grid_rowconfigure(rowNum, weight = 1)

                closeButton = tk.Button(self.root, text = "CLOSE")
                closeButton.grid(row = rowNum,column=0,sticky="sw", padx=10, pady=5)

                nextButton = tk.Button(self.root, text = "NEXT")
                nextButton.grid(row = rowNum,column=colNum,sticky="se",padx = 10, pady=5)
                                

                self.root.mainloop()
r = Results()
r.Results()
