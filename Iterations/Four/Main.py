import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import array as arr
from dateutil import parser

from Batteries import Battery
from Difference import Difference
from Graph import Graph
#from Graph import Graph
def main():
    # these are two data sets found to simulate the inputs
    pathOne = 'Data/T1Day.csv'
    pathTwo = "Data/ExpectedDay.csv"
    # create a difference object and batteryArray 
    #difference will get the two paths and calculate the difference between the two enegeries provided 
    difference = Difference(pathOne, pathTwo) 
    #Number of batteries and their capacity an section they belong to 
    batteries = Battery(100, 2000,1)
    graph = Graph(pathOne, pathTwo)
    #isExist = os.path.exists(path)
    #isExistTwo = os.path.exists(pathTwo)
# calculates the difference
    generatedSurplus = difference.calculate()
    print(generatedSurplus)
    for i in range(generatedSurplus.size):
        if(generatedSurplus[i] > 0):# if positive then we need to store the enrgy
            # the storedEnegry Function will take in the energy as first parameter and second parameter dictates whether it stores or not
            # 0 means to store the energy 1 means to take the energy
            generatedSurplus[i] = batteries.storedEnergy(generatedSurplus[i], 0)

    for i in range(generatedSurplus.size):
        if(generatedSurplus[i] < 0):# if negative then we need to get the energy from storage
            generatedSurplus[i] = batteries.storedEnergy(generatedSurplus[i],1)
            
    print(generatedSurplus)
    graph.GraphGeneratedLoadAndDifference()

if __name__ == "__main__":
    main()
