
import pandas as pds
import numpy as npy
from make_adj_matrix import make_adj_matrix

def remove_loop(g:pds.DataFrame, debug=False)-> None:
    '''
    if [i,i]==1 then [i,i]=0
    '''
    for i in g.columns.values:
        try:
            if g.loc[i,i]:
                g.loc[i,i]=0
        except:
            pass

    if debug:
        print(g)


if __name__=="__main__":
    nodes=npy.array([[1,3],[5,3],[2,1],[3,2],[2,2],[1,1],[3,3],[5,5]])
    print(make_adj_matrix(nodes))
    remove_loop(make_adj_matrix(nodes), debug=True)
