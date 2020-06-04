import numpy as np
import random
import copy
import networkx as nx
from draw_graph import draw

def make_pop(need: "{1:1,2:0,3:2,4:2,5:1}") -> "headers: [1, 3, 3, 4, 4, 5], pop:[5, 4, 3, 3, 4, 1]":
    '''
    input: {1:1,2:0,3:2,4:2,5:1}
             1, 3, 3, 4, 4, 5
    output: [a, b, c, d, e, f]
    '''
    header=[]
    [header.append(i) for i in need.keys() for j in range(need[i])]
    pop=np.random.choice(header, len(header), replace=False)

    return header, list(pop)

def make_initial_population(need, population_number):
    initial_population=[]
    header=[]
    for i in range(population_number):
        _=make_pop(need)
        header=_[0]
        initial_population.append(_[1])
    return header, initial_population

def connection_able(chromos, header):
    '''
    count number of same value at same index
     [1,2,3,4,5]
     [0,2,0,4,0]
     => 2, 4 => 2
    '''
    score=0
    chromos=np.array(chromos)
    header=np.array(header)
    return int(np.sum(chromos==header) * (-1))

def a_to_b_then_b_to_a(chromos, header):
    '''
    check if there x1 = 4 then x4=1
     1 2 3 4 5
    [4,x,x,1,x]
    >>> x
    [1, 2, 3, 4, 5]
    >>> y
    [4, 2, 3, 1, 5]
    >>> score=0
    >>> for a,b in zip(x,y):
            then=x.index(b)
            if y[then]==a and a!=b:
                    score+=1
    >>> score
    2
    '''
    score=0
    for a,b in zip(header,chromos):
        then=header.index(b)
        if chromos[then]==a and a!=b:
            score+=1
    return int(score)

def number_of_nodes_repeat(chromos, header):
    '''
    check that nodes repeats as needed
    header: [1, 1, 3, 3, 4]
    chromos: [1, 1, 1 , 3, 4]
    there there are one 1 that is more than need
    >>> x=np.array([1, 1, 3, 3, 4])
    >>> y=np.array([1, 1, 1 , 3, 4])
    >>> score=0
    >>> for item in set(x):
            if np.sum(x==item) != np.sum(y==item):
                    score+=1


    >>> score
    2
    '''
    score=0
    for item in set(header):
        if np.sum(header==item) != np.sum(chromos==item):
            score+=1
    return score* (-1)

def repeated_connection(chromos, header, g):
    score=0
    for u,v in zip(chromos, header):
        if g.has_edge(u,v):
            score+=1
    return score*(-1)

def fitness(chromos,header, g):
    '''
    calculate fitness of a chromos
    '''
    s1=connection_able(chromos, header)
    s2=a_to_b_then_b_to_a(chromos, header)
    s3=number_of_nodes_repeat(chromos, header)
    s4=repeated_connection(chromos, header, g)
    score=s1+s2+s3+s4
    return score

def selection(header, population, population_number, g, p_c=0.2):
    '''
    select chromos from population base on fitness
    p_cross_over=0.8 then 1 - 0.8 = 0.2 select and remove them
    '''
    #calculate fintness
    fitness_score=[]
    for pop in population:
        fitness_score.append(fitness(pop, header, g))
    #this generates "population_number" samples from the "population" with weights fitness_score
    #map to positive p
    from_min=min(fitness_score)
    from_max=max(fitness_score)
    to_max=1
    to_min=0
    if (from_max - from_min) + to_min:
        p=np.array([(i - from_min) * (to_max - to_min) / (from_max - from_min) + to_min for i in fitness_score])
        p /= p.sum()
    else:
        #if division by zer0 then equal p for all
        '''
        >>> x=np.array([0,0,0,0])
        >>> x
        array([0, 0, 0, 0])
        >>> x+1
        array([1, 1, 1, 1])
        >>> (x+1)/len(x)
        array([ 0.25,  0.25,  0.25,  0.25])
        '''
        p=((np.array(fitness_score)*0)+1)/len(fitness_score)

    # I know no one cant understand this code, so I left it without comments :-*
    if np.any(p==0):
        p[p!=0]=[i-np.min(p[p!=0])*0.001/len([i for i in p if i !=0 ]) for i in p if i !=0]
        p[p==0]=np.min(p[p!=0])*0.001/len([i for i in p if i ==0 ])

    #print([repr(x) for x in p])

    if int(population_number*p_c):
        #select p_c*population_number and remove them
        #EXP: if p_c=0.2 and population_number=10 then remove 2 items
        indexs=np.random.choice(range(len(population)), int(population_number*p_c), p=(1-p)/np.sum(1-p), replace=False)

        for i in sorted(indexs, reverse=True):
            del population[i]
            p=np.delete(p, i)

        #normalize again
        p=np.array(p)
        p /= p.sum()


    #chooses k=population_number-(p_c*population_number) item unique random elements
    indexs=np.random.choice(range(len(population)), population_number-int(p_c*population_number) , p=p, replace=False)

    if int(population_number*p_c):
        #when select p_c*population_number and remove them,
        #then we have to reapet item from survivors
        #to have same population number
        indexs=np.append(indexs, np.random.choice(range(len(population)), int(population_number*p_c), p=p, replace=False))

    return header, [population[i] for i in indexs]

