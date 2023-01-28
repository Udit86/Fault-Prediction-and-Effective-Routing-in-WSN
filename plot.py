from cProfile import label
from typing import NewType
import matplotlib.pyplot as plt

class net_view(object):
    def __init__(self,network):
        self.net = network
        self.net_view = self.plot_network('Network View')
    
    def plot_network(self,name):
        self.view = plt.figure()
        plt.title( label=name)
        for node in self.net.nodes:
            plt.scatter(self.net.nodes[node].pos_x,self.net.nodes[node].pos_y,label='nodes',color='red',marker='o',s=10)
            plt.annotate(str(self.net.nodes[node].id),(self.net.nodes[node].pos_x,self.net.nodes[node].pos_y+0.1))
            for j in self.net.nodes[node].neighbour_nodes:
                plt.plot([self.net.nodes[node].pos_x,self.net.nodes[j].pos_x],[self.net.nodes[node].pos_y,self.net.nodes[j].pos_y],color = 'cyan')
        return self.view

    def plot_msg_paths(self,paths):
        fig = self.plot_network('Message route')
        for path in paths:
            plt.plot([self.net.nodes[i].pos_x for i in path],[self.net.nodes[i].pos_y for i in path],figure = fig,color = 'red')