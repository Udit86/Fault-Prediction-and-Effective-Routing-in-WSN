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

def calculate_energy_consumed(node1,node2,network,msg_len):
    distance = calculate_distance(node1,node2,network)
    energy_consumed = network.E_re*msg_len
    if distance >= network.thres_distance:
        energy_consumed += network.E_mp*(distance**4)*msg_len
    else :
        energy_consumed += network.E_fs*(distance**2)*msg_len
    return energy_consumed

def calculate_num_clusters(network):
    term1 = math.sqrt(network.num_nodes)/(math.sqrt(2*math.pi))
    term2 = network.thres_distance
    avg_gateway_distance = 0
    for i in range(network.num_nodes):
        avg_gateway_distance += network.nodes[i+1].pos_x
    avg_gateway_distance = avg_gateway_distance/network.num_nodes
    print(avg_gateway_distance)
    term3 = network.area_width/(avg_gateway_distance**2)
    return int(term1*term2*term3)

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def total_delay (node1,node2,network,msg_len):
    trans_delay = msg_len/(network.trans_rate*1000)
    prop_delay = calculate_distance(node1,node2,network)/network.trans_speed
    proc_delay = np.random.exponential(scale = 0.5)
    queue_delay = np.random.poisson(lam=1)
    tot_delay = trans_delay + prop_delay + proc_delay + queue_delay
    return tot_delay