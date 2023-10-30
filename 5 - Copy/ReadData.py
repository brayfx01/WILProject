import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.dates import HourLocator, DateFormatter

class ReadData:
    def __init__(self):
        self.df = None
        self.dfTwo = None
        self.differnece = None
        self.generatedSurplus = []
    def read(self,generated,load):
        # getting access to the excell files
        self.df = pd.read_csv(generated)
        self.dfTwo = pd.read_csv(load)
        self.difference =self.df["Power(MW)"].subtract(self.dfTwo["total load forecast"]/1000,fill_value=0)
        # Drop rows with all NaN values
        self.difference = self.difference.dropna(how='all')
        # make an array to pass back the differences for use in the rest of the system
        self.generatedSurplus =self.difference.values
        
        # Convert 'LocalTime' column to datetime format
        self.df['LocalTime'] = pd.to_datetime(self.df['LocalTime'])
        # Drop rows with 'NaN' values in 'LocalTime' column
        self.df.dropna(subset=['LocalTime'], inplace=True)
        # Calculate the time of day within 24 hours
        self.df['TimeOfDay'] = self.df['LocalTime'].dt.hour + self.df['LocalTime'].dt.minute / 60


        # Plot the data
        plt.plot(self.df['TimeOfDay'], self.df['Power(MW)'])
        # Plot the data
        plt.plot(self.dfTwo['TimeOfDay'], self.dfTwo['total load forecast']/1000)
        plt.plot(self.df["TimeOfDay"],self.generatedSurplus)
        # Set labels and title
        plt.xlabel('Time of Day (24-hour range)')
        plt.ylabel('Power (MW)')
        plt.title('Power vs Time')

        # Set the x-axis tick positions and labels
        tick_positions = np.arange(1, 25)
        tick_labels = [str(i) for i in tick_positions]
        plt.xticks(tick_positions, tick_labels)

        # Display the plot
        #plt.show()
    def getGeneratedSurplus(self):
        return self.generatedSurplus

"""
#this resamples the data
dfTwo.set_index('time', inplace=True)
dfre = dfTwo.resample('5T').asfreq()
# Forward fill missing values
dfre.ffill(inplace=True)


# Reset the index
dfre.reset_index(inplace=True)
"""