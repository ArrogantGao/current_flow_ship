import numpy as np
import random
from scipy import interpolate
from scipy.misc import derivative
import pylab as pl
import matplotlib as mpl

def normx(x):
    return x%360

def normy(y):
    return y%180

def discrete_partial_d(A, m, n):
    print(np.shape(A))
    print(m,n)
    v_x = 0.5*(A[m,normy(n+1)] - A[m,normy(n-1)])
    v_y = -0.5*(A[normx(m+1),n] - A[normx(m-1),n])
    return [v_x ,v_y]


def vector_field_gen():
    m_ran = 36
    n_ran = 18
    x = []
    y = []
    A_random = []
    
    for a in range(int(m_ran)):
        for b in range(int(n_ran)):
            x.append(a*10)
            y.append(b*10)
            A_random.append(random.randint(0,10))
    
    newfunc = interpolate.Rbf(x ,y, A_random, function='multiquadric')
    

    m_new = np.linspace(0, 359, 360)
    n_new = np.linspace(0, 179, 180)
    m_grid, n_grid = np.meshgrid(m_new, n_new)
    A_mn = newfunc(m_grid, n_grid)

    A = np.zeros((360, 180))

    for a in range(360):
        for b in range(180):
            A[a, b] = A_mn[b ,a]


    np.savetxt('A.txt', A, fmt='%f', delimiter=',')
    return A


def fluid_field_gen(A,  v_max_given):
    m = 360
    n = 180

    v = np.zeros((360,180,2))
    for x in range(m):
        for y in range(n):
            v[x,y] = discrete_partial_d(A, x, y)
    v_max_local = np.max(v)
    v_l = []
    for x in range(m):
        for y in range(n):
            x = int(x)
            y = int(y)
            v[x,y] = v[x,y] * v_max_given * 2 / v_max_local
            v_l.append([x-180, y-90, v[x, y, 0], v[x,y,1]])
    print('saving')
    np.savetxt('v.txt', v_l, fmt='%f')
    return v
    
A = vector_field_gen()
v = fluid_field_gen(A, 25)
