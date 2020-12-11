#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 14:47:52 2019

@author: clara
"""
import os, datetime
import pandas as pd
from BLrest_scraper import BLrest_scraper
from BLbase_scraper import BLbase_scraper

class BLsuper_scraper(BLbase_scraper):
    
    def __init__(self, datafile_name, datafile_path, districtfile_name, 
                districtfile_path):
        self.datafile_name = datafile_name
        self.datafile_path = datafile_path
        self.districtfile_name = districtfile_name
        self.districtfile_path = districtfile_path
        self.today = datetime.datetime.today()
        self.date_str = self.today.strftime('%Y_%m_%d')
        self.wd = os.getcwd() #working directory
        self.url_start = 'https://www.lieferando.de'
        self.html_class_rest = 'restaurantname'
        self.html_type_rest = 'a'
        self.soup_count = 0
        self.err_file = open(self.date_str + 'err_file.txt', 'w')

        
    def update_dataframe(self):
        dist_list = self.import_dist_list()
        print(dist_list)
        self.load_dataframe()
        self.create_htmldir()
        self.add_todays_columns()
        #Add new restaurants and update all restaurants district data.
        for dist in dist_list:
            print('Overview data for ', dist)
            self.update_overview_data(dist)
        self.save_dataframe()
        
        print('Done with overview data, table size:', len(self.df))
        
        #Add data for today for all restaurants and all variable features.
        self.update_var_features()
        self.save_dataframe()
        print(self.soup_count, 'scrapes done')
        self.err_file.close()
        
    def save_dataframe(self):
        print('saving dataframe of size', self.df.shape)
        for key in self.df.keys():
            print('datatype of ', key, type(self.df.iloc[10][key]))
        current_dir = os.getcwd()
        os.chdir(self.datafile_path)
        self.df.to_pickle(self.datafile_name)
        os.chdir(current_dir)
        
    def create_htmldir(self):
        os.chdir(self.wd)
        self.date_str_time = self.today.strftime('%Y_%m_%d_%H%M')
        html_dir_name = self.date_str_time + 'html_dir'
        os.mkdir(html_dir_name)
        self.htmldir_path = self.wd + '/' + html_dir_name
        
    def update_var_features(self):
        '''Add todays values of all variable features for all restaurants to
        the data frame. Check if adresses have changed, if necessary update.
        '''
        BLr = BLrest_scraper(self)
        
        for name in self.df.index:
            print('row nr ', str(self.df.index.get_loc(name)))
            link = self.df.loc[name]['link']
            details = BLr.scrape(link, name)
            self.df.loc[name][self.date_str + 'rating_num'] = \
                details['rating_num']
            self.df.loc[name][self.date_str + 'rating_val'] = \
                details['rating_val']
            if self.df.loc[name]['adress'] == '':
                self.df.loc[name]['adress'] = details['adress']
            if details['error'] != '':
                self.err_file.write(name + ': ' + details['error'] + '\n')
            

            
    def import_dist_list(self):
        try:
            os.chdir(self.districtfile_path)
            print('district dir???', os.getcwd())
            print('dist file name???', self.districtfile_name)
            f = open(self.districtfile_name, 'r')
            dist = []
            for line in f:
                print(line)
                line = self.format_name(line)
                if line != '':                    
                    dist.append(line)
            os.chdir(self.wd)
            print('Sucessfully imported district data.')
            return dist                            
        except:
            print('Error while importing district data.')
            return ['12049']
        
    def load_dataframe(self):
        '''Load the dataframe from the given file'''
        os.chdir(self.datafile_path)
        self.df = pd.read_pickle(self.datafile_name)
        os.chdir(self.wd)
        
    def add_todays_columns(self):
        '''Add columns to the data frame for today's variable features'''
        self.df[self.date_str + 'districts'] = ''
        self.df[self.date_str + 'rating_num'] = ''
        self.df[self.date_str + 'rating_val'] = ''
        
        
    def update_overview_data(self, dist):
        """Scrape restaurants from districts overview page, add missing 
        restaurants to the dataframe, update todays district list for all 
        restaurants.
        """
        print('dist:', dist)
        dist_soup = self.make_soup(self.url_start + '/' + dist, 
                                   self.date_str +'dist' + dist, 
                                   self)
        # Find all p-elements which contain restaurant names.
        print(self.html_type_rest, self.html_class_rest)
        restaurants = dist_soup.find_all(self.html_type_rest, 
                                              self.html_class_rest)
        restaurants = restaurants[:-1]
        
        print('number of rests to scrape in',dist, ': ', len(restaurants))

        for rest in restaurants:
            # Extract restaurant's fixed feature data.
            name = self.format_name(str(rest.string))
            link = self.url_start + rest['href']
            print(dist, name)
            
            #Add row if restaurant does not exist yet.
            print('rest in index?', name in self.df.index )
            if ((name in self.df.index) == False):
                self.df.loc[name] = ''
            
            #Add/update link.
            self.df.loc[name]['link'] = link
            
            #Add district to today's district data.
            self.df.loc[name][self.date_str + 'districts'] = \
                    self.df.loc[name][self.date_str + 'districts'] + \
                    ';' + dist

    def raise_soup_count(self):
        self.soup_count += 1

