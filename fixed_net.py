from random import random
import math
import random

import yaml
from node import *
from calc import *
from dijkstra import *
from q_learning import *


class network(object):
    def __init__(self,input):
        self.num_nodes = 100
        self.area_length = 80
        self.area_width = 80
        self.net_alive = 1
        self.gateway_node_ids = [-1,-2,-3,-4]
        self.net_properties()
        self.initialise_nodes(input)
        self.net_graph()
        self.routing = q_route(self)
        self.alive_nodes()
    
    def initialise_nodes(self,inp_file):
        print("Initialising nodes...")
        s_nodes = {}
        file = open(inp_file,"r")
        nodes_list = yaml.full_load(file)
        for node , info in nodes_list.items():
            s_nodes[node] = Node(node,info[0],info[1],info[2],self)
        self.nodes = s_nodes
    
    def net_properties(self):
        self.initial_energy = 2
        self.E_re = 50e-9
        self.E_mp = 0.204e-12
        self.E_fs = 10e-12
        self.E_da = 5e-9
        self.thres_distance = math.sqrt(self.E_fs/self.E_mp)
        self.transmission_range = 15 #in m
        self.trans_rate = 250    ##in Kb/s
        self.trans_speed = 3*(10**8)   ##in m/s

    def net_graph(self):
        self.graph = Graph(self)
        ##Adding Sensor Nodes
        for i in range(1,self.num_nodes+1):
            for j in range(i+1,self.num_nodes+1):
                distance = calculate_distance(i,j,self)
                if distance <= self.transmission_range:
                    self.graph.add_edge(i,j,distance)
        ##Adding Gateway Nodes
        for i in range(1,5):
            for j in range(1,self.num_nodes+1):
                distance = calculate_distance(0-i,j,self)
                if distance <= self.transmission_range:
                    self.graph.add_edge(0-i,j,distance)

        for i in range(self.num_nodes) :
            self.nodes[i+1].linked_nodes()
        for i in range(1,5) :
            self.nodes[-i].linked_nodes()                

    def alive_nodes(self):
        num_alive = 0
        for i in range(self.num_nodes):
            if self.nodes[i+1].alive == 1:
                num_alive += 1
        self.num_alive_nodes = num_alive

    def generate_all_msgs(self):
        map(lambda x:x.generate_msg(),self.nodes)

    def check_deadnet(self):
        self.alive_nodes()
        if not self.num_alive_nodes == self.num_nodes:
            self.net_alive = 0

    def reset_nodes(self):
        print("Resetting Nodes...")
        for node in self.nodes.values():
            node.__init__(node.id,node.pos_x,node.pos_y,node.num_sensors,self)