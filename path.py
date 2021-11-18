import numpy as np
import pickle
import networkx as nx

def mn_to_k(m ,n):
    return str(m) + '_' + str(n)
    #here we define m is the x position and n is the y one, k count in x direction first

def k_to_mn(k):
    m, n = k.split('_', 1)
    return [float(m), float(n)]

def find_path(start, end):
    f = open('t.txt', 'rb')
    G = pickle.load(f)
    f.close()
    path=nx.astar_path(G, source=start, target=end)
    path_array = []
    for node in path:
        m, n = k_to_mn(node)
        path_array.append([m,n])
    np.savetxt('path.txt', path_array)
    return 0

if __name__=="__main__":
    start = mn_to_k(114.0, 22.0)
    end = mn_to_k(-122.0, 36.0)
    find_path(start, end)