class FullEmpty:
        def __init__(self,tanks):
            self.allFull = False
            self.allEmpty = False
            self.tanks = tanks  
        def checkIfAllFull(self):
            for tank in self.tanks:
                if(tank.soc == 1): #this tank is full so skip 
                    continue
                elif(tank.soc != 1): # this tank is not full so
                    return False

            return True # they are all full
        def checkIfAllEmpty(self):
            for tank in self.tanks:
                if(tank.soc == 0): #this tank is full so skip 
                    continue
                elif(tank.soc != 0): # this tank is not full so
                    self.allEmpty == False 
                    return(self.allFull)
        
            self.allEmpty = True # if we make it here then all tanks are full
            return self.allEmpty
        
# move this to energy handler