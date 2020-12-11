#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 17:18:02 2019

@author: clara
"""

"""Analyze trans dis"""
plot_hist = trans_dis[:,:5]
fig = plt.figure()
plt.stackplot((trans_sh * consumers)[:5], plot_hist)
fig.suptitle(sup_title)
plt.ylabel('Transactions, stacked')
plt.xlabel('Transacting consumers per timestep')  
plt.xlim(0, 1)
plt.ylim(0,100)
plt.xticks((trans_sh * consumers)[:5])
plt.plot(trans_sh * consumers, trans_sh * consumers)
      
plt.show()