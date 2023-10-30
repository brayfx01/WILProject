from Tank import Tank
from FullEmpty import FullEmpty
import math
class OptimalTanks():
    # the premsise of this is to divide the energy we need 
    # by the amount of tanks max or min volumes 
    # anc continue doing this untill we meet the energy
    def __init__(self,maxVolume,minVolume, maxSoc,minSoc, arrayOfEnergy ,RTE,target,containerMaxCharge,containerOnOffEfficency):
        self.maxVolume = maxVolume
        self.minVolume= minVolume
        self.maxSoc = maxSoc
        self.minSoc = minSoc
        self.RTE = RTE
        self.target = target
        self.containerMaxCharge = containerMaxCharge
        self.containerOnOffEfficency = containerOnOffEfficency

        self.energyArray = arrayOfEnergy
        self.energy = 0
        self.tankArray = []
        self.fullOrEmpty = FullEmpty(self.tankArray)
        # used to capture when a tank has expereinced change and what time it did
        self.currentTime = 0
        # will be used for getting the current Tank data for graphing
        self.tankChangeRecord = []
 
        # bassically the amount of positive energy we need to store to ensure 
        self.targetStorage = target
        #if true then we need not add any more tanks to accommidate 
        # for storing of energy 
        self.met = False
        
    def optimalTanks(self):
        # used to determine the Name of the tank
        tankCount = 0

        temporaryTankArray = []

       
        for energy in self.energyArray:
            
         
            # we are subtracting what we have left to store to balance out the drain
            if(energy > 0):
                if(self.target - energy >= 0): # if we have some left we store all of the enrgy
                    self.target -= energy
                else:# otherwise just store the remaining target
                    energy = self.target
                    self.target = 0
               # we do not need to store any more
            if(self.target <= 0 and energy > 0):
                continue
        
            totalDrainFromContainers = 0
          
        
            totalDrainFromContainers = math.ceil(abs(energy / self.containerMaxCharge)) * self.containerOnOffEfficency
   
            # set the this energy to abs of energy for ease of calculation
            # we also applied round trip effiecny 
            self.energy = energy/(self.RTE.efficency/100) - totalDrainFromContainers
          

             # this basically go thorugh and sees if a tank can satisfies the energy requirements
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
                       
                  
                        # this tank has some charge left
                        if(tank.remainingCapacity() > 0):
                            
                            # if the tank can meet energy demands
                            if(tank.remainingCapacity() >= abs(energy)):
                 
                                # keep reduicng our target if this is less or equal to 0 then 
                                # we do not need to charge or create more tanks
                                self.targetStorage = self.targetStorage - self.energy
                                
                                tank.Charge(abs(energy))
                                self.energy = 0
                                
                            
                                break
                            else:# Tank cannot meet energy demands 
                                # we need to add more
                             
                                self.targetStorage = self.targetStorage - tank.remainingCapacity()
                            
                                energy = energy - tank.remainingCapacity()
                                # set the charged Capacity of this tank to 100 or fully charged
                                tank.soc = 100
                                tank.chargedCapacity = self.maxVolume
                                
                                tankCount = tankCount + 1
                                tankName = "Tank: " + str(tankCount) 
                                newTank = Tank(tankName, self.maxVolume,self.minSoc)
                                self.tankArray.append(newTank)
                                
                                temporaryTankArray.append(Tank(newTank.tName,self.maxVolume,self.minSoc))
                              
                                self.targetStorage = self.targetStorage - newTank.remainingCapacity()
                                
                                continue
                        else:# if this tank is empty pass it
                            continue
                 
                    elif self.energy < 0:

                        # we can handle the energy with this tank
                        if(tank.currentChargedCapacity() >= abs(self.energy)):
                            tank.drain(abs( self.energy))
                          
                            self.energy = 0
                             # recording changes 
                        
                            break
                        # this tank cannot fully hanle energy requirements so use what it has
                        elif(tank.currentChargedCapacity() > 0 and tank.currentChargedCapacity() < abs(energy)):
                            self.energy =  self.energy + tank.currentChargedCapacity()
                            
                            for initialTank in self.tankArray:
                                if(initialTank.tName == tank.tName):
                                    initialTank.Charge(abs( self.energy))
                            #self.energy = 0 # we have charged the energy
             

                        else:# if this tank is empty pass it
                            continue
                # this is only for checking if the initial tanks 
                # can hold the energy
                
                #just checking our created tank if it can store
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
                                tank.Charge(tank.remainingCapacity())
                  
            # if energy is 0 the move on 
            if  self.energy == 0:
                continue
            
            # energy is negative
            if( self.energy < 0):
              
                # make this positive for ease of calculation
                self.energy = abs(self.energy)
                while self.energy != 0:
                    
                   
                    # energy greater than the maxVlume of the tank
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
                                    tank.Charge(abs(self.energy))
                                   

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
                           
   
        return self.tankArray

