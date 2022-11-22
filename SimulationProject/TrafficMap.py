# L'objectif ici est d'avoir un visu sur toutes les voitures présentes sur chaque route en tout temps
from Car import *

class TrafficMap:

    def __init__(self):
        self.traffic_map = {} # Dictionnaire sous la formé k,v : (coordonnées début de route, coordonnées fin de route), liste des voitures sur cette route

    def __str__(self):
        return f"{self.traffic_map}"

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

    def deleteCarFromRoad(self, start_coords, end_coords, car):
        cars_on_road = self.traffic_map[(start_coords, end_coords)]
        if (car not in cars_on_road):
            raise Exception("Erreur : la voiture n'est pas sur la route")

        index = cars_on_road.index(car)
        n = len(cars_on_road)
        if (index != n - 1):
            for i in range (index, len(cars_on_road) - 2):
                cars_on_road[index] = cars_on_road[index + 1]

        cars_on_road = cars_on_road[:-1]

        self.traffic_map[(start_coords, end_coords)] = cars_on_road


# TODO : implémenter une file (les voitures seront rangées les unes à la suite des autres et pop quand elles
# sortent de la route
# Faire aussi en sorte de pouvoir intervertir 2 élt dans le futur (pour des dépassements)

trafficMap = TrafficMap()

voiture1 = Car(10, 1, 1, 1)
voiture2 = Car(10, 10, 1, 1)
voiture3 = Car(10, 20, 1, 1)
voiture4 = Car(10, 30, 1, 1)

trafficMap.addRoad((1, 1, 1), (50, 1, 1))

trafficMap.addCarOnRoad((1, 1, 1), (50, 1, 1), voiture1)
trafficMap.addCarOnRoad((1, 1, 1), (50, 1, 1), voiture2)
trafficMap.addCarOnRoad((1, 1, 1), (50, 1, 1), voiture3)
trafficMap.addCarOnRoad((1, 1, 1), (50, 1, 1), voiture4)

print(trafficMap)

voiture1.speed = 5

print(trafficMap)