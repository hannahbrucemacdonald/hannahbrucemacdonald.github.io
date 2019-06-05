from pyvis.network import Network
import networkx as nx
import pandas as pd
from collections import Counter

net = Network(height="1000px", width="100%",directed=True,bgcolor="#222222", font_color="white")

# set the physics layout of the network
net.barnes_hut()
net.force_atlas_2based()
data = pd.read_csv("details.csv",encoding = "ISO-8859-1", error_bad_lines=False) 

people = data['Person']
supervisors = data['Supervisor']
jobtype = data['Type']

color = {'PhD' : 'blueviolet' , 'postdoc' : 'magenta' , 'link' : 'turquoise'}

all_people = set(list(people)+list(supervisors))
#node_size = Counter(supervisors)

for person in all_people:
    net.add_node(person, title=person,size=5) #,shape='ellipse')

for person, supervisor, job in zip(people,supervisors, jobtype):
    if job != 'link':
        net.add_edge(supervisor, person, arrow=True,color=color[job])

neighbor_map = net.get_adj_list()

# add neighbor data to node hover data
for node in net.nodes:
    supervised = [x for x in net.neighbors(node["id"])]
    num = len(supervised)
    if num > 0: 
        node["title"] += " Students:<br>" + "<br>".join(neighbor_map[node["id"]])
    node["value"] = num 

for person, supervisor, job in zip(people,supervisors, jobtype):
    if job == 'link':
        net.add_edge(supervisor, person, arrow=False,color=color[job],arrowStrikethrough=True)
        net.add_edge(person, supervisor, arrow=False,color=color[job],arrowStrikethrough=True)

net.show("index.html")
