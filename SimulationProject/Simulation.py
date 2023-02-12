from TrafficMap import *
from NetworkGraph import *
from Car import *
from View import *


class Simulation:

    def __init__(self):
        self.network = NetworkGraph()
        self.trafficMap = TrafficMap()
        self.view = View()
        self.carsList = []

    def create_roads(self, roads_to_create, curved=False):
        for road in roads_to_create:
            self.__create_road(road, curved)

    # Road : (coords départ, coords arrivée) curved = courbe (True) ou ligne droite (False)
    def __create_road(self, road, curved):
        start, end = road
        self.network.addEdge(start, end, curved)
        self.view.create_road(start, end, curved)

    def update(self):
        # TODO : actualiser toutes les voitures
        for car in self.carsList:
            car.update(self)

    def spawn_car_test(self, coords):
        chemin = [(850, 0, 1050), (1050, 0, 1150), (1150, 0, 950), (950, 0, 850), (850, 0, 1050)]
        vitesse = 50  # m/s

        vpython_vehicle = spawn_car_test(coords)

        voiture = Car((850, y_voiture, 1050), vitesse, vpython_vehicle, chemin)

        self.carsList.append(voiture)
        self.trafficMap.addCarOnRoad(chemin[0], chemin[1], voiture)
