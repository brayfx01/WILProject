
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
                tank = self.bestCombinationTanks(tanks,energy,0)# in this case we are getting the most charged tank
                if tank == None:
                    tank = tanks
                if(tanksSocStatus.checkIfAllFull(tank) == True): # if there is no room to store 
                    print("THis is energy",energy)
                    print("all tanks are full:")
                    print("putting ", energy , "into backlog")
                    self.backlog.put(energy) # put the remaining energy in a backlog
                    return
                # get the best tanks to store in 
                # get the optimal tank
                # 0 is remainingCapacity, 1 is currentcharged capacity
          
                 # if there are no combinatinos that work  use them all
                if tank == None:
                    tank = tanks
                containers = []
                for section in self.cells:
                    for container in section.containers:
                        containers.append(container) 
                        
                bestCombinationContainers = self.bestCombinationContainers(energy,containers)# giving energy
                if bestCombinationContainers == None:
                    bestCombinationContainers = containers
               # tank = self.removeUnreacheableTanks(tanks,bestCombinationContainers)
                print("After removing unseessary tanks")
                for t in tank:
                    print(t.tName)
            
                # apply theh RTE efficecny here to the energy only for storing
                energy = self.storeEnergy(self.RTE.RTE(energy),tank,containers,tanksSocStatus)
                # drain any remaining tanks that are on
                # only drain if we are finished
                print(tanksSocStatus.checkIfAllFull(tanks) == True)
                if(energy == 0):
                    print("Draining after exiting sotreEnergy")
                    self.drain(containers,tanks)
                print("Exist Store ENergy")
                stop = stop + 1 
                if(stop  == 3):
                    print("ERROR",energy)
                    for tank in tanks:
                        print(tank.tName)
                    quit()
         # now we are going to deal with negative energy
            if(energy < 0): # we need to take energy from the system 
                # if all tanks are empty put the enrgy in a backlog for potential future use
                tank = self.bestCombinationTanks(tanks,abs(energy),1)
                  # can meet the energy requirements use all of them and see what is left after
                if len(tank) == 0:
                    tank = tanks
                if(tanksSocStatus.checkIfAllEmpty(tank) == True): # if there is no room to store 
                    print("all tanks are empty")
                    self.backlog.put(energy) # put the remaining energy in a backlog
                    return
                # finding the optimal tanks for taking energy from
                

                # if there are no combinatino of tanks that 
              
                # getting a containers array
                containers = []
                for section in self.cells:
                    for container in section.containers:
                        containers.append(container) 
                # best combinatino of containers to meet the energy
                bestContainersCombination = self.bestCombinatinoOfContainersForTanks(containers,tanks)
                if bestContainersCombination == None:
                    bestCombinationContainers = containers
            
                # now turning on the containers
                for container in containers:
                    container.onOffStatus = True
                energy = self.storeEnergy(energy,tank,bestContainersCombination,tanksSocStatus) 

        if(tanksSocStatus.checkIfAllEmpty(tanks) == True):
            print("all tanks are emtpy an we cannot drain")
       
        for tank in tanks:
            print(tank.currentChargedCapacity(),tank.tName)
        print(energy, "Exiting")
        print("There is a wrong calculation trace and try again")
        return
                 
        # now after going through once we see what containres are still on and drain the battery
        
        
       #to do 
       # if all charge of containers used drain and recharge them all 
       # then work on energy managemetn to store positive energy 
    def storeEnergy(self,energy,tanks,containers, fullEmptyCheck):
        
        print(energy,"//////////////////////////")
        for tank in tanks:
            print(tank.tName,tank.soc)
   
        if energy >= 0: # this is the positive case of energy 
            
            for container in containers:
                print(container.cName, "//////////////////////////////////////////////////")
    
            # this will remove any tanks that have no connection with any of the best containers
           # tanks = self.removeUnreacheableTanks(tanks,bestContainersCombination)
            # now getting an individual tank
            for container in containers:
                print(container.sName,container.cName)
            for tank in tanks:
                print("This is the current tank", tank.tName,"rem:",tank.remainingCapacity(), energy)
                if(fullEmptyCheck.checkIfAllFull(tanks) == True): # all tanks are full
                    print(energy)
                    print("All Tanks are full:")
                    print("Putting", energy, "IN THE BACKLOG")
                    self.backlog.put(energy)# put the remaining energy in the backlog
                    break
                # this will drain
                # if all containers have charged for the 5 minuets
                if(self.containerRemainingCharge(containers,tank,0)== True):# if all contianers have no remainig charge for the 5 minuets
                    print("all containers charge 0")
                    self.drain(containers,tanks)# drains all active tanks
                    # sets the remainingCharge back to the original value for the next use
                    for container in containers:
                        container.remainingCharge = container.charge # set this back to max
                # this second check will    
                # we have finished but need to drain all tanks used
                if(energy == 0):
                    print("Stored successfully")
                    return energy
                # can we store all of energy in this tank
                if(tank.remainingCapacity() >= energy): # this tank can fully store the energy
                    print("tanks capacity greater than energy")
                    #getting one container from bestContianer
                    for container in containers:
                        if(energy == 0):
                            break
                        if(tank.remainingCapacity() == 0): # we have stored all we can move to next tank
                            print("This tank is full move to next tank")
                            break
                        print("this is the current container", container.sName,container.cName,container.remainingCharge)
                        #if this container cannot charge this tank skip it
                        if(self.correspondingContainer(tank,container) == False):
                            print("Move to next container or tank")
                            continue
                        #if it can charge in one cycle then charge
                        if(container.remainingCharge >= energy):
                            print("container can fully charge this cycle")
                            #set this tank to full
                            # this tank is full
                            print("remaining before charge", tank.remainingCapacity())
                            tank.Charge(energy)
                            print("Remaining After charge", tank.remainingCapacity())
                       
                            container.onOffStatus = True # turn on the container
                            container.remainingCharge = container.remainingCharge - energy # get the difference of these two 
                            energy = 0
                        if(container.remainingCharge < energy and container.remainingCharge != 0): # we need to use multiple cycles
                            print("This container cannot fully charge this cycle")
                            # charge the tank by the container charge
                            print("Tank remaining before", tank.remainingCapacity())
                            tank.Charge(container.remainingCharge)
                            print("Tank remaining After", tank.remainingCapacity())
                            #Turn on the tank
                            container.onOffStatus = True
                            energy = energy - container.remainingCharge
                            container.remainingCharge = 0 # we charge as much as we could in this step with this container   
                elif(tank.remainingCapacity() < energy): # this tank does not have enough storage
                    print("Tank cannot hold all of energy")
                    for container in containers:
                        if(tank.remainingCapacity() == 0): # this tank has no more room for storage
                            print("go to next tank")
                            break
                        print("This is the current container", container.sName, container.cName,container.remainingCharge)
                        if(self.correspondingContainer(tank,container) == False):
                            print("Move to next container or tank")
                            continue
                        if(container.remainingCharge >= tank.remainingCapacity() ): # this container can fully charge in one cycle
                            print("Container can store all")
                            print("energy before",energy)
                            energy = energy - tank.remainingCapacity() # this is the remaining Energy
                            print("Energy after",energy)
                            container.onOffStatus = True # turn on the contianer
                            container.remainingCharge = container.remainingCharge - tank.remainingCapacity() # how much can this container charge in this instance
                            # charge the remaining Capacity
                            tank.Charge(tank.remainingCapacity())
                        elif(container.remainingCharge < tank.remainingCapacity()):
                            print("container cannot store all")
                            # this is what we stored
                            energy = energy - container.remainingCharge
                            container.onOffStatus = True # turn on the tank
                            tank.Charge(container.remainingCharge)
                            container.remainingCharge = 0
        elif energy < 0: # taking energy form system
           
            print("in the < 0")
            # getting the est containers to charge the system with 
            bestContainersCombination = self.bestCombinationContainers(energy,containers)
            # if none then use all containers
            if len(bestContainersCombination) == 0 :
                bestContainersCombination = containers
            # now getting the individual tanks
            
            for tank in tanks:
                if(fullEmptyCheck.checkIfAllEmpty(tanks) == True):
                    print("all tanks are empty")
                    # put the remaining Energy in the backlog
                    self.backlog.put(energy)
                    return 
                

                if(energy == 0):
                    print("Stored Successfully")
                    # drain all the containers in the system
                    self.drain(containers,tanks)
                    return energy
                # checking to see if we can take energy 
                # this tank has enough charge to cover energy
                print("Before >=", energy, tank.tName)
               
                if(self.RTE.RTE(tank.currentChargedCapacity()) >= abs(energy) ):
                    print("> =", self.RTE.RTE(abs(energy)), tank.currentChargedCapacity())
                    # now getting containers to charge this 
                    for container in bestContainersCombination:
                        # this containe take all the energy
                        if(container.remainingCharge >= abs(energy)):
                            print("Store all in one cycle")
                            # drain what we had in the tank
                            print("tank Charge Before drain", tank.currentChargedCapacity(),tank.tName)
                            tank.drain(self.RTE.RTE(tank.currentChargedCapacity()))
                            print("AFter", tank.currentChargedCapacity())
                            # turn on this container so we can drain later on
                            container.onOffStatus = True
                            # see how much this container has lef to charge this cycle
                            container.remainingCharge = container.remainingCharge + energy # energy is negative
                            energy = 0
                            
                        # this container can not charge everythin in one cycle
                        if(container.remainingCharge < abs(energy) and container.remainingCharge != 0):
                            print("Container <")
                            #drain what we have left to charge with container
                            tank.drain(self.RTE.RTE(container.charge))
                            # turn this container on 
                            container.onOffStatus = True
                            print(container.remainingCharge)
                            energy = energy + container.remainingCharge
                            print("This is energy", energy)
                            container.remainingCharge = 0 # we cannot use this in this interval to charge 
                elif(self.RTE.RTE(tank.currentChargedCapacity())< abs(energy)):# we cannot take all the energy from this tank
                    print(" < energy                                                            ////")
                    # getting the drainable amount from this tank
                    for container in bestContainersCombination:
                        print(container.cName, container.remainingCharge, "TTTTTTTTTTTTTTTT")
                        print(tank.tName,tank.soc)
                        if(tank.soc == 0):
                            print("Pass")
                            break
                        # we are going to transfer all of this tanks current energy
                        if(container.remainingCharge >= tank.currentChargedCapacity() and tank.currentChargedCapacity() != 0):
                            # applying the RTE to the current Carhged
                            print("Contianer >=",energy,container.remainingCharge,container.cName)
                            energy = energy + self.RTE.RTE(tank.currentChargedCapacity())
                            print(energy, "After")
                            container.onOffStatus = True
                            container.remainingCharge = container.remainingCharge - tank.currentChargedCapacity()
                            print("Container remaining", container.remainingCharge)
                            tank.soc = 0
                        # now we need to use multipe charges for this tank to transfer energy
                        elif(container.remainingCharge < tank.currentChargedCapacity() and tank.currentChargedCapacity() !=0):
                            print("container < ", container.cName)
                            # this is how much we will be chargeing
                            # applying the RTE to the remaining Charge of the container as this is all that will get transfered
                            print("Container remaining Charge and tank", container.remainingCharge,container.cName,energy )
                            energy = energy + self.RTE.RTE(container.remainingCharge)
                            # we have drained this much from the tank
                            print(tank.currentChargedCapacity(), "Tank Before")
                            tank.drain(container.remainingCharge)
                            print(tank.currentChargedCapacity(), "Tank AFter")
                            print(energy , "Energy after")
                            container.onOffStatus = True
                            container.remainingCharge = 0 # cannot charge untill next cycel
 
        return energy
                           
                            
    def removeUnreacheableTanks(self,tanks,containers):
        newTanks = []
        tankConnected = False
        # for each tank check if there is a container to charge it
        for tank in tanks:
            print("unreacheable tank",tank.tName)
            for container  in containers:
                for correspondingTank in container.correspondingTanks:
                    if(tank.tName == correspondingTank.tName):
                       print("tank name", tank.tName, "Container Name", container.cName)
                       # this tank is chargeable 
                       tankConnected = True
            print("adding this tank", tank.tName)
            if(tankConnected == True):
                newTanks.append(tank)
                tankConnected = False
                   
                
            # add this to new tank

        print("in Remove")
        for tank in newTanks:
            print(tank.tName)     
            
        return newTanks
                
    def correspondingContainer(self,tank,container):
        for correspondingTank in container.correspondingTanks:
            if(correspondingTank.tName == tank.tName):
                return True
        return False           
    # the drain
    def drain(self,containers,tanks):

        containerOnCount = 0
        for container in containers:
            if(container.onOffStatus == True):# getting how many containres are currently on 
                containerOnCount = containerOnCount +1
                # turn off this tank
                container.onOffStatus == False
                
                
        
        drain = -containerOnCount * containers[0].onOffEfficency #get the on off efficency
        # set this back to zero so it does not affect other runs 
        containerOnCount = 0
        #bestTankCombination = self.findCombination(tanks,abs(drain))
        bestTankCombination = tanks

        if bestTankCombination == None:
            bestTankCombination = tanks
        # drain the tank
        #getting an individual tank in bestTankComination
        for tank in bestTankCombination:
            print("Drain ", tank.tName,tank.currentChargedCapacity(),drain)
            if(tank.currentChargedCapacity() >= abs(drain) and drain != 0):
                print("tank has enough to drain")
                amount = drain
                drain = 0
                print("tank drain before", tank.tName,tank.currentChargedCapacity())
                tank.drain(amount)
                print("tank drain after", tank.tName,tank.currentChargedCapacity())
                break
            elif(tank.currentChargedCapacity() < abs(drain) and drain != 0):# now we are dealing with energy drain being greater than the remaining energy in the tank
                drain = drain + tank.currentChargedCapacity()
                tank.soc = 0 # make this tank empty
                # turn off all the containers

        if(drain != 0):
            print("Not enough energy in storage to drain", drain)
            quit()
            
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
    # we are getting all the corresponding containers for a tank
    def getCorrespondingContainers(self,containers, tank):
        correspondingContainers = []
        for container in containers:# getting individual container
                print("IN GET", container.cName)
                for cTank in container.correspondingTanks:
                    print(cTank.tName,tank.tName)
                    if(cTank.tName == tank.tName):
                        print("adding ", container.cName)
                        correspondingContainers.append(container)
        return correspondingContainers

    def tupleCharge(self,tuple):
        charge = 0
        for container in tuple:
            charge = charge + container.charge

        return charge
    def duplicate(self,container,bestContainers):
        for individualContainer in bestContainers:
            print(container.cName,container.sName,individualContainer.cName,individualContainer.sName)
            # if the two containers section and container names are the same then they are a duplicate
            if(container.cName == individualContainer.cName and container.sName == individualContainer.sName):
                return True
        return False
