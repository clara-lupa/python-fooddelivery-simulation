#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 17:17:33 2019

@author: clara
"""
import os, urllib3, random, time, pickle
import bs4 as bs

class BLbase_scraper:
    
    def __init__(self):
        pass
    
    def make_soup(self, url, filename, count_scraper):
        """Download source code of the given url, convert it into a soup object
        and save the source code in the code directory. Return the soup.
        """ 
        
        if count_scraper.soup_count % 100 == 0:
            delay = 5 #change back??
        else:
            delay = random.random()*0.01 #different distribution?
        time.sleep(delay)
        print(count_scraper.soup_count, '--', delay)
        count_scraper.raise_soup_count()
        # Generate the url of the search results for the district,
        # get html-code.
        self.quote_page = url
        self.http = urllib3.PoolManager()
        self.r = self.http.request('GET', self.quote_page)
        self.htmlcode = self.r.data
        
        # Save the html-file in the source code directory.
        os.chdir(self.htmldir_path)
        self.htmlfile_name = self.date_str + filename + '.html'
        pickle.dump(self.htmlcode, open(self.htmlfile_name, 'wb'))
        os.chdir(self.wd)
        
        # Create a soup-object out of the html-code.
        self.soup = bs.BeautifulSoup(self.htmlcode, 'html.parser')
        #print('made soup')
        return self.soup
    
    def format_name(self, name):
        """Remove whitespace and html code from a given string."""
        name = name.strip(' ')
        name = name.strip('\n')
        name = name.strip(' ')
        name = name.strip('<br>')
        name = name.strip('</br>')
        return name