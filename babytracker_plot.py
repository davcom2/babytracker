# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 18:41:41 2018

@author: DWong
"""
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import os as os
import numpy as np
import matplotlib.pyplot as plt

" go to path of file "
baby = pd.read_csv("BabyTracker.csv")
sleeps = baby.loc[baby['RecordCategory'] == 'Sleep']
sleepStart = pd.to_datetime(sleeps.StartDate, format ='%d-%b-%Y %H:%M')
sleepFinish = pd.to_datetime(sleeps.FinishDate, format ='%d-%b-%Y %H:%M')

""" we want x axis to be day, and y axis to be hour """
""" set up a matrix of [24*60/n, days]
n is granularity in minutes 
days is total number of days liver (derived from max date - min date)"""

mindate = sleepStart.iloc[0]
maxdate = sleepFinish.iloc[-1]
days = (maxdate-mindate).days;
n = 15;
intervals = int(24*60/n);
a = np.ndarray((intervals,days-1),int)

""" loop through hour/date and check if sleep is active or not """
""" generate sleepmat"""

for i in range(0, days-1):
    for j in range(0, intervals):
        curr_time = mindate.date() + pd.DateOffset(days=i, minutes=j*n)
        st = sum(curr_time<=sleepStart)
        fn = sum(curr_time<=sleepFinish)
        
        
        if st<fn:
            "then we are in the middle of a sleep"
            a[j,i]=0
        elif st==fn:
            "then we are not in a sleep"
            a[j,i]=1
        else:
            print('error')

"""
plt.imshow(a, cmap='hot', interpolation='nearest')
plt.show()
"""

dx, dy = 1, 0.25
# generate 2 2d grids for the x & y bounds
y, x = np.mgrid[slice(0, 24,dy),
                slice(0, days - 1 + dx, dx)]
plt.pcolor(x,y,a, cmap='terrain')
plt.axis([x.min(), x.max(), y.max(), y.min()])
plt.xlabel('day since birth')
plt.ylabel('hour')
