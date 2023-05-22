#coding: utf8

from Simulation.TrafficMap import *
from Simulation.NetworkGraph import *
from Simulation.Car import *
from Simulation.View import *
from Simulation.PerformanceStats import *
from random import randint


class Simulation:

    def __init__(self):
        self.internal_clock = 0  # Timer interne (la fonction perf_counter par défaut prend en compte la latence du PC)
        self.network = NetworkGraph()
        self.trafficMap = TrafficMap()
        self.view = View()
        self.stat = Perfs()
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
        # Augmenter de 1 le nombre de voiture ayant spawn dans la simulation :
        self.stat.voitures_apparues += 1

        # Trouve un point d'apparition et une destination aléatoires parmi ceux possibles
        spawn_coords = spawn_points[randint(0, len(spawn_points) - 1)]
        destination_coords = spawn_coords
        possible_paths = []

        # On fait en sorte d'avoir un chemin forcément de longueur > 1
        # TODO : Voir si possible d'optimiser encore
        while (destination_coords == spawn_coords or len(possible_paths) == 0) and destination_points != []:
            destination_coords = destination_points[randint(0, len(destination_points) - 1)]
            destination_points.remove(destination_coords) # On retire le point des destinations possibles
            # ça évite de retomber dessus et de faire des calculs inutiles

            # Trouve les chemins possibles entre les deux
            possible_paths = self.network.find_all_paths(spawn_coords, destination_coords)

        # On prend un chemin au hasard
        chemin = possible_paths[0]
        if (len(possible_paths) > 1):
            chemin = possible_paths[randint(0, len(possible_paths) - 1)]

        vpython_vehicle = spawn_car_test(spawn_coords)

        voiture = Car(spawn_coords, vitesse, vpython_vehicle, chemin, self.internal_clock)

        self.carsList.append(voiture)
        self.trafficMap.add_car_on_road(chemin[0], chemin[1], voiture)

    # Fait apparaître une voiture avec un chemin imposé
    def create_car(self, chemin):
        # Augmenter de 1 le nombre de voiture ayant spawn dans la simulation :
        self.stat.voitures_apparues += 1
        
        # 

        vitesse = 13,9  # m/s

        vpython_vehicle = spawn_car_test(chemin[0])

        voiture = Car(chemin[0], vitesse, vpython_vehicle, chemin, self.internal_clock)

        self.carsList.append(voiture)
        self.trafficMap.add_car_on_road(chemin[0], chemin[1], voiture)

    # Fait apparaître une voiture avec un point de spawn et de destination imposé, chemin random:

    def create_car_random_gps(self,start,end,vitesse) :
        # Augmenter de 1 le nombre de voiture ayant spawn dans la simulation :
        self.stat.voitures_apparues += 1

        #  point d'apparition et une destination 
        spawn_coords = start
        destination_coords = end

        # Trouve les chemins possibles entre les deux
        possible_paths = self.network.find_all_paths(spawn_coords, destination_coords)

        # On prend un chemin au hasard
        chemin = possible_paths[randint(0, len(possible_paths) - 1)]

        vpython_vehicle = spawn_car_test(spawn_coords)

        voiture = Car(spawn_coords, vitesse, vpython_vehicle, chemin, self.internal_clock)

        self.carsList.append(voiture)
        self.trafficMap.add_car_on_road(chemin[0], chemin[1], voiture)
        return

    # Fait apparaître une voiture avec un point de spawn et de destination imposé, qui passe par le chemin le plus court :

    def create_car_shortest_path(self,start,end,vitesse) :
        # Augmenter de 1 le nombre de voiture ayant spawn dans la simulation :
        self.stat.voitures_apparues += 1

        #  point d'apparition et une destination 
        spawn_coords = start
        destination_coords = end

        # Trouve les chemins possibles entre les deux
        possible_paths = self.network.find_all_paths(spawn_coords, destination_coords)

        # On teste le chemin le plus court parmi ceux de possible_paths
        chemin = possible_paths[0]
        minimun_longueur = longueur_chemin(chemin)
        for path in possible_paths :
            if longueur_chemin(path) < minimun_longueur :
                chemin = path

        # on spawn la voiture :

        vpython_vehicle = spawn_car_test(spawn_coords)

        voiture = Car(spawn_coords, vitesse, vpython_vehicle, chemin, self.internal_clock)

        self.carsList.append(voiture)
        self.trafficMap.add_car_on_road(chemin[0], chemin[1], voiture)
        return



    
