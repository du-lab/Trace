import os
import math
import numpy as np
from scan_cwt_1 import scan_mp
from getImage_2 import get_image
from predict_3 import predict
import multiprocessing as mp
import pickle
from MasterConfig import MasterConfig
from TraceResults import Results
import pandas as pd

if __name__ == '__main__':
    #Create config and results objects for GUI usage
    params = MasterConfig()
    results = Results()

    if not os.path.isdir(params.RESULTS_PATH):   ## Will create a folder for results if not existent.
        os.makedirs(params.RESULTS_PATH)

    ## First step: CWT and initial scanning
    pks_initial = scan_mp(params.CENTROID_MS_PATH, RESULTS_PATH=params.RESULTS_PATH, NUM_C=params.NUM_C)  ##

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

    # Saving dataframe to Results class
    results.dataFrameInitPeaks = pd.DataFrame(pks_initial_debug, columns=['M/Z', 'Time', 'Intensity', 'Area', 'Snr'])
    results.dataFrameFinalPeaks = pd.DataFrame(pks_final, columns=['M/Z', 'Time', 'Intensity', 'Area', 'Snr', 'Peak Membership', 'Peak Membership'])

    print ('Done! Final results in ' + params.RESULTS_PATH + ' folder.')

