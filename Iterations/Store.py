import matplotlib.pyplot as plt;
import numpy as np;
import pandas as pd;
import os
import array as arr
from dateutil import parser

import Store
import Batteries
def storeTestPrint():
    print("THis is Store")
def StoreExcessEnergy(batteryArray, energy):
    Batteries.StoreEnergy(batteryArray, energy)# stores the energy in the batteries
