from math import dist
from pickle import NONE
import fixed_net as net
from dijkstra import *

class message(object):
    def __init__(self,msg,initial,network):
        self.msg = msg
        self.msg_len = len(msg)
        self.net = network
        self.origin = initial
        self.hop_id = 0
        self.delay = 0
        self.completed = False
        print("Generating message from Node %d..."%(self.origin))
        self.get_path()
        self.update_current_node(self.origin)
        #self.start_msg()
    
    def get_path(self):
        paths = defaultdict(list)
        rewards = {}
        for i in range(4):
            #path = dijsktra(self.net.graph,self.origin,self.net.gateway_node_ids[i])
            path = self.net.routing.get_best_path(self.origin,self.net.gateway_node_ids[i],self.msg_len)
            paths[self.net.gateway_node_ids[i]] = path[:-1]
            rewards[self.net.gateway_node_ids[i]] = path[-1]
            #distances[self.net.gateway_node_ids[i]] = path[-1]
        max_reward_node = max(rewards.items(), key=lambda x: x[1])
        #min_dist_node = min(distances.items(), key=lambda x: x[1])
        self.path=paths[max_reward_node[0]]
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