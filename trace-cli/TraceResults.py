import numpy as np
import pandas as pd

#TODO Are we using class Resulst?
#Stores arrays returned by each module to be used in the GUI
class Results:
    allPeaks = None
    def __init__(self):
        pass

#TODO Class Peak is hard to find. Maybe, we should put it in file `peak.py`
class Peak:
    mz = None
    time = None
    height = None
    area = None
    snr = None
    image = None
    times = None
    mz_values = None
    prediction = False
    def __init__(self):
        pass

allPeaksResults = Results()