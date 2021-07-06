from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import sys
import os
import tensorflow as tf
import math

from MasterConfig import params

import numpy as np
import sys
import random
from peaks import Peak
import matplotlib
matplotlib.use('Agg')  ## Avoid some problem when running on Windows or so..
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.cluster import KMeans
import logging

# Weight Initialization
def weight_variable(shape, var_name):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial, name = var_name )

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

# Convolution and Pooling
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='SAME')

############ Deep Learning Training Process#########################


def predict(pk_list, RESULTS_PATH, PLOT_IMG = False):

    images0 = np.loadtxt(params.MEAN_STD_IMGS_PATH)
    mean_img = images0[0]
    std_img = images0[1]

    pred_mat0 = np.copy(pk_list)
    for i0 in pred_mat0:
        i0.image *= 255.0/i0.image.max()    ## Normalize the image to gray scale

    #pred_mat = np.copy(pred_mat0)
    out_array=[]
    pred_mat0arr = []
    for Peak in pk_list:
        pred_mat0arr.append(Peak.image)
    epsilon = 0.001 #added epsilon
    for ii, pixel in enumerate(np.transpose(pred_mat0arr)):
        tmp2 = [(k-mean_img[ii])/(std_img[ii]+epsilon) for k in pixel]
        out_array.append(tmp2)
    pred_mat = np.transpose( out_array )
    ## Now the prediction matrix created!  Predict!

    learning_rate = 0.0001

    x = tf.placeholder(tf.float32, [None, 60 * 12])

    # First Convolutional Layer
    W_conv1 = weight_variable([4, 4, 1, 32],"W_conv1")    ## 4*4*1*32
    b_conv1 = bias_variable([32])
    x_image = tf.reshape(x, [-1,60,12,1])  # 60, 12

    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    # Second Convolutional Layer
    W_conv2 = weight_variable([4, 4, 32, 64] ,"W_conv2")   ## 4*4*32*64
    b_conv2 = bias_variable([64])

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    # Densely Connected Layer
    W_fc1 = weight_variable([15 * 3 * 64, 256],"W_fc1")   #  ,1024
    b_fc1 = bias_variable([256])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 15*3*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    # Dropout
    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1,keep_prob)

    # Readout Layer
    W_fc2 = weight_variable([256, 2],"W_fc2")
    b_fc2 = bias_variable([2])
    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
    ################### LeNet5 ################

    # Define loss and optimizer
    y_ = tf.placeholder(tf.float32, [None, 2])
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    score_save = []
    num_models = 10
    for jj in range(num_models):
        
        sess = tf.InteractiveSession()
        sess.run(tf.global_variables_initializer())

        saver = tf.train.Saver()
        #saver.restore(sess, tf.train.latest_checkpoint('./models/'))   

        saver.restore(sess, params.MODEL_PATH + str(jj) )
        
        #logging.debug('TensorFlow model {} loaded done!! '.format(str(jj)))

        cc = 0.0
        sss = []
        resultss = []
        resultss = y_conv.eval(feed_dict={x: pred_mat, keep_prob: 1.0})
        for kk in range(len(resultss)):
            diff = round(resultss[kk][0] - resultss[kk][1], 1)
            #if diff*(labels[kk][0]-0.5) > 0:
            # sss.append([int(diff>0)])
            if diff > 0.0:
                sss.extend([1])
                cc+=1.0
            else:
                sss.extend([0])

        score_save.append(sss)
        print ('Model ' + str(jj) + ' Predicted peaks: ', cc, ' from ', len(pk_list), 'target images' )
        logging.critical('Model {} Predicted peaks: {} from  {} target images'.format(str(jj), cc, len(pk_list)))
        sess.close()

    score_vote = np.mean(np.transpose(score_save), axis = 1)
    target_pks = []
    target_imgs = []
    for kk, skk in enumerate(score_vote):
        if skk > 0.5:
            tmp2 = []
            tmp2.append(pk_list[kk])
            tmp2.append(skk)
            target_pks.append(tmp2)
            target_imgs.append(pk_list[kk].image)

    print ('Final peaks predicted: ', len(target_pks))
    logging.critical('\n\nFinal peaks predicted: {} '.format(len(target_pks)) )
    #f2 = (RESULTS_PATH + "/ImageData_Final-pks.txt")
    #np.savetxt(f2, target_imgs, fmt='%.2f',delimiter=' ')

    #Not necessary, not functional when passing Peak object list. Adjust if want to

    if PLOT_IMG :
        if not os.path.isdir(params.RESULTS_PATH + '\Signal_Images'):
            os.system('mkdir .\Results\Signal_Images')
        print ('Now Ploting...')
        for kk in range(np.shape(target_pks)[0]):
            mz0 = round(target_pks[kk][0].mz, 3)
            rt0 = round(target_pks[kk][0].time, 3)
            plt.imshow(np.reshape(target_pks[kk][0].image, (60, 12)), interpolation='bilinear', cmap='jet', aspect='auto')

            plt.title("M/Z: " + str(mz0)+"  RT: " +str(rt0) )
            plt.xlabel('M/Z')
            plt.ylabel('Time')
            plt.colorbar()
            plt.savefig(RESULTS_PATH+ "\Signal_Images\Signal_" + str(kk+1) + '_' + str(mz0) + '_'+ str(rt0) + '.png')
            plt.clf()


    check_mz_time = []
    for target_pk in target_pks:
        check_mz_time.append([target_pk[0].mz, target_pk[0].time, target_pk[0].height, target_pk[0].area, target_pk[0].snr])
    for peak in pk_list:
        if([peak.mz, peak.time, peak.height, peak.area, peak.snr] in check_mz_time):
            peak.prediction = True
    return pk_list

