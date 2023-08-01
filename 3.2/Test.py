def bestCombinationTanks(tanks, energy,action):
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

class Tank:
    def __init__(self,tName,volume,soc):
        self.tName = tName
        self.volume = volume
        self.soc = (soc/100)  #makes this a percentage
        self.chargedCapacity = self.volume * self.soc
    def remainingCapacity(self):
        remainingCapacity = self.volume - self.currentChargedCapacity()
        return remainingCapacity 
    def currentChargedCapacity(self):
        return self.chargedCapacity
t1 = Tank("Tank 1", 10 , 0)
t2 = Tank("Tank 2", 10 , 0)

array = []
array.append(t1)
array.append(t2)
for tank in array:
    if(tank.tName == "Tank 2"):
        array.remove(tank) 
for tank in array:
    print(tank.tName)