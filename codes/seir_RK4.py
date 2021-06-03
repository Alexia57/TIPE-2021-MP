
import matplotlib.pyplot as plt
import numpy as np

# Epidémie Covid-19
# Population globale constituée de trois catégories:
# o Les individus susceptibles d'être infectés, personne saine (S)
# o Les individus atteinds du virus, infectés (I)
# o Les individus guéris (R)

# β : taux d'infection
# γ : taux de rémission

# Sous ces hypothèses, le modèle de propagation de l'épidémie est le suivant:
# S'= -βSI
# I'= βSI-γI
# R'= γI

# Euler explicite :
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
E = YRK4[:,1]
I = YRK4[:,2]
R = YRK4[:,3]
N = YRK4[:,4]


plt.figure(0)
plt.plot(t,S,label="Sains")
plt.plot(t,E,label="Exposés")
plt.plot(t,I,label="Infectés")
plt.plot(t,R,label="Retirés")
plt.plot(t,N,label="Population")
plt.legend()
plt.show()

