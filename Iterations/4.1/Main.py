import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import array as arr
from dateutil import parser

from Difference import Difference
from Graph import Graph
from Battery import Battery
from SystemInitialization import SystemInitialization
# to do for tommorrow
#from Graph import Graph
def main():
    # Provide the path to your config file
    configFile = "config.txt"
    # these are two data sets found to simulate the inputs
    pathOne = 'Data/T1Day.csv'
    pathTwo = "Data/ExpectedDay.csv"
    
    # Create an instance of SystemInitialization
    system = SystemInitialization(configFile)

    # Access array using the getter method
    sections = system.Sections()
    battery = Battery(0,0)
    # create a difference object and batteryArray 
    #difference will get the two paths and calculate the difference between the two enegeries provided 
    difference = Difference(pathOne, pathTwo) 
    graph = Graph(pathOne, pathTwo)
# calculates the difference
    generatedSurplus = difference.calculate()
    print(generatedSurplus)
    for i in range(generatedSurplus.size):
        if(generatedSurplus[i] > 0):# if positive then we need to store the enrgy
            # the storedEnegry Function will take in the energy as first parameter and second parameter dictates whether it stores or not
            # 0 means to store the energy 1 means to take the energy
            # also takes in the sections array. This is where the batteries are stored
            generatedSurplus[i] = battery.storedEnergy(generatedSurplus[i], 0, sections)
            if(generatedSurplus[i] !=0):
                print("Not enough storage space")
                exit

    for i in range(generatedSurplus.size):
        if(generatedSurplus[i] < 0):# if negative then we need to get the energy from storage
            generatedSurplus[i] = battery.storedEnergy(abs(generatedSurplus[i]),1, sections)
        if(generatedSurplus[i] == -1):
            print("not enough energy in storage")
              
    print(generatedSurplus)
    graph.GraphGeneratedLoadAndDifference()

if __name__ == "__main__":
    main()
