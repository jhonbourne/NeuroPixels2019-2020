# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 13:41:05 2020

@author: Administrator
"""

import os
import h5py
import numpy as np

#from sklearn.externals import joblib
import multiprocessing as mp

Path='D:\\welltrained'
s1s=30000

step=0.01 #10ms
window=0.25 #250ms

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
        
        T_idx=np.load('trial_tims.npy')
        
        f=h5py.File('events.hdf5','r')
        Trials=np.asarray(f['trials'][:],dtype=np.int32)
        f.close()
        
        su=np.load('neuron_numbers.npy')

        print('load done')
    #%%
    
    
        params=[]
        for i,u in enumerate(su):
            params.append((u,Trials,T_idx[i]))
                
        FR_idx=list(p.imap(su_fr_piece,params,chunksize=20))  # get number of spikes in every bins   
        p.close()
        p.join()
        
        np.save('firingrate_pieces.npy',FR_idx)
        del FR_idx
        print('done')
    
def su_fr_piece(args):
    (u_id,trials,tims)=args
    
                
    cnt_SU=[]
    for trial_id in range(len(trials)):
        
        IDtims=tims[trial_id]
        
        bin_num=s_bl/step+(trials[trial_id][7]+1)/step+af_t/step+(window/step)
        cnt=np.zeros(int(bin_num),dtype='float32')
        
        start=-s1s*s_bl
        for i in range(int(bin_num)):
            bin_beg=start+i*step*s1s
            bin_end=bin_beg+step*s1s
            for j,t in enumerate(IDtims):
                if t<bin_beg:
                    continue
                elif bin_beg<=t and t<bin_end:
                    cnt[i]+=1
                else:
                    IDtims=IDtims[j:]
                    break             
        
        cnt_SU.append(cnt)
    return cnt_SU
 
    
if __name__ == '__main__':
    main()