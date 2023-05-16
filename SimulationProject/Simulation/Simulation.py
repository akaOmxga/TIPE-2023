#coding: utf8

from Simulation.TrafficMap import *
from Simulation.NetworkGraph import *
from Simulation.Car import *
from Simulation.View import *
from random import randint


class Simulation:

    def __init__(self):
        self.internal_clock = 0  # Timer interne, perf_counter prenant en compte la latence du PC
        self.network = NetworkGraph()
        self.trafficMap = TrafficMap()
        self.view = View()
        self.carsList = []

    def create_roads(self, roads_to_create, curved=False):
        for road in roads_to_create:
            self.__create_road(road, curved)

    # Road : (coords départ, coords arrivée) curved = courbe (True) ou ligne droite (False)
    def __create_road(self, road, curved):
        start, end, threshold, speed_limit = road
        self.network.add_edge(start, end, threshold, speed_limit, curved)
        self.view.create_road(start, end, curved)

    def update(self):
        self.internal_clock += 1

        for car in self.carsList:
            car.update(self)

    # Fait apparaître une voiture avec un chemin choisi au hasard entre
    # Un point aléatoire dans une liste (spawn_points) et un point d'arrivée aléatoire parmi
    # une liste de points (destination_points)
    def create_car_random_path(self, spawn_points, destination_points, vitesse):

        # Trouve un point d'apparition et une destination aléatoires parmi ceux possibles
        spawn_coords = spawn_points[randint(0, len(spawn_points) - 1)]
        destination_coords = spawn_coords
        possible_paths = []

        # On fait en sorte d'avoir un chemin forcément de longueur > 1
        # TODO : optimize
        while destination_coords == spawn_coords or len(possible_paths) < 1:
            destination_coords = destination_points[randint(0, len(destination_points) - 1)]

            # Trouve les chemins possibles entre les deux
            possible_paths = self.network.find_all_paths(spawn_coords, destination_coords)

        # On prend un chemin au hasard
        chemin = possible_paths[0]
        if len(possible_paths) > 1:
            chemin = possible_paths[randint(0, len(possible_paths) - 1)]

        vpython_vehicle = spawn_car_test(spawn_coords)

        voiture = Car(spawn_coords, vitesse, vpython_vehicle, chemin, self.internal_clock)

        self.carsList.append(voiture)
        self.trafficMap.add_car_on_road(chemin[0], chemin[1], voiture)

    # Fait apparaître une voiture avec un chemin imposé
    def create_car(self, chemin):
        vitesse = 13,9  # m/s

        vpython_vehicle = spawn_car_test(chemin[0])

        voiture = Car(chemin[0], vitesse, vpython_vehicle, chemin, self.internal_clock)

        self.carsList.append(voiture)
        self.trafficMap.add_car_on_road(chemin[0], chemin[1], voiture)
