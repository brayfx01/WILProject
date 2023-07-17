
from RoundTripEfficency import roundTripEffiency as RTE
from FullEmpty import FullEmpty
from queue import Queue
class energyHandler:
    def __init__(self,RTE,cells):
        self.RTE = RTE
        self.checkTanksStatus = None
        self.cells = cells
        self.step = 5 # five minutes
        self.backlog = Queue() # backlog 
        self.charge = Queue()# charge queue 
    # we will start with these 
    # taking 1 minute each to do a run
    

    # we want to get the best tanks to store the energy
    def energyManagement(self,energy,tanks,tanksSocStatus):
        self.checkTanksStatus = FullEmpty(tanks) # sets the status of all tanks
        stop = 0
        while(energy != 0 ):
            if(energy >= 0 ): # Storing Energy
                if(tanksSocStatus.checkIfAllFull() == True): # if there is no room to store 
                    print("all tanks are full")
                    self.backlog.put(energy) # put the remaining energy in a backlog
                    return
                    # get the best tanks to store in 
                
                # get the containres with the best storage potential
                containers = self.optimalContainers(energy,self.cells,0)
             
                for container in containers:
                     container.onOffStatus = True
                energy = self.storeEnergy(energy,tank,containers)
                if(energy == 0): # turn off all containers 
                    for container in containers:
                        container.onOffStatus = False
         # now we are going to deal with negative energy
            if(energy < 0): # we need to take energy from the system 
                if(self.checkTanksStatus.checkIfAllEmpty() == True): # all tanks are empty give error message and quit
                    self.backlog.put(energy) # put the remaining energy in a backlog
                    return
                # get the optimal tank
                tank = self.optimalTank(tanks,1)# in this case we are getting the most charged tank
                containers = self.optimalContainers(energy,self.cells,1)# giving energy
                # now turning on the containers
                for container in containers:
                    container.onOffStatus = True
                energy = self.storeEnergy(energy,tank,containers)
        # now after going through once we see what containres are still on and drain the battery
        self.drain(containers,tanks)
   
    def storeEnergy(self,energy,tank,containers):
        #we are currently only doing the positive energy 
        if(energy >= 0):
  
            # now we are getting the total charge of the capaicty
            totalCharge = 0 
            for container in containers:
                totalCharge = totalCharge + container.charge
            #now we are going to do one cycle of charging which does take 5 miutes
            # check if the charge breaks the max capacity of the tank
            if(self.RTE.RTE(totalCharge) > tank.remainingCapacity()): # we are seeing if we charge the energy with container does it go over capacity
                energy = energy - (abs(tank.remainingCapacity()- self.RTE.RTE(totalCharge))) # this is the remaining energy
                tank.soc = 1 # fully charge tank
                return energy
            # now if there is more space in the tank then requried to be charged 
            elif(self.RTE.RTE(totalCharge) <= tank.remainingCapacity()):
                # now the state of charge of the tank wll be the Round Trip Effieincy applied to the charge ability of the containers 
                soc = (tank.currentChargedCapacity() + self.RTE.RTE(totalCharge))/tank.volume
                tank.soc = soc
                energy = energy - totalCharge # update the remaining energy
                if (energy < 0):
                        energy = 0
                return energy
        if(energy < 0): 
            #getting total expenditure 
            totalExpenditure = 0
            for container in containers:
                totalExpenditure = container.charge + totalExpenditure
            #if there is enough energy stored 
            if(totalExpenditure <= self.RTE.RTE(tank.currentChargedCapacity())):
                soc = (self.RTE.RTE(tank.currentChargedCapacity())- abs(totalExpenditure))/tank.volume
                tank.soc = soc
                energy = 0 # all will have been stored
                return energy
            elif(totalExpenditure > self.RTE.RTE(tank.currentChargedCapacity())):
                # we need to get the remaining capacity left in the tank
                energy = energy + tank.currentChargedCapacity() # we are getting the new energy
                tank.soc =0 
                return energy
    def drain(self,containers,tanks):
        # this currently cannot deal with no tanks meeting drain requirmentes
        containerOnCount = 0
        for container in containers:
            if(container.onOffStatus == True):# getting how many containres are currently on 
                containerOnCount = containerOnCount +1
        drain = -containerOnCount * containers[0].onOffEfficency * self.step
        tank = self.optimalTank(tanks,1)
        tank.chargedCapacity = tank.chargedCapacity + drain # we are reducing the charge capacity by the drain amount of the bateires in the system
    # determines the optimal container to use 
    # will check their corresponding tanks
    def optimalContainersTwo(self,energy,cells,tanks,action):
        # we are going to go through and find all the containers connecting to the desired 
        # tanks 
        # then put them through the bestCombination to get the best combination of these tanks
        containers = []
        for section in cells:
            for container in section.containers:
                for tank in container.correspondingTanks:
                    # now we have the corresponding tanks for each container
                    # now we are checking if they connect to one of the tanks if they are add them to containers array 
                    for targetTank in tanks:
                        if(tank.tName == targetTank.tName): # we have found a container that connects to one of the tanks
                            if(len(containers) == 0):# there is nothing in there 
                                containers.append(container)
                            else: # now checking for duplicates
                                for containerTwo in containers:
                                    if (container.sName == containerTwo.sName and container.cName == containerTwo.cName): # this means we found a duplicate
                                        continue
                                    else:
                                        containers.append(container)
       
        return containers
    def optimalContainers(self,energy,cells,action):
        #for now we are going to work on the positive condition 
        #if energy is positive then we will need to charge the system 
        # so we want to get the highest possible charge of the containers that match or add up to the 
        # required energy 
        found = False
        containers = []
        if(action == 0): # this means we need to charge the energy
            cycle = 0 # this will track the first or second action
            while found == False:
                for section in cells:# geting the sections
                    for container in section.containers: # getting the containsers within each section
                        #now there are going to be two things that happen here 
                        # if there is a container that matches the charge requrimenets then use it 
                        # unless we need to use multiple differeing containers
                        if (cycle == 0):
                            if(container.charge == energy):# we have found a continaer with optimal parameters so end the loop and pass it 
                                found == True
                                print("We have found a container")
                                containers.append(container)
                                return containers
                        if(cycle == 1): 
                            # this means there are no containers that meet the requirements so we want to start adding
                            # containers charge to meet requriemnts
                            containers.append(container)
                            if(self.containerSum(containers) >= energy): # we have enough containers to meet demands
                                return containers
                if(cycle == 0):# we completed first loop and did not find optimal container
                    cycle = 1
                elif(cycle == 1): # we conpleted second loop and did not find a combination of optimal containres 
                    # so we have to return what we have
                    cycle == 0
                    return containers
        if(action == 1): # expending energy into the system
            for section in cells:
                for container in section.containers:
                        #we found container with optimal parameters
                        if(container.charge == abs(energy)):
                            return 
            for section in cells:
                for container in section.containers:
                    containers.append(container)
                    if(self.containerSum(containers) >= abs(energy)):
                        return containers
            return containers

    def optimalTank(self,tanks, action):
        optimalTank = None 
        for i in range(len(tanks)):
            if(i == 0): # by default just choose the first tank as best 
                optimalTank = tanks[i]
                continue
                 # as they all have the same capacity we can find wich has the lowest current SOC
            if(action == 0): # we are storing energy
                if(tanks[i].currentChargedCapacity() < optimalTank.currentChargedCapacity()):
                        optimalTank = tanks[i]
            elif(action == 1): # we are taking energy
                self.checkTanksStatus.checkIfAllEmpty()
                if(tanks[i].currentChargedCapacity() > optimalTank.currentChargedCapacity()):
                    optimalTank = tanks[i]
  
        return optimalTank
    
        
    def findCombination(self,tanks, energy):
        length = len(tanks)

        # Helper function to find all combinations recursively
        def findCombinationRecursion(index, currentCombination, currentTotalRemainingCapacity):
            nonlocal best_combination, best_total_volume

            if currentTotalRemainingCapacity >= energy:
                if best_combination is None or (currentTotalRemainingCapacity < best_total_volume and currentTotalRemainingCapacity >= energy):
                    best_combination = currentCombination
                    best_total_volume = currentTotalRemainingCapacity
                return

            if index >= length:
                return

            # Include the current object in the combination
            current_object = tanks[index]
            findCombinationRecursion(index + 1, currentCombination + [current_object], currentTotalRemainingCapacity + current_object.remainingCapacity())

            # Exclude the current object from the combination
            findCombinationRecursion(index + 1, currentCombination, currentTotalRemainingCapacity)

        # Sort objects in descending order based on volume
        tanks.sort(key=lambda obj: obj.remainingCapacity(), reverse=True)

        # Initialize the best combination and total volume
        best_combination = None
        best_total_volume = float('inf')

        # Start the recursive search
        findCombinationRecursion(0, [], 0)

        return best_combination

    def optimalTanks(self,energy,tanks,action):
        optimalTank = []
        # first we are going to check if there are any 
        # tanks that fit the energy properly
        
        for i in range(len(tanks)):
            if(tanks[i].currentCHargedCapacity() == energy):# we have found a tank that can be used to store all the energy
                optimalTank.append(tanks[i])# append this tank and return optimal tank
                return optimalTank
        # now we are going to check for combinations of tanks to meet the energy requirements
        self.bestCombination(tanks,energy)        
    def containerSum(self,containers):
        sum = 0
        for container in containers:
            sum = container.charge + sum
        return sum