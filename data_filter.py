# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 18:42:21 2020

@author: Administrator
"""

import os
import h5py
import numpy as np
import pandas as pd

Path='D:\\welltrained'
s1s=30000

step=0.01
window=0.25

s_bl=2.5
af_t=3

def SU_filter():
    #choose single units: firing rate > 1Hz, KS2 contamination < 10%
    dirs=os.walk(Path)
    for d in dirs:
        if d[2]==[]:
            continue
        
        os.chdir(d[0])
        
        tims=np.load('spike_times.npy')
        info=pd.read_csv("cluster_info.tsv",sep='\t',index_col='id')
        
        spkThres=tims[-1]/s1s
        
        numbers=[]
        
        for u_id in info.index:
            wf = info.loc[u_id].get("group") == "good" or (
                np.isnan(info.loc[u_id]['group'])
                and info.loc[u_id]["KSLabel"] == "good"
            )
            spkCount = info.loc[u_id]["n_spikes"]
            if spkCount>spkThres and wf:
                numbers.append(u_id)
    #            print(u_id)
        np.save('neuron_numbers.npy',numbers)
        
def correct_trial_filter():
    dirs=os.walk(Path)
    tri_n=[]
    for d in dirs:
        if d[2]==[]:
            continue
        os.chdir(d[0])
        f=h5py.File('events.hdf5','r')
        trials=f['trials'][:]
        f.close()
        correct_id=[]
        for n,i in enumerate(trials):
            response=((not i[4]==i[5]) and i[6]==1)
            reject=(i[4]==i[5] and i[6]==-1)
            if response or reject:
                correct_id.append(n)
        np.save('correct_trials_id.npy',correct_id)
        tri_n.append(len(correct_id))
    print(sum(tri_n),tri_n)