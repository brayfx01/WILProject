
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
  