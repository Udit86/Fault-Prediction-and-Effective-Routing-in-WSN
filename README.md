# Fault-Prediction-and-Effective-Routing-in-WSN

The given code is used for simulating Wireless Sensor Network using python. 

A **Q-Learning** algorithm is used for data routing through the network and **Local Outlier Factor(LOF)** algorithm is used for prediction of faulty node in the network. 

Since Wireless Sensor Networks are a densed interconnected Networks and data is transmitted in a Multi-Hop Fashion, failure in any sensor node can effect the performance of the network badly. Hence, we used an unsupervised learning algorithm for prediction of sensor nodes that are going to be faulty in future so that those nodes can be avoided for data transmission and hence data loss can be prevented. 

**How to run this code :-**
- First run [generate_net.py](generate_net.py) to generate a network with length and width of your choice where sensor nodes are randomly deployed. This will generate a YAML file containing the coordinates and number of sensors in each node.
- Then run [run.py](run.py) file to simulate the network. 

The network performance after simulating for 2000 iterations is being checked in terms of "Average Data Latency","Data Throughput","Network Residual Energy" and "Network Life".

The deployed Network looks like this :- 

![Screenshot from 2022-07-06 23-24-52](https://user-images.githubusercontent.com/77680043/177613311-1d52b5af-026c-49d6-8cd0-0538e1ca0670.png)
