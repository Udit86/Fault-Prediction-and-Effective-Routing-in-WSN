from math import dist
from pickle import NONE, TRUE
import fixed_net as net
from dijkstra import *
from calc import *

class message(object):
    def __init__(self,msg,initial,network):
        self.msg = msg
        self.msg_len = len(msg)
        self.net = network
        self.origin = initial
        self.hop_id = 0
        self.delay = 0
        self.da = False
        self.completed = False
        print("Generating message from Node %d..."%(self.origin))
        self.get_path()
        #self.get_leach_path()
        #self.get_beemh_path()
        #self.get_kmeans_path()
        #self.get_nmleach_path()
        #self.get_dt_path()
        #self.get_ql_eebdg_path()
        self.update_current_node(self.origin)
        #self.start_msg()
    
    def get_path(self):
        paths = defaultdict(list)
        pair_rewards = {}
        path_rewards = {}
        for i in range(4):
            #path = dijsktra(self.net.graph,self.origin,self.net.gateway_node_ids[i])
            path, rew = self.net.routing.get_best_path(self.origin,self.net.gateway_node_ids[i],self.msg_len)
            paths[self.net.gateway_node_ids[i]] = path[:-1]
            pair_rewards[self.net.gateway_node_ids[i]] = rew
            path_rewards[self.net.gateway_node_ids[i]] = path[-1]
            #distances[self.net.gateway_node_ids[i]] = path[-1]
        max_reward_node = max(path_rewards.items(), key=lambda x: x[1])
        #min_dist_node = min(distances.items(), key=lambda x: x[1])
        self.reward_pairs = pair_rewards[max_reward_node[0]]
        self.path=paths[max_reward_node[0]]
        print("Path of message :- ",self.path)

    def get_leach_path(self):
        self.path = self.net.leach_routing.get_path(self.origin)
        print("Path of message :- ",self.path)

    def get_beemh_path(self):
        paths = defaultdict(list)
        costs = {}
        for i in range(4):
            path = self.net.beemh_routing.get_path(self.origin,self.net.gateway_node_ids[i])
            #path = self.net.routing.get_best_path(self.origin,self.net.gateway_node_ids[i],self.msg_len)
            paths[self.net.gateway_node_ids[i]] = path[:-1]
            costs[self.net.gateway_node_ids[i]] = path[-1]
            #distances[self.net.gateway_node_ids[i]] = path[-1]
        min_cost_node = min(costs.items(), key=lambda x: x[1])
        #min_dist_node = min(distances.items(), key=lambda x: x[1])
        self.path=paths[min_cost_node[0]]
        print("Path of message :- ",self.path)

    def get_kmeans_path(self):
        self.path = self.net.kmeans_routing.get_path(self.origin)
        print("Path of message :- ",self.path)

    def get_nmleach_path(self):
        self.path = self.net.nmleach_routing.get_path(self.origin)
        print("Path of message :- ",self.path)

    def get_ql_eebdg_path(self):
        paths = defaultdict(list)
        pair_rewards = {}
        path_rewards = {}
        for i in range(4):
            #path = dijsktra(self.net.graph,self.origin,self.net.gateway_node_ids[i])
            path, rew = self.net.ql_eebdg_routing.get_best_path(self.origin,self.net.gateway_node_ids[i],self.msg_len)
            paths[self.net.gateway_node_ids[i]] = path[:-1]
            pair_rewards[self.net.gateway_node_ids[i]] = rew
            path_rewards[self.net.gateway_node_ids[i]] = path[-1]
            #distances[self.net.gateway_node_ids[i]] = path[-1]
        max_reward_node = max(path_rewards.items(), key=lambda x: x[1])
        #min_dist_node = min(distances.items(), key=lambda x: x[1])
        self.reward_pairs = pair_rewards[max_reward_node[0]]
        self.path=paths[max_reward_node[0]]
        print("Path of message :- ",self.path)

    def get_dt_path(self):
        min_energy = math.inf
        min_energy_node = 0
        for i in range(4):
            consumption = calculate_energy_consumed(self.origin,self.net.gateway_node_ids[i],self.net,self.msg_len)
            if consumption < min_energy:
                min_energy = consumption
                min_energy_node = self.net.gateway_node_ids[i]
        self.path = [self.origin,min_energy_node]
        print("Path of message :- ",self.path)

    def update_current_node(self,id):
        self.current_node = id
        self.hop_id += 1
        if self.current_node == self.path[-1]:
            self.next_node = NONE
        else:
            self.update_next_node()

    def update_next_node(self):
        self.next_node = self.path[self.hop_id]

    # def start_msg(self):
    #     self.net.nodes[self.path[0]].recieve_msg(self)