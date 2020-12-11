#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 16:55:21 2019

@author: clara
"""

'''script to scrape'''
from BLsuper_scraper import BLsuper_scraper
import os, timeit
import pandas as pd

start = timeit.default_timer()
datafile_path = os.getcwd()
case_code = 'BerLief'
datafile_name = case_code + '_data.p'
districtfile_name = 'plz_berlin.txt'
districtfile_path = os.getcwd() + '/district_data'

BLs = BLsuper_scraper(datafile_name, datafile_path, districtfile_name, 
                districtfile_path)
BLs.update_dataframe()

df = pd.read_pickle(datafile_name)

stop = timeit.default_timer()
runtime = stop - start
print('runtime: ', runtime/60)

