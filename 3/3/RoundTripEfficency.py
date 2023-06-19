class roundTripEffiency:
    def __init__(self,target,efficency):
        self.remaining = target *( efficency/100)
    def RTE(self):
        return self.target