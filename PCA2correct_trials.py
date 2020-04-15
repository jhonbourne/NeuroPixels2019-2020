# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:35:17 2020

@author: Administrator
"""

import numpy as np
from sklearn.decomposition import PCA
from scipy import io
#%%
norm_all=np.load('D:\\all_correct_trials_normalized_firingrate.npy')
#%%
norm_all=np.load('D:\\all_correct_trials_normalized_firingrate2.npy')
#%%
norm_fr=np.asarray(norm_all)
norm_fr=norm_fr.T

pca=PCA(n_components=3)
pric_com=pca.fit_transform(norm_fr)

io.savemat('D:\\MATLABdata\\bin_principal_component2.mat',{'coordinates':pric_com})

#%%
norm_fr=[]
for u in norm_all:
    b2t=u[np.r_[0:750,950:2000,2200:2950,3150:4200,4400:5150,5350:6400,6600:7350,7550:8600]]
    norm_fr.append(b2t)

norm_fr=np.asarray(norm_fr)
norm_fr=norm_fr.T

pca=PCA(n_components=3)
pric_com=pca.fit_transform(norm_fr)

io.savemat('D:\\MATLABdata\\b2t_bin_principal_component.mat',{'coordinates':pric_com})    
#%%
norm_fr=[]
for u in norm_all:
    b2t=u[np.r_[0:650,950:1900,2200:2850,3150:4100,4400:5050,5350:6300,6600:7250,7550:8500]]
    norm_fr.append(b2t)

norm_fr=np.asarray(norm_fr)
norm_fr=norm_fr.T

pca=PCA(n_components=3)
pric_com=pca.fit_transform(norm_fr)

io.savemat('D:\\MATLABdata\\b2to_bin_principal_component.mat',{'coordinates':pric_com}) 

#%%
norm=np.load('D:\\all_correct_trials_normalized_firingrate-test_unclassified.npy')
#%%
norm=np.load('D:\\all_correct_trials_normalized_firingrate-test_unclassified2.npy')
#%%
norm_fr=[]
for u in norm:
    b2t=u[np.r_[0:650,950:1900,2200:2850,3150:4100]]
    norm_fr.append(b2t)

norm_fr=np.asarray(norm_fr)
norm_fr=norm_fr.T

pca=PCA(n_components=20)
pric_com=pca.fit_transform(norm_fr)

io.savemat('D:\\MATLABdata\\test_unclassified_bin_principal_component_trainsent6row1.mat',{'coordinates':pric_com})
