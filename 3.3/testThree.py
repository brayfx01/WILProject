from itertools import combinations
# pass tanks as a parameter 
# for each tank create an array of their corresponding containers 
# then combo these and get the best ones 

# calculate the sum of the tuple
def tupleSum(containerArray):
    sum = 0
    for container in containerArray:
        sum = sum + container.charge

    return sum
def duplicate(container,bestContainers):
    for individualContainer in bestContainers:
        print(container.cName,container.sName,individualContainer.cName,individualContainer.sName)
        # if the two containers section and container names are the same then they are a duplicate
        if(container.cName == individualContainer.cName and container.sName == individualContainer.sName):
            return True
    return False
def find_combos(arr,tanks):
    bestContainers = []
    for tank in tanks:
       
        # will be used to see if we found any containers and so return them
        found = False
        for container in arr:
            if(container.charge >= tank.remainingCapacity()):# an individual container can charge this tank
                print("container cna fully charge")
                if(corresponding(container,tank) == True):# this container can charge this tank
                    found = True
                    bestContainers.append(container)
                    break
        if(found == False):
            print(tank.tName, "Before entering")
            correspondingContainers = getCorrespondingContainers(arr,tank)
            if(len(correspondingContainers) == 0):
                print("No corresponding tanks found")
            else:# we have some corresponding containers
                print("these are the corresponding containers found ")
                for container in correspondingContainers:
                    print(container.sName,container.cName)
                #now we are going to get their combination
                print("getting combination")
                # how many combination we can take
                length = len(correspondingContainers)
                # get a list of all combination of containers
                combos = list(combinations(arr, length))
                # will hold all the sums of the combinations
                sumArray = []
                # this holds the combinatino of containers that meet the remaining capacity requirement
                smallestCombination = []
                # for each tuple we will get their sums
                for tuple in combos:
                    sum = 0
                    currentSmallest = 0
                    for container in tuple:
                        sum = sum + container.charge
                    print(sum)
                    if(sum >= tank.remainingCapacity()):
                        sumArray.append(sum)
                        # add in this combination to the smallest combination
                        smallestCombination.append(tuple)
               
                smallestCombination =min(smallestCombination, key=tupleSum)
                # now we are going to go through our best containers array and append containers that are not already in there
                for container in smallestCombination:
                    #if this is true do not add this to container
                    if duplicate(container,bestContainers) == True:
                        continue
                    else:
                        bestContainers.append(container)
                # now go through the sumArray and grab the smallest meeting requriments
                # or perhapse anouther way is to only add the sums that are greater than the tanks remaining capacity
                        
                
                
        
    for container in bestContainers:
        print(container.cName, "BEst containers")
    return bestContainers


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
        
t1 = Tank("Tank 1", 10 , 0)
t2 = Tank("Tank 2", 10 , 0)
#t3 = Tank("Tank 3", 10 , 0)
dummy = []
dummy.append(t1)
dummy.append(t2)
section = "Section 1"
cont1 = container(section, "container 1", 1, 5,[t1] )
cont2 = container(section, "container 2", 1, 5,[t1,t2] )
cont3 = container(section, "Container 3",1,10,[t2])

array = []
tarray = []
tarray.append(t1)
tarray.append(t2)
#tarray.append(t2)
#tarray.append(t3)

array.append(cont1)
array.append(cont2)
array.append(cont3)
newArray = find_combos(array,tarray)


