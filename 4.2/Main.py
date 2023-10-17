from SystemInitalization import systemInitalization
from ReadData import ReadData
from EnergyHandler import energyHandler
from OptimalTanks import  OptimalTanks
from OptimalContainers import OptimalContainers
from queue import Queue
import pandas as pd
from datetime import datetime, timedelta
from InitialUI import InitialUI
from getTankData import GetTankData
from GetContainerData import GetContainerData
from GraphTanksChange import GraphTanksChange
from ContainerGraph import ContainerGraph
from Graphs import Graphs

from ExpandedGraphs import ExpandedGraphs

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
        self.finished = False
        
    def run(self):
        # Main window for getting the config files
        while(self.finished == False):
            window = InitialUI()

            window.createWindow()

            print("Main")
            configFile = window.getConfigFile()
            generatedCsv= window.getGenFile()
            loadFile = window.getLoadFile()
            print("Main", configFile)
            print("Main",generatedCsv)
            print("Main", loadFile)
            
            
        
            #initialization of the system
            system = systemInitalization(generatedCsv, loadFile,configFile) # this will create all the sections
            
            self.tankMaxVolume = system.getCriticalInfo("Tank Max Volume")
            self.tankMinVolume = system.getCriticalInfo("Tank Min Volume")
            
            self.tankMaxSOC = system.getCriticalInfo("Tank Max SOC")
            self.tankMinSOC = system.getCriticalInfo("Tank Min SOC")
            
            self.containerMaxCharge = system.getCriticalInfo("Container Max Charge")
            self.containerMinCharge = system.getCriticalInfo("Container Min Charge")
            
            self.cells = system.getSections()# gets the sectiosn which contain the containers
            self.tanks = system.getTanks()#gets tank

            self.RTE = system.getRTE()#gwets RTE
            self.fullEmpty = system.getFullEmpty()#gets the FULLEMPTY checher
        
            self.data = pd.read_excel("new_data_with_difference.xlsx") 
            self.difference = self.data["Difference"].to_numpy()
            #self.difference = system.generateSurplus().to_numpy()
    
        
        
            print("Tank max charge", self.tankMaxVolume, self.tankMinVolume, "CONTAINERS", self.containerMaxCharge, self.containerMinCharge)
            print("tanks max and min soc", self.tankMaxSOC, self.tankMinSOC)
        
            # now just deal with the case of allways positive
            #bassically we just want to add enough tanks for storage to meet the drain 
            # so sum drain and reduce this everythime we store positive energy
    
            tempArray = []

            for i in range(len(self.difference)):

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
            posSum = 0
            negSum =0
            for tank in self.optimalTanks:
                posSum += tank.currentChargedCapacity()
            for energy in self.difference:
                if(energy < 0):
                    negSum += energy
        
            data = GetTankData(self.optimalTanks, self.difference)
            
            totaltankData, individualTankData, totalSoc = data.calculateData()
           
            for tank in self.optimalTanks:
                print(tank.tName, tank.currentChargedCapacity())
            totaldrain = 0
            
            #optimalTankGraph = GraphTanksChange(totaltankData)
            #optimalTankGraph.graph()
            total = 0
            tn = 0
            pe = 0
            for tank in self.optimalTanks:
                total += tank.currentChargedCapacity()
            for energy in self.difference:
                if(energy < 0):
                    tn += energy
                else:
                    pe += energy

            self.optimalContainers, containerData = OptimalContainers(1000,10,10,self.difference,self.optimalTanks,abs(totalNegative)).optimalContainers()
            """
            for cont in self.optimalContainers:
                print(cont.sName,cont.cName)
    
            """
        
            print(len(self.difference))
            contData = GetContainerData(self.optimalContainers,self.optimalTanks, self.difference)
           
            totalContData, individualContainerData  = contData.getData()
     
            #OptimalContainersGraph = ContainerGraph(totalContData)
            #OptimalContainersGraph.graph()


            
            #expand = ExpandedGraphs(self.difference, totaltankData,individualTankData,totalSoc,individualTankData,totalContData,individualContainerData)
            #expand.graph(1)
            
            graphWindow = Graphs(totalContData,totaltankData,self.difference, individualTankData,totalSoc, individualContainerData,window,self.finished)

            self.finished = graphWindow.graph()
    
        quit()

 
# Instantiate the Main class and run the program
if __name__ == "__main__":
    main = Main()
    main.run()
    
