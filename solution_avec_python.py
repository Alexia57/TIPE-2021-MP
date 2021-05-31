import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integr

T = 10 # temps final
k = 8
h = T/(2**k)
t = np.linspace(0,T,2**k+1)

β=0.08
γ=0.05
α=0.75
ν=0.009
μ=0.01

S0 = 500
E0 = 0
I0 = 1
R0 = 0
N0 = S0+E0+I0+R0
Y = [np.array([S0,E0,I0,R0,N0])]

def f(Y):
    return np.array([-β*Y[0]*Y[2]+ν*Y[4]-μ*Y[0],
    β*Y[0]*Y[2]-α*Y[1]-μ*Y[1],
    α*Y[1]-γ*Y[2]-μ*Y[2],
    γ*Y[2]-μ*Y[3],
    Y[0]+Y[1]+Y[2]+Y[3]])

X=integr.odeint(f,Y,t)
plt.plot(X[:,0],X[:,1],X[:,2],X[:,3],X[:,4])
plt.show()