import numpy as np
import random
from calc import *

class LEACH(object):
    def __init__(self,net):
        self.net = net
        self.num_clusters = calculate_num_clusters(net)
        #self.num_clusters = 
        self.rounds_table = {node+1:0 for node in range(self.net.num_nodes)}
        self.rounds = 0
        self.heads_gate = {}
        self.cluster_heads = {}
        self.setup_phase()
        
    def setup_phase(self):
        print('LEACH: setup phase.')
        # decide which network are cluster heads
        #prob_ch = float(self.num_clusters)/float(self.net.num_nodes)
        heads = []
        alive_nodes = self.net.alive_nodes()
        print('LEACH: deciding which nodes are cluster heads.')
        idx = 0
        loop = 0
        while len(heads) != self.num_clusters:
            if loop == self.net.num_nodes*4:
                self.rounds_table =  {node+1:0 for node in range(self.net.num_nodes)}
                self.rounds = 0
                loop = 0
            node = alive_nodes[idx]
            if self.rounds - self.rounds_table[node]< (self.rounds%(int(self.net.num_nodes/self.num_clusters))):
                prob = 0
            else :
                prob = self.num_clusters/(self.net.num_nodes - self.num_clusters*(self.rounds%(int(self.net.num_nodes/self.num_clusters))))
            # node will be a cluster head
            if random.random() < prob:
                #node.next_hop = cf.BSID
                heads.append(node)
                self.rounds_table[node] = self.rounds + 1
        
            idx = idx+1 if idx < len(alive_nodes)-1 else 0
            loop += 1

        # ordinary network choose nearest cluster heads
        print('LEACH: ordinary nodes choose nearest nearest cluster head')
        heads_gate = {}
        cluster_heads = {}
        for node in alive_nodes:
            if node in heads: # node is cluster head
                nearest_gateway = self.net.gateway_node_ids[0]
                for gateway in self.net.gateway_node_ids[1:]:
                    if calculate_energy_consumed(node, nearest_gateway,self.net,4000) > calculate_energy_consumed(node, gateway,self.net,4000):
                        nearest_gateway = gateway
                heads_gate[node] = nearest_gateway
                continue
            nearest_head = heads[0]
            # find the nearest cluster head
            for head in heads[1:]:
                if calculate_energy_consumed(node, nearest_head,self.net,4000) > calculate_energy_consumed(node, head,self.net,4000):
                    nearest_head = head

            cluster_heads[node] = nearest_head

        self.cluster_heads = cluster_heads
        self.heads_gate = heads_gate
        self.rounds += 1
        print(self.num_clusters)
        print(heads)

    def get_path(self,origin):
        path = [origin]
        if origin in self.heads_gate.keys():
            path.append(self.heads_gate[origin])
            print("yes")
        else:
            print("no")
            path.append(self.cluster_heads[origin])
            path.append(self.heads_gate[self.cluster_heads[origin]])
        return path