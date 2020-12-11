#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 11:43:45 2019

@author: clara
class that controlls the simulation, i.e. the restaurants, consumers and platform agents
"""
from Rest import Rest
from Con import Con
from PF import PF
import random
import numpy as np

class Simulation:
    def __init__(self, timesteps, pf_number, con_number, con_share, rest_number):
        # exogenous parameters
        self.con_number = con_number
        self.rest_number = rest_number
        self.pf_number = pf_number
        self.con_share = con_share
        self.timesteps = timesteps

        # endogenous parameters stored in numpy arrays
        """modify single elements: hist[pf_number, timestep] = new_value"""
        self.trans_distrib_hist = \
                    np.zeros([self.pf_number, self.timesteps])
        self.rest_distrib_hist = \
                    np.zeros([self.pf_number, self.timesteps])
        self.multihomers_distrib_hist = \
                    np.zeros([self.pf_number, self.timesteps])

        # agents
        self.cons = self.create_cons()
        self.rests = self.create_rests()
        self.pfs = self.create_pfs()
        self.assign_init_rest()

    def assign_init_rest(self):
        for pf in self.pfs:
            chosen_rest_numbers = self.choose_rests(5)#3)
            for rest_number in chosen_rest_numbers:
                self.rests[rest_number].join_pf(pf)
        self.update_endo_pars(0)

    def iterate(self):
        for t in range(1,self.timesteps):
            self.carry_out_transactions()
            self.iterate_over_rests()
            self.update_endo_pars(t)
            """print(t, 'transactions:', self.trans_distrib_hist[:,-1:],
                  'restaurants:', self.rest_distrib_hist[:,-1:],
                  'multihoming rests:', self.multihomers_distrib_hist[:,-1:])"""

        return self.trans_distrib_hist, self.rest_distrib_hist, \
                self.multihomers_distrib_hist

    def iterate_over_rests(self):
        for rest in self.rests:
            rest.update_pf_memberships()
        return

    def carry_out_transactions(self):
        chosen_con_numbers = self.choose_cons()
        self.iterate_over_cons(chosen_con_numbers)

    def iterate_over_cons(self, chosen_con_numbers):
        for con_number in chosen_con_numbers:
            con = self.cons[con_number]
            con.order()
        return

    def update_endo_pars(self, t):

        for pf in self.pfs:
            self.rest_distrib_hist[pf.id, t] = pf.rest_number
            self.trans_distrib_hist[pf.id, t] = pf.trans_number
            pf.reset_endo_pars()
            self.multihomers_distrib_hist[pf.id, t] = pf.multihoming_members()

        return


    def create_cons(self):
        """Initialize the consumers. Return a list of instances of the consumer
        class.
        """
        cons =[]
        for con_id in range(self.con_number):
            con = Con(self, con_id)
            cons = cons + [con]

        return cons

    def create_rests(self):
        """Initialize the restaurants. Return a list of instances of the
        restaurant class.
        """
        rests =[]
        for rest_id in range(self.rest_number):
            rest = Rest(self, rest_id)
            rests = rests + [rest]

        return rests

    def create_pfs(self):
        """Initialize the platforms. Return a list of instances of the platform
        class.
        """
        pfs =[]
        for pf_id in range(self.pf_number):
            pf = PF(self, pf_id)
            pfs = pfs + [pf]

        return pfs

    def choose_cons(self):
        """ Pick a random subset of consumers of the size of the consumer
        share. Return their position in the list of all cons.
        """
        chosen_con_numbers = random.sample(range(self.con_number),int(round(\
                                           self.con_share * self.con_number)))
        return chosen_con_numbers

    def choose_rests(self, size):
        """ Pick a random subset of restaurnts of a given size.
        Return their position in the list of all rests.
        """
        chosen_rest_numbers = random.sample(range(self.rest_number),size)
        return chosen_rest_numbers

