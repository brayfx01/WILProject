class roundTripEffiency:
    def __init__(self,efficency):
        self.efficency = efficency
    def RTE(self,target):
         self.remaining = target *( self.efficency/100)
         return self.remaining