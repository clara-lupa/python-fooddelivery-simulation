#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 12:11:33 2019

@author: clara
class that models consumer agents
"""
import random
class Con:
    def __init__(self, sim, con_id):
        self.sim = sim
        self.id = con_id
        #exogenous parameters
        self.r = 0.1 #weighting coefficient of network utility

    def order(self):
        pf = self.choose_pf()
        if pf.rest_number > 0:
            pf.receive_order()

    def choose_pf(self):
        ex_rets = {}
        for pf in self.sim.pfs:
            ex_ret = self.calc_ex_ret(pf)
            pf_number = pf.id
            ex_rets[pf_number] = ex_ret

        chosen_pf_number = max(ex_rets, key = ex_rets.get)
        max_ret = ex_rets[chosen_pf_number]
        chosen_pf = self.sim.pfs[chosen_pf_number]

        # If the chosen pf has no restaurants, choose the next best which has.
        while (chosen_pf.rest_number == 0 and len(ex_rets) > 0):
            chosen_pf_number = max(ex_rets, key = ex_rets.get)
            chosen_pf = self.sim.pfs[chosen_pf_number]
            ex_rets.pop(chosen_pf_number)

        # Check for multiple maxima, if yes then pick random platform
        all_max_pf_numbers = [pf_number for pf_number in ex_rets
                      if ex_rets[pf_number] == max_ret]

        if len(all_max_pf_numbers) > 1:
            chosen_pf_number = random.choice(all_max_pf_numbers)
            chosen_pf = self.sim.pfs[chosen_pf_number]
        return chosen_pf

    def calc_ex_ret(self, pf):
        """ Calculate the expected net returns of a transaction with platform
        pf.
        """
        ex_ret = pf.a_c - pf.p_ct + pf.rest_number * self.r
        return ex_ret



