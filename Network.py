import numpy as np
import pandas as pd
import networkx as nx
import networkx.classes.function as fn
import networkx.algorithms.centrality as ct
from networkx.algorithms import distance_measures

def create_network(file_name):
    df = pd.read_csv(filename, header=0, index_col=0)
    df = df.transform(lambda x: x.replace(np.nan, 0))

    G = nx.from_pandas_adjacency(df, create_using=nx.DiGraph())
    G.edges(data=True)
    G.name = "Graph from numpy adjacency matrix"
    nx.write_gml(G, "network.gml")
    
    with open('network_info.csv', 'w') as f:
        info = nx.info(G).split('\n')
        for i in info:
            f.write("%s,%s\n"%(i.split(":")[0], i.split(":")[1]))  
        f.write("%s,%s\n"%('Density', fn.density(G)))
        f.write("%s,%s\n"%('Diameter', distance_measures.diameter(G.to_undirected())))
        
    return G

G = create_network(file_name)

measures = {}
measures['betweenness'] = ct.betweenness_centrality(G, normalized=True, weight="weight")
measures['closeness'] = ct.closeness_centrality(G, distance="weight")
measures['degree'] = ct.degree_centrality(G)
measures['in_degree'] = ct.in_degree_centrality(G)
measures['out_degree'] = ct.out_degree_centrality(G)

for key in measures:
    csv_file = str(FILE_NUMBER) + '_' + key + '.csv'
    my_dict = measures[key]

    with open(csv_file, 'w') as f:
        for key in my_dict.keys():
            f.write("%s,%s\n"%(key, my_dict[key]))  