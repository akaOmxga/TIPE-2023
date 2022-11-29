from math import *

class Car:

    ## trajectoire, une fonction donnant la trajectoire de la voiture dans la simulation (propre à chaque lignes/virages) ; chemin, un chemin du graphe représentant l'ensemble des routes (lignes et virages) que la voitures doit empreinter
    # c.f. Victor si on a un problème
    def __init__(self, spawnpoint, speed, vehicle, trajectoire, chemin):
        self.position = spawpoint # (x,y,z)
        self.speed = speed # m.s^(-1)
        self.accel = 0  # m.s^(-2), 0 par défaut car en mvt rect et unif
        self.vehicle = vehicle
        self.trajectoire = trajectoire
        self.chemin = chemin

    def __str__(self):
        return f"Objet voiture, position : {position}"