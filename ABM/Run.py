#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 13:27:22 2019

@author: clara
class that represents a run with different parameters and an Run#run function that
carries out simulation runs.
"""
from Simulation import Simulation
from Plot import Plot
from Analyze import Analyze
import numpy as np
"""measure dying times, how to plot multihomers?"""
class Run:
    def __init__(self, runs, timesteps, pf_number, con_number, con_share,
                 rest_number):
        self.runs = runs
        self.timesteps = timesteps + 2
        self.pf_number = pf_number
        self.con_number = con_number
        self.con_share = con_share
        self.rest_number = rest_number
        """arrays to store distribution object in """
        self.trans_distrib = np.zeros([self.pf_number, self.runs,
                                       self.timesteps])
        self.rest_distrib = np.zeros([self.pf_number, self.runs,
                                      self.timesteps])
        self.mult_distrib = np.zeros([self.pf_number, self.runs,
                                      self.timesteps])
        self.mult_distrib_abs = np.zeros([self.runs, self.timesteps])
        """arrays to store averages in"""
        self.trans_av = np.zeros([self.pf_number, self.timesteps])
        self.rest_av = np.zeros([self.pf_number, self.timesteps])
        #absolut number of multihomers would be interesting
        #self.mult_av = np.zeros([self.pf_number, self.timesteps])
        #self.mult_av_abs = np.zeros([self.timesteps])
    def run(self):
        for i in range(self.runs):
            S = Simulation(self.timesteps, self.pf_number, self.con_number,
                           self.con_share, self.rest_number)
            S.iterate()
            an = Analyze(S)
            sorted_results = an.sort_pf_by_survival()
            for pf_n in range(self.pf_number):
                self.trans_distrib[pf_n,i] = sorted_results['trans'][pf_n]
                self.rest_distrib[pf_n,i] = sorted_results['rest'][pf_n]
                self.mult_distrib[pf_n,i] = sorted_results['mult'][pf_n]
        self.calc_av(self.trans_distrib, self.trans_av)
        self.calc_av(self.rest_distrib,self.rest_av)

    def calc_av(self,distrib,output_ar):
        """ output array: array of size [pf_n, timesteps] where average
        values per timestep are stored"""
        for pf_n in range(self.pf_number):
            output_ar[pf_n] = sum(distrib[pf_n][:])/self.runs



    def plot(self):
        p = Plot(self)
        p.stackplot(self.trans_av, 'Average transactions per platform')
        p.simple_hist_plot(self.rest_av, 'Average rest per platform')
