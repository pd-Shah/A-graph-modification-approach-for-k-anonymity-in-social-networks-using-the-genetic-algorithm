import numpy
import community_detection
import community
import operator
import networkx as nx

def find_candidate(Graph, Vertex, V_plus):
    candidate=list()
    dendrogram = community_detection.comunity_detection_function()
    #detect_community_for_vertex in each level
    Vertex_community=detect_community_for_specific_node(Vertex, dendrogram)
    #dictionary of nodes and comunities of that nodes
    all_partitions_all_levels_list=all_partitions_all_levels(dendrogram)

    #dendrogram = communities_dict
    for counter, com_id in  enumerate(Vertex_community):
        #a list of same communies of nodes with Vertex
        com_keys = [key for key,value in all_partitions_all_levels_list[counter].items() if com_id==value]
        #test
        #print("for id_com=", com_id, "com_keys=", com_keys)
        temp=list()
        for u in V_plus:
            if u in com_keys and (not(((u, Vertex) in G.edges()))) and (not(((Vertex, u) in G.edges()))):
                distance=nx.single_source_shortest_path_length(G,u)[Vertex]
                temp.append((u,distance))
        temp.sort(key=operator.itemgetter(1))
        candidate.append(temp)
    return candidate


def detect_community_for_specific_node(node_label, dendrogram): 
    node_communities=list()
    for level in range(len(dendrogram)):
        node_communities.append(community.partition_at_level(dendrogram, level)[node_label])
    return node_communities

def all_partitions_all_levels(dendrogram):
    all_partitions=list()
    for level in range(len(dendrogram)):
        all_partitions.append(community.partition_at_level(dendrogram, level))
    return all_partitions
    
def test_mode(G, Vertex, V_plus):
    candidate=list()
    dendrogram = community_detection.test_mode()
    #detect_community_for_vertex in each level
    Vertex_community=detect_community_for_specific_node(Vertex, dendrogram)
    #dictionary of nodes and comunities of that nodes
    all_partitions_all_levels_list=all_partitions_all_levels(dendrogram)

    #dendrogram = communities_dict
    for counter, com_id in  enumerate(Vertex_community):
        #a list of same communies of nodes with Vertex
        com_keys = [key for key,value in all_partitions_all_levels_list[counter].items() if com_id==value]
        #test
        #print("for id_com=", com_id, "com_keys=", com_keys)
        temp=list()
        for u in V_plus:
            if u in com_keys and (not(((u, Vertex) in G.edges()))) and (not(((Vertex, u) in G.edges()))):
                distance=nx.single_source_shortest_path_length(G,u)[Vertex]
                temp.append((u,distance))
        temp.sort(key=operator.itemgetter(1))
        candidate.append(temp)
    return candidate
