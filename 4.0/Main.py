from SystemInitalization import systemInitalization
from ReadData import ReadData
from EnergyHandler import energyHandler
from OptimalTanks import  OptimalTanks
from OptimalContainers import OptimalContainers
from Clock import clock
from queue import Queue
import pandas as pd
from datetime import datetime, timedelta
from InitialUI import InitialUI

from GraphTanksChange import GraphTanksChange
from ContainerGraph import ContainerGraph
from Graphs import Graphs

class Main:
    def __init__(self):
       # these are the vairables that will be used for the boundaries
        self.tankMaxVolume = 0
        self.tankMinVolume = 0
        
        self.tankMaxSOC = 0
        self.tankMinSOC = 0
        
        self.containerMaxCharge = 0
        self.containerMinCharge = 0
        
        self.RTE = 0
        self.step = 5 # 5 minutes
        # array of the differences to determine if we are storing or expending
        self.difference = []
        self.backlog = Queue()
        
        self.cells =[]
        self.tanks = []
        self.tankVolumesForSection = []
        self.tankSOCForSections = []
       
        
        # will move into surplus if all full or empty
        self.data = None
        self.fullEmpty = None
        self.energyManagement = None
        self.clock = None
        
    def run(self):
        # Main window for getting the config files
        window = InitialUI()
        window.createWindow()

        configFile = window.getConfigFile()
        generatedCsv= window.getCsvFile()
        print("Main", configFile)
        print("Main",generatedCsv)
        
        print("HERE")
    
        #initialization of the system
        system = systemInitalization(generatedCsv,"loadResampled.csv",configFile) # this will create all the sections
        
        self.tankMaxVolume = system.getCriticalInfo("Tank Max Volume")
        self.tankMinVolume = system.getCriticalInfo("Tank Min Volume")
        
        self.tankMaxSOC = system.getCriticalInfo("Tank Max SOC")
        self.tankMinSOC = system.getCriticalInfo("Tank Min SOC")
        
        self.containerMaxCharge = system.getCriticalInfo("Container Max Charge")
        self.containerMinCharge = system.getCriticalInfo("Container Min Charge")
        
        self.cells = system.getSections()#initializes the system
        self.tanks = system.getTanks()#gets tank

        self.RTE = system.getRTE()#gets RTE
        self.fullEmpty = system.getFullEmpty()#gets the FULLEMPTY checher

        self.data = pd.read_excel("DataSets/new_data_with_difference.xlsx") 
        self.difference = self.data["Difference"].to_numpy()
    
      
     
        print("Tank max charge", self.tankMaxVolume, self.tankMinVolume, "CONTAINERS", self.containerMaxCharge, self.containerMinCharge)
        print("tanks max and min soc", self.tankMaxSOC, self.tankMinSOC)
       
        # now just deal with the case of allways positive
        #bassically we just want to add enough tanks for storage to meet the drain 
        # so sum drain and reduce this everythime we store positive energy
        array = []
        count = 0
        neg = []
        pos = []
        for element in self.difference:
            if(count <= 1):
                array.append(self.difference[count])
            count = count + 1
        print(array)
        for element in self.difference:
            if element < 0:
                neg.append(element)
            else:
                pos.append(element)
        tempArray = []
        for i in range(len(self.difference)):
            if i < 1000:
                if i >= 95 and self.difference[i] < 0:
                    print(i)
                    quit()
                tempArray.append(self.difference[i])
        
        totalNegative =0
        sumTwo= 0
        for element in tempArray:
            if element < 0:
                totalNegative = totalNegative + element
            else:
                sumTwo = sumTwo + element
        print(totalNegative/100000, "SUM")
        print(sumTwo/100000, "TWO")
        
        self.optimalTanks, tankData = OptimalTanks(100000,100,100,0,self.difference,self.RTE, abs(totalNegative)).optimalTanks()
     
        
        #optimalTankGraph = GraphTanksChange(tankData, self.data)
        #optimalTankGraph.graph()
     
     
        self.optimaContainers, containerData = OptimalContainers(100000,100000,10,self.difference,self.optimalTanks,abs(totalNegative)).optimalContainers()
        #OptimalContainersGraph = ContainerGraph(containerData, self.difference)
        #OptimalContainersGraph.graph()
        # we do not need to optimalContainer graph and tank Graph just this one
        graphWindow = Graphs(containerData,tankData,self.difference)
      
        graphWindow.graph()
        print("after")
        quit()

        self.energyManagement = energyHandler(self.RTE,self.cells) # handles the storage and the management of the energy
      
        containers = []
        for section in self.cells:
            for container in section.containers:
                containers.append(container)
        
        self.energyManagement.energyManagement(-10,self.tanks,self.fullEmpty)
        
        quit()
# Instantiate the Main class and run the program
if __name__ == "__main__":
    main = Main()
    main.run()
    
