from math import *
import View

epsilon = 10  # TODO : modif


class Car:

    ## trajectoire, une fonction donnant la trajectoire de la voiture dans la simulation (propre à chaque lignes/virages) ; chemin, un chemin du graphe représentant l'ensemble des routes (lignes et virages) que la voitures doit empreinter
    # c.f. Victor si on a un problème
    def __init__(self, spawnpoint, speed, vehicle, chemin):
        (x, y, z) = spawnpoint
        self.position = (x, y, z)  # (x,y,z)
        self.speed = speed  # m.s^(-1)
        self.accel = 0  # m.s^(-2), 0 par défaut, car en mvt rect et unif
        self.vehicle = vehicle
        self.chemin = chemin

    def __str__(self):
        return f"Objet voiture, position : {self.position}"

    def update(self,
               simulation_object):  # dispawn les voitures, avancer les voitures, les transitions entre les différents noeud du graphe si la voiture nous informe que c'est le cas
        chemin = self.chemin
        n = len(chemin)

        sommet_fin = chemin[1]
        voiture = self.vehicle  # car = objet Car, voiture = objet vpython

        dm = 1  # distance infinitésimale parcourue par la voiture sur dt
        x, y, z = voiture.pos.x, voiture.pos.y, voiture.pos.z
        if View.distance(sommet_fin, (x, y,
                                      z)) < epsilon:  ## cas où la voiture est proche (à epsilon près) d'une transition de route ; on fait la transition vers a la prochaine route, avec toutes les modifications que cela implique
            if n == 1:
                self.dispawn(simulation_object)
                return

            # update la position
            View.update_car(self, chemin, None)  # dm = none → on change de route

            new_chemin = chemin[1::]
            self.chemin = new_chemin
        else:  # cas où la voiture peut parcourir dm sur la portion de route actuelle
            View.update_car(self, chemin, dm)

    def dispawn(self, simulation_object):
        # Envoyer les infos à vpython + liste voitures dans TrafficMap
        View.dispawn_car(self.vehicle)
        simulation_object.carsList.remove(self)
        del self
