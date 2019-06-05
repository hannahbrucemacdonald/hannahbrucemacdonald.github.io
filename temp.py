from pyvis.network import Network
import networkx as nx
import pandas as pd
from collections import Counter

net = Network(height="750px", width="100%", bgcolor="white", font_color="black",directed=True)

# set the physics layout of the network
net.barnes_hut()
data = pd.read_csv("themob.csv")

people = data['Person']
supervisors = data['Supervisor']
jobtype = data['Type']

color = {'PhD' : 'blueviolet' , 'postdoc' : 'magenta'}

all_people = set(list(people)+list(supervisors))
node_size = Counter(supervisors)

for person in all_people:
    net.add_node(person, title=person,size=1)

for person, supervisor, job in zip(people,supervisors, jobtype):
    net.add_edge(supervisor, person, arrow=True,color=color[job])

neighbor_map = net.get_adj_list()

# add neighbor data to node hover data
for node in net.nodes:
    node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
    node["value"] = len(neighbor_map[node["id"]])

net.show("themob.html")
