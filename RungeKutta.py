import matplotlib.pyplot as plt
import numpy as np

T = 30 # temps final
k = 8
h = T/(2**k)
t = np.linspace(0,T,2**k+1)

β=0.001
γ=0.005

S0 = 500
I0 = 1
R0 = 0
Y = [np.array([S0,I0,R0])]

def f(Y):
    return np.array([-β*Y[0]*Y[1] , β*Y[0]*Y[1] - γ*Y[1] , γ*Y[1] ])

for i in range (2**k):
    Y0 = Y[-1]
    k1 = f(Y0)
    k2 = f(Y0 + (h/2)*k1)
    k3 = f(Y0 + (h/2)*k2)
    k4 = f(Y0 + h*k3)
    Y1 = Y0 + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
    Y.append(Y1)

YRK4 = np.array(Y)

S = YRK4[:,0]
I = YRK4[:,1]
R = YRK4[:,2]
plt.figure(0)
plt.plot(t,S,label="Sains")
plt.plot(t,I,label="Infectés")
plt.plot(t,R,label="Rétablis")
plt.legend()
plt.show()
