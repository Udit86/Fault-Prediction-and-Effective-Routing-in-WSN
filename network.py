from random import random
import math
import random
from node import *
from calc import *
from dijkstra import *
from q_learning import *


class network(object):
    def __init__(self,num,length,width):
        self.num_nodes = num
        self.area_length = length
        self.area_width = width
        self.net_alive = 1
        self.gateway_node_ids = [-1,-2,-3,-4]
        self.net_properties()
        self.initialise_nodes()
        self.net_graph()
        self.routing = q_route(self)
        self.alive_nodes()
    
    def initialise_nodes(self):
        print("Initialising nodes...")
        s_nodes = {}
        part = 16
        dim = int(math.sqrt(part))
        for i in range(dim):
            gx = self.area_length
            gy = self.area_width/(2*dim)+(i*self.area_width/dim)
            s_nodes[-1-i] = Node(-1-i,gx,gy,self)
            for j in range(dim):
                num_part = i*dim + j
                for k in range(num_part*self.num_nodes//part,self.num_nodes-((part-num_part-1)*self.num_nodes//part)):
                    # if k == self.num_nodes-1:
                    #     break
                    posx = random.random()*(self.area_length/dim)+(j*self.area_length/dim) 
                    posy = random.random()*(self.area_width/dim)+(i*self.area_width/dim)
                    s_nodes[k+1] = Node(k+1,posx,posy,self)
        #s_nodes[self.gateway_node_id] = Node(self.gateway_node_id,self.area_length,self.area_width,self)
        self.nodes = s_nodes
    
    def net_properties(self):
        self.initial_energy = 2
        self.E_re = 50e-9
        self.E_mp = 0.013e-12
        self.E_fs = 10e-12
        self.E_da = 5e-9
        self.thres_distance = math.sqrt(self.E_fs/self.E_mp)
        self.transmission_range = 200
        self.trans_rate = 100    ##in Kb/s
        self.trans_speed = 500   ##in m/s

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
            self.nodes[0-i].linked_nodes()                

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
        for node in self.nodes.values():
            node.__init__(node.id,node.pos_x,node.pos_y,self)