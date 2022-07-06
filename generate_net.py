import random
import yaml
import math

num_nodes = int(input("Enter the total number of nodes : "))
net_length = int(input("Enter the length of network (in m) : "))
net_width = int(input("Enter the width of network (in m) : "))

nodes = {}
part = 16
dim = int(math.sqrt(part))
for i in range(dim):
    gx = net_length
    gy = net_width/(2*dim)+(i*net_width/dim)
    nodes[-1-i] = [gx,gy,0]
    for j in range(dim):
        num_part = i*dim + j
        for k in range(num_part*num_nodes//part,num_nodes-((part-num_part-1)*num_nodes//part)):
            # if k == num_nodes-1:
            #     break
            posx = random.random()*(net_length/dim)+(j*net_length/dim) 
            posy = random.random()*(net_width/dim)+(i*net_width/dim)
            nodes[k+1] = [posx,posy,random.choice([1,2,3])]

file = open("init_network.yaml","w")
network = yaml.dump(nodes,file)