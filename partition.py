import numpy as npy
from math import inf
import networkx as nx
import collections

def greedy_partition_algorithm(degree_sequence_list, k, return_need_matrix=True):

    p=[] #2D array, anonymization groups

    while len(degree_sequence_list)> k :
        try:# for better performance can just pass anonymization_groups[-1] to find_nearest_group
            p_merge, c_merge= find_nearest_group(degree_sequence_list[0].copy(), p[-1].copy())
        except: # for empty p
            p_merge, c_merge= find_nearest_group(degree_sequence_list[0].copy(), p.copy())

        p_new, c_new= create_new_group(degree_sequence_list[0], degree_sequence_list.copy(), k)

        if c_merge<c_new:
            #merge it
            degree_sequence_list.remove(p_merge[-1])
            #p.remove(p[-1]) nodes,  remove old merge and then add new merge
            [p[-1].remove(node) for node in  p[-1].copy()]
            [p[-1].append(node) for node in p_merge]#add new element

        else:
            #make new list
            add_node(*p_new,add_to_list=p)
            #delete new list from degree_sequence_list
            [degree_sequence_list.remove(item) for item in p_new[-1]]

    #end while
    #remained element in d, add to nearest group
    for node in degree_sequence_list.copy():
        p_merge, c_merge= find_nearest_group(degree_sequence_list[0].copy(), p[-1].copy())
        #merge it
        degree_sequence_list.remove(p_merge[-1])
        #p.remove(p[-1]) nodes,  remove old merge and then add new merge
        [p[-1].remove(node) for node in  p[-1].copy()]
        [p[-1].append(node) for node in p_merge]#add new element

    # (i,j), find max of each partition of j's
    for partition in p.copy():
        p.remove(partition) #remove selected element
        result=find_max(partition, return_need_matrix) # find max
        p.append(result) # add selected element with (V,max)



    return p

def find_nearest_group(node, anonymization_groups):
    '''

    anonymization_groups[-1]: the lastest node of anonymization_groups

    cost=anonymization_groups[-1][1]: degreee of the last node of anonymization_groups:  (9,2) => 2

    cost=anonymization_groups[-1][-1][1]:degreee of the last node of anonymization_groups when cost is an array
    '''
    #variables:
    seed, d_seed= node
    p_merge, c_merge,  = [] , 0
    if not len(anonymization_groups): # anonymization_groups is empty
        c_merge=inf #c_merge= infinit
    else:
        cost=anonymization_groups[-1][1]#anonymization_groups= [(a,b),...,(9,2)] => 2
        if type(cost)==list:
            cost=anonymization_groups[-1][-1][1]#anonymization_groups={(e,f),...,[(a,b),...,(9,2)]} => 2
        #c_merge: merge cost
        c_merge= cost-d_seed
        #p_merge: merge group
        anonymization_groups.append(node)
        p_merge=anonymization_groups
    return p_merge, c_merge

def create_new_group(node, degree_sequence_list, k):
    seed, d_seed= node
    p_new, c_new, cost_list= npy.array([]), 0, npy.array([])
    cost_list=npy.asarray(degree_sequence_list[:k]) #k-1 member of d + input node => k node
    cost_list=(d_seed-cost_list).flatten()[1::2]
    c_new=cost_list.sum()
    p_new=degree_sequence_list[:k]
    p_new=npy.reshape(p_new,(1,len(p_new),2))
    return p_new.tolist(), c_new

def add_node(node_list,add_to_list):
    add_to_list.append(node_list)


def find_max(nodes, return_need_matrix=True):
    #test
    #nodes=[[3, 4], [2, 3], [8, 3], [7, 30], [5, 3]]
    max_degree=npy.amax(nodes,axis=0)[1]
    if return_need_matrix:
        for i,j in nodes.copy():
            nodes.remove([i,j])
            nodes.append([i,max_degree-j])
    else:
        for i,j in nodes.copy():
            nodes.remove([i,j])
            nodes.append([i,max_degree])

    return nodes

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

if __name__ == "__main__":

    nodes=npy.array([(1,2),(1,3),(1,4),(1,5),(1,6),(2,3),(3,4),(2,7)]) #unordered adj list
    #nodes=npy.array([(1,2),(1,3),(1,4),(1,5),(1,6),(2,3),(3,4),(2,7)]) #unordered adj list

    G=nx.Graph()
    G.add_edges_from(nodes)

    #make degree_sequence_list
    degree_sequence_list=npy.array([[label, degree] for label, degree in G.degree().items()])
    #ordered list, descending
    degree_sequence_list=(degree_sequence_list[npy.argsort(degree_sequence_list[::,-1])][::-1]).tolist()


    print("ordered degree_sequence_list: ", degree_sequence_list)

    #for k=2 and defined nodes
    #_partitions of need matrix
    _partitions=greedy_partition_algorithm(degree_sequence_list, 3, True)
    print("_partitions:", _partitions)

    temp=npy.array([i for i in flatten(_partitions)])
    _partitions=temp.reshape(int(len(temp)/2),2)
    print("_partitions.tolist():",_partitions.tolist())

    print("dict(_partitions):", dict(_partitions))
