
from math import *
import matplotlib.pyplot as plt

t = 1.0  # temps d'actualisation
a_max = 1.5  # acceleration max
delta = 3.0  # coefficient de smoothness ??
dec_confort = 1.5  # décélération confortable
dec_max = 10.0  # décélération max
v_max = 13.9  # vitesse max
d_min = 2.0  # distance minimale entre deux véhicules
temps_reac = 1.0  # temps de réaction des usagers
l = 2.0  # longueur des véhicules
N = 4  # nombre de voitures
deltat = 30 # intervalle de mesure


def v_etoile(v, delta_v):  # utile pour IDM
    return (d_min + v * temps_reac + v * delta_v / sqrt(2 * a_max * dec_confort))


def acc(V, X):  # calcul des accélérations de chaque voiture avec IDM
    n = len(V)
    L = []
    for k in range(n):
        if k == 0:
            acc = a_max * (1.0 - (V[k] / v_max) ** delta)
            L.append(acc)
        else:
            if X[k - 1] - X[k] - l <= 0:
                acc = 0
            else:
                acc = a_max * (1.0 - (V[k] / v_max) ** delta - (v_etoile(V[k], V[k] - V[k - 1]) / (X[k] - X[k - 1] - l)) ** 2)
            L.append(acc)
    return L


def actualise(X, V, A):  # actualisation de la vitesse et position des voitures
    newX = []
    newV = []
    for k in range(len(V)):
        newV.append(V[k] + t * A[k])
        newX.append(X[k] + t * newV[k])
    return (newX, newV)


liste_position = [[0] for k in range(N)]
liste_vitesse = [[0] for k in range(N)]
pos_init = [0 for k in range(N)]
vit_init = [0 for k in range(N)]
A = acc(vit_init, pos_init)
liste_acc = [[elm] for elm in A]

for k in range(deltat):  # visualisation d l'évolution des données sur 60 secondes
    X, V = actualise(pos_init, vit_init, A)
    pos_init = X
    vit_init = V
    A = acc(vit_init, pos_init)
    for k in range(N):
        liste_position[k].append(X[k])
        liste_vitesse[k].append(V[k])
        liste_acc[k].append(A[k])
T = [k for k in range(deltat + 1)]
for k in range(N):
    plt.plot(T, liste_vitesse[k])

plt.xlabel('temps en seconde')
plt.ylabel('vitesse en m/s')

plt.show()

