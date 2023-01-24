from TrafficMap import *
from NetworkGraph import *
from View import *


class Simulation:

    def __init__(self):
        self.network = NetworkGraph()
        self.trafficMap = TrafficMap()
        self.view = View()


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
        pass