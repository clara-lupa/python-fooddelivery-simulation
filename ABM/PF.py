#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 12:36:41 2019

@author: clara
class that represents the platform agents
"""

class PF:
    def __init__(self, sim, pf_id):
        self.sim = sim
        self.id = pf_id

        # exogenous parameters
        self.p_ct = 3 # Delivery fee
        self.p_rt = 0.3 # Commission share

        self.a_r = 100 #network-independent benefit for restaurants
        self.a_c = 5 #network-independent benefit for consumers

        #endogenous parameters
        self.trans_number = 0
        self.trans_number_old = 0 #ever used anywhere?
        self.rest_number = 0
        self.rest_number_old = 0
        self.rest_list = []
        self.rest_list_old = []

    def receive_order(self):
        self.trans_number +=1


    def reset_endo_pars(self):
        self.trans_number_old = self.trans_number
        self.trans_number = 0
        self.rest_number_old = self.rest_number


    def loose_rest(self, rest):

        self.rest_number -= 1
        self.rest_list.remove(rest)

    def gain_rest(self, rest):

        self.rest_number += 1
        self.rest_list.append(rest)



    def multihoming_members(self):
        multihomers = 0
        for rest in self.rest_list:
            if len(rest.platforms) > 1:
                multihomers += 1
        return multihomers

