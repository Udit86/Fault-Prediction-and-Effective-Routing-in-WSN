from email import message
from pickle import FALSE, NONE
from calc import *
from message import *
from lof import *
import numpy as np
import random
import string
from colorama import Back,Style

class Node(object):
    def __init__(self,id,x,y,num_sensors,network):
        self.id = id
        self.pos_x = x
        self.pos_y = y
        self.net = network
        self.num_sensors = num_sensors
        self.fault_predictor = predictor()
        self.pred_faulty = 1
        self.faulty = 1
        self.set_fault = FALSE
        self.num_gen_msg = 0
        if id in self.net.gateway_node_ids:
            self.energy = 10
        else:
            self.energy = self.net.initial_energy
        self.data_recieved = 0
        self.data_transmitted = 0
        self.queue_size = 0
        self.interference = 0
        self.t_delay = 0
        self.lof = 0
        self.node_data = np.empty((0,6),dtype='float32')
        self.alive = 1
        self.state = [self.energy,self.interference,self.queue_size,self.data_transmitted,self.data_recieved,self.t_delay]
    
    def generate_msg(self):
        if self.faulty == -1 or self.alive == -1:
            print(Back.RED+"Message cannot be generated ! at node %d"%(self.id))
            print(Style.RESET_ALL)
            return
        msg_content = ''.join(random.choices(string.ascii_letters + string.digits, k = 2000 + self.num_sensors*1000))
        self.gen_msg = message(msg_content,self.id,self.net)
        self.queue_size += len(msg_content)
        self.num_gen_msg += 1
        # if self.num_gen_msg >=100:
        #     self.fault_predictor.fit_predictor(self.node_data)
        self.curr_msg = self.gen_msg
        self.transmit_msg(self.gen_msg)
    
    def recieve_msg(self,msg):
        if not self.id == msg.path[0]:
            print("Node %d recieving msg"%self.id)
        msg.update_current_node(self.id)
        self.curr_msg = msg
        energy_consumed = self.net.E_re*self.curr_msg.msg_len
        self.energy -= energy_consumed
        self.data_recieved += self.curr_msg.msg_len
        self.queue_size += self.curr_msg.msg_len
        if self.curr_msg.next_node == NONE:
            print("Message recieved at Node %d"%(self.id))
            self.curr_msg.completed = True
            pass
        elif self.faulty == -1 or self.alive == -1:
            print(Back.RED+"Message cannot be transmitted !")
            print(Style.RESET_ALL)
            return
        else:
            self.transmit_msg(self.curr_msg)        

    def transmit_msg(self,msg):
        print("Transmitting msg from Node %d to Node %d"%(self.id,msg.next_node))
        distance = calculate_distance(self.id,msg.next_node,self.net)
        energy_consumed = self.net.E_re*msg.msg_len
        if distance >= self.net.thres_distance:
            energy_consumed += self.net.E_mp*(distance**4)*msg.msg_len
        else :
            energy_consumed += self.net.E_fs*(distance**2)*msg.msg_len
        self.energy -= energy_consumed 
        self.t_delay = total_delay(self.id,msg.next_node,self.net,msg.msg_len)
        self.curr_msg.delay += self.t_delay
        self.data_transmitted += msg.msg_len
        self.queue_size -= msg.msg_len
        self.update_interference()
        #self.predict_fault()
        self.net.nodes[msg.next_node].recieve_msg(msg)
        if self.set_fault == TRUE:
            self.energy -= self.net.initial_energy*0.025
            self.data_transmitted += 30000
            self.t_delay += 0.5  
            self.update_interference()
            if random.random() > 0.25:
                self.faulty = -1
        self.update_data()
        self.dead_node()
    
    def dead_node(self):
        if self.energy <=(self.net.E_re + self.net.E_fs)*4000:
            self.alive=-1

    def update_interference(self):
        total_net_trans = 0
        for i in range(self.net.num_nodes) :
            total_net_trans += self.net.nodes[i+1].data_transmitted
        self.interference = (self.data_transmitted/total_net_trans)*100 

    def linked_nodes(self):
        self.neighbour_nodes = self.net.graph.edges[self.id]

    def update_data(self):
        self.state = [self.energy,self.interference,self.queue_size,self.data_transmitted,self.data_recieved,self.t_delay]
        curr_state = np.array(self.state).reshape(1,-1)
        self.node_data = np.append(self.node_data,curr_state,axis = 0)
        if self.num_gen_msg>=100:
            np.delete(self.node_data,0,0)

    def predict_fault(self):
        # curr_state = np.array([self.num_sensors,self.energy,self.interference,self.queue_size,self.data_transmitted,self.data_recieved,self.t_delay]).reshape(1,-1)
        # self.node_data = np.append(self.node_data,curr_state,axis = 0)
        self.pred_faulty, self.lof = self.fault_predictor.predict_outlier(self.node_data)
        #print("LOF of node %d : %f"%(self.id,self.lof))
        if self.pred_faulty == -1:
            print(Back.GREEN+"Node %d is prone to a fault."%(self.id))
            print(Style.RESET_ALL)

    def generate_fault(self):
        print(Back.YELLOW+"Generating Fault on node %d"%(self.id))
        print(Style.RESET_ALL)
        self.set_fault = TRUE
        self.energy -= self.net.initial_energy*0.025
        self.data_transmitted += 30000
        self.t_delay += 0.5  
        self.update_interference()
        self.update_data()