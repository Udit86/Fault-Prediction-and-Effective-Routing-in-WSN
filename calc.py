import math
import queue
import sys,os
import numpy as np

def calculate_distance(node1,node2,network):
    x1 = network.nodes[node1].pos_x
    y1 = network.nodes[node1].pos_y
    x2 = network.nodes[node2].pos_x
    y2 = network.nodes[node2].pos_y

    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return dist

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def total_delay (node1,node2,network,msg_len):
    trans_delay = msg_len/(network.trans_rate*1000)
    prop_delay = calculate_distance(node1,node2,network)/network.trans_speed
    proc_delay = np.random.exponential(scale = 0.1)
    queue_delay = np.random.poisson(lam=2)
    tot_delay = trans_delay + prop_delay + proc_delay + queue_delay
    return tot_delay