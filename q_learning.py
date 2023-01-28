from collections import defaultdict
from csv import reader
from email.policy import default
from importlib.resources import path


import numpy as np
import random
from calc import *

class q_route():
    def __init__(self,network):
        self.net = network
        self.lr = 0.01
        self.discount_factor = 0.9
        self.epsilon = 1
        self.q_table = {}
        self.initialise_qtable()
        self.initialise_max_min_values()

    def initialise_qtable(self):
        for node in self.net.nodes:
            self.q_table[node] = {}
            for neighbour in self.net.nodes[node].neighbour_nodes:
                if neighbour in self.net.gateway_node_ids:
                    self.q_table[node][neighbour] = 500
                else:    
                    #self.q_table[node][neighbour] = -2 - (calculate_distance(node,neighbour,self.net)/self.net.transmission_range)
                    self.q_table[node][neighbour] = -2 + ((self.net.nodes[neighbour].pos_x-self.net.nodes[node].pos_x)/self.net.transmission_range)

    def initialise_max_min_values(self):
        self.min_en_r = 1
        self.max_en_r = 1
        self.min_t = 5
        self.max_t = 0
        self.min_int_r = 1
        self.max_int_r = 0
        self.min_d_ratio = 1
        self.max_d_ratio = 0
    
    def update_max_min_values(self,en_r,t_delay,d_ratio,int_r):
        if en_r <= self.min_en_r:
            self.min_en_r = en_r
        
        if t_delay >= self.max_t:
            self.max_t = t_delay
        if t_delay <= self.min_t:
            self.min_t = t_delay

        if d_ratio >= self.max_d_ratio:
            self.max_d_ratio = d_ratio
        if d_ratio <= self.min_d_ratio:
            self.min_d_ratio = d_ratio
        
        if int_r >= self.max_int_r:
            self.max_int_r = int_r
        if int_r <= self.min_int_r:
            self.min_int_r = int_r



    def get_normalized_values(self,e_ratio,t_delay,d_ratio,int_ratio):
        try:
            n_e_ratio = (e_ratio - self.min_en_r)/(self.max_en_r - self.min_en_r)
        except:
            n_e_ratio = 1

        try:
            n_t_delay = (t_delay - self.min_t)/(self.max_t - self.min_t)
        except:
            n_t_delay = 1

        try:
            n_d_ratio = (d_ratio - self.min_d_ratio)/(self.max_d_ratio - self.min_d_ratio)
        except:
            n_d_ratio = 1

        try:
            n_int_ratio = (int_ratio - self.min_int_r)/(self.max_int_r - self.min_int_r)
        except:
            n_int_ratio = 1

        return n_e_ratio,n_t_delay,n_d_ratio,n_int_ratio

    def get_next_action(self,curr_loc,path,epsilon):
        #print(path)
        if random.random() < epsilon:
            # next_loc = max(self.q_table[curr_loc], key=lambda k: self.q_table[curr_loc][k][1])
            next_loc = max(self.q_table[curr_loc].items(), key=lambda x: x[1])[0]
        else:
            next_loc = random.choice(list(self.q_table[curr_loc]))
        if epsilon == 1:
            while next_loc in path:
                second = -5
                for v in self.q_table[curr_loc].values():
                    if (v>second and v < self.q_table[curr_loc][next_loc]):
                        second = v
                if second == -5:
                    next_loc = random.choice(list(self.q_table[curr_loc]))
                    break
                next_loc = [k for k,v in self.q_table[curr_loc].items() if v==second][0]
            #next_loc = random.choice(list(self.q_table[curr_loc]))
            #print(second,curr_loc,next_loc)
        return next_loc
    
    def calculate_reward(self,curr_loc,path,msg_len):
        next_loc = path[-1]
        hop_count = len(path)
        t_delay = total_delay(curr_loc,next_loc,self.net,msg_len)
        e_ratio = self.net.nodes[next_loc].energy/self.net.initial_energy
        d_ratio = (calculate_distance(curr_loc,next_loc,self.net)/self.net.transmission_range)**2
        int_ratio = self.net.nodes[next_loc].interference
        self.update_max_min_values(e_ratio,t_delay,d_ratio,int_ratio)
        n_e_ratio , n_t_delay , n_d_ratio , n_int_ratio = self.get_normalized_values(e_ratio,t_delay,d_ratio,int_ratio)
        if next_loc in self.net.gateway_node_ids:
            reward = -1
        else:
            reward = -1 + (n_e_ratio - n_t_delay)
            reward = (hop_count**self.discount_factor)*reward
            if next_loc in path[:-1]:
                reward -= 500
        #print(reward)
        return reward

    def update_q_value(self,node,next,reward):
        max_next_qvalue = max(self.q_table[next].items(), key=lambda x: x[1])[1]
        q_val = self.q_table[node][next]
        self.q_table[node][next] = (1-self.lr)*q_val + self.lr*(reward + self.discount_factor*max_next_qvalue)

    def avoid_faulty_nodes(self,nodes):
        for node in nodes:
            for neighbour in self.net.nodes[node].neighbour_nodes:
                #self.q_table[neighbour][node] = -50000
                self.q_table[neighbour][node] = min(self.q_table[neighbour].items(), key=lambda x: x[1])[1] - 1

    def avoid_dead_nodes(self,dead):
        for node in dead:
            for neighbour in self.net.nodes[node].neighbour_nodes:
                self.q_table[neighbour][node] = min(self.q_table[neighbour].items(), key=lambda x: x[1])[1] - 1
    
    def get_best_path(self,start,end,msg_len):
        total_reward = 0
        curr_loc = start
        shortest_path = []
        shortest_path.append(curr_loc)
        rewards = {}
        while not curr_loc==end:
            #print(shortest_path)
            #print(self.q_table)
            next_loc = self.get_next_action(curr_loc,shortest_path,self.epsilon)
            shortest_path.append(next_loc)
            if next_loc == end:
                reward = 100
            elif next_loc in self.net.gateway_node_ids:
                reward = -100
            else:
                reward = self.calculate_reward(curr_loc,shortest_path,msg_len)
            total_reward += reward
            rewards[(curr_loc,next_loc)] = reward
            #if not self.epsilon == 1: 
            #self.update_q_value(curr_loc,shortest_path,reward)
            curr_loc=next_loc
        shortest_path.append(total_reward)
        return shortest_path ,rewards