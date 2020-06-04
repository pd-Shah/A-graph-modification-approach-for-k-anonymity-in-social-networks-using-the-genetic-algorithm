
import networkx as nx
import matplotlib.pyplot as plt
import csv
import pandas as pds
import community


def comunity_detection_function(datafile, G, show=True, db_name='facebook_combined.csv'):
    '''
    requirment:

    networkx
    matplotlib
    pandas
    community: https://bitbucket.org/taynaud/python-louvain
    '''

    #community
    #first compute the best partition
    partition = community.best_partition(G)
    values = [partition.get(node) for node in G.nodes()]
    print("community detection finished!")

    if show:
        '''
        drawing community
        '''

        ###drawing nodes
        print("drawing nodes of communites...")
        size = int(len(set(partition.values())))
        pos = nx.spring_layout(G)

        ###C0 C1 ... are color
        counter=1
        my_colors=[('C'+ str(count)) for count in range(size+counter)]


        for com in set(partition.values()):
            list_nodes = [nodes for nodes in partition.keys()
                                        if partition[nodes] == com]
            nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 10,
                                        node_color = str(my_colors[counter]))
            counter+=1
        print("drawing community detection finished!")
        ##
        ##
        ###drawing edges
        print("drawing network edges...")
        nx.draw_networkx_edges(G,pos)
        plt.show()

    return community.generate_dendrogram(G)

def all_partitions_all_levels(dendrogram):
    all_partitions=list()
    for level in range(len(dendrogram)):
        all_partitions.append(community.partition_at_level(dendrogram, level))
    return all_partitions

def find_community(_community):
    #comunities dict:
    d={}

    #all comunities ids:
    community_ids=set((value for value in _community.values()))

    #update community dict
    for number in community_ids:
        d.update({number:[]})

    #append community members
    for key,val in _community.items():
        d[val].append(key)

    return d

def test_mode():
    G=nx.Graph()
    G.add_edges_from([(1,2),(1,3),(2,4),(2,3),(4,5),(5,3),
                      (5,8),(8,9),(9,7),(7,6),(6,3),(2,5),(8,7)])
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos, label=True)
    partition = community.best_partition(G)
    nx.draw_networkx_edges(G,pos)
    nx.draw_networkx_labels(G,pos)
    plt.show()
    values = [partition.get(node) for node in G.nodes()]


    '''
    drawing community
    '''

    ###drawing nodes
    print("drawing nodes of communites...")
    size = int(len(set(partition.values())))
    pos = nx.spring_layout(G)

    ###C0 C1 ... are color
    counter=1
    my_colors=[('C'+ str(count)) for count in range(size+counter)]

    for com in set(partition.values()):
        list_nodes = [nodes for nodes in partition.keys()
                                    if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes,node_color = str(my_colors[counter]))
        counter+=1
    print("drawing community detection finished!")
    ##
    ##
    ###drawing edges
    print("drawing network edges...")
    nx.draw_networkx_edges(G,pos)
    nx.draw_networkx_labels(G,pos)
    plt.show()
    return community.generate_dendrogram(G)

if __name__=="__main__":

    # #read file
    # datafile = pds.read_csv("facebook_combined.csv", header=None)
    # print("reading file finished!")
    #
    # #make empty graph
    # G=nx.Graph()
    #
    # #make facebook graph
    # G.add_edges_from(datafile.values)
    # print("makeing facebook graph finished!")
    #
    # ###show orginal graph
    # nx.draw(G)
    # plt.show()
    #
    # dendrogram = comunity_detection_function(datafile, G)
    dendrogram=test_mode()
    #dictionary of nodes and comunities of that nodes
    all_partitions_all_levels_list=all_partitions_all_levels(dendrogram)
    for i in all_partitions_all_levels_list:
        print(i)

    print(find_community(all_partitions_all_levels_list[0]))