def cross_over(parents):
    #line index
    splite_line=int(len(parents[0])/2)

    #make cross over
    for index in range(0, len(parents), 2):
        x=parents[index]
        y=parents[index+1]
        tmp = x[:splite_line].copy()
        x[:splite_line], y[:splite_line]  = y[:splite_line], tmp
        parents[index]=x
        parents[index+1]=y
    childs=parents

    return childs

def mutation(childs, population_number, p=0.1):
    '''
    in 10% make mutation
    '''
    #select k=int(p*len(childs[0])) random gen
    gen_index_list=np.random.choice(range(len(childs[0])), int(p*len(childs[0])))
    if list(gen_index_list):
        #make mutation
        for child_index in range(0, len(childs), 2):
        	for gen_index in gen_index_list:
        		childs[child_index][gen_index], childs[child_index+1][gen_index]= childs[child_index+1][gen_index], childs[child_index][gen_index]
    return childs

# def add_node_before_GA(need):
#     sub=0
#     for item in sorted(list(need.values()), reverse=True):
#          sub=abs(abs(sub)-abs(item))
#     return sub
#
# def make_need(node_number):
#     need=[]
#     while sum(node_number)>0:
#         need.append(len([item for item in node_number if item>0]))
#         node_number=[item-1 for item in node_number if item>0]
#     return need
#
# def add_node_after_GA(need, connections, com):
#     edges=[i for i in need.values()]
#     node=max(edges)
#     new_node={}
#     need_list=make_need(edges)
#
#     for index, count in enumerate(range(node)):
#         new_node.update({str(com)+"node"+str(count):need_list[index]})
#
#     #make asc by second item, list from need
#     ar=np.array(list(need.items()))
#     sort_need=(ar[np.argsort(ar[::,-1])][::-1]).tolist()
#
#     for v,e in sort_need:
#         for new_item in [l for l,d in list(new_node.items()) if d>0]:
#             connections.extend([v,new_item])
#             new_node[new_item]-=1
#
#
#     return connections


if __name__=="__main__":
    '''
    initial config
    '''
    #com=[{1: 0}]
    com=[{1: 1, 2: 1, 3: 0, 4:0}, 1,2,2,3,1,3]
    #com=[{1: 1, 2: 5, 3: 7, 4: 2, 5: 1, 6: 2, 7: 1, 8: 2, 9: 2}, 1,2,2,3,1,3,8,9,7,6,5,7,8,3,3,7,5,8]
    need=com[0]
    edges=com[1:]
    population_number=10
    com_number=0
    generation_number=10

    '''
    make graph
    '''
    G=nx.Graph()
    G.add_nodes_from(list(com[0].keys()))
    G.add_edges_from(np.array(edges).reshape(int(len(edges)/2),2))
    draw(G)

    # '''
    # make genetic ready
    # '''
    # #check if it need add node
    # not_fit=add_node_before_GA(need)
    #
    # #add a node by need = add_node_before_GA
    # if not_fit:
    #     need.update({str(com_number)+"fit":not_fit})
    # print("need", need)

    '''
    run genetic
    '''
    #if np.sum(np.array(list(x.values()))) != 0 then run genetic
    header, init_pop=make_initial_population(need, population_number)
    parents=copy.deepcopy(init_pop)
    for i in range(generation_number):
        header, parents= selection(header, parents, population_number, G)
        new_generation=cross_over(parents)
        new_generation=mutation(new_generation, population_number)
        parents=copy.deepcopy(new_generation)

    #calculate fintness and select best answer
    fitness_score=[]
    for pop in new_generation:
        fitness_score.append(fitness(pop, header, G))

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
            com.extend([node1,node2])

    #if need to add nodes
    #connections=add_node_after_GA(need, com[1:], com_number)
    modifiedges=np.array(com[1:], dtype=str).reshape(int(len(com[1:])/2),2)
    print(modifiedges)
    G=nx.Graph()
    G.add_edges_from(modifiedges)
    draw(G)
