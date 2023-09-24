import tkinter as tk


def createCell(rowNum, columnNum, sectionName):
      
        root.grid_rowconfigure(rowNum, weight= 1, minsize= 200)
        root.grid_columnconfigure(columnNum , weight=1 , minsize= 200)
        # now adding frames to the cells

        #empty frame for background
       
        BlackOutline = tk.Frame(root, bg = "black", width= 10 , height= 10)
        # Place the frames in the grid layout
        BlackOutline.grid(row=rowNum, column=columnNum, sticky="nsew", padx = 10 , pady = 10)

        background = tk.Frame(BlackOutline, bg='White', width=5, height= 5)
        background.pack(expand= True, fill = "both",padx = 1, pady=1)

        heading = tk.Label(root,text =sectionName)
        heading.grid(row= rowNum, column=columnNum,sticky="n",pady=15)
        


root = tk.Tk()
root.title("Main Window")
createCell(0,0, "DataSet Graph")
createCell(0,1,"Optimal Results")
createCell(0,2," Configuration FIle Results")



# this will ensure that the number of columns in this row is the same 
# as the number of cells created
rowNum = root.grid_size()[0] - 1
colNum = rowNum

root.grid_rowconfigure(rowNum, weight = 1)

closeButton = tk.Button(root, text = "CLOSE")
closeButton.grid(row = rowNum,column=0,sticky="sw", padx=5, pady=5)

closeButton = tk.Button(root, text = "NEXT")
closeButton.grid(row = rowNum,column=colNum,sticky="se",padx = 5, pady=5)
                

root.mainloop()
quit()

# creating 3 rows as well
root.grid_rowconfigure(0, weight= 1, minsize= 100)
root.grid_rowconfigure(1, weight= 1, minsize= 100) 
root.grid_rowconfigure(2, weight= 1, minsize= 100)


# createing three columns one for the optimal containers and tanks 
# one for the manual configure
# one for the dataset 
root.grid_columnconfigure(0, weight=0 , minsize= 100)
root.grid_columnconfigure(1, weight= 0, minsize= 100)
root.grid_columnconfigure(2, weight= 0, minsize= 100)

# now adding frames to the cells
topLeft = tk.Frame(root, bg= "lightGrey", width = 10 , height = 10)
topLeft.grid(row=0,column=0, sticky="nsew",padx =0,pady = 0)

root.mainloop()
