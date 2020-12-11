#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 12:10:49 2019

@author: clara
class that models restaurant agents
"""

class Rest:
    def __init__(self, sim, rest_id):
        self.sim = sim #instance of Simulation class creating this rest
        self.id = rest_id

        # exogenous parameters
        self.r = 30 #weighting coefficient of network utility
        self.c_f = 150 #fixed cost of using platform
        self.min_ret = 150 #necessary min expected return to join a platform


        # endogenous parameters
        self.platforms = []

    def update_pf_memberships(self):
        self.check_leaving_pfs()
        self.check_joining_pfs()

    def check_leaving_pfs(self):
        for pf in self.platforms:
            if self.calc_ex_ret(pf) < 0:
                self.leave_pf(pf)

    def check_joining_pfs(self):
        not_joined_platforms = [pf for pf in self.sim.pfs \
                                if pf not in self.platforms]
        for pf in not_joined_platforms:
            if self.calc_ex_ret(pf) > self.min_ret:
                self.join_pf(pf)

    def calc_ex_ret(self, pf):
        if pf.rest_number_old > 0:
            ex_ret = pf.a_r + self.r * \
            pf.trans_number / pf.rest_number_old * (1-pf.p_rt) - self.c_f

        else:
            ex_ret = pf.a_r - self.c_f
        return ex_ret

    def leave_pf(self, pf):
        pf.loose_rest(self)
        self.platforms.remove(pf)
        return

    def join_pf(self,pf):
        pf.gain_rest(self)
        self.platforms.append(pf)
        pass
