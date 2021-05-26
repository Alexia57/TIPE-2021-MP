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
T = 30 # temps final
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
    S1 = S0 + h*(f(Y0)[0])
    E1 = E0 + h*(f(Y0)[1])
    I1 = I0 + h*(f(Y0)[2])
    R1 = R0 + h*(f(Y0)[3])
    N1=S1+E1+I1+R1
    Y.append([S1,E1,I1,R1,N1])
YEulerExpl = np.array(Y)

S = YEulerExpl[:,0]
E = YEulerExpl[:,1]
I = YEulerExpl[:,2]
R = YEulerExpl[:,3]
N = YEulerExpl[:,4]
plt.figure(0)
plt.plot(t,S,label="Sains")
plt.plot(t,E,label="Exposés")
plt.plot(t,I,label="Infectés")
plt.plot(t,R,label="Rétablis")
plt.plot(t,N,label="Population")
plt.legend()
plt.show()