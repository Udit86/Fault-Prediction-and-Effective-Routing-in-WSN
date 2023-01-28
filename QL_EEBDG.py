from collections import defaultdict
from csv import reader
from email.policy import default
from importlib.resources import path


import numpy as np
import random
from calc import *

class QL_EEBDG():
    def __init__(self,network):
        self.net = network
        self.lr = 0.01
        self.discount_factor = 0.9
        self.epsilon = 1
        self.q_table = {}
        self.initialise_qtable()

    def initialise_qtable(self):
        for node in self.net.nodes:
            self.q_table[node] = {}
            for neighbour in self.net.nodes[node].neighbour_nodes:
                # if neighbour in self.net.gateway_node_ids:
                #     self.q_table[node][neighbour] = 500
                # else:    
                #     self.q_table[node][neighbour] = 0
                    #self.q_table[node][neighbour] = -2 + ((self.net.nodes[neighbour].pos_x-self.net.nodes[node].pos_x)/self.net.transmission_range)
                self.q_table[node][neighbour] = 0

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
    
    def calc_average_energy(self,node):
        tot = 0
        for neighbour in self.net.nodes[node].neighbour_nodes:
            tot += self.net.nodes[neighbour].energy
        return (tot/len(self.net.nodes[node].neighbour_nodes))

    def calculate_reward(self,curr_loc,path,msg_len):
        next_loc = path[-1]
        hop_count = len(path)
        cp_s = 1 - self.net.nodes[curr_loc].energy/self.net.initial_energy
        cp_r = 1 - self.net.nodes[next_loc].energy/self.net.initial_energy
        E_s = self.calc_average_energy(curr_loc)
        E_r = self.calc_average_energy(next_loc)
        gp_s = (2/math.pi)*math.atan(self.net.nodes[curr_loc].energy) - E_s
        gp_r = (2/math.pi)*math.atan(self.net.nodes[next_loc].energy) - E_r
        R_s = -1 - 0.5*(cp_s + cp_r) + 0.05*(gp_s + gp_r)
        R_f = -1 -0.5*cp_s + 0.05*gp_s
        P_s = 1/len(self.net.nodes[curr_loc].neighbour_nodes)
        if next_loc in self.net.gateway_node_ids:
            reward = -1
        else:
            reward = P_s*R_s + (1 - P_s)*R_f
            if next_loc in path[:-1]:
                reward -= 500
        #reward = P_s*R_s + (1 - P_s)*R_f
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
            # elif next_loc in self.net.gateway_node_ids:
            #     reward = -100
            else:
                reward = self.calculate_reward(curr_loc,shortest_path,msg_len)
            total_reward += reward
            rewards[(curr_loc,next_loc)] = reward
            #if not self.epsilon == 1: 
            #self.update_q_value(curr_loc,shortest_path,reward)
            curr_loc=next_loc
        shortest_path.append(total_reward)
        return shortest_path ,rewards