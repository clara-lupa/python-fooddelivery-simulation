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

#upper limits are not included!
lower_lim = 0.4
steps = 9
step_size = 0.001
upper_lim = round(lower_lim + steps*step_size,4)
print(upper_lim)
plot_dim = (3,3)

""" multiple runs with varying transaction number"""
trans_sh = np.arange(lower_lim,upper_lim, step_size)
axes_pos = np.reshape(np.arange(1, steps + 1),plot_dim )
if len(trans_sh) != steps:
    print('Error: steps do not match trans shares!')
    trans_sh = trans_sh[0:-1]
    print('trans_sh corrected:', trans_sh)

runs = 200
timesteps = 50
platforms = 3
consumers = 1000
restaurants = 50
count = 0

sup_title = 'Transaction share varying' + \
                         '; Consumers: ' + str(consumers) + \
                         '; Restaurants: '+ str(restaurants) + \
                         '; Platforms: ' + str(platforms) + \
                         '; Runs: ' + str(runs) + \
                         '; Timesteps: ' + str(timesteps)
                         
fig, ax = plt.subplots(plot_dim[0],plot_dim[1])
fig.suptitle(sup_title)
for ts in trans_sh:
    count += 1
    print('count', count, 'ts', ts)
    r = Run(runs, timesteps, platforms, consumers, ts, restaurants)
    r.run()
    p = Plot(r)
    pos = np.where(axes_pos == count)
    pos = [int(pos[0]), int(pos[1])]
    print('Position:', pos)
    title = 'transaction share = ' + str(ts)
    print(title)
    ax[pos[0], pos[1]].set_title(title)
    ax[pos[0], pos[1]].set_ylim(0, ts * consumers)
    if pos[0]+1 != plot_dim[0]:
        ax[pos[0],pos[1]].set_xticklabels([])
    """else:
        print('lables should be set')
        ax[pos[0],pos[1]].set_xticklabels([str(0), str(timesteps)])"""
    p.stackplot_ax(r.trans_av, ax[pos[0], pos[1]])
