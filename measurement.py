from fixed_net import *


class Measurement_models(object):
    def __init__(self,network):
        self.net = network
        self.throughput_ratio = 1
        self.net_life = 1
        self.total_energy = self.net.initial_energy*self.net.num_nodes
        self.data_latency = 0 

    def data_throughput_ratio(self):
        total_data_generated = 0
        total_data_recieved = 0
        for i in range(self.net.num_nodes):
            total_data_generated += self.net.nodes[i+1].num_gen_msg * self.net.nodes[i+1].num_sensors
        for i in  self.net.gateway_node_ids:
            total_data_recieved += self.net.nodes[i].data_recieved
        throughput_ratio = total_data_recieved/total_data_generated
        return throughput_ratio

    def lifetime(self):
        life = self.net.num_alive_nodes/self.net.num_nodes
        return life

    def net_energy(self):
        total_energy = 0
        for i in range(self.net.num_nodes):
            total_energy += self.net.nodes[i+1].energy
        return total_energy

    def avg_data_latency(self):
        tot_delay = 0
        for i in range(self.net.num_nodes):
            tot_delay += self.net.nodes[i+1].gen_msg.delay
        avg_data_latency = tot_delay/self.net.num_nodes
        return avg_data_latency

    def calculate_all_models(self):
        total_data_generated = 0
        total_data_recieved = 0
        num_alive_nodes = 0
        total_energy = 0
        tot_delay = 0
        completed_msgs = 0
        for i in range(self.net.num_nodes):
            total_data_generated += self.net.nodes[i+1].num_gen_msg * (2000 + self.net.nodes[i+1].num_sensors*1000)
            if self.net.nodes[i+1].alive == 1:
                num_alive_nodes += 1
            total_energy += self.net.nodes[i+1].energy
            if ((self.net.nodes[i+1].gen_msg.completed == True) and (self.net.nodes[i+1].alive == 1)):
                tot_delay += self.net.nodes[i+1].gen_msg.delay
                completed_msgs += 1
        for i in  self.net.gateway_node_ids:
            total_data_recieved += self.net.nodes[i].data_recieved

        self.throughput_ratio = total_data_recieved/total_data_generated
        self.net_life = num_alive_nodes/self.net.num_nodes
        self.total_energy = total_energy
        self.data_latency = tot_delay/completed_msgs