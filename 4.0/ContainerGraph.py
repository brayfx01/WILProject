import matplotlib.pyplot as plt

class ContainerGraph:
    def __init__(self,data, difference):
        self.data = data
        self.difference = difference
    def graph(self):
        data = self.data
        ContCharg = [entry[0] for entry in data]
        Time = [entry[1] for entry in data]
        


        # Create a scatter plot or line plot
        plt.figure(figsize=(8, 6))
        plt.plot(Time, ContCharg, label='Tank Volume', marker='o')
    
        plt.xlabel('Time')
        plt.ylabel('ContCharge')
        plt.legend()
        plt.title('plot of cont charge over time')
        plt.grid(True)
        plt.show()

