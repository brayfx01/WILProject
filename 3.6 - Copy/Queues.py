
from queue import Queue
class Queues:
    def __init__(self):
        self.backlog = Queue()
        self.charge = Queue()
    def moveToBacklog(self,energy):
        self.backlog.put(energy)
      #add to charge
    def backlogEmpty(self):
        return(self.backlog.empty())
    def chargeEmpty(self):
        return(self.charge.empty())
    def moveToCharge(self):
        print(self.backlogEmpty())
        if(self.backlogEmpty() == False):
            self.charge.put(self.backlog.get())# put energy into this queue
   
