from Tank import Tank
from Containers import container
from FullEmpty import FullEmpty


class OptimalContainers():
    def __init__(self, maxCharge, minCharge, maxContainersPerSection, arrayOfEnergy, tanksArray,drain):

        self.maxCharge = maxCharge
        self.minCharge = minCharge
        self.maxPerSection = maxContainersPerSection
        self.energyArray = arrayOfEnergy
        self.energy = 0
        self.tankArray = tanksArray
        self.fullOrEmpty = FullEmpty(self.tankArray)
        self.empty = False
        self.drainLeftToMatch = False
        self.totalDrain = abs(drain)
        # used to record the changes of the contaiers over time
        self.currentTime = 0
        # container charge, time
        self.containerChangeData = []
        
    def duplicateTank(self, container, tank):
        for cTank in container.correspondingTanks:
            if(cTank.tName == tank.tName):
                # this means we found a duplicate
                return True
        # no duplicates
        return False

    
    # gets the remaining energy after using container
    def remainingEnergy(self, currentContainer, containerArray, tankCapacity, tank, drain, charge,num):
      

                                                          
        # if tank capacity == 0 then there is nothign we can do
        if len(containerArray )  >= 1 and tankCapacity != 0:
            for currentContainer in containerArray:
             
                if(currentContainer.remainingCharge == 0):
                    continue
                if(tankCapacity == 0 ):
                    break
              
                # if this container can fully charge the energy
                # and container charge <= tanksCapacity
               
                if(currentContainer.remainingCharge >= abs(self.energy)):
                       
                        if(tankCapacity >= abs(self.energy)):  # this means we are done
                         
                            # now we can reduce everything
                            # note we do not reduce containers charge as it will be set back to full imeediately after
                            if(drain == True):
                       
                                tank.drain(self.energy)
                                # update the tankCapacity
                                tankCapacity = tank.currentChargedCapacity()
                             
                      
                            elif(charge == True):
                                # we drain by energy

                                tank.Charge(self.energy)
                                tankCapacity = tank.remainingCapacity()

                            
                    
                            self.energy = 0
                            
                            #duplication protection
                            if(self.duplicateTank(currentContainer, tank) == False):
                                currentContainer.correspondingTanks.append(tank)
                        

                        elif(tankCapacity <= abs(self.energy)):
                       
                            # get the remaining energy
                     
                            self.energy = abs(
                                self.energy) - tankCapacity
                         
                            if(drain == True):
                                # this is empty
                                tank.drain(tank.currentChargedCapacity())
                                # set this back to negative for the next run
                                #self.energy = -self.energy
                                tankCapacity = tank.currentChargedCapacity()

                            elif(charge == True):
                               # self.totalDrain = self.totalDrain - tank.remainingChargeCapacity()
                                # the tank is full
                                tank.Charge(tank.remainingCapacity())
                                tankCapacity = tank.remainingCapacity()
                            # put a duplication check in here
                            if(self.duplicateTank(currentContainer, tank) == False):
                                currentContainer.correspondingTanks.append(tank)
                            #this tank is empty
                            self.empty = True
                       
                # we will need to use multiple containers
                
                elif(currentContainer.remainingCharge < abs(self.energy)):
        
                    # this tank can hold it all 
                    if(tankCapacity >= abs(self.energy)):

                        if(drain == True):
                            tank.drain(currentContainer.remainingCharge)
                            tankCapacity = tank.currentChargedCapacity()
                          
                        elif(charge == True):
                            
                            tank.Charge(currentContainer.remainingCharge)
                            tankCapacity = tank.remainingCapacity()
                        self.energy = abs(self.energy) - currentContainer.remainingCharge
                        # only if not a duplicate 
                        if(self.duplicateTank(currentContainer, tank) == False):
                            currentContainer.correspondingTanks.append(tank)
                        currentContainer.remainingCharge = 0    
                       
                    elif(tankCapacity < abs(self.energy)):
                    
                        # if our tank can hold all of the our containers remainingCharge
                        if(tankCapacity >= currentContainer.remainingCharge):
                            # calculate the remaining eneryg
                   
                            
                            self.energy = abs(
                                self.energy) - currentContainer.remainingCharge
                            
                            # charge or drain
                            if(drain == True):
                                tank.drain(currentContainer.remainingCharge)
                                tankCapacity = tank.currentChargedCapacity()
                           
                            elif(charge == True):
                                tank.Charge(currentContainer.remainingCharge)
                                tankCapacity = tank.remainingCapacity()
                            # IFF not duplicate
                            if(self.duplicateTank(currentContainer, tank) == False):
                                currentContainer.correspondingTanks.append(tank)
                            # set the remaining CHarge of this container to 0
                            currentContainer.remainingCharge = 0
                         
                        # tank is least
                        elif(tankCapacity <= currentContainer.charge):
                         
            
                            if(tankCapacity <= currentContainer.charge):
                            
                                self.energy = abs(self.energy) - tankCapacity
                                currentContainer.remainingCharge = currentContainer.remainingCharge - tankCapacity
                                if(drain == True):
                                    # tank is empty
                                    tank.drain(tankCapacity)
                                    tankCapacity = tank.currentChargedCapacity()
                             
                                elif(charge == True):
                                    # tank is full
                                    tank.Charge(tankCapacity)
                                    tankCapacity = tank.remainingCapacity()
                                    # IFF not duplicate
                         
                    
                                if(self.duplicateTank(currentContainer, tank) == False):
                                    currentContainer.correspondingTanks.append(tank)
                 
        
    def optimalContainers(self):
        
   
        tempTankArray = []
        # creating an popu.ating a temporary tank array so the original doe not become edited
        for tank in self.tankArray:
            tempTankArray.append(Tank(tank.tName,tank.volume,tank.soc))

        # if this is = maxContianersPerSection we increment currentSEction by 1
        # and set this back to 0
        maxContainers = 0
        # these will determine if we need to drain or charge the tanks
        charge = False
        drain = False

        # ussed to determine what section a container belongs to
        currentSection = 0
        # used for both charge and remaining
        tankCapacity = 0
        # this helps deal witth the case of containers
        # needing multiple tanks

        multipleConnections = False
        tanks = []
        # an array of all the containers that were created
        containerArray = []
       
        num = 0
        # do  we need to check corresponding tanks
        for energy in self.energyArray:
         
      
            # if we have a container in the array make 
            # sure to set the charge back to full whenever 
            # dealing with new energy
       
         
            self.energy = energy
        
           
            k = 0
            # if energy not zero then we are not done
            while(self.energy != 0):
           
                #resets all the containers remaining Charge
                if(len(containerArray) >= 1):
                    for cont in containerArray:
                        cont.remainingCharge = cont.charge
              
                   
                k += 1
                if(energy >0 and self.totalDrain <= 0):# no longer need to store positive energy
        
                    break
                
                # we are going to go through each tank
                # and coneect containers to them
                # we will keep connecting one container untill charge of container 0
                i = 0
                for tank in tempTankArray:
                    
             
             
                    if(self.energy == 0):
                        break
                 
                 
                    # this is going to get wether we need to
                    # use that tanks currentChared Capacity
                    # or the remaining Capacity
                    
                    # if negative then we want currentChargedCapacity()
                   
           
                       
                    if(energy < 0):
                       
                        drain = True
                        charge = False
                        tankCapacity = tank.currentChargedCapacity()
                      
              
                        # if the tank capacity is 0 then we have no charge so go to next tank
                  
                        if(tankCapacity == 0):
                            continue
                      
                        
                    else:  # if positive then we use the remaining capacity
                      
                        tankCapacity = tank.remainingCapacity()
                        # if the tankCapacity is 0 then this meanse we have no remaining Capacity so go to the next tank
                        # or if we do not need to store any more positive energy
                        if(tankCapacity == 0):
                            
                            continue
                         
                        # we do not need to store any more positive energy
                        elif(self.totalDrain <= 0):
                            # we no longer need to meet any draining requirements
                            # hence any new energy needing to be stored does not 
                            # require the creation of a new container
                            break
                        self.totalDrain -= energy
                        drain = False
                        charge = True
                  
                
                    # this gets the remaining energy after fully using a container to charge or drain
                    
                    #   currentContainer, containerArray, tankCapacity, drain , charge
             
                    self.energy = abs(self.energy)
                   
                    if(len(containerArray) >= 1):
                      
                 
                        self.remainingEnergy(
                            cont, containerArray, tankCapacity, tank, drain, charge,num)
                        # if after calcualtion tankCapacity is 0 go to the next tank
                        if(drain):
                            tankCapacity = tank.currentChargedCapacity()
                        else:
                            tankCapacity = tank.remainingCapacity()
                        i += 1
                     
                        # just break out after we have finished storing the last 
                        # positive enrgy we neeed
                        if(charge == True):
                            
                            if(self.totalDrain <=0):
                                break
                        if(tankCapacity == 0):
                            
                            continue
                            
                            
                        
                     
                        # go to next energy
                        # if energy 0 or this tank is empty or full
                        if(self.energy == 0 or self.empty == True):
                         
                            continue
 
                  
                
                    # this is determining if we need more containers
                    # gets the remaining energy
                    # if negative then we want currentChargedCapacity()
                    
                    # use energy as self.energy will be positive later on
                    if(energy <= 0):
                        tankCapacity = tank.currentChargedCapacity()
                        # if the tank capacity is 0 then we have no charge so go to next tank
                        if(tankCapacity == 0):
                            continue
                        
                        drain = True
                        
                    else:  # if positive then we use the remaining capacity
                        tankCapacity = tank.remainingCapacity()
                        # if the tankCapacity is 0 then this meanse we have no remaining Capacity so go to the next tank
                        if(tankCapacity == 0):
                            continue
                        charge = True
                    if(self.energy == 0):
                        # reset all the containers remaing
                        for cont in containerArray:
                            cont.remainingCharge = cont.charge
                            break
                    elif(drain == True and tank.currentChargedCapacity() == 0):
                       
                        # go to the next tank
                        continue
                    elif(charge == True and tank.remainingCapacity() == 0):
                       
                        continue

             

                    # we can handle all the energy
                    if(tankCapacity >= abs(self.energy)):
                  
                        # if the container the container can full charge
                        # create a container with max charge

                        # create a container with max charge
                        while(self.energy != 0  or (energy >0 and self.totalDrain > 0)):
                            
                          
                            # if it lies in the max and min
                            if(self.maxCharge >= abs(self.energy) and abs(energy) >= self.minCharge):
                             
                                # we need to create anouther section
                                if(maxContainers == self.maxPerSection):
                                    maxContainers = 0
                                    currentSection = currentSection + 1
                                maxContainers = maxContainers + 1

                                if(multipleConnections == False):
                                  
                                    # create a container with energy charge
                                    cont = container("Section: " + str(currentSection + 1), "Container: " + str(
                                        maxContainers), 85, abs(self.energy), [])
                                    containerArray.append(cont)
                                    
                                    
                                    if(self.duplicateTank(cont, tank) == False):

                                        # append this tank tot he corresponding tanks to the container
                                        cont.correspondingTanks.append(tank)
                                        
                            
                                    if(charge == True):
                                        # reduce the totalDrain 
                                        tank.Charge(self.energy)
                                    elif(drain == True):
                                      
                                        tank.drain(self.energy)
                                 
                                
                                   
                                    # set energy to 0
                                    self.energy = 0
                        

                                else: # charge by energy

                                    # append this new tank to the container
                                    if(self.duplicateTank(cont, tank) == False):
                                        cont.correspondingTanks.append(tank)
                                    multipleConnections = False
                                # set energy to 0 and append the container to the array

                                # charge this tank by energy then set energy to 0
                                if(charge == True):
                                    tank.Charge(self.energy)
                                    charge = False
                                elif(drain == True):
                                    tank.drain(self.energy)
                                 
                                    drain = False
                              
                                
                                self.energy = 0
                            # it is strictly less than maxCharge
                            elif(self.maxCharge >= abs(self.energy)):
                                  # do we need to create another section
                                if(maxContainers == self.maxPerSection):
                                    maxContainers = 0
                                    currentSection = currentSection + 1
                                maxContainers = maxContainers + 1
                                
                                if(multipleConnections == False):
                                  
                                    # create a container with maxCharge
                                    cont = container("Section: " + str(currentSection + 1), "Container: " + str(
                                        maxContainers), 85, self.maxCharge, [])
                                    containerArray.append(cont)
                                    self.containerChangeData.append([self.maxCharge, self.currentTime])
                                 
                                
                                    if(self.duplicateTank(cont, tank) == False):

                                        # append this tank tot he corresponding tanks to the container
                                        cont.correspondingTanks.append(tank)
                                        

                                    if(charge == True):
                                        # reduce the totalDrain 
                                        tank.Charge(self.energy)
                                    elif(drain == True):
                                        tank.drain(self.energy)
                                      

                                    
                                   
                                    # set energy to 0
                                    self.energy = 0
                               

                                else:

                                    # append this new tank to the container
                                    if(self.duplicateTank(cont, tank) == False):
                                        cont.correspondingTanks.append(tank)
                                    multipleConnections = False
                                # set energy to 0 and append the container to the array

                                # charge this tank by energy then set energy to 0
                                if(charge == True):
                                    tank.Charge(self.energy)
                                    charge = False
                                elif(drain == True):
                                    tank.drain(self.energy)
                            
                                    drain = False
                         
                                self.energy = 0
                            # next is if our max charge is less than the energy
                            elif(self.maxCharge <= abs(self.energy)):

                                # reduce this tank capacity
                                tankCapacity = tankCapacity - abs(self.maxCharge)

                                # now we are going to be adding multiple new containers

                                if(maxContainers == self.maxPerSection):
                                    maxContainers = 0  # set this back to 0
                                    currentSection = currentSection + 1  # go to the next section
                                maxContainers = maxContainers + 1
                                # add a container with max chareg
                                cont = container("Section: " + str(currentSection + 1), "Container: " + str(
                                    maxContainers), 85, self.maxCharge, [])
                                self.containerChangeData.append([self.maxCharge, self.currentTime])
                          
                                containerArray.append(cont)
                                # now we reduce energy by the max charge of the container

                                self.energy = abs(self.energy) - self.maxCharge
                                if(charge == True):
                                    tank.Charge(self.maxCharge)
                                elif(drain == True):
                                    tank.drain(self.maxCharge)
                            
                                if(self.duplicateTank(cont, tank) == False):
                                    cont.correspondingTanks.append(tank)

                    # this means we will need to go over multiple tanks
                    elif(tankCapacity < abs(self.energy)):

                        # this means if we created a container
                        # with max charge we could charge this tank fully or more

                        # bassically the same as for tankCap >= energy except
                        # energy is being reduced by the remaining of the tankCap
                       
                        if(self.maxCharge >= abs(self.energy)):

                            # we need to create anouther section
                            if((maxContainers+1) == self.maxPerSection):
                                maxContainers = 0
                                currentSection = currentSection + 1
                            maxContainers = maxContainers + 1

                            # create a container with energy charge

                            # changed the charge for this to be max so that
                            # if we only need on container
                            # it was self.energy

                            if(multipleConnections == False):
                                cont = container("Section: " + str(currentSection + 1), "Container: " + str(
                                    maxContainers), 85, abs(self.energy), tanks)
                                
                                self.containerChangeData.append([self.energy, self.currentTime])
                            
                            containerArray.append(cont)
                         
                            self.energy = abs(self.energy) - tankCapacity
                            # the remaining Charge of this Container
                            cont.remainingCharge = cont.remainingCharge - tankCapacity
                            self.containerChangeData.append([cont.remainingCharge, self.currentTime])
                  
                            # append this tnak to the container
                            cont.correspondingTanks.append(tank)
                            # this means we can use this container to charge anouther tank
                            multipleConnections = True

                        elif(self.maxCharge < abs(self.energy)):
                            # keep doing this until we are finished
                            while(tank.currentChargedCapacity() != 0 and drain == True or tank.remainingCapacity() != 0 and charge == True):

                                if(maxContainers == self.maxPerSection):
                                    maxContainers = 0  # set this back to 0
                                    currentSection = currentSection + 1  # go to the next section

                                maxContainers = maxContainers + 1

                                # add a container with max chareg
                                cont = container("Section: " + str(currentSection + 1), "Container: " + str(
                                    maxContainers), 85, self.maxCharge, tanks)
                                self.containerChangeData.append([self.maxCharge, self.currentTime])
                                # add this tank to the connection for the container
                                if(self.duplicateTank(cont, tank) == False):
                                    cont.correspondingTanks.append(tank)

                                containerArray.append(cont)
                                # now we reduce energy by the max charge of the container

                                # we also update the remaining Charge of this container
                                # to ensure that we do not reuse it to charge the rest of
                                # the energy
                                if(tankCapacity < self.maxCharge):
                                    self.energy = abs(
                                        self.energy) - tankCapacity
                                    cont.remainingCharge = cont.remainingCharge - tankCapacity
                                    
                                    # empty
                                    if(drain == True):
                                        tank.drain(tankCapacity)
                                        tankCapacity = 0
                                    # fully charged
                                    elif(charge == True):
                                        tank.Charge(tankCapacity)
                                        tankCapacity = 0
                                elif(tankCapacity >= self.maxCharge):
                                    tankCapacity = tankCapacity - self.maxCharge
                                    self.energy = abs(
                                        self.energy) - self.maxCharge
                                    cont.remainingCharge = 0
                                   
                                    if(drain == True):
                                        tank.drain(self.maxCharge)
                                    elif(charge == True):
                                        tank.Charge(self.maxCharge)

                                # this being false means we need to use anouther container
                                # to fulfill the energy requirements
                                multipleConnections = False
        return containerArray, self.containerChangeData
