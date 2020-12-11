#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 10:51:13 2019

@author: clara
class that produces various plots
"""
import matplotlib.pyplot as plt
import numpy as np

class Plot:
    #sim can also be a run (i.e. several equal simulations)
    def __init__(self, run):
        self.run = run
        self.title = 'Transactions per timestep: '+ \
                        str(self.run.con_number * self.run.con_share) + \
                         '; Restaurants: '+ str(self.run.rest_number) + \
                         '; Platforms:' + str(self.run.pf_number) + \
                         '; Runs: ' + str(self.run.runs)

    def simple_hist_plot(self, hist, var_name):
        """ hist: list of lists"""
        fig = plt.figure()
        plt.ylim(0,1.2 * np.amax(hist))
        plt.xlim(0, self.run.timesteps)
        fig.suptitle(self.title)
        for pl in range(len(hist)):
            plt.plot(hist[pl][1:])

        plt.ylabel(var_name)
        plt.xlabel('Time')
        plt.legend(['died first', 'died second', 'died last'],
                   loc='upper right')

        plt.show()



    def stackplot(self, hist, var_name):
        plot_hist = hist[:,1:]
        fig = plt.figure()
        plt.stackplot(np.arange(len(plot_hist[0])), plot_hist)
        fig.suptitle(self.title)
        plt.ylabel(var_name + ', stacked')
        plt.xlabel('Time')
        plt.legend(['died first', 'died second', 'died last'], loc='upper right')


        plt.show()
        #plots enden bei dem vorletzten zeitschritt!!!

    def stackplot_ax(self, hist, ax):
        plot_hist = hist[:,1:]
        ax.stackplot(np.arange(len(plot_hist[0])), plot_hist)




    """def hist_plot(self, interactive, time, history):


        #colors = ["r"]*self.number_of_pf_agents
        #names = ["vulnerable", "infected", "immune", "dead"]

        if self.figure is None:
            self.figure = plt.figure()
            self.figure_axes = self.figure.add_subplot(1, 1, 1)
            self.figure_axes.spines['top'].set_visible(False)
            self.figure_axes.spines['right'].set_visible(False)
            self.figure_axes.set_xlabel("Time")
            self.figure_axes.set_ylabel("Number of Members")
            self.figure_axes.set_xlim(0, self.timesteps)
            self.figure_axes.set_ylim(0, self.number_of_u_agents * 1.1)


        if interactive:
            plt.ion()

            for i in range(len(self.history)):
                if len(self.history[i]) > 1:
                    self.figure_axes.plot(self.timelist[-2:], self.history[i][-2:],"r")
                    ''', colors[i],\ label = names[i])'''
            if time == 1:
                plt.title("Membership distribution, Switching prob= "\
                          +str(self.switching_prob)+", number of platforms = "\
                          +str(self.number_of_pf_agents))
            plt.draw()
            plt.pause(.00001)
        else:
            plt.ioff()
            plt.show()"""
