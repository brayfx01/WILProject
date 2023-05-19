import numpy as np
class Battery:
    def __init__(self, maxCapacity, currentCapacity):
        self.maxCapacity = maxCapacity
        self.currentCapacity = currentCapacity
    def allEmpty(self, sections):
        # Check if all batteries are empty
        totalBateries = sum(len(container) for section in sections for container in section)
        return totalBateries == self.empty_batteries

    def allFull(self, sections):
        # Check if all batteries are at maximum capacity
        totalBatteries = sum(len(container) for section in sections for container in section)
        return totalBatteries == self.full_batteries
    # these two will get the least and max cpacity currently in the entire system
    def currentLowestCapacity(self, sections):
            # Filter batteries with current capacity less than their max capacity
        filtered_batteries = [(battery.currentCapacity, i+1, j+1, k+1) for i, section in enumerate(sections) for j, container in enumerate(section) for k, battery in enumerate(container) if battery.currentCapacity < battery.maxCapacity]

        if len(filtered_batteries) == 0:
        # No batteries satisfy the condition
            return None

        # Find the battery with the lowest current capacity
        lowestBattery = min(filtered_batteries)
        return lowestBattery
    def currentHighestCapacity(self, sections):
        # Find the battery with the lowest current capacity across all sections and containers
        highestBattery = max((battery.currentCapacity, i+1, j+1, k+1) for i, section in enumerate(sections) for j, container in enumerate(section) for k, battery in enumerate(container))
        return highestBattery        
    # this will take in the energy needed to be stored
    # this takes in as parameters the energy and the action 
    # the action will determine if the energy will be stored or taken
    def storedEnergy(self,energy, action, sections):
        if(action == 0): # stroing energy
            # get the lowest cpacity, section, container and battery 
            # while there is energy left to store and non-full batteries
            i = 0
            while(energy != 0): 
                print("stuck in here", energy)
                #if there are no more to store in then there is an issue
                lowestBattery = self.currentLowestCapacity(sections)
                if lowestBattery is None:
                    print("Cannot store all energy")
                    for i in range(len(sections)):
                        print("Section ", i +1)
                        for k in range(len(sections[i])):
                            print("     Container ", k + 1)
                            for l in range(len(sections[i][k])):
                                print("         Battery " ,l + 1)
                                print("             CurrentCapacity ", sections[i][k][l].currentCapacity)
                                print("             CurrentCapacity ", sections[i][k][l].maxCapacity)
                                
                    return energy
                currentCapacity, sectionOfBattery, ContainerOfBattery, battery = lowestBattery
                
                print("current", currentCapacity, "section", sectionOfBattery, "container", ContainerOfBattery, "battery", battery) 
                i += 1
                print("this is i", i)
                remainingCapacity = sections[sectionOfBattery -1 ][ContainerOfBattery- 1][battery - 1].maxCapacity - sections[sectionOfBattery - 1][ContainerOfBattery - 1][battery - 1].currentCapacity 
                print("remaingingCap", remainingCapacity)    
                if(energy == 0):
                    return energy
                if(remainingCapacity >= energy) : # we can fit all in
                    sections[sectionOfBattery-1][ContainerOfBattery - 1][battery - 1].currentCapacity = sections[sectionOfBattery-1][ContainerOfBattery-1][battery -1].currentCapacity + energy
                    print("THis is in the >=", "current", currentCapacity, "section", sectionOfBattery, "container", ContainerOfBattery, "battery", battery) 
                    print( sections[sectionOfBattery-1][ContainerOfBattery - 1][battery - 1].currentCapacity)
                    energy = 0
                    return energy
                else:# we cannot and thus get the smallest one and set to max to represent this
                    print("else")
                    sections[sectionOfBattery-1][ContainerOfBattery-1][battery-1].currentCapacity = sections[sectionOfBattery -1][ContainerOfBattery -1][battery -1].maxCapacity
                    print("this is new capacity in else", sections[sectionOfBattery-1][ContainerOfBattery-1][battery-1].currentCapacity)
                    energy  -= remainingCapacity
            return energy
        elif(action == 1):    
               while(energy != 0): 
                   #this will get the highest capacity of the batteries over all the sections
                currentCapacity, sectionOfBattery, ContainerOfBattery, battery = self.currentHighestCapacity(sections)  # get the battey with the highest stored energy  
                if(currentCapacity == 0): # this means that all batteries are empty
                    return -1
                if(currentCapacity - energy >= 0 ) : # the highest capacity has more energy or equal energy than needed then
                    sections[sectionOfBattery- 1][ContainerOfBattery-1][battery-1].currentCapacity = sections[sectionOfBattery-1][ContainerOfBattery-1][battery-1].currentCapacity - energy
                    energy = 0
                    return energy
                else: # now there is more nergy needing to be taken then there is available in the largest Battery
                    energy  -= currentCapacity
                    sections[sectionOfBattery-1][ContainerOfBattery-1][battery-1].currentCapacity = 0 # this is minimum capacity
                    
        return energy 
            
    
    