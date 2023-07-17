
class Tank:
    def __init__(self,tName,volume,soc):
        self.tName = tName
        self.volume = volume
        self.soc = (soc/100)  #makes this a percentage
    #how much of the battery is charged
    def currentChargedCapacity(self):
        self.chargedCapacity = self.volume *(self.soc)
        return self.chargedCapacity
    # how much is not chraged
    def remainingCapacity(self):
        remainingCapacity = self.volume - self.currentChargedCapacity()
        return remainingCapacity 

