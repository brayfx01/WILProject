
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
        print("BEGGINING ALL OF ENERGY MANAGMENT|||||||||||||||||||||||||||||||||||||||||", energy)

        while(energy != 0 ):
            if(energy >= 0 ): # Storing Energy
                tank = self.bestCombinationTanks(tanks,energy,0)# in this case we are getting the most charged tank
                if tank == None:
                    tank = tanks
                if(tanksSocStatus.checkIfAllFull(tank) == True): # if there is no room to store 
                    print("THis is energy",energy)
                    print("all tanks are full so let the rest go")
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
         # now we are going to deal with negative energy
            
            if(energy < 0): # we need to take energy from the system 
                if(tanksSocStatus.checkIfAllEmpty(tanks) == True):
                    if(energy != 0):
                        {
                            print("NOt enough charged energy")
                        }
                    print("all tanks are emtpy an we cannot drain")
                    for tank in tanks:
                        print(tank.currentChargedCapacity())
                    quit()
       
                # if all tanks are empty put the enrgy in a backlog for potential future use
                tank = self.findBestCombinationTanks(tanks,energy)
                for t in tank:
                    print(t.tName)
               
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
                bestCombinationContainers = self.findBestCombinationContainersForTanks(containers, tanks,1)

                if bestCombinationContainers == None:
                    bestCombinationContainers = containers

                
                energy = self.storeEnergy(energy,tank,bestCombinationContainers,tanksSocStatus) 
                # now we drain the tank for each container on 
                if(energy == 0):
                    print("Draining after exiting sotreEnergy")
                    self.drain(containers,tanks)
                stop = stop +1
                if(stop == 5):
                    print("ERROR")
                    quit()
                

       
        for tank in tanks:
            print(tank.currentChargedCapacity(),tank.tName)
        print(energy, "Exiting")
        print("There is a wrong calculation trace and try again")
        return
                 
        # now after going through once we see what containres are still on and drain the battery
        
        
       #to do 
       # if all charge of containers used drain and recharge them all 
       # then work on energy managemetn to store positive energy 
    def printBacklog(self):
        if(self.backlog.empty() != True):
            while self.backlog.empty() != True:
                print(self.backlog.get())
        else:
            print("nothing in backlog")
    def storeEnergy(self,energy,tanks,containers, fullEmptyCheck):
        
        print(energy,"START //////////////////////////")
        for tank in tanks:
            print(tank.tName,tank.soc)
            
        # this will drain
        # if all containers have charged for the 5 minuets
        if(self.containerRemainingCharge(containers,tank,0)== True and energy != 0):# if all contianers have no remainig charge for the 5 minuets

                    print("all containers charge 0, energy > 0 we need more containers")
                    for container in containers:
                        print(container.remainingCharge)
                    quit()
                    self.drain(containers,tanks)# drains all active tanks
                    # sets the remainingCharge back to the original value for the next use
                    for container in containers:
                        container.remainingCharge = container.charge # set this back to max
                    print("FAILED BECAUSE not enough containers to store in one cycle")
                    quit()
            
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
                    print("NEED MORE TANKS")
                    quit()
                    break

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
                        # if we cannot do this is one cycel then display an error
                        if(container.remainingCharge < energy and container.remainingCharge != 0): # we need to use multiple cycles
                            print("This container cannot fully charge this cycle", container.cName)
                            # charge the tank by the container charge
                            print("Tank remaining before", tank.remainingCapacity())
                            tank.Charge(container.remainingCharge)
                            print("Tank remaining After", tank.remainingCapacity())
                            #Turn on the tank
                            container.onOffStatus = True
                            energy = energy - container.remainingCharge
                            container.remainingCharge = 0 # we charge as much as we could in this step with this container
                # in this case we want to also adapt the tanks based on the given data in the config   
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
            # checkinf if all tanks are empty
            for tank in tanks:
                if(fullEmptyCheck.checkIfAllEmpty(tanks) == True):
                    print("all tanks are empty we need more")
                    # put the remaining Energy in the backlog
                    self.backlog.put(energy)
                    quit()
                    return energy
                
                # no more energy then drain and return
                if(energy == 0):
                    print("Stored Successfully")
                    # drain all the containers in the system
                    self.drain(containers,tanks)
                    return energy
                # checking to see if we can take energy 
                # this tank has enough charge to cover energy
                print("BEFORE tank current greater than energy")
                print("RTE of tank", self.RTE.RTE(tank.currentChargedCapacity()))
                if(self.RTE.RTE(tank.currentChargedCapacity()) >= abs(energy) ):
                    print("> =", self.RTE.RTE(abs(energy)), tank.currentChargedCapacity())
                    # now getting containers to charge this 
                    for container in containers:
                        # this containe take all the energy
                        
                        # apply RTE to container
                        if(container.remainingCharge >= abs(energy) and  self.corresponding(container,tank) == True):
                            print("Store all in one cycle", container.cName, container.sName)

                            # drain what we had in the tank
                            print("tank Charge Before drain for energy", tank.currentChargedCapacity(),tank.tName)
                            # energy is what we want to drain hence if RTE Tank >= energy 
                            # then we just want to drain energy and be done no need to apply 
                            # RTE IN THIS CASE
                            tank.drain(energy)
                            print("AFter", tank.currentChargedCapacity())

                            
                            # turn on this container so we can drain later on
                            container.onOffStatus = True
                            # see how much this container has lef to charge this cycle
                            container.remainingCharge = container.remainingCharge + energy # energy is negative
                            energy = 0
                            print("ENERGY after",energy)
             
                        print("////////////////")

                        # this container can not charge everythin in one cycle
                        
                        # this will pose an error and from this reccomend better number of containers
                        if(container.remainingCharge < abs(energy) and container.remainingCharge != 0):
                            print("Container cannot fully charge this tank", container.cName, container.sName)
                            #drain what we have left to charge with container
                            tank.drain(self.RTE.RTE(container.charge))
                            # turn this container on 
                            container.onOffStatus = True
                           
                            print("ENERGY BEFORE", energy)
                            energy = energy + self.RTE.RTE(container.remainingCharge)
                            print("ENERGY AFTER",energy)
                            print("This is energy", energy)
                            container.remainingCharge = 0 # we cannot use this in this interval to charge 
                            print("What remains in container after draining",container.remainingCharge)
                # this is fine but if we cannot take from all tanks then push out an errro
                elif(self.RTE.RTE(tank.currentChargedCapacity())< abs(energy)):# we cannot take all the energy from this tank
                    print(" < energy                                                            ////")
                    # getting the drainable amount from this tank
                    for container in containers:

                        print(tank.tName,tank.soc)
                        if(tank.soc == 0):
                            print("Pass")
                            break
                        # we are going to transfer all of this tanks current energy
                        print("BEFORE >=", container.cName)
                        if(container.remainingCharge >= tank.currentChargedCapacity() and tank.currentChargedCapacity() != 0 and self.corresponding(container,tank) == True):
                            # applying the RTE to the current Carhged
                            print("Contianer >=",energy,container.remainingCharge,container.cName, container.sName)
                            print("Tnkas current charge", tank.currentChargedCapacity())
                            energy = energy + self.RTE.RTE(tank.currentChargedCapacity())
                            print(energy, "After")
                            container.onOffStatus = True
                            container.remainingCharge = container.remainingCharge - tank.currentChargedCapacity()
                            print("Container remaining", container.remainingCharge)

                            tank.drain(tank.currentChargedCapacity())

                        # now we need to use multipe charges for this tank to transfer energy
                        
                        # this should throw an error and give reccomended containes
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
        print("RETURNING ENERGY",energy)
        return energy
    
        
        # calculate the sum of the tuple
    def remainingSum(self,tanks):
        sum = 0
        for tank in tanks:
            sum = sum + tank.remainingCapacity()
        return sum
    def currentChargedSum(self,tuples):
        sum = 0
        for tank in tuples:
            sum = sum + tank.currentChargedCapacity()
        return sum
        
            
        
    def duplicateTank(self,tank,bestTanks):
        for bTank in bestTanks:
            if(bTank.tName == tank.tName):
                return True
            else:
                continue
        return False
    def findBestCombinationTanks(self,tanks, energy):
        bestTanks = []
        found = False
        for tank in tanks:
            # we want to go and find a tank that is suitable
            # first case there is a tank that can handle all the energy
            if(energy > 0):
                if(tank.remainingCapacity() >= abs(energy)):
                    found = True
                    bestTanks.append(tank)
                    break
            elif energy < 0: # negative energy 
                if(tank.currentChargedCapacity() >= abs(energy)):
                    found = True 
                    bestTanks.append(tank)
                    break
                
            # now there is no tank that can handle all the energy so we find the best combination
            # will be used to see if we found any containers and so return them
        if(found == False):
                length = len(tanks) # this will be the maxium length of the combinations
                combos = []
                # getting all the combination of tanks based on length
                for r in range(2, length + 1):  # Generating combinations of length 2 to length of items
                    combos.extend(combinations(tanks, r))
                # holds the sum of the tanks currentCharge
                sumArray = []
                #hold the combination of containers Meeting the requirements
                combinationsMeetingEnergy = []
                # the smallest possible combinatino that meets the requirements
                smallestCombination = []
                #going through each tuple to determine their charged value
                for tuple in combos:
                    sum = 0
                    for tank in tuple:
                        if(energy >= 0): # negative energy
                            sum = sum + tank.remainingCapacity()
                        elif(energy < 0):# energy is negative
                            sum = sum + tank.currentChargedCapacity()
                    #this tuple can handle the energy
                    if(sum >= abs(energy)):
                        sumArray.append(sum)
                        #append this tuple
                        combinationsMeetingEnergy.append(tuple)
                    # now we get the smallestCOmbination in combinatinosMeeting
                if(len(combinationsMeetingEnergy) != 0):
                    # getting the smallest combination from combinations that meet the energy requirement
                    if(energy >= 0):
                        smallestCombination =  min(combinationsMeetingEnergy, key = self.remainingSum)
                    elif(energy < 0):
                        smallestCombination =  min(combinationsMeetingEnergy, key = self.currentChargedSum)
                    
                    for tank in smallestCombination:
                        if(self.duplicateTank(tank,bestTanks) == True):
                            continue
                        else:
                            bestTanks.append(tank)
                        # now go through the sumArray and grab the smallest meeting requriments
                        # or perhapse anouther way is to only add the sums that are greater than the tanks remaining capacity
                else:
                    bestTanks = tanks               
            # getting rid of duplicate 

        return bestTanks


                           
                            
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
        bestTankCombination = self.findBestCombinationTanks(tanks,drain)
        for tank in bestTankCombination:
            print(tank.tName)

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
                tank.drain(drain) # make this tank empty
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


    
    def tupleSum(self,containerArray):
        sum = 0
        for container in containerArray:
            sum = sum + container.charge

        return sum
    def duplicate(self,container,bestContainers):
        for individualContainer in bestContainers:
            # if the two containers section and container names are the same then they are a duplicate
            if(container.cName == individualContainer.cName and container.sName == individualContainer.sName):
                return True
        return False
    
    def corresponding(self,container,tank): 
        for correspondingTanks in container.correspondingTanks:
            if(len(container.correspondingTanks)!= 1):
                    if(correspondingTanks.tName == tank.tName):
                        return True
                    else:
                        continue
            else:
                if(correspondingTanks.tName == tank.tName):
                    return True 
                else:
                    continue
        return False
    
    
    
    def findBestCombinationContainersForTanks(self,containers,tanks,action):

        bestContainers = []
        # array containing all corresponding containers for the tanks
        useableContainers = []
        for tank in tanks:
            for container in containers:
                # if this container corresponds to at least one tank we can use it
                if(self.corresponding(container,tank) == True):
                    if(self.duplicate(container,useableContainers) ==False):
                        useableContainers.append(container)
        print("These are all the useable containers")
        for container in useableContainers:
            print(container.cName, container.sName)
        # if there is only 1 in the arr then use this container if it is corresponding
        if len(containers) == 1:
            for tank in tanks:
                for container in useableContainers:
                    if(self.corresponding(container,tank) == True):
                        bestContainers.append(container)
                        return bestContainers
                    else:
                        print("No corresponding containers to charge tank")
            
        for tank in tanks:
            # will be used to see if we found any containers and so return them
            found = False
            for container in useableContainers:
                # if this container can fully charge this tank use it
                if(action == 0):
                    if(container.charge >= tank.remainingCapacity()):# an individual container can charge this tank
                        # add this if it can charge this tank
                        if(self.corresponding(container,tank) == True and self.duplicate(container,bestContainers) == False):# this container can charge this tank
                            found = True
                            bestContainers.append(container)
                            break
                elif(action == 1):# negative case 
                    if(container.charge >= tank.currentChargedCapacity() and self.duplicate(container,bestContainers) == False):
                        if(self.corresponding(container,tank)== True):
                            found = True 
                            bestContainers.append(container)
                            break
            # going through and cheking if all tanks have a corresponding contianer

        for tank in tanks:
                    
                    for container in bestContainers:
                        if(self.corresponding(container,tank) == True):

                            found = True
                            break
                        else:
                            found = False
                            continue
                    if(found == False):# if we reach here and found == false then get out of tanks
                        break
       
        if(found == False):
                # now we want to get all combinations of best containers
                length = len(useableContainers)
                combos = []
                # combinations that meet the charge requirements
            
                minimumCombination = []
                for i in range(2, length + 1):
                    combos.extend(combinations(useableContainers,i))
                # now we get the sums of each of the combos and place them in useable combos
                # if they are greater than the sum of the tanks remainingCapcity
                for tank in tanks:
                    useableCombos = []
                    for tuple in combos:
                        sum = 0
                        for container in tuple:
                            if(self.corresponding(container,tank) == True):   
                                sum = sum + container.charge
                        if(action == 0):
                            if(sum >= tank.remainingCapacity()):
                                # this cobonation is useable
                                useableCombos.append(tuple)
                        elif(action == 1):
                            if(sum >= tank.currentChargedCapacity()):
                                # this cobonation is useable
                                useableCombos.append(tuple)
                    # get the min of useable combos for each tank

                        
                    # if there is only one tuple then just use this as minimum
                    if(len(useableCombos) != 0):
                        minimumCombination.append( min(useableCombos, key=self.tupleSum))
                    else:
                        minimumCombination.append(useableCombos)
                # now go through the remaining tuples and extract their containers
                print("going thorugh minComb before getting rid of anything")

                for tuple in minimumCombination:
                    for container in tuple:
                        # only add them if they are not a duplicate
                        if(self.duplicate(container,bestContainers) == False):
                            bestContainers.append(container)

        # if we have reached this point and no combination of containers are satisfactory use all containers
        if len(bestContainers) == 0:
            bestContainers = useableContainers
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
        print("WE are in here")
        full = False
        empty = False
        if(action == 0): # checking if full
            # going through all contianers to see if they are able to continue charging this cycle
            for container in containers:
                print("COntainer start")
                # only check the corresponding tanks
                for cTank in container.correspondingTanks:
                    if(cTank.tName == tank.tName):
                        print(container.cName , "has a corresponding tank")
                        if container.remainingCharge == 0: # cannot charge more this step
                            continue
                        if(container.remainingCharge != 0):# at least one container is not emtpy
                            full = False
                            print("this container is not emtpy and can charge")
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

                
                