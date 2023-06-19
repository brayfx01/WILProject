
from RoundTripEfficency import roundTripEffiency as RTE
class energyHandler:
    def __init__(self, energy,tanks):
        # all this does is dtermine if we need to store the energy or take energy
        if(energy >= 0):
            self.energyManagement(energy, 0,tanks)
        elif(energy < 0):
            self.energyManagement(energy, 1,tanks)
    # we will start with these taking 1 minute each to do a run
    def energyManagement(self, energy, action,tanks):
        if(action == 0): # this means we are storing 
            # we want to get the remaining storage potential 
            tank = self.optimalTank(tanks, 0)
            # Storage process
            while(energy != 0):
                #get the best tank to store the energy in
                tank = self.optimalTank(tanks, 0)
                # store the energy and set the new energy to the remainder
                energy = self.storeEnergy(tank,energy,0)
                # if 0 is remainer then we end
            print("Store Energy")
        elif(action == 1): # this means we need to expend energy
            while(energy != 0):
                tank = self.optimalTank(tanks,1)
                
                # we use ABS as energy should be negative
                energy = self.storeEnergy(tank,energy,1)
                print("Take Energy")
   
    def optimalTank(self,tanks, action):
        optimalTanks = None 
        for i in range(len(tanks)):
            if(i == 0): # by default just choose the first tank as best 
                optimalTank = tanks[i]
                continue
                 # as they all have the same capacity we can find wich has the lowest current SOC
            if(action == 0):
                if(tanks[i].currentChargedCapacity() < optimalTank.currentChargedCapacity()):
                        optimalTank = tanks[i]
            elif(action == 1):
                if(tanks[i].currentChargedCapacity() > optimalTank.currentChargedCapacity()):
                    optimalTank = tanks[i]
        return optimalTank

      
    def storeEnergy(self,tank,energy,action):
        #we are going to charge the battery by energy
        # we are going to get the total volume 
        # get the SOC 
        # get add the energy to this ratio 
        # then get new SOC 
        if(action == 0):
            print("Beggining")
            if(RTE(energy, 85).remaining > tank.remainingCapacity()):
                print("This is the starting energy", energy)
                print(RTE(energy,85).remaining)
                print(tank.remainingCapacity())
                energy = RTE(energy, 85).remaining  - tank.remainingCapacity()
                print("This is the remaining Energy", energy)
                tank.soc = 1  # this means full charge
                return energy
            elif(RTE(energy, 85).remaining < tank.remainingCapacity()):# means we can store all energy in this tank
                soc = (tank.currentChargedCapacity() + RTE(energy,85).remaining)/tank.volume
                soc = soc 
                tank.soc = soc # this updates the new charged capacity
                energy = 0 
                return energy
        # expending energy
        if(action == 1):
            # We have enough charged energy to meet the demand
           if(abs(energy)  <= RTE(tank.currentChargedCapacity(), 85)):
               soc = (RTE(tank.currentChargedCapacity(),85) - abs(energy))/tank.volume # no charge left 
               tank.soc = soc
               energy = 0
               return energy
           #we do not have enough charged energy to meet the demand
           elif(abs(energy)>=  RTE(tank.currentChargedCapacity(),85)):
                energy = energy + RTE(tank.currentChargedCapacity(),85)
                tank.soc = 0
                return energy
          