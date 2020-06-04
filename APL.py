import networkx as nx
import matplotlib.pyplot as plt
import numpy as npy
def APL(G, node1, node2):
    length=nx.single_source_shortest_path_length(G,node1)[node2]
    return length

def APL_test_mode():
    G=nx.Graph()
    # G.add_edges_from([(1,2),(1,3),(2,4),(2,3),
    #                       (5,8),(8,9),(9,7),(7,6),(8,7)])
    #
    #
    # pos = nx.spring_layout(G)
    # nx.draw_networkx_nodes(G,pos, label=True)
    # nx.draw_networkx_edges(G,pos)
    # nx.draw_networkx_labels(G,pos)
    # plt.show()

    # cost from 1 to 7
    #length=nx.single_source_shortest_path_length(G,3)[7]

    dataset=npy.loadtxt("runs/CA-AstroPh/k50.txt", dtype=str)
    G.add_edges_from(dataset)
    # pos = nx.spring_layout(G)
    # nx.draw_networkx_nodes(G,pos)
    # nx.draw_networkx_edges(G,pos)
    # plt.show()
    _=[]
    for g in nx.connected_component_subgraphs(G):
        try:
            _.append(nx.average_shortest_path_length(g))
        except:
            pass

    # _=npy.array([i for i in length.values()])
    # _=npy.array([])
    # for i in length.values():
    #     _.append(npy.array([j for j in i.values()]).mean())

    _=npy.array(_)

    print("APL: min:{0}, max:{1}, mean:{2}".format( _.min(), _.max(), _.mean()))
    print("Transitivity: ", nx.transitivity(G))
    print("Average Clustering Coefficient: ", nx.average_clustering(G))

if __name__=="__main__":
    APL_test_mode()
