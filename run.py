from numpy import block
from fixed_net import *
from message import *
from plot import *
from calc import *
from measurement import *
import matplotlib.pyplot as plt
import random
import csv
from colorama import Back,Style

my_net = network("init_network.yaml")
view = net_view(my_net)


######################################################################################
###---PROPOSED METHOD---###
###---TRAINING THE Q-LEARNING ALGORITHM---###
def train_proposed_algo(my_net):
    print("Training the q-learning algorithm...")
    blockPrint()
    for i in range(5000):
        print(i)
        start = random.randint(1,my_net.num_nodes)
        print(start)
        msg_len = my_net.header_length + my_net.msg_len_per_sensor*my_net.nodes[start].num_sensors 
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
            my_net.routing.update_q_value(curr_state,next_state,reward)
            curr_state=next_state
        print(path)
    enablePrint()
    print("Training Complete")
###---Q_LEARNING TRAINING DONE !---###
######################################################################################


######################################################################################
###---TRAINING THE QL_EEBDG ALGORITHM---###
def train_QL_EEBDG_algo(my_net):
    print("Training the ql_eebdg algorithm...")
    blockPrint()
    for i in range(10000):
        print(i)
        start = random.randint(1,my_net.num_nodes)
        print(start)
        msg_len = my_net.header_length + my_net.msg_len_per_sensor*my_net.nodes[start].num_sensors 
        curr_state = start
        path=[]
        path.append(curr_state)
        while not curr_state in my_net.gateway_node_ids:
            #print(my_net.routing.q_table)
            next_state = my_net.ql_eebdg_routing.get_next_action(curr_state,path,0.9)
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
                reward = my_net.ql_eebdg_routing.calculate_reward(curr_state,path,msg_len)
            my_net.ql_eebdg_routing.update_q_value(curr_state,next_state,reward)
            curr_state=next_state
        print(path)
    enablePrint()
    print("Training Complete")
###---TRAINING DONE !---###
#######################################################################################

train_proposed_algo(my_net)
#train_QL_EEBDG_algo(my_net)
my_net.reset_nodes()



models = Measurement_models(my_net)

Measurement_data = np.empty((0,5),dtype='float32')
init_data = np.array([models.throughput_ratio,models.net_life,models.total_energy,models.data_latency,models.energy_balance]).reshape(1,-1)
Measurement_data = np.append(Measurement_data,init_data, axis = 0)

generated_fault = []
prediction_results = np.empty((0,2),dtype='int')

k=0
while True :
    k=k+1
    #my_net.check_deadnet()
    # if my_net.net_alive == 0:
    #     break
    # if k%10 == 0:
    #     my_net.leach_routing.setup_phase()

    # if k%10 == 0:
    #     my_net.kmeans_routing.setup_phase()

    # if k%10 == 0:
    #     my_net.nmleach_routing.setup_phase()

    if k == 200:
        print(Back.CYAN+"%d"%(k))
        print(Style.RESET_ALL)
    else:
        print(k)

    # for i in range(my_net.num_nodes):
    #     if my_net.nodes[i+1].faulty == -1:
    #         print(i+1)

    #blockPrint()
    if k >= 200:
        if random.random() > 0.97:
            f_node = random.randint(1,my_net.num_nodes)
            my_net.nodes[f_node].generate_fault()
            generated_fault.append(f_node)

    faulty = []
    Dead = []
    if k > 100:
        for i in range(my_net.num_nodes):
            my_net.nodes[i+1].predict_fault()
            pred = 0
            if my_net.nodes[i+1].pred_faulty == -1:
                faulty.append(i+1)
                pred = 1
            if my_net.nodes[i+1].alive == -1:
                Dead.append(i+1)
            if not my_net.nodes[i+1].faulty == -1:
                if (i+1) in generated_fault:
                    gen = 1
                else:
                    gen = 0
            #     #kmeans = my_net.nodes[i+1].kmeans_prediction()
            #     #svm_pred = my_net.nodes[i+1].svm_prediction()
            #     #dec_tree = my_net.nodes[i+1].dec_tree_prediction()
            #     #prediction = np.array([svm_pred,gen]).reshape(1,-1)
                prediction = np.array([pred,gen]).reshape(1,-1)
                prediction_results = np.append(prediction_results,prediction,axis = 0)
    print(faulty)
    print(Dead)
    my_net.routing.avoid_faulty_nodes(faulty)
    #my_net.routing.avoid_dead_nodes(Dead)
    #my_net.ql_eebdg_routing.avoid_dead_nodes(Dead)

    for i in range(my_net.num_nodes):
        my_net.nodes[i+1].generate_msg()
        
    if k >= 100:
        for i in range(my_net.num_nodes):
            my_net.nodes[i+1].fault_predictor.fit_predictor(my_net.nodes[i+1].node_data)
    
    # if k == 100:
    #     for i in range(my_net.num_nodes):
    #         my_net.nodes[i+1].kmeans_predictor.fit_predictor(my_net.nodes[i+1].node_data)

    if (k+1) in [200,400,600,800,1000,1200,1400,1600,1800,2000]:
        models.update_energies()

    if k in [200,400,600,800,1000,1200,1400,1600,1800,2000]:
        models.calculate_all_models()
        curr_data = np.array([models.throughput_ratio,models.net_life,models.total_energy,models.data_latency,models.energy_balance]).reshape(1,-1)
        Measurement_data = np.append(Measurement_data,curr_data, axis = 0)
    
    if k == 2000:
            break

    enablePrint()
    # my_net.generate_all_msgs()
    view.plot_msg_paths([my_net.nodes[z+1].gen_msg.path for z in range(my_net.num_nodes)])
    plt.show(block = False)
    plt.pause(10)
    plt.close(view.view)

enablePrint()
print(Measurement_data)
q_learning = "q_learn.csv"
q_learn_with_p = "ql_lof.csv"
leach = "leach.csv"
beemh = "beemh.csv"
kmeans = "kmeans.csv"
nmleach = "nmleach.csv"
ql_eebdg = "ql_eebdg.csv"
dt = "dt.csv"

# fields = ['Throughput','Net_Life','Net_Energy','Latency','Energy_Balance']
# with open(ql_eebdg,'w') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(fields)
#     csvwriter.writerows(Measurement_data)

print(prediction_results)
accuracy,precision,recall = Measurement_models.prediction_models(prediction_results)
print(accuracy)
print("Accuracy : %f  Precision : %f  Recall : %f"%(accuracy,precision,recall))