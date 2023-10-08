import matplotlib.pyplot as plt

class GraphTanksChange:
    def __init__(self,data, difference):
        self.data = data
    def graph(self):
        data = self.data
        tankVolume = [entry[0] for entry in data]
        tankSoc = [entry[1] for entry in data]
        time = [entry[2] for entry in data]

        # Create a scatter plot or line plot
        plt.figure(figsize=(8, 6))
        #plt.plot(time, tankVolume, label='Tank Volume', marker='o')
        #plt.plot(time, tankSoc, label='TankSoc', marker='s')
        plt.xlabel('Time')
        plt.ylabel('SOC/VOLUME')
        plt.legend()
        plt.title('Plot of Volume And SOC over time')
        plt.grid(True)
     

