# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 16:21:43 2020

choose well-trained data and copy

@author: Administrator
"""
import os
import shutil

raw_data_directory='D:\\NeuPix_data\\raw'
all_folder=['Part1','Part2','Part3']
new_directory='D:\\welltrained'

def txt_select():
    f=open("welltrained tracks.txt","r")
    lines=f.readlines()
    f.close
    sheet=lines[::3]
    wordings=[]
    #get well-trained data list
    for x in sheet:
        wording=x.split()
        wordings.append(wording[::2])
        
    #select from all data and copy
    search_path=raw_data_directory #
    newpath=new_directory
       
    directory=os.listdir(search_path)
    
    for s in directory:
        n=1
        while n<=len(wordings):
            if wordings[n-1][0] in s and wordings[n-1][1] in s:
                try:
                    shutil.copytree(os.path.join(search_path,s),os.path.join(newpath,s))
                except FileExistsError:
                    pass
            n=n+1
        
    
def csv_select():
    import csv
    with open('su_list.csv','r') as sheet:
        l=csv.reader(sheet)
        last=''
        for i in l:
            
            fold=i[0].replace('D:\\neupix\\DataSum','')[1:]
            if fold==last:
                continue
            last=fold
            
            dirs=os.walk(raw_data_directory)
            for d in dirs:
                if fold in d[0]:
                    try:
                        shutil.copytree(d[0],os.path.join(new_directory,fold))
                    except FileExistsError:
                        print(d[0])


            
            
            
            
            
            