
from RoundTripEfficency import roundTripEffiency as RTE
from FullEmpty import FullEmpty
from queue import Queue
from itertools import combinations
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
                tank = self.findCombination(tanks,1)# in this case we are getting the most charged tank
                # if there are no combinatinos that work  use them all
                if tank == None:
                    tank = tanks
                # getting the containers from the cells
                containers = []
                for section in self.cells:
                    for container in section.containers:
                        containers.append(container) 
                          
                bestCombinationContainers = self.bestCombinationContainers(energy,containers)# giving energy
                if bestCombinationContainers == None:
                    bestCombinationContainers = containers
                # now turning on the containers
                for container in containers:
                    container.onOffStatus = True
                energy = self.storeEnergy(energy,tank,containers)
        # now after going through once we see what containres are still on and drain the battery
        self.drain(containers,tanks)
        
    def storeEnergy(self,energy,tanks,containers, fullEmptyCheck):
        if energy > 0: # this is the positive case of energy 
            # get the best combination of containers to charge the energy 
            bestContainersCombination = self.bestCombinationContainers(containers,energy)
            # if no combination => energy use them all any ways
            if bestContainersCombination == None :
                bestContainersCombination = containers
            # now getting an individual tank
            for tank in tanks:
                if(energy == 0):
                    print("Stored successfully")
                    break
                if(fullEmptyCheck.checkIfAllFull() == True): # all tanks are full
                    print("All Tanks are full")
                    break
                # this will drain
                if(self.containerRemaingCharge(bestContainersCombination,0)== True):# if all contianers have no remainig charge for the 5 minuets
                    print("Finish the cycel")
                    print("Finish up store by adding the drain for the cycle")
                    break
                # can we store all of energy in this tank
                if(tank.remainingCapacity() >= self.RTE.RTE(energy)): # this tank can fully store the energy
                    #getting one container from bestContianer
                    for container in bestContainersCombination:
                        #if it can charge in one cycle then charge
                        if(container.remainingCharge >= energy):
                            #set this tank to full
                             # this tank is full
                            tank.Charge(self.RTE.RTE(energy))
                            container.onOffStatus = True # turn on the tank
                            container.remainingCharge = container.remainingCharge - energy # get the difference of these two 
                            energy = 0
                        if(container.remainingCharge < energy): # we need to use multiple cycles
                            # charge the tank by the container charge
                            tank.Charge(self.RTE.RTE(container.charge))
                            #Turn on the tank
                            container.onOffStatus = True
                            container.remainingCharge = 0 # we charge as much as we could in this step with this container
                            energy = energy - container.charge
                elif(tank.remainingCapacity() < self.RTE.RTE(energy)): # this tank does not have enough storage
                    storeable = energy - tank.remainingCapacity() # how much can we store
                    for container in bestContainersCombination:
                        if(container.remainingCharge >= energy ): # this container can fully charge in one cycle
                            energy = energy - tank.remainingCapacity() # this is the remaining Energy
                            tank.soc =1 # this tank is full
                            container.onOffStatus = True # turn on the contianer
                            container.remainingCharge = container.remainingCharge - storeable # how much can this container charge in this instance
                           
                            
                            
                        

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
        duplicateFound = False
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
                                   # print("beggining of loop", containerTwo.sName,containerTwo.cName)
                                    if (container.sName == containerTwo.sName and container.cName == containerTwo.cName): # this means we found a duplicate
                                        duplicateFound = True
                                        break
                                #check if a duplicate has been found if not add to containers 
                                # else reset duplicate to false
                                if(duplicateFound == False):
                                    containers.append(container)
                                else:
                                    duplicateFound = False 
                            

       
        return containers
   
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
    def bestCombinationContainers(self,containers, energy):
        length = len(containers)

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
            current_object = containers[index]
            findCombinationRecursion(index + 1, currentCombination + [current_object], currentTotalRemainingCapacity + current_object.charge)

            # Exclude the current object from the combination
            findCombinationRecursion(index + 1, currentCombination, currentTotalRemainingCapacity)

        # Sort objects in descending order based on volume
        containers.sort(key=lambda obj: obj.charge, reverse=True)

        # Initialize the best combination and total volume
        best_combination = None
        best_total_volume = float('inf')

        # Start the recursive search
        findCombinationRecursion(0, [], 0)

        return best_combination
          
    def containerSum(self,containers):
        sum = 0
        for container in containers:
            sum = container.charge + sum
        return sum
    def containerRemaingCharge(self,containers,action):
        full = False
        empty = False
        if(action == 0): # checking if full
            # going through all contianers to see if they are able to continue charging this cycle
            for container in containers:
                if container.remainingCharge == 0: # cannot charge more this step
                    continue
                if(container.remainingCharge != 0):
                    full = True
                    return full
            full = False 
            return full
        elif action == 1: # if we need to tak
            for container in containers:
                if container.remainingCharge != 0:
                    continue
                else:
                    return True
            return False

                
                