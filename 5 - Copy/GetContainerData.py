from Tank import Tank
from Containers import container
class GetContainerData:
    def __init__(self, optimalContainers, optimalTanks,difference,RTE):
        self.optimalcontainers = optimalContainers
        self.optimaltanks = optimalTanks
        self.difference = difference
        self.RTE = RTE
    def calculateTotalData(self,totalChargeDataRecord,totalCharge,targetSum):
        # starting point
        totalChargeDataRecord.append(totalCharge)
        for energy in self.difference:
            if(energy > 0):
                targetSum  -= energy
                if(targetSum <= 0):
                    totalChargeDataRecord.append(totalCharge)
            elif(energy < 0):
                totalChargeDataRecord.append(totalCharge - abs(energy))
            elif targetSum > 0:
                totalChargeDataRecord.append(totalCharge - abs(energy))
          
        return totalChargeDataRecord
    def getData(self):
        temporaryContainerArray = []
        temporaryTanksArray = []
        containerDataRecord = []
        totalChargeDataRecord = []

        totalCharge = 0
       
        for cont in self.optimalcontainers:
            containerDataRecord.append([cont.sName,cont.cName,cont.remainingCharge])

        # the amount of positive charge we need to store to negate the negative
        targetSum = 0
        for energy in self.difference:
            if energy < 0 :
                targetSum += energy
        targetSum = abs(targetSum)
        for cont in self.optimalcontainers:
            totalCharge += cont.charge
        # go and caclulate the total change   
        totalChargeDataRecord = self.calculateTotalData(totalChargeDataRecord,totalCharge,targetSum)

        # creating a temporary array to hold everything 
        for cont in self.optimalcontainers:
            temporaryContainerArray.append(container(cont.sName,cont.cName,cont.onOffEfficency, cont.charge,cont.correspondingTanks))
        for tank in self.optimaltanks:
            temporaryTanksArray.append(Tank(tank.tName,tank.volume,tank.soc))
        # now we don't care how they interact for this just how they charge

        for energy in self.difference:
           
            charge = False
            drain = False

            if energy <0:
                drain = True
            elif(energy >0):
             
                charge = True
                targetSum = abs(targetSum) - energy
              
    
               # set them back to full and record them 
            for cont in temporaryContainerArray:
                cont.remainingCharge = cont.charge
                
              
            if(targetSum <= 0):
               
                for cont in temporaryContainerArray:
                    containerDataRecord.append([cont.sName,cont.cName,cont.remainingCharge])
                continue
                            

            energy = abs(energy/(self.RTE.efficency/100))
            for tank in temporaryTanksArray:
                  
                    # skip tanks that cannot be charged or drained when needed
                    if charge == True and tank.remainingCapacity() == 0:
                        continue
                    elif drain == True and tank.currentChargedCapacity() == 0:
                        continue

                        
                    # go to next energy if current is 0
               
                    if(energy == 0):
                        #containerDataRecord.append([cont.cName,cont.remainingCharge])
                        break
                    # this first condition if tank can hold everything
                
                    if(tank.currentChargedCapacity() >= energy and drain == True or tank.remainingCapacity() >= energy and charge == True):
                       
                        for cont in temporaryContainerArray:
                    
                            # if container can charge everything
                        
                            if(cont.remainingCharge >= energy):
                               
                                if(drain):
                                    tank.drain(energy)
                                else:
                                    tank.Charge(energy)

                                cont.remainingCharge = cont.remainingCharge - energy
                                energy = 0
                            
                                # record the change to the container
                                containerDataRecord.append([cont.sName,cont.cName,cont.remainingCharge])
                            # container cannot charge everything
                            elif(cont.remainingCharge < energy):
                                if(drain):
                                    tank.drain(cont.remainingCharge)
                                else:
                                    tank.Charge(cont.remainingCharge)
                                energy = energy - cont.remainingCharge

                                cont.remainingCharge = 0
                               
                                containerDataRecord.append([cont.sName,cont.cName,cont.remainingCharge])
                                
                    #tank cannot hold everytin
                    elif(tank.currentChargedCapacity() < energy and drain == True or tank.remainingCapacity() < energy and charge == True):

                            # if cont greater than verything 
                           
                            if(cont.remainingCharge >= energy or cont.remainingCharge >= tank.currentChargedCapacity() and drain == True or cont.remainingCharge >= tank.remainingCapacity() and charge == True):
                                if(drain):#drain what we have left
                                    energy = energy - tank.currentChargedCapacity()
                                   
                                    tank.drain(tank.currentChargedCapacity())
                                    cont.remainingCharge = cont.remainingCharge - tank.currentChargedCapacity()
                                   
                                    if energy == 0: # record the data of the container here 
                                         containerDataRecord.append([cont.sName,cont.cName,cont.remainingCharge])
                               
                                else:
                           
                                    # reduce energy by the remaining capacity 
                                    energy = energy - tank.remainingCapacity()
                                    # full charge the tank
                                    tank.Charge(tank.remainingCapacity())
                                    # how much remaining charge this contaienr has 
                                    cont.remainingCharge = cont.remainingCharge - tank.remainingCapacity()
                                 
                                    if energy == 0: # record our data here
                                         containerDataRecord.append([cont.sName,cont.cName,cont.remainingCharge])
                            
                                    
                                
                                
                            elif(cont.remainingCharge < energy):
                                if(drain):
                                    tank.drain(cont.remainingCharge)
                                else:
                                    tank.Charge(cont.remainingCharge)
                                energy = energy - cont.remainingCharge

                                cont.remainingCharge = 0
                             
                                containerDataRecord.append([cont.sName,cont.cName,cont.remainingCharge])
        
 
         

        return totalChargeDataRecord,containerDataRecord         