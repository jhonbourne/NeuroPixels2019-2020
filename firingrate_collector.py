# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 22:58:26 2020
classify firing rate of all correct trials
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

fr_all=[]
dir_idx=[]
def main():   
    #%%
    dirs=os.walk(Path)
    for d in dirs:
        print(d)
        if d[2]==[]:
            continue
        if 'correct_trials_firingrate.npy' in d[2]:
            continue
        os.chdir(d[0])
        p=mp.Pool(processes=cores,maxtasksperchild=1)
        
        fr_idx=np.load('firingrate_pieces.npy')
        
        f=h5py.File('events.hdf5','r')
        trials=np.asarray(f['trials'][:],dtype=np.int32)
        f.close()
        
        print('load done')
    
        types_dic={'s4t4d3':[],'s4t4d6':[],'s8t8d3':[],'s8t8d6':[],'s4t8d3':[],'s4t8d6':[],'s8t4d3':[],'s8t4d6':[]}
        for i in range(len(trials)):
            if (trials[i][4]==4 and trials[i][5]==4) and trials[i][6]==-1:
                if trials[i][7]==3:
                    types_dic['s4t4d3'].append(i)
                elif trials[i][7]==6:
                    types_dic['s4t4d6'].append(i)
            if (trials[i][4]==8 and trials[i][5]==8) and trials[i][6]==-1:
                if trials[i][7]==3:
                    types_dic['s8t8d3'].append(i)
                elif trials[i][7]==6:
                    types_dic['s8t8d6'].append(i)
            if (trials[i][4]==4 and trials[i][5]==8) and trials[i][6]==1:
                if trials[i][7]==3:
                    types_dic['s4t8d3'].append(i)
                elif trials[i][7]==6:
                    types_dic['s4t8d6'].append(i)
            if (trials[i][4]==8 and trials[i][5]==4) and trials[i][6]==1:
                if trials[i][7]==3:
                    types_dic['s8t4d3'].append(i)
                elif trials[i][7]==6:
                    types_dic['s8t4d6'].append(i)
        
        params=[]
        for u in fr_idx:
            params.append((u,types_dic))
#        print(params)
        #%%
        
        correct_FR=list(p.imap(fr_classify,params,chunksize=20))  
        p.close()
        p.join()
        
        np.save('correct_trials_firingrate.npy',correct_FR)
        del correct_FR
#        fr_all.append(correct_FR)
#        dir_idx.append(d[0])
#        dir_idx.append(len(fr_idx))
#        
#np.save('D:\\all_correct_trials_firingrate.npy',fr_all)
#np.save('D:\\directory_of_firing_rate.npy',dir_idx)
        
def fr_classify(args):
    (fr_u,types)=args
    fr_dic={'s4t4d3':[],'s4t4d6':[],'s8t8d3':[],'s8t8d6':[],'s4t8d3':[],'s4t8d6':[],'s8t4d3':[],'s8t4d6':[]}
    for typ in types.keys():
        if '3' in typ:
            bin_num=s_bl/step+(3+1)/step+af_t/step
        elif '6' in typ:
            bin_num=s_bl/step+(6+1)/step+af_t/step
        
        for i in types[typ]:
            
            cnt=[]
        
            for j in range(int(bin_num)):
                cnt.append(sum(fr_u[i][j:j+int(window/step)])/window)
            
            fr_dic[typ].append(cnt)
    
    for typ in fr_dic.keys():
        fr_dic[typ]=np.asarray(fr_dic[typ])
    return fr_dic
        

if __name__ == '__main__':
    main()