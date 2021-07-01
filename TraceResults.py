import numpy as np
import pandas as pd

#Stores arrays returned by each module to be used in the GUI
class Results():
    initial_peaks = [] #From the cwt scanning module
    images_peaks = [] #All signal image data
    final_peaks = [] #Final peaks from all the imaged peaks
    dataFrameInitPeaks = [] #dataframe for initial peaks
    dataFrameFinalPeaks = [] #dataframe for final peaks
    def __init__(self):
        pass