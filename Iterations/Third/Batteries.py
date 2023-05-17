import numpy as np
""" Properties
    - Storage Capacity 
    - Current Capacity 
    - Number of Batteries
"""
class Battery:
    # Constructor
   # Constructor(sectinos will indicate which sectin of the wind farm, solar farm ect)
    def __init__(self, numBatteries, maxCapacity, sections):
        #we are creating an empty array of length sections that will hold in each element anouther array 
        # this is done so that each of these elements will represent a battery determined by their max batteries 
        # then for know the max capacity and current capacity can be set so 
        self.sections = np.empty(sections, dtype=object)
        self.numBatteries = numBatteries
        self.maxCapacity = maxCapacity
        self.currentCapacity = 0
        #this is just a dummy to test if my idea works 
        for i in range(self.sections.size):
            # essentially in this seciton we have the number of batteries ther max capacity of this cell and current capacity
            self.sections[i] = np.array([self.numBatteries, self.maxCapacity,self.currentCapacity],dtype=object)
            
            
    # this will take in the energy needed to be stored
    # this takes in as parameters the energy and the action 
    # the action will determine if the energy will be stored or taken
    def storedEnergy(self, energy, action):
        if(action == 0):
            for i in range(self.sections.size):# cycling trhough the batteries
                if(energy == 0):# this will ensure a full cycle is not compeleted if there is no energy left to store
                    return energy
                remainingCapacity = float(self.sections[i][1]) - float(self.sections[i][2]) # get the remaining possible sotrage of the current battery
                if remainingCapacity >= energy: # can fit all the energy into the batterys
                    self.sections[i][1] += energy
                    energy = 0
                    break
                else:#if there is not enough capcaity then
                    self.sections[i][1] = self.maxCapacity # set to current to max
                    # subtract the remaining cpacity from energy and go around
                    energy -= remainingCapacity
            return energy
        elif(action == 1):
            #sort the sectinos in terms of capacity in decending order
            sortedByCapacity = np.argsort(-1 * np.array([subarray[1] for subarray in self.sections]), kind='quicksort')
            sortedSections = self.sections[sortedByCapacity]
        for i in range(self.sections.size):
            if self.sections[i][1] >= abs(energy):# if there is more energy stored than needed then
                self.sections[i][1] += energy # energy should be negative in this situtation so it will subtract the energy from current capacity
                energy = 0 # set energy to 0 
                return energy
            else:# there is more energy than stored in the 
                energy += self.sections[i][1] # this will substract current capacity from energy
                self.sections[i][1] = 0# set current capacity to 0
        return energy

