# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 13:50:19 2020

@author: Administrator
"""

import os
import h5py
import numpy as np

#from sklearn.externals import joblib
import multiprocessing as mp

Path='D:\\welltrained'
s1s=30000

step=0.01
window=0.25

s_bl=2.5
af_t=3

cores=os.cpu_count()
                
def main():   
    #%%
    dirs=os.walk(Path)
    for d in dirs:
        print(d)
        if d[2]==[]:
            continue
        
        os.chdir(d[0])
        p=mp.Pool(processes=cores,maxtasksperchild=1)
        
        Tims=np.asarray(np.load('spike_times.npy'),dtype=np.int32)
        Nums=np.load('spike_clusters.npy')
        f=h5py.File('events.hdf5','r')
        Trials=np.asarray(f['trials'][:],dtype=np.int32)
        f.close()
        
        su=np.load('neuron_numbers.npy')
        
        print('load done')
        #%%
        
        params=[]
        
        for u in su:
            params.append((u,Trials,Tims,Nums))
            
        T_idx=list(p.imap(su_tim_frag,params,chunksize=20))  #get every spikes in every trials of every choosen single units    
        p.close()
        p.join()

        np.save('trial_tims.npy',T_idx)
        del T_idx
        print('done')
        
# =============================================================================
#         for u in su:
#             params.append((u,Trials,Tims,Nums))
#             
#         FR_idx=list(p.imap(su_fr,params,chunksize=20))  #    
#         p.close()
#         p.join()
#         
# 
#         np.save('firingrate_bins.npy',FR_idx)
#         del FR_idx
#         print('done')
# =============================================================================
        
def su_tim_frag(args):
    (u_id,trials,tims,nums)=args
    print(u_id)
    
    IDtims=tims[nums==u_id]
                
    tim_SU=[]
    for trial_id in range(len(trials)):
        
        start=trials[trial_id][0]-s1s*s_bl
        end=trials[trial_id][1]+s1s*(af_t+1)
        tim=[]
        for j,t in enumerate(IDtims):
            if t<start:
                continue
            elif start<=t and t<end:
                tim.append(int(t-trials[trial_id][0]))
            else:
                tri_end_idx=j
                break
#                bin_tim=[t for t in IDtims if bin_beg<=t and t<bin_end]
#                cnt[i]=len(bin_tim)/window
        IDtims=IDtims[tri_end_idx:]
        
        tim_SU.append(tim)
    return tim_SU        

def su_fr_piece(args):
    (u_id,trials,tims,nums)=args
    print(u_id)
    
    IDtims=tims[nums==u_id]
                
    cnt_SU=[]
    for trial_id in range(len(trials)):
        
        bin_num=s_bl/step+(trials[trial_id][7]+1)/step+af_t/step
        cnt=np.zeros(int(bin_num),dtype='float32')
        
        start=trials[trial_id][0]-s1s*s_bl
        for i in range(int(bin_num)):
            bin_beg=start+i*step*s1s
            bin_end=bin_beg+step*s1s
            if i==(int(bin_num)-1):
                bin_end=bin_beg+window*s1s
            for j,t in enumerate(IDtims):
                if t<bin_beg:
                    continue
                elif bin_beg<=t and t<bin_end:
                    cnt[i]+=1
                else:
                    IDtims=IDtims[j:]
                    break
#                    bin_tim=[t for t in IDtims if bin_beg<=t and t<bin_end]
#                    cnt[i]=len(bin_tim)/window
        cnt=list(cnt)
        
        
        cnt_SU.append(cnt)
    return cnt_SU

def su_fr(args):
    (u_id,trials,tims,nums)=args
    print(u_id)
    
    IDtims=tims[nums==u_id]
                
    cnt_SU=[]
    for trial_id in range(len(trials)):
        
        bin_num=s_bl/step+(trials[trial_id][7]+1)/step+af_t/step
        cnt=np.zeros(int(bin_num),dtype='float32')
        
        start=trials[trial_id][0]-s1s*s_bl
        for i in range(int(bin_num)):
            bin_beg=start+i*step*s1s
            bin_end=bin_beg+window*s1s
            for j,t in enumerate(IDtims):
                if t<bin_beg:
                    continue
                elif bin_beg<=t and t<bin_end:
                    cnt[i]+=1
                else:
                    tri_end_idx=j
                    break
#                    bin_tim=[t for t in IDtims if bin_beg<=t and t<bin_end]
#                    cnt[i]=len(bin_tim)/window
        cnt=[c/window for c in cnt]
        IDtims=IDtims[tri_end_idx:]
        
        cnt_SU.append(cnt)
    return cnt_SU             
 
if __name__ == '__main__':
    main()        