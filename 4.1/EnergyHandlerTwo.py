
from RoundTripEfficency import roundTripEffiency as RTE
from FullEmpty import FullEmpty
from queue import Queue
from itertools import combinations


class energyHandlerTwo:
    def __init__(self, RTE, cells):
        self.RTE = RTE
        self.checkTanksStatus = None
        self.cells = cells
        self.step = 5  # five minutes

        # these are uesd to record the changes of tank
        # and ocntainer
        self.containerChange = []
        self.tankChange = []
        self.currentEnergy = []

        self.currentTime = 0
          # calculate the sum of the tuple
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

                
                
    
    
          
    def duplicate(self,container,bestContainers):
        for individualContainer in bestContainers:
            # if the two containers section and container names are the same then they are a duplicate
            if(container.cName == individualContainer.cName and container.sName == individualContainer.sName):
                return True
        return False
    def tupleSum(self,containerArray):
        sum = 0
        for container in containerArray:
            sum = sum + container.charge

        return sum       
    def correspondingContainer(self,tank,container):
        for correspondingTank in container.correspondingTanks:
            if(correspondingTank.tName == tank.tName):
                return True
        return False    
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
                   
    # the drain
    def duplicateTank(self,tank,bestTanks):
        for bTank in bestTanks:
            if(bTank.tName == tank.tName):
                return True
            else:
                continue
        return False
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
    def findBestCombinationTanks(self, tanks, energy):
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
            elif energy < 0:  # negative energy
                if(tank.currentChargedCapacity() >= abs(energy)):
                    found = True
                    bestTanks.append(tank)
                    break

            # now there is no tank that can handle all the energy so we find the best combination
            # will be used to see if we found any containers and so return them
        if(found == False):
            # this will be the maxium length of the combinations
            length = len(tanks)
            combos = []
            # getting all the combination of tanks based on length
            # Generating combinations of length 2 to length of items
            for r in range(2, length + 1):
                combos.extend(combinations(tanks, r))
            # holds the sum of the tanks currentCharge
            sumArray = []
            # hold the combination of containers Meeting the requirements
            combinationsMeetingEnergy = []
            # the smallest possible combinatino that meets the requirements
            smallestCombination = []
            # going through each tuple to determine their charged value
            for tuple in combos:
                sum = 0
                for tank in tuple:
                    if(energy >= 0):  # negative energy
                        sum = sum + tank.remainingCapacity()
                    elif(energy < 0):  # energy is negative
                        sum = sum + tank.currentChargedCapacity()
                # this tuple can handle the energy
                if(sum >= abs(energy)):
                    sumArray.append(sum)
                    # append this tuple
                    combinationsMeetingEnergy.append(tuple)
                # now we get the smallestCOmbination in combinatinosMeeting
            if(len(combinationsMeetingEnergy) != 0):
                # getting the smallest combination from combinations that meet the energy requirement
                if(energy >= 0):
                    smallestCombination = min(
                        combinationsMeetingEnergy, key=self.remainingSum)
                elif(energy < 0):
                    smallestCombination = min(
                        combinationsMeetingEnergy, key=self.currentChargedSum)

                for tank in smallestCombination:
                    if(self.duplicateTank(tank, bestTanks) == True):
                        continue
                    else:
                        bestTanks.append(tank)
                    # now go through the sumArray and grab the smallest meeting requriments
                    # or perhapse anouther way is to only add the sums that are greater than the tanks remaining capacity
            else:
                bestTanks = tanks
            # getting rid of duplicate

        return bestTanks

    def findBestCombinationContainersForTanks(self, containers, tanks, action):

        bestContainers = []
        # array containing all corresponding containers for the tanks
        useableContainers = []
        for tank in tanks:
            for container in containers:
                # if this container corresponds to at least one tank we can use it
                if(self.corresponding(container, tank) == True):
                    if(self.duplicate(container, useableContainers) == False):
                        useableContainers.append(container)
        print("These are all the useable containers")
        for container in useableContainers:
            print(container.cName, container.sName)
        # if there is only 1 in the arr then use this container if it is corresponding
        if len(containers) == 1:
            for tank in tanks:
                for container in useableContainers:
                    if(self.corresponding(container, tank) == True):
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
                    # an individual container can charge this tank
                    if(container.charge >= tank.remainingCapacity()):
                        # add this if it can charge this tank
                        # this container can charge this tank
                        if(self.corresponding(container, tank) == True and self.duplicate(container, bestContainers) == False):
                            found = True
                            bestContainers.append(container)
                            break
                elif(action == 1):  # negative case
                    if(container.charge >= tank.currentChargedCapacity() and self.duplicate(container, bestContainers) == False):
                        if(self.corresponding(container, tank) == True):
                            found = True
                            bestContainers.append(container)
                            break
            # going through and cheking if all tanks have a corresponding contianer

        for tank in tanks:

            for container in bestContainers:
                if(self.corresponding(container, tank) == True):

                    found = True
                    break
                else:
                    found = False
                    continue
            if(found == False):  # if we reach here and found == false then get out of tanks
                break

        if(found == False):
            # now we want to get all combinations of best containers
            length = len(useableContainers)
            combos = []
            # combinations that meet the charge requirements

            minimumCombination = []
            for i in range(2, length + 1):
                combos.extend(combinations(useableContainers, i))
            # now we get the sums of each of the combos and place them in useable combos
            # if they are greater than the sum of the tanks remainingCapcity
            for tank in tanks:
                useableCombos = []
                for tuple in combos:
                    sum = 0
                    for container in tuple:
                        if(self.corresponding(container, tank) == True):
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
                    minimumCombination.append(
                        min(useableCombos, key=self.tupleSum))
                else:
                    minimumCombination.append(useableCombos)
            # now go through the remaining tuples and extract their containers
            print("going thorugh minComb before getting rid of anything")

            for tuple in minimumCombination:
                for container in tuple:
                    # only add them if they are not a duplicate
                    if(self.duplicate(container, bestContainers) == False):
                        bestContainers.append(container)

        # if we have reached this point and no combination of containers are satisfactory use all containers
        if len(bestContainers) == 0:
            bestContainers = useableContainers
        return bestContainers

    def storeEnergy(self, energy, tanks, containers, fullEmptyCheck):
        finish = False
        charge = False
        drain = False
        # if all container remainin charge have no charge
        if(self.containerRemainingCharge(containers, tanks, 0) == True and energy != 0):
            # drain
            self.drain(containers, tanks)
            print("we have an issue save it and drain")

        if energy >= 0:
            charge = True
        elif energy < 0:
            drain = True
            # make this positive for ease of computing
            energy = abs(energy)
            # going through containers

            # just gets out of the double loop if we are done
            # and the tanks
            for tank in tanks:
                # are all tanks full
                
                if(fullEmptyCheck.checkIfAllFull(tanks) == True and charge == True or fullEmptyCheck.checkIfAllFull(tanks) == True and drain == True):
                    # nothing we can do
                    # save move on
                    self.drain(containers, tanks)
                    finish = True
                    # we want to save the current tanks and container parameters
                    # along with the energy
                    self.containerChange.append(
                        [container.remainingCharge, self.currentTime])
                    self.tankChange.append(
                        [tank.currentChargedCapacity(), tank.soc, self.currentTime])
                    self.currentEnergy.append([energy, self.currentTime])
                    self.currentTime += self.step
                    break
                # tank can store all of energy
                if(tank.remainingCapacity() >= energy):
                    # going through the containers again to use them
                    for container in containers:
                        if(energy == 0):
                            # we can exit
                            self.drain(containers, tanks)
                            finish = True
                            self.containerChange.append(
                                [container.remainingCharge, self.currentTime])
                            self.tankChange.append(
                                [tank.currentChargedCapacity(), tank.soc, self.currentTime])
                            self.currentEnergy.append(
                                [energy, self.currentTime])
                            # increment the current time by step
                            self.currentTime += self.step
                            # move to the next tank if we cannot charge or drain when we need to
                        elif(tank.remainingCapacity() == 0 and charge == True or tank.soc == 100 and drain == True):
                            break
                        # tank can hold all of energy
                        if tank.remainingChargedCapacity() >= energy:
                            # this container cannot charge the tank
                            if(self.correspondingContainer(tank, container) == False):
                                # move on
                                continue
                            # this is the case the container can full charge the enrgy
                            if(container.remainingCharge >= energy):
                                # we can charge all with this container
                                if(charge == True):
                                    tank.charge(energy)
                                else:
                                    tank.drain(energy)
                                container.onOffStatus = True
                                container.remainingCharge = container.remainingCharge - energy
                                energy = 0
                                self.containerChange.append(
                                    [container.remainingCharge, self.currentTime])
                                self.tankChange.append(
                                    [tank.currentChargedCapacity(), tank.soc, self.currentTime])
                                self.currentEnergy.append(
                                    [energy, self.currentTime])
                                # increment the current time by step
                                self.currentTime += self.step
                            elif(container.remainingCharge < energy):
                                if container.remainingCharge == 0:
                                    continue
                                else:
                                    if charge == True:
                                        tank.Charge(container.remainingCharge)
                                    elif drain == True:
                                        tank.drain(container.remainingCharge)
                                    container.onOffStatus = True
                                    energy = energy - container.remainingCharge
                                    container.remainingCharge = 0
                                    self.containerChange.append(
                                        0, self.currentTime)
                        elif(tank.remainingCapacity() < energy):  # need to use multiple tanks
                            for container in containers:
                                if(self.correspondingContainer(tank, container) == False):
                                    continue
                                # means this container can meet energy requirements but not the tank
                                if(container.remainignCharge >= tank.currentChargedCapacity()):
                                    energy = energy - tank.currentChargedCapacity()
                                    container.onOffStatus = True
                                    container.remainingCharge = container.remainingCharge - tank.currentChargedCapacity()
                                    if(charge == True):
                                        tank.Charge(tank.remainingCapacity())
                                    elif(drain == True):
                                        tank.drain(tank.currentChargedCapacity())
                                    # recording the tank
                                    self.tankChange.append(
                                        [0, 0, self.currentTime])
                                elif(container.remainingCharge <= tank.remainingCapacity() and charge == True or
                                     container.remainingCharge < tank.currentChargedCapacity() and tank.currentChargedCapacity() !=0 ):
                                    energy = energy - container.remainingCharge
                                    container.onOffStatus = True
                                    if(charge == True):
                                        tank.charge(container.remainingCharge)
                                    elif(drain== True):
                                        tank.drain(container.remainingCharge)
                                    container.remainingCharge = 0
        return energy        

    def energyManagement(self, energyArray, tanks, tanksSocStatus):
        self.checkTanksStatus = FullEmpty(tanks)
        containers = []
        # just getting the containers from the sections
        for section in self.cells:
            for container in section.containers:
                containers.append(container)
        # going through each element of the energy array
        for energy in energyArray:
            while(energy != 0):
                if energy > 0:
                    # find best combination of tanks
                    tank = self.bestCombinationTanks(tanks, energy, 0)
                    # just use all of them if there are no optimal ones
                    if(tank == None):
                        tank = tanks
                    # getting the best combination
                    bestCombinationContainers = self.bestCombinationContainers(
                        energy, containers)
                    if bestCombinationContainers == None:
                        bestCombinationContainers = containers

                    # Store
                    # apply theh RTE efficecny here to the energy only for storing
                    energy = self.storeEnergy(self.RTE.RTE(
                        energy), tank, containers, tanksSocStatus)

                    # make sure to drain the tanks
                    if(energy == 0):
                        #
                        self.drain(containers, tanks)
                elif(energy < 0):  # now the draining of the tank
                    # find best combination of tanks
                    tank = self.bestCombinationTanks(tanks, energy, 1)
                    # just use all of them if there are no optimal ones
                    if(tank == None):
                        tank = tanks
                    # getting the best combination
                    bestCombinationContainers = self.bestCombinationContainers(
                        energy, containers)
                    if bestCombinationContainers == None:
                        bestCombinationContainers = containers

                    # Store
                    # apply theh RTE efficecny here to the energy only for storing
                    energy = self.storeEnergy(self.RTE.RTE(
                        energy), tank, containers, tanksSocStatus)

                    # make sure to drain the tanks
                    if(energy == 0):
                        self.drain(containers, tanks)
