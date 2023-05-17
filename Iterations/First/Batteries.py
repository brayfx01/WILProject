import numpy as np
""" Properties
    - Storage Capacity 
    - Current Capacity 
    - Number of Batteries
    - transfer rate both in and out
    - the section the batteries are associatd with
"""
class Battery:
    # Constructor(sectinos will indicate which sectin of the wind farm, solar farm ect)
    def __init__(self, numBatteries, maxCapacity, sections):
        #we are creating an empty array of length sections that will hold in each element anouther array 
        # this is done so that each of these elements will represent a battery determined by their max batteries 
        # then for know the max capacity and current capacity can be set so 
        self.sections = np.empty(sections, dtype=object)
        self.numBatteries = numBatteries
        self.maxCapacity = maxCapacity
        self.sections = np.array(sections)
        self.currentCapacity = np.zeros(numBatteries, dtype=float)
        #this is just a dummy to test if my idea works 
        for i in range(self.sections.size):
            # essentially in this seciton we have the number of batteries ther max capacity of this cell and current capacity
            self.sections[i] = np.array(self.numBatteries, self.maxCapacity,self.currentCapacity)
    # this will take in the energy needed to be stored
    # this takes in as parameters the energy and the action 
    # the action will determine if the energy will be stored or taken
    def storedEnergy(self, energy, action):
        if(action == 0):
            for i in range(self.sections.size):# cycling trhough the batteries
                if(energy == 0):# this will ensure a full cycle is not compeleted if there is no energy left to store
                    return energy
                remainingCapacity = self.sections[i][1] - self.sections[i][2] # get the remaining possible sotrage of the current battery
                if remainingCapacity >= energy: # can fit all the energy into the batterys
                    self.sections[i][2] += energy
                    energy = 0
                    break
                else:#if there is not enough capcaity then
                    self.sections[i][2] = self.maxCapacity # set to current to max
                    # subtract the remaining cpacity from energy and go around
                    energy -= remainingCapacity
            return energy
        elif(action == 1):
             sortBatteries = np.argsort(self.currentCapacity)[::-1] # this wills sort the batteries in decedning order in respect ot current Capacity
        for i in range(self.numBatteries):
            if self.currentCapacity[i] >= abs(energy):# if there is more energy stored than needed then
                self.currentCapacity[i] += energy # energy should be negative in this situtation so it will subtract the energy from current capacity
                energy = 0 # set energy to 0 
                return energy
            else:# there is more energy than stored in the 
                energy += self.currentCapacity[i] # this will substract current capacity from energy
                self.currentCapacity[i] = 0# set current capacity to 0
        return energy
    # wil cycle through the number of batteries
    def takeEnergy(self, energy):
        sortBatteries = np.argsort(self.currentCapacity)[::-1] # this wills sort the batteries in decedning order in respect ot current Capacity
        for i in range(self.numBatteries):
            if self.currentCapacity[i] >= abs(energy):# if there is more energy stored than needed then
                self.currentCapacity[i] += energy # energy should be negative in this situtation so it will subtract the energy from current capacity
                energy = 0 # set energy to 0 
                return energy
            else:# there is more energy than stored in the 
                energy += self.currentCapacity[i] # this will substract current capacity from energy
                self.currentCapacity[i] = 0# set current capacity to 0
        return energy
