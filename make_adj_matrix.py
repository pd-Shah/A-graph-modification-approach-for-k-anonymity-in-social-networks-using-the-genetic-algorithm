import numpy as npy
import pandas as pds

def make_adj_matrix(g:npy.array)-> pds.DataFrame:
    '''
    g must be sorted input
    if modes: nodes=[[1,3],[5,3],[2,1],[3,2]]
    matrix item= 1,2,3,5
    =>
      1  2  3   5
    1
    2
    3
    5
    '''
    #sort in -1 dimetion [2,1][1,3] -> [1,2][1,3]
    g=npy.sort(g, axis=-1)
    # matrix_items: list of unique items of g
    matrix_items=npy.array(list(set([j for i,j in g]+[i for i,j in g])))
    #zer0 adjacency matrix
    adj=npy.zeros_like(npy.arange(len(matrix_items)*len(matrix_items)).reshape(len(matrix_items),len(matrix_items)))
    #add labels to adj matrix
    adj=pds.DataFrame(adj, index=matrix_items, columns=matrix_items)
    for i,j in g:
        adj.loc[i][j]=1
    return(adj)

if __name__=="__main__":
    nodes=[[2,1],[3,1],[2,3],[2,4],[5,3],[4,5],[5,8],[7,6],[7,9],[8,7],[3,6]]
    print(make_adj_matrix(nodes))
