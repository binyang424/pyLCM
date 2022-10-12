# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 10:01:32 2018

@author: palme
"""
import sys
import numpy as np
import matplotlib.pyplot as plt

####################################
#####     Input Parameters      ####
####################################

data_lt=np.loadtxt(r'D:\04 YangBin\00 LCM\00 杨斌 博士\02 Programs for in-plane permeability test\1.txt',skiprows=4)
t = data_lt[:,0]                        # time
L = data_lt[:,1]/1000                   # flow front position
Vf =          0.6946                    # fiber volume fraction
delta_p =     0.385*10**6               # delta pressure
visco =       0.25                     # viscosity of fluid Pa.s

# y=1.6294×10-4x-2.9054×10-6
# K1avg=5.155×10-11 m2

L_sq= np.square(L)
f1_coe=np.polyfit(t,L_sq,1)
'''
np.polyfit(x,y,degree)
Least squares polynomial fit.    Fit a polynomial ``p(x) = p[0] * x**deg + ... + p[deg]`` of degree `deg`to points `(x, y)`. 
Returns a vector of coefficients `p` that minimises the squared error(ndarray, shape (deg + 1,) or (deg + 1, K)).
'''
p1 = np.poly1d(f1_coe)
yvals = p1(t)  
plt.plot(t,yvals)
plt.scatter(t,L_sq)
plt.show()

In_perm = (1-Vf)*f1_coe[0]*visco/2/delta_p
