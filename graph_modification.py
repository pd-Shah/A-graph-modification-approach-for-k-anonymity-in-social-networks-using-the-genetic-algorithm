import find_candidate
def graph_modification(G, k, d, _d, id_communities):
    V_plus= list()
    _G=G
    n=len(G.nodes())
    for i in range(n):
        #d, dv= d[i]
        v, d_v=d[i]
        #d'v=d'[i]
        v, _d_v= _d[i]
        #degree deficiency
        DEF= _d_v - d_v    
        if DEF > 0:
            V_plus.append((v,DEF))
            
    for i in len(V_plus):
        v, DEF= V_plus[i]
        temp= DEF
        candidates=find_candidate.find_candidate(Graph, v, V_plus)
        while temp>0:
            candidate=candidates.pop(0)
            #check empty list
            #(if not y) then y is empty
            #(if y) then y != null
            if y:
                _G.add_edge(v, candidate)
                temp-=1
            else:
                break
        if temp==0:
            V_plus.remove(V_plus[i])
        else:
            V_plus[i]=(v,temp)
    ADDVErtex
    return _G
