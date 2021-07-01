import numpy as np

#Configure Parameters For All Modules and GUI
class MasterConfig():
    #Reference parameter descriptions at: https://pubs.acs.org/doi/suppl/10.1021/acs.analchem.8b05985/suppl_file/ac8b05985_si_001.pdf

    # --------------PATHS---------------
    RESULTS_PATH = r"C:\Users\jerry\Desktop\Results"
    # MS Data must be in .mzML format. Convert using MSConvert from Proteowizard. Specify the path on your computer and include "r" before
    CENTROID_MS_PATH = r"C:\Users\jerry\Desktop\2016-03-15_EP03_D11_cell-E2-2.mzML"
    PROFILE_MS_PATH = r"C:\Users\jerry\Desktop\D11LE22.mzML"
    MEAN_STD_IMGS_PATH = r"C:\Users\jerry\Desktop\Trace-master\Imgs_mean_std.txt"
    MODEL_PATH = r"C:\Users\jerry\Desktop\Trace-master\pre-trained_models\model" #path to any pre-trained model but without the integer at the end
    # -----------------------------------

    # --------GENERAL PARAMETERS--------
    NUM_C = 1  ## MP use (all-2) threads by default. Adjusted to 1 core due to parallel processing error
    Big_RAM = 0  ## See if the RAM of PC is big enough (> 8 times bigger than profile file size)
    K_MEANS = 8  ## Or some integer (2~10 recommended); for k-means clustering of signal images
    window_mz = 6  # the m/z range is 6 points (on both sides)
    window_rt = 30  # The time range is 30 points (on both sides)
    Plot_images = False  # choose to plot final predicted signal images or not

    mz_min = 25.000  # The minimum of m/z to be evaluated
    mz_max = 550.01  # The maximum of m/z to be evaluated
    mz_r = 0.0050  # The m/z bin for signal detection and evaluation (window is +/- this value)
    ms_freq = 2  ## The scanning frequency of MS: spectrums/second. Change accordingly
    # ---------------------------------

    # ----------CWT PARAMETERS---------
    min_len_eic = 6  ## Minimum length of a EIC to be scanned by CWT
    widths = np.asarray([i for i in range(1, int(10 * ms_freq), 1)] + [int(20 * ms_freq)])
    gap_thresh = np.ceil(widths[0])
    window_size = 30
    min_length = int(len(widths) * 0.2)  # org: 0.25
    min_snr = 4  # org: 8. This is the Signal Noise Ratio for the wavelet and may needed to be adjusted.
    perc = 90

    Pick_mlist = np.arange(mz_min, mz_max, mz_r)
    max_distances = widths / 4.0
    max_scale_for_peak = 18
    hf_window = int(0.5 * window_size)
    # ----------------------------------

    # ADD DEEP LEARNING PARAMETERS HERE

    #Constructor
    def __init__(self):
        pass

params = MasterConfig()