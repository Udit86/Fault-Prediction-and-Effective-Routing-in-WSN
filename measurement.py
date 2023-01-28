from fixed_net import *
import numpy as np


class Measurement_models(object):
    def __init__(self,network):
        self.net = network
        self.throughput_ratio = 1
        self.net_life = 1
        self.total_energy = self.net.initial_energy*self.net.num_nodes
        self.data_latency = 0 
        self.energy_balance = 0

    def update_energies(self):
        self.prior_energies = {}
        for i in range(self.net.num_nodes):
            self.prior_energies[i+1]=self.net.nodes[i+1].energy

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
        faulty_msgs = 0
        energy_diffs = []
        for i in range(self.net.num_nodes):
            msg_len = self.net.header_length + self.net.msg_len_per_sensor*self.net.nodes[i+1].num_sensors
            total_data_generated += self.net.nodes[i+1].num_gen_msg * (msg_len)
            if self.net.nodes[i+1].alive == 1:
                num_alive_nodes += 1
            total_energy += self.net.nodes[i+1].energy
            if ((self.net.nodes[i+1].gen_msg.completed == True) and (self.net.nodes[i+1].alive == 1)):
                tot_delay += self.net.nodes[i+1].gen_msg.delay
                completed_msgs += 1
            elif ((self.net.nodes[i+1].gen_msg.completed == False) and (self.net.nodes[i+1].alive == 1)):
                print("1")
                tot_delay += self.net.nodes[i+1].gen_msg.delay + 15
                faulty_msgs += 1
            energy_diffs.append(self.net.nodes[i+1].energy-self.prior_energies[i+1])
        for i in  self.net.gateway_node_ids:
            total_data_recieved += self.net.nodes[i].data_recieved

        self.throughput_ratio = total_data_recieved/total_data_generated
        self.net_life = num_alive_nodes/self.net.num_nodes
        self.total_energy = total_energy
        self.data_latency = tot_delay/(completed_msgs+faulty_msgs)
        self.energy_balance = np.std(energy_diffs)

    def prediction_models(prediction_results):
        TP = 0
        TN = 0
        FP = 0
        FN = 0
        for i in range(np.shape(prediction_results)[0]):
            if prediction_results[i][0] == 1:
                if prediction_results[i][1] == 1:
                    TP += 1
                else:
                    FP += 1
            else:
                if prediction_results[i][1] == 1:
                    FN += 1
                else:
                    TN += 1

        print(TP,TN,FP,FN)
        accuracy = (TP+TN)/(TP+TN+FP+FN)
        precision = TP/(TP+FP)
        recall = TP/(TP+FN)
        print(accuracy,precision,recall)

        return accuracy,precision,recall