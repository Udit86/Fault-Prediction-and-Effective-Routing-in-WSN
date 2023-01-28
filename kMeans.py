from collections import defaultdict
from email.policy import default
from sklearn.cluster import KMeans
import numpy as np
from calc import *

class K_means():
    def __init__(self,net):
        self.net = net
        self.num_clusters = calculate_num_clusters(net)
        #self.num_clusters = 20
        self.make_clusters()
        self.heads_gate = {}
        self.cluster_heads = {}
        self.setup_phase()

    def make_clusters(self):
        print("Making cluster using K-Means++...")
        coordinates_array = np.empty((0,2),dtype='float32')
        for i in range(self.net.num_nodes):
            position = np.array([self.net.nodes[i+1].pos_x,self.net.nodes[i+1].pos_y]).reshape(1,-1)
            coordinates_array = np.append(coordinates_array,position,axis = 0)

        kmeans = KMeans(n_clusters = self.num_clusters,random_state = 0).fit(coordinates_array)
        self.clusters = defaultdict(list)
        for i in range(self.net.num_nodes):
            self.clusters[kmeans.labels_[i]].append(i+1)
        #print(self.clusters)
        
    def setup_phase(self):
        print("Modified K-Means ++ : Setup Phase.")
        heads_gate = {}
        cluster_heads = {}
        for cluster in self.clusters.values():
            max_energy = 0
            max_energy_node = 0
            for node in cluster:
                if self.net.nodes[node].energy > max_energy:
                    max_energy = self.net.nodes[node].energy
                    max_energy_node = node
            for node in cluster:
                if node == max_energy_node:
                    nearest_gateway = self.net.gateway_node_ids[0]
                    for gateway in self.net.gateway_node_ids[1:]:
                        if calculate_distance(node,nearest_gateway,self.net) > calculate_distance(node, gateway,self.net):
                            nearest_gateway = gateway
                    heads_gate[node] = nearest_gateway
                else:
                    cluster_heads[node] = max_energy_node
        
        self.heads_gate = heads_gate
        self.cluster_heads = cluster_heads
        # print(self.cluster_heads)
        # print(self.heads_gate)

    def get_path(self,origin):
        path = [origin]
        if origin in self.heads_gate.keys():
            path.append(self.heads_gate[origin])
            #print("yes")
        else:
            #print("no")
            path.append(self.cluster_heads[origin])
            path.append(self.heads_gate[self.cluster_heads[origin]])
        return path