#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 13:37:24 2019

@author: clara

how does this relate to the Plot class?
"""

"""plot transactions per platform at the end of the simulation
 against transaction share"""

from Run import Run
import matplotlib.pyplot as plt
import numpy as np


steps = 50
trans_sh = np.arange(0, steps + 1)/steps



runs = 50
timesteps = 50
platforms = 3
consumers = 1000
restaurants = 50
count = 0

'''sup_title = 'Varying transaction number, average transaction distribution after '\
            + str(timesteps) + ' timesteps out of ' + str(runs) + ' runs'
'''

"""goal: np array with the average distribution of transactions in the last
 timestep for each transaction share step"""
trans_dis = np.zeros([platforms, steps + 1])

for ts in trans_sh:

    print('count', count, 'ts', ts)
    r = Run(runs, timesteps, platforms, consumers, ts, restaurants)
    r.run()
    for pf in range(platforms):
        trans_dis[-(pf+1)][count] = r.trans_av[pf][timesteps-1]
    count += 1

plot_hist = trans_dis[:,:]
fig = plt.figure()
plt.stackplot(trans_sh * consumers, plot_hist)
#fig.suptitle(sup_title, fontsize = 18)
plt.ylabel('Transactions per platform, stacked', fontsize = 18)
plt.xlabel('Total number of transactions per timestep', fontsize = 18)
plt.xlim(0, 1)
plt.xticks(np.arange(0,1100,100))
plt.plot(trans_sh * consumers, trans_sh * consumers)

plt.show()
