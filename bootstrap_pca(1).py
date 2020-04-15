# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 00:00:12 2020

@author: Administrator
"""

import numpy as np
import os
import random
import math
from sklearn.decomposition import PCA
from scipy import io

import multiprocessing as mp
import time


cores=os.cpu_count()
#%%


Trial_num={'s4t4d3': 299749, 's4t4d6': 304624, 's4t8d3': 321384, 's4t8d6': 314461, 's8t4d3': 320591, 's8t4d6': 313711, 's8t8d3': 257678, 's8t8d6': 245876}

chs_idx=np.load('su_coding_choose.npy')

def main():
    t0=time.time()
    p=mp.Pool(processes=cores,maxtasksperchild=1)
    params=[(Trial_num,chs_idx) for n in range(100)]
    
    Samples=p.map(bootstrap,params,chunksize=1)
#    Samples=list(p.imap(bootstrap,params,chunksize=2))
    p.close()
    p.join()
# =============================================================================
#     Samples=[]
#     for n in range(1):
#         Samples.append(bootstrap((Trial_num,chs_idx)))
# =============================================================================
        
    Samples=np.asarray(Samples)
    (x,y,z)=Samples.shape
#    forsave=np.zeros((x,y,z))
#    for i in range(x):
#        for j in range(y):
#            for k in range(z):
#                forsave[x,y,z]=Samples[x,y,z]
                
    
    t1=time.time()-t0
    print('done at ',t1)
    io.savemat('C:\\NeuPix_data\\bootstrap_principal_component.mat',{'samples_of_pc':Samples})
#    io.savemat('C:\\NeuPix_data\\shuffles_principal_component.mat',{'shuffles_of_pc':Samples})
#%%    
def bootstrap(args):  
    Path='C:\\welltrained'
    su_num=13709
    (trial_num,choose_idx)=args
#    rand_sam=[ [] for i in range(8)]
    samples=[ [] for i in range(8)]
#    counter=[0 for n in range(8)]
    Key=sorted(trial_num.keys())
#    for k in [0,1,4,5]:
#        rand_sam[k]=np.random.randint(0,trial_num[Key[k]]+trial_num[Key[k+2]],size=su_num)
#        rand_sam[k].sort()     
    sample_fr=[]    
    dirs=os.walk(Path)
    for d in dirs:
        print(d)
        if d[2]==[]:
            continue
#            os.chdir(d[0])
        
        fr_container=np.load(d[0]+'\\correct_trials_firingrate.npy')
        su=np.load(d[0]+'\\neuron_numbers.npy')
        su_list=[u[1] for u in choose_idx if u[0] in d[0]]
        for i,u in enumerate(fr_container):
            if not (str(su[i]) in su_list):
                continue
            
            baseline=[]
            for key in u.keys():
                base=[k[0:250] for k in u[key]]
                for k in base:
                    baseline=baseline+list(k)
            averange=np.mean(baseline)
            std=np.std(baseline)
            if std==0:
                continue
            
            for k in [0,1,4,5]:
                key_container=np.concatenate((u[Key[k]],u[Key[k+2]]))
                rand_sam=[random.randint(0,len(key_container)-1) for num in range( random.randint(math.ceil(len(key_container)/2),len(key_container)) )]
                
                sam_list=[key_container[u_id] for u_id in rand_sam]
                samples[k]=sam_list
                
            
# =============================================================================
            #for shuffle
#             xchg=random.sample(range(len(samples[0])),random.randint(math.ceil(len(samples[0])/2),len(samples[0])))
#             for t_num in xchg:
#                 tchg=random.randint(0,len(samples[4])-1)
#                 samples[0][t_num],samples[4][tchg]=samples[4][tchg],samples[0][t_num]
#             
#             xchg=random.sample(range(len(samples[1])),random.randint(math.ceil(len(samples[1])/2),len(samples[1])))
#             for t_num in xchg:
#                 tchg=random.randint(0,len(samples[5])-1)
#                 samples[1][t_num],samples[5][tchg]=samples[5][tchg],samples[1][t_num]
# =============================================================================
            
            seq=[]
            for k in [0,1,4,5]:   
                sam_list=np.asarray(samples[k])   
                sam_su=np.mean(sam_list,axis=0)
                
                seq=seq+[(x-averange)/std for x in sam_su]
            sample_fr.append(seq)
            #np.save('D:\\all_firingrate_samples_by_type.npy',all_sam)                 
    
    container=[]
    for u in sample_fr:
        u=np.asarray(u)
        b2t=u[np.r_[0:650,950:1900,2200:2850,3150:4100]]
        
        container.append(b2t)
    container=np.asarray(container)
    container=container.T
        
    pca=PCA(n_components=20)
    pric_com=pca.fit_transform(container)
    
    return pric_com
            
if __name__ == '__main__':
    main()            