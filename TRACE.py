import os
import math
import numpy as np
from scan_cwt_1 import scan_mp
from getImage_2 import get_image
from predict_3 import predict
import multiprocessing as mp
import pickle

if __name__ == '__main__':

    num_cores = mp.cpu_count()   ## Count the cores of the PC.
    print ('Number of cores detected in this PC:', num_cores)

    NUM_C = 1 ## MP use (all-2) threads by default. Adjusted to 1 core due to joblib error

    Big_RAM = 0  ## See if the RAM of PC is big enough (> 8 times bigger than profile file size)

    K_MEANS = 8  ## Or some integer (2~10 recommended); for k-means clustering of signal images

    window_mz = 6  # the m/z range is 6 points (on both sides)
    window_rt = 30  # The time range is 30 points (on both sides)


    RESULTS_PATH = r"C:\Users\jerry\Desktop\Results"
    if not os.path.isdir(RESULTS_PATH):   ## Will create a folder for results if not existent.
        os.makedirs(RESULTS_PATH)

    ## First step: Preprocessing and initial scanning.
    #pks_initial = scan_mp(r"C:\Users\jerry\Desktop\DCSM_CENTROID.mzML", RESULTS_PATH = RESULTS_PATH, NUM_C = NUM_C )  ##
    #pickle.dump(pks_initial, open( RESULTS_PATH + "\\save.p", "wb" ))
    ## Second step: Signal image evaluation.
    pks_initial_debug = pickle.load(open( RESULTS_PATH + "\\save.p", "rb" ))
    images = get_image(r"C:\Users\jerry\Desktop\DCSM_PROFILE.mzML", pks_initial_debug, RESULTS_PATH, Big_RAM, window_mz, window_rt)

    pks_final = predict(images, pks_initial_debug, RESULTS_PATH = RESULTS_PATH, K_means = K_MEANS )


    print ('Done! Final results in ' +  RESULTS_PATH + ' folder.')

