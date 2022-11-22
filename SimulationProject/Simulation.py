from TrafficMap import *
from NetworkGraph import *

class Simulation:

    def __init__(self):
        self.network = NetworkGraph()
        self.trafficMap = TrafficMap()


    def create_roads(self, roads_to_create, curved=False):
        for road in roads_to_create:
            self.__create_road(road, curved)

    # Road : (coords départ, coords arrivée) curved = courbe (True) ou ligne droite (False)
    def __create_road(self, road, curved):
        start, end = road
        self.network.addEdge(start, end, curved)
        #vpython.createRoad(la route, curved)
        # Ou alors 2 fonctions (une pour les lignes droites, une pour les courbes ? Revient quasi au même avec un if en plus)