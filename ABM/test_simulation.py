#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 12:05:29 2019

@author: clara
"""
from Simulation import Simulation
from Plot import Plot
from Analyze import Analyze

"""test Simulation"""
S = Simulation(20,3)
results = S.iterate()



an = Analyze(S)
sorted_results = an.sort_pf_by_survival()

p = Plot()

""" Plot transaction distribution """
p.simple_hist_plot(sorted_results['trans'], 'Transactions per platform')

""" Plot restaurant distribution """
p.simple_hist_plot(sorted_results['rest'], 'Restaurants per platform')

p.cum_hist_plot(sorted_results['trans'], 'Transactions, ')