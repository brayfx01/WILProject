from SystemInitalization import systemInitalization


from OptimalTanks import  OptimalTanks
from OptimalContainers import OptimalContainers
from queue import Queue
import pandas as pd

from InitialUI import InitialUI
from getTankData import GetTankData
from GetContainerData import GetContainerData
from SaveTanksContainers import saveTanksContainers

from ResultsUI import Graphs

class Main:
    def __init__(self):
       # these are the vairables that will be used for the boundaries
        self.tankMaxVolume = 0
        self.tankMinVolume = 0
        
        self.tankMaxSOC = 0
        self.tankMinSOC = 0
        
        self.containerMaxCharge = 0
        self.containerMinCharge = 0
        self.containerOnOffEfficency = 0

        self.generatedColumnName = ""
        self.loadColumnName = ""
        
        self.RTE = 0
        self.onOffEfficency = 0
      
        # array of the differences to determine if we are storing or expending
        self.difference = []

        
        self.cells =[]
        self.tanks = []
        self.tankVolumesForSection = []
        self.tankSOCForSections = []
       
        
        # will move into surplus if all full or empty
        self.data = None
        self.fullEmpty = None

        self.finished = False


        
    def run(self):
        # Main window for getting the config files
        while(self.finished == False):
            window = InitialUI()

            window.createWindow()

            configFile = window.getConfigFile()
            generatedCsv= window.getGenFile()
            loadFile = window.getLoadFile()
         
        
            #initialization of the system
            system = systemInitalization(generatedCsv, loadFile,configFile) # this will create all the sections
            # 0 means getting a number 1 means getting a string
            self.tankMaxVolume = system.getCriticalInfo("Tank Max Volume",0)
            self.tankMinVolume = system.getCriticalInfo("Tank Min Volume",0)
            
            self.tankMaxSOC = system.getCriticalInfo("Tank Max SOC",0)
            self.tankMinSOC = system.getCriticalInfo("Tank Min SOC",0)
            
            self.containerMaxCharge = system.getCriticalInfo("Container Max Charge",0)
            self.containerMinCharge = system.getCriticalInfo("Container Min Charge",0)
            self.containerOnOffEfficency = system.getCriticalInfo("Container On Off Efficency",0)
         
            self.onOffEfficency = system.getCriticalInfo("Container On Off Efficency",0)
            self.generatedColumnName = system.getCriticalInfo("Generated Column Name:",1)
            self.loadColumnName = system.getCriticalInfo("Load Column Name:",1)
            
            self.cells = system.getSections()# gets the sectiosn which contain the containers
            self.tanks = system.getTanks()#gets tank

            self.RTE = system.getRTE()#gwets RTE
            self.fullEmpty = system.getFullEmpty()#gets the FULLEMPTY checher
        
            print(self.RTE.efficency)
      
            self.difference = system.generateSurplus(self.generatedColumnName,self.loadColumnName).to_numpy()
    
     
         
            # now just deal with the case of allways positive
            #bassically we just want to add enough tanks for storage to meet the drain 
            # so sum drain and reduce this everythime we store positive energy
    
            tempArray = []

            for i in range(len(self.difference)):

                    tempArray.append(self.difference[i])

            totalNegative =0
         
           
            for element in tempArray:
                if element < 0:
                    totalNegative = totalNegative + element
        
            self.optimalTanks = OptimalTanks(self.tankMaxVolume,self.tankMinVolume,self.tankMaxSOC,self.tankMinSOC,self.difference,self.RTE, abs(totalNegative),self.containerMaxCharge,self.containerOnOffEfficency ).optimalTanks()
    


        
            data = GetTankData(self.optimalTanks, self.difference)
            # this gets the data for the graphs in the UI
            totaltankData, individualTankData, totalSoc = data.calculateData()
     
        
      
      

            dummy = []
        
            for energy in self.difference:
                if(energy < 0):
                    dummy.append(energy)
                if(energy > 0):
                    dummy.append(energy)
                    break
            print(max(dummy))
            self.optimalContainers, containerData = OptimalContainers(self.containerMaxCharge,self.containerMinCharge,100,dummy,self.optimalTanks,abs(totalNegative),self.RTE).optimalContainers()
            print(max(self.difference))
            for container in self.optimalContainers:
                print(container.cName,container.charge)
                for tank in container.correspondingTanks:
                    print(tank.tName)
          
            contData = GetContainerData(self.optimalContainers,self.optimalTanks, self.difference,self.RTE)

            totalContData, individualContainerData  = contData.getData()


            graphWindow = Graphs(totalContData,totaltankData,self.difference, individualTankData,totalSoc, individualContainerData,window,self.finished)

            self.finished,saveFile = graphWindow.graph()
        # saving all the data to a designated file
        saveFile = saveTanksContainers(saveFile,self.onOffEfficency, self.RTE.efficency,self.tankMaxVolume,self.tankMinVolume,self.tankMaxSOC,self.tankMinSOC,self.containerMaxCharge,self.containerMinCharge,
                 self.generatedColumnName,self.loadColumnName, self.optimalTanks,self.optimalContainers)
        saveFile.writeToFile() 

 
# Instantiate the Main class and run the program
if __name__ == "__main__":
    main = Main()
    main.run()
    
