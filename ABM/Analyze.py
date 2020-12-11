#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:14:48 2019

@author: clara
"""

"""Plotting"""
import numpy as np

class Analyze:
    def __init__(self, sim):
        self.sim = sim
    
    def sort_pf_by_survival(self):
        times_of_death = {}
        for pf in self.sim.pfs:
            times_of_death[pf] = self.when_dies(pf)
        """ sorted_pfs: list of platforms sorted by death time"""
        sorted_pfs = sorted(times_of_death, key=times_of_death.get)
        
        sorted_trans_hist = self.sort_hist(sorted_pfs, 
                                           self.sim.trans_distrib_hist)
        sorted_rest_hist = self.sort_hist(sorted_pfs, 
                                          self.sim.rest_distrib_hist)
        sorted_mult_hist = self.sort_hist(sorted_pfs, 
                                          self.sim.multihomers_distrib_hist)
        
        return {'trans': sorted_trans_hist, 'rest': sorted_rest_hist,\
                'mult': sorted_mult_hist}
        
        
            
    def when_dies(self, pf):        
        for t in range(self.sim.timesteps):
            
            time_of_death = self.sim.timesteps + 1
            if self.sim.rest_distrib_hist[pf.id,t] == 0:
                if all(self.sim.rest_distrib_hist[pf.id, t:] == 
                        np.zeros([self.sim.timesteps - t])):
                    time_of_death = t
                    break
        return time_of_death
    
    def sort_hist(self, sorted_pfs, unsorted_hist):
        sorted_hist = unsorted_hist.copy()
        
        for pf in sorted_pfs:
            unsorted_index = pf.id
            sorted_index = sorted_pfs.index(pf)
            sorted_hist[sorted_index,:] = unsorted_hist[unsorted_index,:]
            
        return sorted_hist
    

            
            
            