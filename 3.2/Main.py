from SystemInitalization import systemInitalization
from ReadData import ReadData
from EnergyHandler import energyHandler
from Clock import clock
from queue import Queue
class Main:
    def __init__(self):
       

        self.RTE = 0
        self.step = 5 # 5 minutes
        self.backlog = Queue()
        
        self.cells =[]
        self.tanks = []
        self.tankVolumesForSection = []
        self.tankSOCForSections = []
        
        self.data = ReadData() #this is the queue for energy to be handled 
        # will move into surplus if all full or empty
        
        self.fullEmpty = None
        self.energyManagement = None
        self.clock = None
    def run(self):
        # Main execution code
        system = systemInitalization("Generated.csv","loadResampled.csv") # this will create all the sections
        self.cells = system.getSections()#initializes the system
        self.tanks = system.getTanks()#gets tank
        self.RTE = system.getRTE()#gets RTE
        self.fullEmpty = system.getFullEmpty()#gets the FULLEMPTY checher
        self.data.read("Generated.csv","loadResampled.csv") #Reads data 
    
        generatedSurplus = self.data.getGeneratedSurplus()
        # every element will be five minute intervals
        for element in generatedSurplus:
            self.backlog.put(element)
        


        self.energyManagement = energyHandler(self.RTE,self.cells) # handles the storage and the management of the energy
        self.clock = clock(self.step,self.cells,self.tanks,self.energyManagement) # clcok for each five minute step
        
        
        #self.energyManagement.energyManagement(-40,self.tanks,self.fullEmpty)

        print
        self.energyManagement.storeEnergy(30,self.tanks,self.cells[0].containers,self.fullEmpty)

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