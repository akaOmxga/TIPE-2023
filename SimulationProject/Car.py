from math import *
import View

epsilon = 10  # TODO : modif


class Car:

    ## trajectoire, une fonction donnant la trajectoire de la voiture dans la simulation (propre à chaque lignes/virages) ; chemin, un chemin du graphe représentant l'ensemble des routes (lignes et virages) que la voitures doit empreinter
    # c.f. Victor si on a un problème
    def __init__(self, spawnpoint, speed, vehicle, trajectoire, chemin):
        (x, y, z) = spawnpoint
        self.position = (x, y, z)  # (x,y,z)
        self.speed = speed  # m.s^(-1)
        self.accel = 0  # m.s^(-2), 0 par défaut, car en mvt rect et unif
        self.vehicle = vehicle
        self.trajectoire = trajectoire
        self.chemin = chemin

    def __str__(self):
        return f"Objet voiture, position : {self.position}"

    def update(self, road):  ## dispawn les voitures, avancer les voitures, les transitions entre les différents noeud du graphe si la voiture nous informe que c'est le cas
        c = self.chemin
        n = len(c)

        if(n <= 1):
            # n'arrivera plus quand dispawn sera réglé (à suppr)
            return

        sommet_fin = c[1]
        v = self.speed
        voiture = self.vehicle  # car = objet Car, voiture = objet vpython
        dm = 1
        x, y, z = voiture.pos.x, voiture.pos.y, voiture.pos.z
        if View.distance(sommet_fin, (x, y, z)) < epsilon and n == 1:  ## cas où la voiture est  proche  (à epsilon près) de son point d'arrivée ; on fait dispawn la voiture
            self.dispawn()
        elif View.distance(sommet_fin, (x, y, z)) < epsilon:  ## cas où la voiture est proche (à epsilon près) d'une transition de route ; on fait la transition vers a la prochaine route, avec toutes les modifications que cela implique
            # update la position
            (new_x, new_y, new_z) = c[1]
            new_chemin = c[1::]
            voiture.pos = vector(new_x, new_y, new_z)
            # update les propriétés : le chemin
            self.chemin = new_chemin
        else:  ## cas où la voiture peut parcourir dm sur la portion de route actuelle
            start = c[0]
            end = c[1]
            virage = est_virage(start, end)
            new_x, new_y, new_z = trajectoire(x, y, z, dm, start, end, virage, road)
            new_pos = vector(new_x, new_y, new_z)
            #        oriente(voiture,voiture.pos,new_pos)
            voiture.pos = new_pos
        return

    def dispawn(self):
        # Envoyer les infos à vpython + liste voitures dans TrafficMap
        pass