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
T = 50 # temps final
k = 8
h = T/(2**k)
t = np.linspace(0,T,2**k+1)

β=0.0008
γ=1/6
α=0


S0 = 1000
I0 = 10
R0 = 0
N0 = S0+I0+R0
Y = [[S0,I0,R0,N0]]

for i in range (2**k):
    S0,I0,R0,N0 = Y[-1]
    S1 = S0 + h*(-β*S0*I0-α*S0)
    I1 = I0 + h*(β*S0*I0-γ*I0)
    R1 = R0 + h*(γ*I0+α*S0)
    N1=S1+I1+R1
    Y.append([S1,I1,R1,N1])

YEulerExpl = np.array(Y)

S = YEulerExpl[:,0]
I = YEulerExpl[:,1]
R = YEulerExpl[:,2]
N = YEulerExpl[:,3]
plt.figure(0)
plt.plot(t,S,label="Susceptibles")
plt.plot(t,I,label="Infectés")
plt.plot(t,R,label="Retirés")
plt.plot(t,N,label="Population")
plt.xlabel("Temps")
plt.ylabel("nombre d'individus")
plt.title("Solution du modèle SIR avec vaccination")
plt.legend()
plt.show()