import os
import math
import numpy as np
from app.trace.scan_cwt_1 import scan_mp
from app.trace.getImage_2 import get_image
from app.trace.predict_3 import predict
import multiprocessing as mp
import pickle
import time
from app.trace.MasterConfig import params
from app.trace.peaks import Peak
from app.trace.TraceResults import allPeaksResults
import pandas as pd
import logging

#Call this function after main() to export CSV
def exportCSV():
    # Saving dataframe to Results class and CSV files
    peakarrform = []
    for peak in allPeaksResults.allPeaks:
        peakarrform.append([peak.mz, peak.time, peak.height, peak.area, peak.snr, peak.prediction])
    dataFrameFinalPeaks = pd.DataFrame(peakarrform ,columns=['M/Z', 'Time', 'Intensity', 'Area', 'Snr', 'Peak Prediction'])
    dataFrameFinalPeaks.to_csv(params.RESULTS_PATH + "\Final_pks.csv")

#Returns an array of Peak objects storing certain parameters and the prediction of true or false
def main(parameters):
    if os.path.exists(params.LOGGING_PATH):
        os.remove(params.LOGGING_PATH)
    time.sleep(10)
    logger = logging.getLogger("TRACE")
    logger.propagate = False
    fhandler = logging.FileHandler(filename=params.LOGGING_PATH, mode='a')
    formatter = logging.Formatter('%(message)s')
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)
    logger.setLevel(logging.INFO)

    logger.info('Starting Trace...\n')
    logger.info('\nGeneral Parameters:\nResults Path: {}\nCentroid MS Path: {}\nProfile MS Path: {}\nCores: {}\nRAM 8 Times Size Of Profile Data File: {}\nWindow M/Z: {}\nWindow Time: {}\nPlot Images: {}\nMin M/Z: {}\nMax M/Z: {}\nM/Z Bin: {}\nMS Frequency: {}\n\nCWT Parameters:\nMin Length Of EIC To Be Scanned: {}\nMax Peak Width: {}\nTime window: {}\nWindow Size: {}\nSNR For Wavelet: {}\nMax Scale For Peak: {}\n'.format(params.RESULTS_PATH, params.CENTROID_MS_PATH, params.PROFILE_MS_PATH, params.NUM_C, params.Big_RAM, params.window_mz, params.window_rt, params.Plot_images, params.mz_min, params.mz_max,params.mz_r, params.ms_freq, params.min_len_eic, params.max_peak_width, params.time_window, params.window_size, params.min_snr,params.max_scale_for_peak ))
    # for i in range(10):
    #     logging.critical(i)
    #     time.sleep(5)
    if not os.path.isdir(params.RESULTS_PATH):   ## Will create a folder for results if not existent.
        os.makedirs(params.RESULTS_PATH)

    ## First step: CWT and initial scanning
    pks_initial = scan_mp(params.CENTROID_MS_PATH, NUM_C=params.NUM_C)  ##

    pickle.dump(pks_initial, open(params.RESULTS_PATH + "\\save.p", "wb"))

    ## Second step: Signal image evaluation.
    pks_initial_debug = pickle.load(open(params.RESULTS_PATH + "\\save.p", "rb"))
    peaks_with_images = get_image(params.PROFILE_MS_PATH, pks_initial_debug, params.RESULTS_PATH, params.Big_RAM, params.window_mz, params.window_rt)
    pickle.dump(peaks_with_images, open(params.RESULTS_PATH + "\\save2.p", "wb"))


    ## Final prediction
    peaks_with_images_debug = pickle.load(open(params.RESULTS_PATH + "\\save2.p", "rb"))
    pks_final = predict(peaks_with_images_debug, RESULTS_PATH=params.RESULTS_PATH, PLOT_IMG=params.Plot_images)
    logger.info('\nDone! Final disk results in {} folder.'.format(params.RESULTS_PATH))
    allPeaksResults.allPeaks = pks_final
    return pks_final

if __name__ == '__main__':
    main(params)
    exportCSV()
