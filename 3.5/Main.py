from SystemInitalization import systemInitalization
from ReadData import ReadData
from EnergyHandler import energyHandler
from OptimalTanks import  OptimalTanks
from OptimalContainers import OptimalContainers
from Clock import clock
from queue import Queue
import pandas as pd
from datetime import datetime, timedelta

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
        # Main execution code
        system = systemInitalization("Generated.csv","loadResampled.csv") # this will create all the sections
        
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
        
        print(len(self.difference))
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

        result,self.optimalTanks = OptimalTanks(200,100,100,0,[-100,-200],self.RTE, 200).optimalTanks()
      
        # what happens if draing is greater than the remaining 
        print("AFTER")
        print("Double negative not wokring properly, -100,-100 creating two tanks insead of 1")
        for tank in self.optimalTanks:
            print(tank.tName)
            print(" ", tank.volume)
            print("     ", tank.soc, "this is soc")
            print("         ", tank.currentChargedCapacity())
            print("         ", tank.remainingCapacity() <= 100000 , " remaining")
        #self.optimalContainers = OptimalContainers(1000,100,5,[-1000], self.optimalTanks).optimalContainers()
        print("BEFORE")
        self.optimaContainers = OptimalContainers(100,100,10,[-100,-200],self.optimalTanks).optimalContainers()
        print("after")
        
        for container in self.optimaContainers:
            print(container.cName,container.charge)
            for tank in container.correspondingTanks:
                print(tank.tName)
        print("YAYA we should have two containers with this")   
        quit()
      
        self.energyManagement = energyHandler(self.RTE,self.cells) # handles the storage and the management of the energy
        self.clock = clock(self.step,self.cells,self.tanks,self.energyManagement) # clcok for each five minute step
  
        containers = []
        for section in self.cells:
            for container in section.containers:
                containers.append(container)


        self.energyManagement.energyManagement(-10,self.tanks,self.fullEmpty)
        
        #best = self.energyManagement.bestCombinatinoOfContainersForTanks(containers,self.tanks)
        # now we are going to store and expend energy
        for energy in self.difference:
            self.energyManagement.energyManagement(energy,self.tanks,self.fullEmpty)
        print("Fnished")
        self.energyManagement.printBacklog()
        print("AFTER")
        
        #self.energyManagement.storeEnergy(30,self.tanks,self.cells[0].containers,self.fullEmpty)

        '''
    
            bestCombination = self.energyManagement.findCombination(self.tanks,200)
            if(bestCombination != None):
                containers = self.energyManagement.optimalContainersTwo(50,self.cells,bestCombination,0)
                
            for container in containers:
                print(container.sName,container.cName,container.charge)
            bestContainers = self.energyManagement.bestCombinationContainers(containers,4)
        '''

        
        """
        for energy in generatedSurplus:
            self.clock.update(self.tanks,self.cells,self.fullEmpty)# move five minutes
            self.energyManagement.energyManagement(self.surplus.get(),self.tanks,self.fullEmpty)
        print(self.clock.time)
        print("Finished")
        
        print(self.cells[0].containers[0].charge)
        """
        """_summary_

        for section in self.cells:
                print(section.sName)
                for container in section.containers:
                    print("         ",container.cName, container.onOffEfficency)

        for tank in self.tanks:
            print(tank.tName)
        """
# Instantiate the Main class and run the program
if __name__ == "__main__":
    main = Main()
    main.run()
    
#to do 
    """
    Test the energy system if it works and if all full and empty work 
    then think of some more questions to ask at the end of the week
    
    - containers are on for as long as they need to charge the required energy
    - so they may need multiple cycles
    """
    """
    Questions to email to Thomas Nan in regards to the project functionality
    - does section one have access to all tanks 
    - do tanks go across sections
    - how does the on off drain work 
    - is there a total energy capacity for each section 
    - do all sections have the same container count
    """
    #next Version 
    # Use threads to simultate the sections perhapse