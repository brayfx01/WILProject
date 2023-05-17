import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import array as arr
from dateutil import parser

from Batteries import Battery
from Difference import Difference

def main():
    # these are two data sets found to simulate the inputs
    path = 'Data/T1Day.csv'
    pathTwo = "Data/ExpectedDay.csv"
    # create a difference object and batteryArray 
    #difference will get the two paths and calculate the difference between the two enegeries provided 
    difference = Difference(path, pathTwo) 
    #Number of batteries and their capacity
    batteryArray = Battery(100, 2000)
    
    #isExist = os.path.exists(path)
    #isExistTwo = os.path.exists(pathTwo)
# calculates the difference
    differenceArray = difference.calculate()
    print(differenceArray)
    for i in range(differenceArray.size):
        if(differenceArray[i] > 0):# if positive then we need to store the enrgy
            differenceArray[i] = batteryArray.storeEnergy(differenceArray[i])

    for i in range(differenceArray.size):
        if(differenceArray[i] < 0):# if negative then we need to get the energy from storage
            differenceArray[i] = batteryArray.takeEnergy(differenceArray[i])
            
    print(differenceArray)

if __name__ == "__main__":
    main()
