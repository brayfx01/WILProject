from Tank import Tank
from FullEmpty import FullEmpty
class OptimalTanks():
    # the premsise of this is to divide the energy we need 
    # by the amount of tanks max or min volumes 
    # anc continue doing this untill we meet the energy
    def __init__(self,maxVolume,minVolume, maxSoc,minSoc, arrayOfEnergy ,RTE,target):
        self.maxVolume = maxVolume
        self.minVolume= minVolume
        self.maxSoc = maxSoc
        self.minSoc = minSoc
        self.RTE = RTE
        self.energyArray = arrayOfEnergy
        self.energy = 0
        self.tankArray = []
        self.fullOrEmpty = FullEmpty(self.tankArray)
        
        
        # bassically the amount of positive energy we need to store to ensure 
        # the next day will go smoothly
        self.targetStorage = target
        self.target = target
        #if true then we need not add any more tanks to accommidate 
        # for storing of energy 
        self.met = False
        
    def optimalTanks(self):
       
        # used to determine the tame of the tank
        tankCount = 0
        # this is needed as for the positive energy we 
        # want to know if we can fully store it all 
        # but we do not want to keep it 
        # so we use this to charge 
        # put only add to the original Tanks array
        temporaryTankArray = []
        #we need to crate a get remaining energy 
        # essentially we go through all current tanks 
        # with some remaining energy 
        # and then we subtract the energy from them 
        # if energy 0 we done else we continue
        
       
        for energy in self.energyArray:
            
            totalStorage = 0
            for tank in self.tankArray:
                # bassically add max volume to this 
                totalStorage = totalStorage + self.maxVolume
            # if this happens then if we need to add tank to store 
            # we do not need to do it 
            if totalStorage >= self.target:
                self.met = True
                print(energy)
       
        
           # print("ENERGY START", energy)

           
            # set the this energy to abs of energy for ease of calculation
            # we also applied round trip effiecny 
            self.energy = energy/(self.RTE.efficency/100)
          
            # if negative again then we see if one tank can still 
            #be charged enough to satisfy
         
            if(len(self.tankArray )) >= 1:
                
                # creating a temp array with temp objects
                if(len(temporaryTankArray) == 0):
                    for tank in self.tankArray:
                        #this is done so that temp array does not affect self.tanksArray
                        temporaryTankArray.append(Tank(tank.tName,tank.volume,tank.soc))
                for tank in temporaryTankArray:
                    #negatives
                   
                    
                    if(self.energy > 0 and self.met == False):
                        # we are done
                       
                        if(self.targetStorage <= 0):
                            break
                        # this tank has some charge left
                        if(tank.remainingCapacity() > 0):
                            
                            # if the tan can charge all of energy
                            if(tank.remainingCapacity() >= abs(energy)):
                 
                                # keep reduicng our target if this is less or equal to 0 then 
                                # we do not need to charge or create more tanks
                                self.targetStorage = self.targetStorage - self.energy
                                
                                tank.Charge(abs(energy))
                                self.energy = 0
                     
                                break
                            else:# we cannot so we need to add anouther tank in here for positve
                                print(self.targetStorage, "BEFORE")
                                self.targetStorage = self.targetStorage - tank.remainingCapacity()
                                print(self.targetStorage, "AFTER")
                                energy = energy - tank.remainingCapacity()
                                # set the charged Capacity of this tank to 100 or fully charged
                                tank.soc = 100
                                tank.chargedCapacity = self.maxVolume
                                
                                tankCount = tankCount + 1
                                tankName = "Tank: " + str(tankCount) 
                                newTank = Tank(tankName, self.maxVolume,self.minSoc)
                                self.tankArray.append(newTank)
                                
                                temporaryTankArray.append(Tank(newTank.tName,self.maxVolume,self.minSoc))
                                # also subtract this
                                self.targetStorage = self.targetStorage - newTank.remainingCapacity()
                                continue
                        else:# if this tank is empty pass it
                            continue
                 
                    elif self.energy < 0:
        
                         # can we charge the tank any more 
                         # if not then we need to add anouther tank
                            # we do not need to do anything but draing temporary tank
                       
                        if(tank.currentChargedCapacity() >= abs(self.energy)):
                            tank.drain(abs( self.energy))
                            self.energy = 0
                            break
                        # we do not have enough stored so drain what we can and charge the offcial one with what is left
                        elif(tank.currentChargedCapacity() > 0 and tank.currentChargedCapacity() < abs(energy)):
                            self.energy =  self.energy + tank.currentChargedCapacity()
                            
                            for initialTank in self.tankArray:
                                if(initialTank.tName == tank.tName):
                                    initialTank.Charge(abs( self.energy))
                            self.energy = 0 # we have charged the energy
                            
                            
                            
                        # alther this to work with the initial tanks instead of temporary tanks
                        # as we need to know if we have any remaining capacity to charge
                       
                        else:# if this tank is empty pass it
                            continue
                # this is only for checking if the initial tanks 
                # can hold the energy
                
                if self.energy != 0 and self.energy < 0:
                    for tank in self.tankArray:
                        if(tank.remainingCapacity() == 0):
                            continue

                    
                        # we have some space remaining to store
                        if tank.remainingCapacity() > 0:
                           
                            # we can charge and then leave
                            # we do not do anything to the temp tanks as we would just drain what we charged
                            if tank.remainingCapacity() >= abs(self.energy):
                                tank.Charge(abs(self.energy))
                                self.energy = 0 
                            else:
                                self.energy = self.energy +  tank.remainingCapacity()
                                # set this tank to full
                                tank.soc = 100
                                tank.chargedCapacity = self.maxVolume
                            
                                
         
            
            if  self.energy == 0:
                continue
            
            # energy is negative
            if( self.energy < 0):
              
                # make this positive
                self.energy = abs(self.energy)
                while self.energy != 0:
                    
                    # if energy > max Tank charge
                    # then we need to add a tank with the maximum charge
               
                    # if energy is greater than the maximum charge of the tank
                            
                    
                    if(self.energy > self.maxVolume * (self.maxSoc)/100):

                        self.energy = abs(self.energy)- (self.maxVolume * self.maxSoc)/100
                        tankCount = tankCount + 1
                        tankName = "Tank: " + str(tankCount) 
                        # we want to create a tank  with maxVolume and maxSoc
                        tank = Tank(tankName, self.maxVolume,self.maxSoc)
                        self.targetStorage =  self.targetStorage - (self.maxVolume * self.maxSoc)/100
                            
                        # add this tank to the array
                        self.tankArray.append(tank)
                        # this array will be manipulated on the above 
                        
                        #array will be returned to get the optimal containers
                        # however it will be 0 in charge as it is supposed to be drained
                        temporaryTankArray.append(Tank(tankName, self.maxVolume,0))
                        
                        
                        
                    # this means we do not need a fully charged tank
                    # so we want to find what ratio it is 
                    # then if this ratio falls between the two minSoc and Max Soc
                    elif(self.energy <=self.maxVolume):
                       
                        # add a tank with max SOC
                        
                        # if energy greater than what our tanks max SOC is 
                       
                        # is the energy required greater than the max charge of a tank
                        
                        if(self.energy >= (self.maxVolume * self.maxSoc)/100):
                            
                           
                            # getting the remaining Energy
                            self.energy = self.energy - (self.maxVolume * self.maxSoc)/100
                            tankCount = tankCount +1
                            tank = Tank("Tank: " + str(tankCount), self.maxVolume, self.maxSoc)
                            self.targetStorage =  self.targetStorage - (self.maxVolume * self.maxSoc)/100
                            
                            self.tankArray.append(tank)
                            
                            temporaryTankArray.append(Tank(tank.tName, self.maxVolume,0))
                            # add a tank with the ratio as the new SOC
                        # bassically the energy that we need is inbetween max and min
                     
                        elif(self.energy < self.maxVolume *self.maxSoc and self.energy >= self.maxVolume * self.minSoc):
                            
                            
                            tankCount = tankCount + 1
                            #create a tank with maxVolume and soc equal to energy
                            tankName = "Tank: " + str(tankCount)
                            #self.energy/self.maxVolume *100  is the SOC we need  
                            # e.g if self.energy is 10% of volume then this will put the SOC to 10 %
                            tank =Tank(tankName, self.maxVolume, (self.energy/self.maxVolume)*100)
                    
                            self.targetStorage = self.targetStorage - tank.remainingCapacity()
                            self.tankArray.append(tank)
                     
                            temporaryTankArray.append(Tank(tankName, self.maxVolume,0))
                            # bassically creating a tank with an soc equal to energy

                            self.energy = 0
                       
                                
                       
                       
                            # add a tank that is the least filled possible
                        # we add a tank with the minimum state of charge
                        elif(self.energy < self.maxVolume *self.minSoc):
                            
                            tankCount = tankCount +1
                            tankName = "Tank: " + str(tankCount)
                            # create a tank with the minimum charge possible
                            tank =Tank(tankName, self.maxVolume,self.minSoc)
                            self.targetStorage = self.targetStorage - tank.remainingCapacity()
                            self.tankArray.append(tank)
                            
                            temporaryTankArray.append(Tank(tankName, self.maxVolume,0))
                            
                            self.energy = 0
                    
            elif(energy > 0 and self.met == False):
               
                if(energy == 0):
                    # go to the next energy 
                    continue
                
                # check if we have tanks already
                # and see if we can fit the energy in with what we currently have
               
                if(len(self.tankArray )>= 1):
                    # if temp array has not been populized yte 
                    # add of of self.tankarray elements to it
                 
                    if(len(temporaryTankArray) == 0):
                        for tank in self.tankArray:
                            #this is done so that temp array does not affect self.tanksArray
                            temporaryTankArray.append(Tank(tank.tName,tank.volume,tank.soc))
                 
                
                    
                    while(self.energy!= 0):
                        # if true then all tanks are full;
                        # if this returns true then all are full 
                        # if it returns false then there is at least one tank not full
                        
                        # if we have met our target there is no need to keep adding tanks 
                        # to store more energy
                        if(self.targetStorage <= 0):
                            break
                        if(self.fullOrEmpty.checkIfAllFull(temporaryTankArray)== False):
                            
                            for tank in temporaryTankArray:
                              
                                # this is full so skip it
                                if(tank.remainingCapacity()  == 0):
                                    continue
                                    
                           
                                if(tank.remainingCapacity() >= self.energy):
                                    #if we can fit all of energy in this tank 
                                    # charge it by this amount
                                    
                                    # target is the total negative energy of the day that we need to store 
                                    # to ensure that we will be fine for tomorrow
                                    self.targetStorage = self.targetStorage - self.energy
                                    tank.Charge(self.energy)
                                   

                                    self.energy = 0
                                    
                                    break
                                    
                                elif(tank.remainingCapacity() < self.energy):
                                    # fit what we can
                                    self.targetStorage = self.targetStorage - tank.remainingCapacity()
                                    remaining = tank.remainingCapacity()
                                    tank.Charge(tank.remainingCapacity())
                                    self.energy = self.energy - remaining

                                         
                        else: # we are going to add in multiple tanks
                            # add a tank with the lowest possible charge
                            
                            self.targetStorage = self.targetStorage - self.maxVolume*self.minSoc
                            tankCount = tankCount + 1
                            tank = Tank("Tank: " + str(tankCount),self.maxVolume,self.minSoc)
                            # add this tank to the array
                            self.tankArray.append(tank)
                            temporaryTankArray.append(Tank(tank.tName,tank.volume,tank.soc))

  
        return tankCount,self.tankArray

# mCharge, minCharge, MaxSOC, MINSOC, energy  
""" 
energyArray =[-100,100]
tankArray = []

# maxVolume,minVoluem,maxSOC,minSOC,energyArray

optimal = OptimalTanks(1000,50,90,10,energyArray)
result,tankArray = optimal.optimalTanks()

for tank in tankArray:
    print(tank.tName)
    print(" ", tank.volume)
    print("     ", tank.soc, "this is soc")
    print("         ", tank.currentChargedCapacity())
quit()
print("NOW IF ALL ARE FULL WE ADD IN MORE TANKS")

print(result)
"""