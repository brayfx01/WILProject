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
        # if the two containers section and container names are the same then they are a duplicate
        if(container.cName == individualContainer.cName and container.sName == individualContainer.sName):
            return True
    return False
def find_combos(arr,tanks,action):

    bestContainers = []
    # array containing all corresponding containers for the tanks
    useableContainers = []
    for tank in tanks:
        for container in arr:
            # if this container corresponds to at least one tank we can use it
            if(corresponding(container,tank) == True):
                if(duplicate(container,useableContainers) ==False):
                    useableContainers.append(container)
    # if there is only 1 in the arr then use this container if it is corresponding
    if len(array) == 1:
        for tank in tanks:
            for container in useableContainers:
                if(corresponding(container,tank) == True):
                    bestContainers.append(container)
                    return bestContainers
                else:
                    print("No corresponding containers to charge tank")
        
    for tank in tanks:
        # will be used to see if we found any containers and so return them
        found = False
        for container in useableContainers:
            # if this container can fully charge this tank use it
            if(action == 0):
                if(container.charge >= tank.remainingCapacity()):# an individual container can charge this tank
                    # add this if it can charge this tank
                    if(corresponding(container,tank) == True and duplicate(container,bestContainers) == False):# this container can charge this tank
                        found = True
                        bestContainers.append(container)
                        break
            elif(action == 1):# negative case 
                if(container.charge >= tank.currentChargedCapacity() and duplicate(container,bestContainers) == False):
                    print(tank.currentChargedCapacity())
                    if(corresponding(container,tank)== True):
                        found = True 
                        bestContainers.append(container)
                        break
        # going through and cheking if all tanks have a corresponding contianer
    for container in bestContainers:
        print(container.cName)
    for tank in tanks:
                
                for container in bestContainers:
                    if(corresponding(container,tank) == True):

                        found = True
                        break
                    else:
                        found = False
                        continue
                if(found == False):# if we reach here and found == false then get out of tanks
                    break
            
    if(found == False):

            # now we want to get all combinations of best containers
            length = len(useableContainers)
            combos = []
            # combinations that meet the charge requirements
          
            minimumCombination = []
            for i in range(2, length + 1):
                combos.extend(combinations(useableContainers,i))
            # now we get the sums of each of the combos and place them in useable combos
            # if they are greater than the sum of the tanks remainingCapcity
            for tank in tanks:
                useableCombos = []
                for tuple in combos:
                    sum = 0
                    for container in tuple:
                        if(corresponding(container,tank) == True):   
                            sum = sum + container.charge
                    if(action == 0):
                        if(sum >= tank.remainingCapacity()):
                            # this cobonation is useable
                            useableCombos.append(tuple)
                    elif(action == 1):
                        if(sum >= tank.currentChargedCapacity()):
                            # this cobonation is useable
                            useableCombos.append(tuple)
                # get the min of useable combos for each tank

                    
                # if there is only one tuple then just use this as minimum
                if(len(useableCombos) != 0):
                    minimumCombination.append( min(useableCombos, key=tupleSum))
                else:
                    minimumCombination.append(useableCombos)
            # now go through the remaining tuples and extract their containers
            print("going thorugh minComb before getting rid of anything")

            for tuple in minimumCombination:
                for container in tuple:
                    # only add them if they are not a duplicate
                    if(duplicate(container,bestContainers) == False):
                        bestContainers.append(container)

            
            # now we want to get the minimum such that all tanks have a corresponding container to them


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
t2 = Tank("Tank 2", 10 , 100)
t3 = Tank("Tank 3", 10 , 100)
dummy = []
dummy.append(t1)
dummy.append(t2)
dummy.append(t3)

section = "Section 1"
cont1 = container(section, "container 1", 1, 5,[t3] )


sectionTwo = "Section 2"
cont3 = container(sectionTwo, "Container 3",1,10,[t1])

SectionThree = "Section 3"
cont2 = container(SectionThree, "container 2", 1, 10,[t2] )
array = []
tarray = []
tarray.append(t1)
tarray.append(t2)
tarray.append(t3)
#tarray.append(t2)
#tarray.append(t3)

array.append(cont1)
array.append(cont2)
array.append(cont3)

newArray = find_combos(array,tarray,1)
print("This is best containers")
for container in newArray:
    print(container.cName)