# alter this instead to subtract the remaining charge of tanks so that one container 
# does not dominate the entire system
# first half is done just have to do it for the second half of the function
    def bestCombinatinoOfContainersForTanks(self,containers,tanks):
        bestContainers = []# holds the best containesr
        
        
        #now we are going to go through each container passed and check if it 
        #corresponds with a tank 
        for tank in tanks:
            found = False
            cannotCharge = False
            for container in containers:
                # check if this container corresponds with this tank
                if(found == True):
                    continue
                if(self.correspondingContainer(tank,container) == False):
                    # if not corresponding skip this container
                    continue 
                # if the container can fully charge the tank
                if(container.remainingCharge >= tank.remainingCapacity()):
                    print("IN BestComb, cont can fully charge")
                    found = True
                    # add this to best container then move to next tank
                    # check if container is already been added 
                    if(len(bestContainers) != 0):
                        if(self.duplicate(container,bestContainers) == False):
                            # this will ensure that one container does not dominate over the rest of containers
                            container.remainingCharge = container.remainingCharge - tank.remainingCapacity()
                            bestContainers.append(container)
                    else:
                        container.remainingCharge = container.remainingCharge - tank.remainingCapacity()
                        bestContainers.append(container)
                    
            if(found == False): # we did not find any containres that can fully charge
                print("Finding combinations of tanks, for", tank.tName)
                # get all corresponding containers fo rthis tank
                correspondingContainers = []
                print("BEFORE CORRESPONDING CONTAINERS", tank.tName)
                correspondingContainers = self.getCorrespondingContainers(containers,tank)
                print("//////////")
                for container in correspondingContainers:
                    print(container.sName,container.cName)
                if(len(correspondingContainers)==0):
                    print("No corresponding containers found")
                    quit()
                else: # we have some containers to work with
                    # now we get the best combination 
                    print("THERE IS A Corresponding tank")
                    length = len(correspondingContainers)
                    # combination 
                    combonationOfContainers = list(combinations(correspondingContainers,length)) # conbination of length size
                    
                    combinationsArray = []
                    # now we are going to find the total charge of each of the tuples
                    for tuple in combonationOfContainers:
                        charge = 0
                        print(tuple)
                        for container in tuple:
                            charge = charge + container.charge
                            print("THIS IS CHARGE", charge, container.cName)
                            print("Tanks ", tank.tName, "Remaining", tank.remainingCapacity())
                        print(charge, tank.tName,container.cName)
                        if(charge >= tank.remainingCapacity()):
                            # we need to substract each containers charge from this and
                            # if charge < tanks remaining set to 0 > 0 get the difference
                            print("Add to combinationsArray")
                            combinationsArray.append(tuple)
                            # jsut do anouther for here to finish this
                            
                    # if this charge of the combination is >= remaining capacity add it to the array
                    # there are no combination of containers that can charge this tank so just use all available one
                
                print(">>>>>>>>>>>>>>>")
                if len(combinationsArray) == 0: # there are no combinations that can fully charge
                    combinationsArray = correspondingContainers
                    cannotCharge = True
                    for container in correspondingContainers:
                        print(container.cName)
                else:
                    for tuple in combinationsArray:
                        for container in tuple:
                            print(container.cName)
                # now we are going to get rid of any duplicates in the tuple
                
                # there is no best combination of tanks so use all corresponding tanks
                if(cannotCharge == True):
                    cannotCharge = False
                else:
                    combinationsArray = min(combinationsArray, key=self.tupleCharge)
                # adding non duplicates 
                for container in combinationsArray:
                    if self.duplicate(container,bestContainers) == True:
                        continue # skip this tank
                    else:

                        bestContainers.append(container)
                for container in bestContainers:
                    #reset all containers remainingCharges
                    container.remainingCharge = container.charge

        return bestContainers
        
    def bestCombinationTanks(self,tanks, energy,action):
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
            if(action == 0):
                findCombinationRecursion(index + 1, currentCombination + [current_object], currentTotalRemainingCapacity + current_object.remainingCapacity())

                # Exclude the current object from the combination
                findCombinationRecursion(index + 1, currentCombination, currentTotalRemainingCapacity)
            elif(action == 1):
                # we are finding best combination in regards to chargedCapacity
                findCombinationRecursion(index + 1, currentCombination + [current_object], currentTotalRemainingCapacity + current_object.currentChargedCapacity())

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
    
    def bestCombinationContainers(self,energy, containers):
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
    # this is wether the containers can continue charging this cycle
    def containerRemainingCharge(self,containers,tank,action):
        full = False
        empty = False
        if(action == 0): # checking if full
            # going through all contianers to see if they are able to continue charging this cycle
            for container in containers:
                # only check the corresponding tanks
                for cTank in container.correspondingTanks:
                    if(cTank.tName == tank.tName):
                        if container.remainingCharge == 0: # cannot charge more this step
                            continue
                        if(container.remainingCharge != 0):
                            full = False
                            return full
            full = True 
            return full
        elif action == 1: # if we need to tak
            for container in containers:
                if container.remainingCharge != 0:
                    continue
                else:
                    return True
            return False

                
                