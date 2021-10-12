import numpy as np

from os.path import join

#Configure Parameters For All Modules and GUI
class MasterConfig:
    #Reference parameter descriptions at: https://drive.google.com/file/d/1sFaYOJhUzy4CGAyHIkhhx4Vdc1x7Sx9x/view?usp=sharing

    # --------------PATHS---------------
    #Do not need to create the directories
    RESULTS_PATH = r"C:\Users\jerry\Desktop\Results"
    # MS Data must be in .mzML format. Convert using MSConvert from Proteowizard. Specify the path on your computer and include "r" before
    CENTROID_MS_PATH = r"C:\Users\jerry\Desktop\2016-03-15_EP03_D11_cell-E2-2.mzML"
    PROFILE_MS_PATH = r"C:\Users\jerry\Desktop\D11LE22.mzML"
    MEAN_STD_IMGS_PATH = join("trace-cli", "Imgs_mean_std.txt")
    MODEL_PATH = r"C:\Users\jerry\Desktop\Trace-master\pre-trained_models\model" #path to any pre-trained model but without the model number at the end
    LOGGING_PATH = r"C:\Users\jerry\Desktop\Trace-master\trace-cli\logs.log" #path to the logs
    # -----------------------------------

    # --------GENERAL PARAMETERS--------
    NUM_C = 1  ## MP use (all-2) threads by default. Adjusted to 1 core due to parallel processing error
    Big_RAM = 1  ## See if the RAM of PC is big enough (> 8 times bigger than profile file size) [Set to True to run faster]
    window_mz = 6  # the m/z range is 6 points (on both sides)
    window_rt = 30  # The time range is 30 points (on both sides)
    Plot_images = True  # choose to plot final predicted signal images or not

    mz_min = 25.000  # The minimum of m/z to be evaluated
    mz_max = 550.01  # The maximum of m/z to be evaluated
    mz_r = 0.0050  # The m/z bin for signal detection and evaluation (window is +/- this value)
    ms_freq = 2  ## The scanning frequency of MS: spectrums/second. Change accordingly
    # ---------------------------------

    # ----------CWT PARAMETERS---------
    min_len_eic = 6  ## Minimum length of a EIC to be scanned by CWT
    max_peak_width = 1.5 * 5 * 0.503 / 60 #In Mins, can use seconds depending on data)
    time_window = 0.5 #time window in mins, can use seconds depending on data parameters
    window_size = 30
    min_snr = 4  # org: 8. This is the Signal Noise Ratio for the wavelet and may needed to be adjusted.
    perc = 90
    max_scale_for_peak = 18
    # ----------------------------------

    # ADD DEEP LEARNING PARAMETERS HERE IF NEEDED

    #Constructor
    def __init__(self):
        pass

#Create params object
params = MasterConfig()