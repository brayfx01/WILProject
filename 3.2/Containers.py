class container:
    def __init__(self, sName,cName,onOffEfficency,charge,correspondingTanks):
        self.cName = cName# contianer name
        self.sName = sName# Section Name
        self.charge = charge # how much it can charge in 5 minute
        self.remainingCharge = self.charge # used to determine how much in 5 minutes this has charged
        self.onOffEfficency = onOffEfficency/60 # it will be in minutes
        self.onOffStatus = False # false means off 
        self.correspondingTanks = correspondingTanks # an array of the container objects 
    def drain(self, charged):
        print(self.onOffEfficency)
        self.remaining = charged *( 1 - self.onOffEfficency)
        return self.remaining