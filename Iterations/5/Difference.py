import numpy as np
import pandas as pd

class Difference:
    def __init__(self, pathOne, pathTwo):
        self.pathOne = pathOne
        self.pathTwo = pathTwo
        
    def calculate(self):
        # create five batteries 
        # just setting up a data frame for the csv's
        df = pd.read_csv(self.pathOne)
        dft = pd.read_csv(self.pathTwo)
        # Convert the date/time column to a datetime object
        df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%d %m %Y %H:%M')
        # Extract the hour, minute, and second components of the data generated
        df['hour'] = df['Date/Time'].dt.hour
        df['minute'] = df['Date/Time'].dt.minute
        df['second'] = df['Date/Time'].dt.second

        # This will generate the hourly sum and put it into an array with the first entry denoting the firs hour
        hourlySumOfGenerated = df.groupby(df['Date/Time'].dt.hour)['LV ActivePower (kW)'].sum()
        # this converts the predicted output for the hourly load. No sum is required in this context as the hourly sum already taken
        hourlyLoad = dft['total load actual'].to_numpy()
        difference = np.zeros(24, dtype=float)
        # now just creating an array of their differences to be able to determine where we need to store and where we need to grab from
        for i in range(hourlySumOfGenerated.size):
            difference[i]  = hourlySumOfGenerated[i]-hourlyLoad[i]

        return difference
