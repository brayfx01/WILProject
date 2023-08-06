from itertools import combinations
# pass tanks as a parameter 
# for each tank create an array of their corresponding containers 
# then combo these and get the best ones 

# calculate the sum of the tuple
def remainingSum(tanks):
    sum = 0
    for tank in tanks:
        sum = sum + tank.remainingCapacity()
    return sum
def currentChargedSum(tuples):
    print("IN HERE")
    sum = 0
    i =0
    for tank in tuples:
        print("this is tank", tank.tName)
        sum = sum + tank.currentChargedCapacity()
        print("SUM AFTER", sum)
        print("tank name",tank.tName) 
    i = i+1
    return sum
    
        
    
def duplicateTank(tank,bestTanks):
    for bTank in bestTanks:
       if(bTank.tName == tank.tName):
           return True
       else:
           continue
    return False
def find_combos(tanks, energy):
    bestTanks = []
    found = False
    for tank in tanks:
        # we want to go and find a tank that is suitable
        # first case there is a tank that can handle all the energy
        if(energy > 0):
            print("Positive energy", energy)
            if(tank.remainingCapacity() >= abs(energy)):
                print("Tank has more remaining Capacity to store", tank.remainingCapacity())
                found = True
                bestTanks.append(tank)
                break
        elif energy < 0: # negative energy 
            print("negative energy", energy)
            if(tank.currentChargedCapacity() >= abs(energy)):
                print("tank can fully charge",tank.tName, tank.currentChargedCapacity())
                found = True 
                bestTanks.append(tank)
                break
            
        # now there is no tank that can handle all the energy so we find the best combination
        # will be used to see if we found any containers and so return them
    if(found == False):
            length = len(tanks) # this will be the maxium length of the combinations
            print("length",length)
            combos = []
            # getting all the combination of tanks based on length
            for r in range(2, length + 1):  # Generating combinations of length 2 to length of items
                combos.extend(combinations(tanks, r))
            i = 0
            for tuple in combos:
                for tank in tuple:
                    print(tank.tName)
            # holds the sum of the tanks currentCharge
            sumArray = []
            #hold the combination of containers Meeting the requirements
            combinationsMeetingEnergy = []
            # the smallest possible combinatino that meets the requirements
            smallestCombination = []
            #going through each tuple to determine their charged value
            for tuple in combos:
                print("//////////////")
                sum = 0
                for tank in tuple:
                    print("Combinations", tank.tName)
                    if(energy >= 0): # negative energy
                        sum = sum + tank.remainingCapacity()
                    elif(energy < 0):# energy is negative
                        print("sum before", sum)
                        sum = sum + tank.currentChargedCapacity()
                        print("sum after", sum)
                #this tuple can handle the energy
                if(sum >= abs(energy)):
                    sumArray.append(sum)
                    #append this tuple
                    print("this tuple has made the cut")
                    combinationsMeetingEnergy.append(tuple)
                # now we get the smallestCOmbination in combinatinosMeeting
            if(len(combinationsMeetingEnergy) != 0):
                print("What is in best tank")
                for tank in bestTanks:
                    print("BEST")
                    print(tank.tName)
                for tuple in combinationsMeetingEnergy:
                    print("TUple")
                    for tuple in combinationsMeetingEnergy:
                        for tank in tuple:
                            print(tank.tName)
                    print("after")
                # getting the smallest combination from combinations that meet the energy requirement
                if(energy >= 0):
                    smallestCombination =  min(combinationsMeetingEnergy, key = remainingSum)
                elif(energy < 0):
                    smallestCombination =  min(combinationsMeetingEnergy, key = currentChargedSum)
                print("this is smallest")
                
                for tank in smallestCombination:
                    if(duplicateTank(tank,bestTanks) == True):
                        continue
                    else:
                        bestTanks.append(tank)
                    # now go through the sumArray and grab the smallest meeting requriments
                    # or perhapse anouther way is to only add the sums that are greater than the tanks remaining capacity
            else:
                bestTanks = tanks               
        # getting rid of duplicate 

                
        
    for tank in bestTanks:
        print("Tank in best")
        print(tank.tName)
    return bestTanks


# we are getting all the corresponding containers for a tank
def getCorrespondingContainers(containers, tank):
    correspondingContainers = []
    for container in containers:# getting individual container
        for correspondingTanks in container.correspondingTanks:# getting individual tank from list
            for cTank in correspondingTanks:
                if(cTank.tName == tank.tName):
                    correspondingContainers.append(container)
    return correspondingContainers
def corresponding(container,tank): 
    print(tank.tName)
    for correspondingTanks in container.correspondingTanks:
        for cTank in correspondingTanks:
            
            if(cTank.tName == tank.tName):
                return True
            else:
                continue
    return False
class container:
    def __init__(self, sName,cName,onOffEfficency,charge,correspondingTanks):
        self.cName = cName# contianer name
        self.sName = sName# Section Name
        self.charge = charge # how much it can charge in 5 minute
        self.remainingCharge = self.charge # used to determine how much in 5 minutes this has charged
        self.onOffEfficency = onOffEfficency/60 # it will be in minutes
        self.onOffStatus = False # false means off 
        self.correspondingTanks = []
        self.correspondingTanks.append(correspondingTanks) # an array of the container objects 
    def drain(self, charged):
        print(self.onOffEfficency)
        self.remaining = charged *( 1 - self.onOffEfficency)
        return self.remaining
    

class Tank:
    def __init__(self,tName,volume,soc):
        self.tName = tName
        self.volume = volume
        self.soc = (soc/100)  #makes this a percentage
        self.chargedCapacity = self.volume * self.soc
    #how much of the battery is charged
    def currentChargedCapacity(self):
        return self.chargedCapacity
    # how much is not chraged
    def remainingCapacity(self):
        remainingCapacity = self.volume - self.currentChargedCapacity()
        return remainingCapacity 
    # charges the tank based on the amount given
    def Charge(self,amount):
        self.chargedCapacity = self.chargedCapacity + amount
        self.soc = self.chargedCapacity/self.volume * 100 

    def drain(self,amount):
        self.chargedCapacity = self.chargedCapacity - abs(amount)
        self.soc = self.chargedCapacity/self.volume # update soc
        
t1 = Tank("Tank 1", 10 , 100)
t2 = Tank("Tank 2", 10 , 60)
t3 = Tank("Tank 3", 10 , 100)
t4 = Tank("Tank 4", 10, 60)
dummy = []
dummy.append(t1)
dummy.append(t2)
dummy.append(t3)
dummy.append(t4)

array = []
tarray = []
tarray.append(t1)
tarray.append(t2)
#tarray.append(t2)
#tarray.append(t3)
newArray = find_combos(dummy,5)



