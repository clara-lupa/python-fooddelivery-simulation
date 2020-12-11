#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 16:20:42 2019

@author: clara
"""
from BLbase_scraper import BLbase_scraper

class BLrest_scraper(BLbase_scraper):

    def __init__(self, superscraper):
        self.superscraper = superscraper
        self.date_str = superscraper.date_str
        self.htmlfile_name = superscraper.htmlfile_name
        self.htmldir_path = superscraper.htmldir_path
        self.wd = superscraper.wd
    
        
    def scrape(self, link, name):
        
        error = ''
        try:  
            #print('trying to make rest soup')
            self.soup = self.make_soup(link, self.date_str + 
                                       'rest' + name, 
                                       self.superscraper)
        except Exception as e:
            print('exception while making rest soup', e)
            error = 'Rest Soup not available for' + name
        

        try:
            rating_val, rating_num = self.get_ratings()
        except:
            error = error + ' Ratings not available for' + name
            rating_val = 'n.a.'
            rating_num = 'n.a.'

        try:
            adress = self.get_adress()            
        except:
            error = error + ' Adress not available for' + name
            adress = 'n.a.'
        
        rest_details = {'rating_val': rating_val, 'rating_num': rating_num,
                        'adress': adress, 'error': error}

        return rest_details
        

    def get_ratings(self):
        try:
            review_div = self.soup.find('div', 'review-rating')
            sp = review_div.find('span', 'rating-total')
            # Check if rest has 0 ratings.
            if '(0' not in sp.string.split():                
                rating_value_div = self.soup.find('div', 'rating-number-container')
                rating_value = self.format_name(
                        rating_value_div.find('span').string)
                rating_number_div = self.soup.find('div', 'overviewstar')
                rating_number = self.format_name(
                        rating_number_div.find('span').string)
            else:
                rating_value = 'n.a.'
                rating_number = '0'
            
        except:
            rating_value = 'n.a.'
            rating_number = 'n.a.'
        
        
        return rating_value, rating_number

    
    def get_adress(self):
        infobox = self.soup.find('div', 'infoMapWrapper')
        adr = infobox.find('section','card-body').contents
        adr_string = self.format_name(str(adr[0])) + ', ' + \
                     self.format_name(str(adr[1]))
        return adr_string