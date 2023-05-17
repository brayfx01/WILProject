import numpy as np
""" Properties
    - Storage Capacity 
    - Current Capacity 
    - Number of Batteries
"""
class Battery:
    # Constructor
    def __init__(self, numBatteries, maxCapacity):
        self.numBatteries = numBatteries
        self.maxCapacity = maxCapacity
        self.currentCapacity = np.zeros(numBatteries, dtype=float)
    # this will take in the energy needed to be stored
    def storeEnergy(self, energy):
        for i in range(self.numBatteries):# cycling trhough the batteries
            if(energy == 0):# this will ensure a full cycle is not compeleted if there is no energy left to store
                return energy
            remainingCapacity = self.maxCapacity - self.currentCapacity[i] # get the remaining possible sotrage of the current battery
            if remainingCapacity >= energy: # can fit all the energy into the batterys
                self.currentCapacity[i] += energy
                energy = 0
                break
            else:#if there is not enough capcaity then
                self.currentCapacity[i] = self.maxCapacity # set to current to max
                # subtract the remaining cpacity from energy and go around
                energy -= remainingCapacity
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
