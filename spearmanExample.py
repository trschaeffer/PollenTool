# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:15:44 2020

@author: Tobias
"""

import scipy.stats as stats
import numpy as np


def calculatecoefficients(array1,array2):
    filtered_arr = np.array([])
    filtered_arr2 = np.array([])
    for i in range (np.size(array1)):
        if array1[i]!=None and array2[i]!=None:
            filtered_arr = np.append(filtered_arr, array1[i])
            filtered_arr2 = np.append(filtered_arr2, array2[i])
            
    #return filtered_arr, filtered_arr2
    r,p = stats.spearmanr(filtered_arr,filtered_arr2)
    return (r,p)
    
"""arr = np.array([100,None,1000,100000,40000])
arr2 = np.array([100000,100,50000,30000,None])
print(calculatecoefficients(arr, arr2))"""
