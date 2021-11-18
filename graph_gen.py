import numpy as np
import networkx as nx
from scipy import  interpolate
from numpy import sin, cos, pi, sign, sqrt
import matplotlib.pyplot as plt
import math
from global_land_mask import globe
import pickle

def normx(x):
    return (x + 180)%360 - 180

def normy(y):
    return (y + 90)%180 - 90

def sign_check(x):
    if x > 0.01:
        return 1
    if x < -0.01:
        return -1
    
    return 0

def t_cal(v_x, v_y, v_n, theta):
    v_0 = v_x*cos(theta) + v_y*cos(theta)
    a = sign_check(cos(theta))
    b = sign_check(sin(theta))
    L = np.sqrt( a**2 + b**2 )
    v = v_0/2 + np.sqrt(v_n**2 + (v_0/2)**2)
    if v > 0 :
        t = L/v
    else:
        t = 9999999999999
    return t

def mn_to_k(m ,n):
    return str(m) + '_' + str(n)
    #here we define m is the x position and n is the y one, k count in x direction first

def k_to_mn(k):
    m, n = k.split('_', 1)
    return [int(m), int(n)]

def load_v():
    v = np.loadtxt('v.txt')
    return v

def graph_gen(v, v_n):
    G=nx.DiGraph()
    node_list = []
    for v_i in v:
        lon, lat, v_x, v_y = v_i
        if globe.is_land(lat, lon) == 0:
            G.add_node(mn_to_k(lon, lat))
            node_list.append(mn_to_k(lon, lat))
    theta_list = np.arange(0, 2*pi, pi/4)
    for v_i in v:
        lon, lat, v_x, v_y = v_i
        node = mn_to_k(lon, lat)
        if node in node_list:
            for theta in theta_list:
                delta_lon = sign_check(cos(theta))
                delta_lat = sign_check(sin(theta))
            #print(delta_lon, delta_lat)
                new_lon = normx(lon+delta_lon)
                new_lat = normy(lat+delta_lat)
                new_node = mn_to_k(new_lon, new_lat)
                if new_node in node_list:
                    print(node, new_node)
                    G.add_weighted_edges_from([(node, new_node, t_cal(v_x, v_y, v_n, theta) )])
    #print(G.nodes())
    f=open('t.txt','wb')  
    pickle.dump(G,f,-1)  
    f.close()   
    return 0

if __name__=="__main__":
    v_n = 25
    v = load_v()
    graph_gen(v, v_n)