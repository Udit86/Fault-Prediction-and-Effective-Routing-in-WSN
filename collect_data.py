from attr import fields
from fixed_net import *
import random
from calc import * 
import csv

my_net = network("init_network.yaml")

data = np.empty((0,3),dtype='float32')
labels = []
num_iters = 5000
for i in range(num_iters):
    node1 = random.randint(1,my_net.num_nodes)
    node2 = random.choice(my_net.nodes[node1].neighbour_nodes)
    if random.random() < 0.95:
        labels.append(0)
        data_transmitted = my_net.header_length + my_net.msg_len_per_sensor*random.choice([1,2,3])
        energy_cons = calculate_energy_consumed(node1,node2,my_net,data_transmitted)
        t_delay = total_delay(node1,node2,my_net,data_transmitted)
    else:
        labels.append(1)
        data_transmitted = my_net.msg_len_per_sensor*random.choice([19,20])
        energy_cons = my_net.initial_energy*random.uniform(0.022,0.026)
        t_delay = random.uniform(2.4,2.7)
    curr_data = np.array([energy_cons,data_transmitted,t_delay]).reshape(1,-1)
    data = np.append(data,curr_data,axis=0)

labels = np.array(labels).reshape(num_iters,-1)
total_data = np.append(data,labels,axis=1)
fields = ["energy_cons","data_transmitted","t_delay","labels"]
with open("data.csv",'w') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(fields)
    csv_writer.writerows(total_data)