import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def draw(G:nx.Graph)->plt.show:
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos, label=True)
    nx.draw_networkx_edges(G,pos)
    nx.draw_networkx_labels(G,pos)
    plt.show()

if __name__=="__main__":
    G=nx.Graph()
    #g=np.array([(1,2),(1,3)])
    # g=np.array([(1,2),(1,3),(2,4),(2,3),(4,5),(5,3),
    #                       (5,8),(8,9),(9,7),(7,6),(6,3),(2,5),(8,7)])
    #G.add_edges_from(g)
    #G.add_
    #draw(G)
    #G.add_edges_from([(1,2), (1,2), (2,1)])
    #draw(G)
