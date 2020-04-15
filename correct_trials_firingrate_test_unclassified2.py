# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 17:14:08 2020
从baseline取到test onset，因没有test之后的部分，因此不对test进行分类
baseline:-2.5~0s，根据coding筛选的版本
@author: Administrator
"""

import numpy as np
#from sklearn.decomposition import PCA
import os
import csv

Path=Path='D:\\welltrained'

SU_list=[]
choose_flg=[]
reader=csv.reader(open('transient_3.csv','r'))
for row in reader:
    if row==['# Sustained', 'transient', 'switched', 'unclassified']:
             continue
    choose_flg.append(row)
reader=csv.reader(open('transient_6.csv','r'))
for row in reader:
    if row==['# Sustained', 'transient', 'switched', 'unclassified']:
             continue
    choose_flg.append(row)
    
reader=csv.reader(open('su_list.csv','r'))
for row in reader:
    fold=row[0].replace('D:\\neupix\\DataSum','')[1:]
    SU_list.append([fold,row[1]])
    
choose_idx=[]
for i,u in enumerate(SU_list):
    for j in range(8):
        if choose_flg[j][i]=='1':
            choose_idx.append(u)
            break

np.save('su_coding_choose.npy',choose_idx)
    #%%
    
def main():
    norm_all=[]
    #%%  
    choose_idx=np.load('su_coding_choose.npy')
    dirs=os.walk(Path)
    for d in dirs:
        print(d)
        if d[2]==[]:
            continue
            
        Seq=fold_statistic(d[0],choose_idx)    
        norm_all=norm_all+Seq
            
        
    np.save('D:\\all_correct_trials_normalized_firingrate-test_unclassified2.npy',norm_all)

def fold_statistic(fold,chs_idx):
    os.chdir(fold)
        
    norm_unable=[]
    fr_container=np.load('correct_trials_firingrate.npy')
    su=np.load('neuron_numbers.npy')
    su_list=[u[1] for u in chs_idx if u[0] in fold]
    
    seq_list=[]
    for i,u in enumerate(fr_container):
        if not (str(su[i]) in su_list):
            continue
        baseline=[]
        #nor_unable_flg=0
        seq=[]
        
        for key in u.keys():
            base=[k[0:250] for k in u[key]]
            for k in base:
                baseline=baseline+list(k)
        averange=np.mean(baseline)
        std=np.std(baseline)
        if std==0:
            print(i,'std is zero')
            norm_unable.append(i)
            #nor_unable_flg=1
            continue
        Key=sorted(u.keys())
        for k in [0,1,4,5]:
            fr=np.concatenate((u[Key[k]],u[Key[k+2]]))
            FR=np.mean(fr,axis=0)
            
            seq=seq+[(x-averange)/std for x in FR]
            
        seq_list.append(seq)
            
#    if not norm_unable==[]:
#        np.savetxt('unable2normalized_index_of_ctFR.txt',norm_unable,fmt="%d",delimiter=',')
        
    return seq_list

if __name__ == '__main__':
    main()