from numpy import block
from fixed_net import *
from message import *
from plot import *
from calc import *
from measurement import *
import matplotlib.pyplot as plt
import random
import string
from colorama import Back,Style

# num_nodes = int(input("Enter the total number of nodes : "))
# net_length = int(input("Enter the length of network (in m) : "))
# net_width = int(input("Enter the width of network (in m) : "))

# my_net = network(num_nodes,net_length,net_width)
my_net = network("init_network.yaml")
view = net_view(my_net)

###---TRAINING THE Q-LEARNING ALGORITHM---###
print("Training the q-learning algorithm...")
blockPrint()
for i in range(10000):
    print(i)
    start = random.randint(1,my_net.num_nodes)
    print(start)
    msg_len = 2000 + my_net.nodes[start].num_sensors*1000
    curr_state = start
    path=[]
    path.append(curr_state)
    while not curr_state in my_net.gateway_node_ids:
        #print(my_net.routing.q_table)
        next_state = my_net.routing.get_next_action(curr_state,path,0.9)
        path.append(next_state)
        ###---Updating Energy of nodes after transmission---###
        distance = calculate_distance(curr_state,next_state,my_net)
        t_energy_consumed = my_net.E_re*msg_len
        if distance >= my_net.thres_distance:
            t_energy_consumed += my_net.E_mp*(distance**4)*msg_len
        else :
            t_energy_consumed += my_net.E_fs*(distance**2)*msg_len
        my_net.nodes[curr_state].energy -= t_energy_consumed
        r_energy_consumed = my_net.E_re*msg_len
        my_net.nodes[next_state].energy -= r_energy_consumed
        # my_net.nodes[curr_state].data_transmitted += msg_len
        # my_net.nodes[curr_state].update_interference()
        ###---Updating q-value of curr node---###
        if next_state in my_net.gateway_node_ids:
            reward = 1000
        else:
            reward = my_net.routing.calculate_reward(curr_state,path,msg_len)
        my_net.routing.update_q_value(curr_state,path,reward)
        curr_state=next_state
    print(path)
enablePrint()
print("Training Complete")
#print(my_net.routing.q_table)


my_net.reset_nodes()
models = Measurement_models(my_net)

Measurement_data = np.empty((0,4),dtype='float32')
init_data = np.array([models.throughput_ratio,models.net_life,models.total_energy,models.data_latency]).reshape(1,-1)
Measurement_data = np.append(Measurement_data,init_data, axis = 0)

#blockPrint()

k=0
while True :
    k=k+1
    #my_net.check_deadnet()
    # if my_net.net_alive == 0:
    #     break

    if k == 200:
        print(Back.CYAN+"%d"%(k))
        print(Style.RESET_ALL)
    else:
        print(k)

    #blockPrint()
    if k >= 200:
        if random.random() > 0.97:
            f_node = random.randint(1,my_net.num_nodes)
            my_net.nodes[f_node].generate_fault()

    faulty = []
    Dead = []
    if k > 50:
        for i in range(my_net.num_nodes):
            my_net.nodes[i+1].predict_fault()
            if my_net.nodes[i+1].pred_faulty == -1:
                faulty.append(i+1)
            if my_net.nodes[i+1].alive == -1:
                Dead.append(i+1)
    print(faulty)
    print(Dead)
    my_net.routing.avoid_faulty_nodes(faulty)
    my_net.routing.avoid_dead_nodes(Dead)

    for i in range(my_net.num_nodes):
        my_net.nodes[i+1].generate_msg()
        
    if k >= 50:
        for i in range(my_net.num_nodes):
            my_net.nodes[i+1].fault_predictor.fit_predictor(my_net.nodes[i+1].node_data)

    if k in [400,600,800,1000,1200,1600,2000]:
        models.calculate_all_models()
        curr_data = np.array([models.throughput_ratio,models.net_life,models.total_energy,models.data_latency]).reshape(1,-1)
        Measurement_data = np.append(Measurement_data,curr_data, axis = 0)
        if k == 2000:
            break

    #enablePrint()
    # my_net.generate_all_msgs()
    # view.plot_msg_paths([my_net.nodes[z+1].gen_msg.path for z in range(my_net.num_nodes)])
    # plt.show(block = False)
    # plt.pause(3)
    # plt.close(view.view)

enablePrint()
print(Measurement_data)
# print(my_net.nodes_linkage)
# for i in range(my_net.num_nodes):
#     print(my_net.nodes[i+1].linked_nodes)