# L'objectif ici est d'avoir un visu sur toutes les voitures présentes sur chaque route en tout temps

from Car import *

class TrafficMap:

    def __init__(self):
        self.traffic_map = {} # Dictionnaire sous la formé k,v : (coordonnées début de route, coordonnées fin de route), liste des voitures sur cette route

    # Créé une "route"
    def addRoad(self, start_coords, end_coords):
        if start_coords == end_coords:
            raise Exception("Erreur : impossible de créer la route, elle n'est pas valide")

        self.traffic_map[(start_coords, end_coords)] = []

    # Ajoute la voiture car sur le segment de route donné
    def addCarOnRoad(self, start_coords, end_coords, car):
        if (start_coords, end_coords) not in self.traffic_map:
            raise Exception("Erreur : la route n'exist pas")
        if start_coords == end_coords:
            raise Exception("Erreur : la route n'est pas valide")

        cars_on_road = self.traffic_map[(start_coords, end_coords)]
        cars_on_road += [car]

        self.traffic_map[(start_coords, end_coords)] = cars_on_road

# TODO : implémenter une file (les voitures seront rangées les unes à la suite des autres et pop quand elles
# sortent de la route
# Faire aussi en sorte de pouvoir intervertir 2 élt dans le futur (pour des dépassements)