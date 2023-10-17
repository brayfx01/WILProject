
from Tank import Tank
class GetTankData:
    def __init__(self, optimalTanks, difference):
        self.optimaltanks = optimalTanks
        self.difference = difference
    def calculateSocOverTime(self,socData, temporaryTanks):
        # what percentage from 0 to 100 is the system starting at
        currentSoc = 0
        totalSoc = 0
        totalEntries = 0
        # target is when to stop charging 
        target = 0
        for energy in self.difference:
            if energy < 0:
                target += energy
        target = abs(target)

        for tank in temporaryTanks:
            totalSoc += tank.soc
            totalEntries += 1
        # turning it into a percentage
        totalSoc = totalSoc/totalEntries * 100
        currentSoc = totalSoc
        print("original",totalSoc)
        # now recording the initial soc 
        socData.append(totalSoc)
        # when this changes so too does the soc of the entier system
        totalChargedVolume = 0
        for tank in temporaryTanks:
            totalChargedVolume += tank.currentChargedCapacity()
        
        currentChargedVolume = totalChargedVolume
    
        # now calculating the changes enegery does to it and saving it as a percentage of initial volume
        for energy in self.difference:
            if(energy < 0):# subtract the energy
                currentChargedVolume += energy
                # what is our current percentage
                percentage = (currentChargedVolume/totalChargedVolume)
                # now save this data 
                # finding the new percentage
                socData.append( totalSoc * percentage)
                currentSoc = totalSoc * percentage
            elif(energy > 0):
                if(target > 0):
                    target -= energy
                    currentChargedVolume += energy
                    percentage = (currentChargedVolume/totalChargedVolume)
                    socData.append( totalSoc * percentage)
                    currentSoc = totalSoc * percentage
                    # now save this data 
                else:
                    socData.append(currentSoc)
        return socData

    def calculateData(self):
        currentTime = 0
        # an array taking the name of the tanks and their energy
        temporaryTanks = []
        #recording the tanks data and how it changes
        tankRecord = []
        #recording the volume and SOC
        volume = []

        totalSocOverTime = []
        # this is when we stop chargin our tanks
        target = 0
        for energy in self.difference:
            if energy < 0:
                target += energy
        target = abs(target)

        totalVolume = 0
        # create a temporary array so the original does not get changed
        for tank in self.optimaltanks:
            temporaryTanks.append(Tank(tank.tName,tank.volume,tank.soc))
        # getting the total volume
        for tank in temporaryTanks:
            totalVolume += tank.currentChargedCapacity()
        # append this first one
        volume.append(totalVolume)

        totalSocOverTime = self.calculateSocOverTime(totalSocOverTime,temporaryTanks)
        # substracting and adding to energy and recording
        for energy in self.difference:
            if(energy < 0):# subtracting
             
                totalVolume = totalVolume + energy
                # record this change
                volume.append(totalVolume)
            else: #adding
                if(target > 0):
                    totalVolume = totalVolume + energy
                    # record this change
                    volume.append(totalVolume)
                    target -= energy
                else:
                    volume.append(totalVolume)

        target = 0
        for energy in self.difference:
            if energy < 0:
                target += energy
        target = abs(target)

        
        # now getting individual Tanks data       
        # setting all of their initial parametsers 
        for tank in temporaryTanks:
             tankRecord.append([tank.tName, tank.currentChargedCapacity(), (tank.currentChargedCapacity()/tank.volume) * 100 ,currentTime])
        for energy in self.difference:
            currentTime += 5

            for tank in temporaryTanks:
                #records this
                if(tank.currentChargedCapacity() == 0  and energy < 0 or tank.remainingCapacity() == 0  and energy > 0 or energy == 0): 
                    tankRecord.append([tank.tName, tank.currentChargedCapacity(), (tank.currentChargedCapacity()/tank.volume) * 100,currentTime])
                elif(energy < 0):# subtracting case
                    energy = abs(energy)
                    if(tank.currentChargedCapacity() >= energy):
                        tank.drain(energy)
                        # record this drain
                        tankRecord.append([tank.tName, tank.currentChargedCapacity(), (tank.currentChargedCapacity()/tank.volume) * 100,currentTime])
                        energy = 0
                    elif(tank.currentChargedCapacity() < energy):
                        energy = energy - tank.currentChargedCapacity()
                
                        # set this to 0 
                        tank.drain(tank.currentChargedCapacity())
                        tankRecord.append([tank.tName, tank.currentChargedCapacity(), (tank.currentChargedCapacity()/tank.volume) * 100,currentTime])
                        
                elif(energy > 0):# adding case
                    if(target > 0):
                        target -= energy
                        if(tank.remainingCapacity() >= energy):
                            tank.Charge(energy)
                    
                            # record this drain
                            tankRecord.append([tank.tName, tank.currentChargedCapacity(), (tank.currentChargedCapacity()/tank.volume) * 100,currentTime])
                            energy = 0
                        elif(tank.remainingCapacity() < energy):
                            energy = energy - tank.remainingCapacity()
                            # set this to 0 
                            tank.Charge(tank.remainingCapacity())
                            tankRecord.append([tank.tName, tank.currentChargedCapacity(), (tank.currentChargedCapacity()/tank.volume) * 100,currentTime])
                    else: # recrod the current data of each tank
                        tankRecord.append([tank.tName, tank.currentChargedCapacity(), (tank.currentChargedCapacity()/tank.volume) * 100,currentTime])    

        return volume, tankRecord, totalSocOverTime
        # now dealing with the SOC and individual Tanks