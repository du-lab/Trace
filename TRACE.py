import os
import math
import numpy as np
from scan_cwt_1 import scan_mp
from getImage_2 import get_image
from predict_3 import predict
import multiprocessing as mp
import pickle
from MasterConfig import params
from TraceResults import Results
import pandas as pd

if __name__ == '__main__':
    #Create config and results objects for GUI usage
    results = Results()

    if not os.path.isdir(params.RESULTS_PATH):   ## Will create a folder for results if not existent.
        os.makedirs(params.RESULTS_PATH)

    ## First step: CWT and initial scanning
    pks_initial = scan_mp(params.CENTROID_MS_PATH, NUM_C=params.NUM_C)  ##

    results.initial_peaks = pks_initial
    pickle.dump(pks_initial, open(params.RESULTS_PATH + "\\save.p", "wb"))

    ## Second step: Signal image evaluation.
    pks_initial_debug = pickle.load(open(params.RESULTS_PATH + "\\save.p", "rb"))

    images = get_image(params.PROFILE_MS_PATH, pks_initial_debug, params.RESULTS_PATH, params.Big_RAM, params.window_mz, params.window_rt)
    results.images_peaks = images

    pickle.dump(images, open(params.RESULTS_PATH + "\\save2.p", "wb"))
    images_debug = pickle.load(open(params.RESULTS_PATH + "\\save2.p", "rb"))

    #Saving csv files
    #TODO It's an unneceaary work to create a text file first, read it, and then create a csv file.
    # Instead, add the code to create a csv file and remove the code to create a txt file. We shouldn't have any text files at all.
    initPeaks = pd.read_csv(params.RESULTS_PATH + "\Initial_pks.txt", delimiter="  ", header=None)
    initPeaks.columns = ['M/Z', 'Time', 'Intensity', 'Area', 'Snr']
    initPeaks.to_csv(params.RESULTS_PATH + "\Initial_pks.csv", index=None)
    finalPeaks = pd.read_csv(params.RESULTS_PATH + "\Final_pks.txt", delimiter=" ", header=None)
    finalPeaks.columns = ['M/Z', 'Time', 'Intensity', 'Area', 'Snr', 'Peak Membership', 'Peak Membership']
    finalPeaks.to_csv(params.RESULTS_PATH + "\Final_pks.csv", index=None)

    ## Final prediction
    pks_final = predict(images_debug, pks_initial_debug, RESULTS_PATH=params.RESULTS_PATH, K_means=params.K_MEANS, PLOT_IMG=params.Plot_images)
    results.final_peaks = pks_final

    # Saving dataframe to Results class and CSV files
    results.dataFrameInitPeaks = pd.DataFrame(pks_initial_debug, columns=['M/Z', 'Time', 'Intensity', 'Area', 'Snr'])
    results.dataFrameFinalPeaks = pd.DataFrame(pks_final, columns=['M/Z', 'Time', 'Intensity', 'Area', 'Snr', 'Peak Membership', 'Peak Membership'])
    results.dataFrameInitPeaks.to_csv(params.RESULTS_PATH + "\Initial_pks.csv")
    results.dataFrameFinalPeaks.to_csv(params.RESULTS_PATH + "\Final_pks.csv")

    print ('Done! Final results in ' + params.RESULTS_PATH + ' folder.')

if __name__ == '__main__':

    num_cores = mp.cpu_count()   ## Count the cores of the PC.
    print ('Number of cores detected in this PC:', num_cores)

    NUM_C = 1 ## MP use (all-2) threads by default. Adjusted to 1 core due to joblib error

    Big_RAM = 0   ## See if the RAM of PC is big enough (> 8 times bigger than profile file size)

    K_MEANS = 8  ## Or some integer (2~10 recommended); for k-means clustering of signal images

    window_mz = 6  # the m/z range is 6 points (on both sides)
    window_rt = 30  # The time range is 30 points (on both sides)


    RESULTS_PATH = r"C:\Users\jerry\Desktop\Results"
    if not os.path.isdir(RESULTS_PATH):   ## Will create a folder for results if not existent.
        os.makedirs(RESULTS_PATH)

    ## First step: Preprocessing and initial scanning.
    pks_initial = scan_mp(r"C:\Users\jerry\Desktop\IC1_22.mzML", RESULTS_PATH = RESULTS_PATH, NUM_C = NUM_C )  ##

    ## Second step: Signal image evaluation.
    images = get_image(r"C:\Users\jerry\Desktop\IC1_22.mzML", pks_initial, RESULTS_PATH, Big_RAM, window_mz, window_rt)

    pks_final = predict(images, pks_initial, RESULTS_PATH = RESULTS_PATH, K_means = K_MEANS )


    print ('Done! Final results in ' +  RESULTS_PATH + ' folder.')


