#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 13:47:57 2019

@author: clara
"""

"""test run"""

from Run import Run
import matplotlib.pyplot as plt
import numpy as np
from Plot import Plot
"""r = Run(10, 50, 3, 1000, 0.4, 50)
r.run()
r.plot()"""

""" multiple runs with varying transaction number"""
trans_sh = np.arange(7,13)*0.1
axes_pos = np.reshape(np.arange(7,13)*0.1,(2,3) )
print(axes_pos)
runs = 50
timesteps = 600
platforms = 3
consumers = 1000
restaurants = 50

fig, ax = plt.subplots(2,3)
"""fig.suptitle('Varying number of transactions, average transaction distribution out of ' 
             + str(runs) + ' runs, timesteps =' + str(timesteps), 
             fontsize = 18)"""
'''fertig'''
for ts in trans_sh:
    print(ts)
    r = Run(runs, timesteps, platforms, consumers, ts/10, restaurants)
    r.run()
    p = Plot(r)
    pos = np.where(axes_pos == ts)
    pos = [int(pos[0]), int(pos[1])]
    print('Position:', pos)
    title = '# transactions = ' + str(ts*100)
    print(title)
    ax[pos[0], pos[1]].set_title(title, fontsize = 14)
    if pos[0] != 1:
        ax[pos[0], pos[1]].set_xticks([])
    else:
        ax[pos[0], pos[1]].set_xlabel('time', fontsize = 14)
        
    if pos[1] == 0:
        ax[pos[0], pos[1]].set_ylabel('transactions per pf', fontsize = 14)
    p.stackplot_ax(r.trans_av, ax[pos[0], pos[1]])
