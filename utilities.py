from __future__ import print_function
from psutil import virtual_memory as vm
from time import sleep

import os
from os.path import join

import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp

# This function computes total completed training batches
def completed_batches(intermediate_checkpoints, pretrained_checkpoints): 
    if os.listdir(pretrained_checkpoints) == []: 
        last_batch = 0 
    else: 
        last_batch = sorted([int( f.split('_')[1].split('.')[0]) for f in os.listdir(pretrained_checkpoints)])[-1] 
    with open(join(intermediate_checkpoints,'checkpoint')) as f:  
        checkpoint_path = f.readline().split('"')[1]
    current = checkpoint_path.split('-')[-1]
    completed = str(last_batch + int(current)) 
    return (completed, current)


# Draw receiver operator characteristic curves
def draw_rocs(roc_base, roc_curves_batch, labels):
#    with open(data_labels_path) as f:
#        labels = [line.rstrip('\n') for line in f]
    plt.figure(figsize=[10,8])
    colors = ['C'+str(x) for x in range(len(labels))] + ['deeppink', 'navy']
    lws = [2] * len(labels) + [4, 4]
    curves = [x for x in labels] + ['micro', 'macro']
    fileIds = ['c'+str(x+1)+'auc' for x in range(len(labels))] + ['micro', 'macro']
    linestyles = ['-'] * len(labels) + [':', ':']
    for curve, fileId, color, lw, linestyle in zip(curves, fileIds, colors, lws, linestyles):
        f = [x for x in os.listdir(roc_curves_batch) if x.find(roc_base + fileId)==0][0]
        if not "nan" in f:
            lines = np.loadtxt(join(roc_curves_batch,f), comments="#", delimiter="\t", unpack=True)
            plt.plot(lines[0], lines[1], color = color, lw=lw, linestyle=linestyle,
                 label = '{0} ROC curve (area = {1:0.3f})'.format(curve,float(f[f.find('auc_')+4:f.find('auc_')+10])))
        else:
            print("Curve for {} undefined".format(fileId))

    plt.plot([0, 1], [0, 1], 'k--', lw=lw)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc="lower right")
    plt.show()
    
# Monitor and report the maximum memory used
def max_used_mem(period=5):
    m = 0.0
    while True:
        used = float(vm().used)/2**30
        m = max(m,used)
        print("Max used: {:0.2f}GiB, Used: {:0.2f}GiB, Available: {:0.2f}GiB, Total: {:0.2f}GiB\t\t".
            format(m, float(vm().used)/2**30, float(vm().available)/2**30, float(vm().total)/2**30),
            end="\r")
        sleep(period)

        

