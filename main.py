from matplotlib import pyplot as plt
import pandas as pds
import numpy as np
import networkx as nx
import collections
import copy

from community_detection import comunity_detection_function, all_partitions_all_levels, find_community
import genetic as GA
from partition import greedy_partition_algorithm
from draw_graph import draw

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

if __name__=="__main__":
    '''
    initial config
    '''
    population_number=10
    generation_number=10
    k=3
    show=True

    '''
    read_csv
    '''
    #read file
    # datafile = pds.read_csv("datasets/CA-AstroPh.csv", header=None)
    # datafile=datafile.values
    # print(datafile)

    datafile=np.array([(1,2),(1,3),(2,4),(2,3),(4,5),(5,3),(5,8),(8,9),(9,7),(7,6),(6,3),(2,5),(8,7)])
    #datafile=np.array([(1,2),(1,3),(1,4),(1,5),(1,6),(2,3),(3,4),(2,7)])

    print("reading file finished!")

    '''
    make graph and plot
    '''
    print("drawing graph.")
    G=nx.Graph()
    G.add_edges_from(datafile)
    # nx.draw(G)
    # plt.show()
    if show:
        draw(G)
    print("draw finished.")

    '''
    run partitining
    '''
    print("run partitining")
    #make degree_sequence_list
    degree_sequence_list=np.array([[label, degree] for label, degree in G.degree()])
    #ordered list, descending
    degree_sequence_list=(degree_sequence_list[np.argsort(degree_sequence_list[::,-1])][::-1]).tolist()
    #print("degree_sequence_list:", degree_sequence_list)

    #_partitions of need matrix
    _partitions=greedy_partition_algorithm(degree_sequence_list, k, True)
    #print("_partitions:", _partitions)

    #make format of {lable:need}
    _=np.array([i for i in flatten(_partitions)])
    _partitions=_.reshape(int(len(_)/2),2)
    need=dict(_partitions)
    # print("need:", need)

    '''
    run comunities detection
    '''
    print("run community detection")
    dendrogram = comunity_detection_function(datafile, G, show=show)
    #dictionary of nodes and comunities of that nodes
    all_partitions_all_levels_list=all_partitions_all_levels(dendrogram)
    #com format: {0: [1, 2, 3, 4, 5], 1: [6, 7, 8, 9]}
    com=find_community(all_partitions_all_levels_list[-1])
    # print("com:",com)

    '''
    com & need
        com={0: [0, 1, 2], 1:[3,4,5]}
        need={0:1,1:2,2:0,3:4,4:1,5:2}

        com_need= [[[0, 1], [1, 2], [2, 0]], [[3, 4], [4, 1], [5, 2]]]
    '''
    com_need=[]
    for item in com.values():
    	com_need.append([])
    	for i in item:
    		com_need[-1].append([i,need[i]])
    # print("com_need:",com_need)

    '''
    genetic init config
    '''
    #final edges
    modified_edges=[]

    #make template
    template=[]
    for item in com_need:
        template.append([])
        template[-1].append(dict(item))
        template[-1].extend(np.array(G.edges()).flatten())

    _len_template=len(template)
    #run genetic
    for index,item in enumerate(template):
        print(str(index/_len_template)+"% is running. making ready genetic for:", item)
        need=item[0]
        edges=item[1:]

        # #check if needs add node
        # not_fit=GA.add_node_before_GA(need)
        #
        # #add a node by need = add_node_before_GA
        # if not_fit:
        #     need.update({str(index)+"fit":not_fit})
        # print("need", need)

        '''
        run genetic
        '''
        if np.sum(np.array(list(need.values()))) != 0:
            print("running GA for ", need)
            #print("making init pop")
            header, init_pop=GA.make_initial_population(need, population_number)
            # print("header", header)
            # print("init_pop", init_pop)
            parents=copy.deepcopy(init_pop)
            for i in range(generation_number):
                header, parents= GA.selection(header, parents, population_number, G)
                # print("selection header", header)
                # print("selection parents", parents)
                new_generation=GA.cross_over(parents)
                # print("cross over", new_generation)
                new_generation=GA.mutation(new_generation, population_number)
                # print("mutation", new_generation)
                parents=copy.deepcopy(new_generation)
                # print(str(i/generation_number)+"% GA done; of "+str(index/_len_template)+"%.")
                # print("\n")

            #calculate fintness and select best answer
            fitness_score=[]
            for pop in new_generation:
                fitness_score.append(GA.fitness(pop, header, G))
            # print("fitness_score", fitness_score)

            genetic_output=np.unique(np.sort(np.array([[i,j] for i,j in zip(header, new_generation[ fitness_score.index(max(fitness_score))])]), axis=1), axis=0)
            #update needs
            for node1,node2 in genetic_output:
                try:
                    node1=int(node1)
                except:
                    pass
                try:
                    node2=int(node2)
                except:
                    pass
                if need[node1] > 0 and need[node2] > 0 and (not G.has_edge(node1, node2)) and node2 != node1:
                    need[node1]-=1
                    need[node2]-=1
                    edges.extend([node1,node2])

        #if need to add nodes
        #connections=GA.add_node_after_GA(need, edges, index)
        connections=np.array(edges, dtype=str).reshape(int(len(edges)/2),2)
        # print("connections",connections)
        modified_edges.extend(np.array(connections))
        modified_edges=np.unique(np.sort(modified_edges, axis=1), axis=0).tolist()


    '''
    draw output
    '''
    print("drawing graph.")
    G=nx.Graph()
    G.add_edges_from(modified_edges)
    nx.draw(G)
    plt.show()
    if show:
        draw(G)
    print("draw finished.")

print("writing to file...")
with open("final.txt", "w") as final:
    for i,j in G.edges():
        final.write(str(i)+" "+str(j)+"\n")
