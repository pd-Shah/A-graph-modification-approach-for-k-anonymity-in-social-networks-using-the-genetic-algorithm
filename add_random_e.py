import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from draw_graph import draw

def add_random_e(Grph:nx.Graph, add_dict:dict)-> nx.Graph:
    '''
    input:
        a partion slice Graph
        need matrix

    output:
        modified partition Graph
        all needed V are satisfied
    '''
    #stop infinit loop
    #if add={1:0,4:2,2:1,3:1} and connect 2->3 => infinit loop
    while True:
        #make backup and reset vars
        arr=np.array([1])
        inifit_loop_counter=1000
        G=Grph.copy()
        add=add_dict.copy()

        #while all element in add are not zero do
        while np.any(arr):
            #select two node randomly, a,b
            a, b=random.sample(list(add.keys()), 2)
            #print("{} and {} selected.".format(a, b))
            #if a,b need to add V and are not connected
            if add[a]>0 and add[b]>0 and not(a in G.adj[b]):
                print("draw {} to {} ".format(a, b))
                #a,b need one less V => update add dictionary
                add[a]=add[a]-1
                add[b]=add[b]-1
                #add V to Graph
                G.add_edge(a,b)
                draw(G)
            arr=np.array(list(add.values()))

            #check infinit loop
            inifit_loop_counter-=1
            if inifit_loop_counter <= 0:
                print("inifit loop detected.\nrestart loop.")
                break

        #exit while True
        #if all element in add are zero then finish the exit while
        if not np.any(arr):
            break

    return(G)


# TODO: how many labels do you need for each nodes


if __name__=="__main__":
    # g=np.array([(1,2),(1,3),(4,1)])
    # add={1:0,4:2,2:1,3:1}
    #
    # # g=np.array([(1,2),(1,3),(1,4),(3,4),(3,5)])
    # # add={1:0,4:0,2:1,3:0,5:1}
    # G=nx.Graph()
    # G.add_edges_from(g)
    # draw(G)
    # new_graph=add_random_v(G, add)
    # draw(new_graph)

    G=nx.Graph()
    g=np.array([(1,10), ])
    G.add_edges_from(g)
    add={1: 1, 2: 5, 3: 5, 4: 2, 5: 1, 6: 1, 7: 1, 8: 2, 9: 2}
    new_graph=add_random_e(G, add)
    draw(new_graph)
