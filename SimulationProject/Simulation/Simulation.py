#coding: utf8

from Simulation.TrafficMap import *
from Simulation.NetworkGraph import *
from Simulation.Car import *
from Simulation.View import *
from Simulation.GPS import * 
from Simulation.PerformanceStats import *
from random import randint


class Simulation:

    def __init__(self, max_length):
        self.internal_clock = 0  # Timer interne (la fonction perf_counter par défaut prend en compte la latence du PC)
        self.network = NetworkGraph()
        self.trafficMap = TrafficMap()
        self.view = View()
        self.stats = PerformanceStats(self)
        self.carsList = []
        self.max_length = max_length
        self.gps = PositioningSystem(max_length/4)
        

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
    def create_car_random_path(self, spawn_points, destination_points_to_copy, vitesse):
        # Augmenter de 1 le nombre de voiture ayant spawn dans la simulation :
        self.stats.voitures_apparues += 1

        destination_points = destination_points_to_copy.copy()
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
            possible_paths = self.network.find_all_paths(spawn_coords, destination_coords,self.max_length)

        # test si les chemins existent 
        if len(possible_paths) == 0:
            #print("Pas de chemin depuis ", spawn_coords, " on retente avec des nouveaux points randoms")
            return

        # On prend un chemin au hasard
        chemin = possible_paths[0]
        if (len(possible_paths) > 1):
            chemin = possible_paths[randint(0, len(possible_paths) - 1)]
        
        # On fait spawn la voiture
        vpython_vehicle = spawn_car_test(spawn_coords)
        voiture = Car(spawn_coords, vitesse, vpython_vehicle, chemin, self.internal_clock)
        self.carsList.append(voiture)
        self.trafficMap.add_car_on_road(chemin[0], chemin[1], voiture)

    # Fait apparaître une voiture avec un chemin imposé
    def create_car(self, chemin):
        # Augmenter de 1 le nombre de voiture ayant spawn dans la simulation :
        self.stats.voitures_apparues += 1
        
        # on fait spawn la voiture
        vitesse = 13.9  # m/
        vpython_vehicle = spawn_car_test(chemin[0])
        voiture = Car(chemin[0], vitesse, vpython_vehicle, chemin, self.internal_clock)
        self.carsList.append(voiture)
        self.trafficMap.add_car_on_road(chemin[0], chemin[1], voiture)

    # Fait apparaître une voiture avec un point de spawn et de destination imposé, chemin random:

    def create_car_random_gps(self,start,end,vitesse) :
        # Augmenter de 1 le nombre de voiture ayant spawn dans la simulation :
        self.stats.voitures_apparues += 1

        #  point d'apparition et une destination 
        spawn_coords = start
        destination_coords = end

        # Trouve les chemins possibles entre les deux
        possible_paths = self.network.find_all_paths(spawn_coords, destination_coords,self.max_length)
        
        # test si les chemins existent 
        if len(possible_paths) == 0:
            #print("Pas de chemin depuis ", spawn_coords, " on retente avec des nouveaux points randoms")
            return

        # On prend un chemin au hasard
        chemin = possible_paths[0]
        if (len(possible_paths) > 1):
            chemin = possible_paths[randint(0, len(possible_paths) - 1)]

        # On prend un chemin au hasard
        chemin = possible_paths[randint(0, len(possible_paths) - 1)]
        vpython_vehicle = spawn_car_test(spawn_coords)
        voiture = Car(spawn_coords, vitesse, vpython_vehicle, chemin, self.internal_clock)
        self.carsList.append(voiture)
        self.trafficMap.add_car_on_road(chemin[0], chemin[1], voiture)
        return

    # Fait apparaître une voiture avec un point de spawn et de destination imposé, qui passe par le chemin le plus court :

    def create_car_shortest_path_length(self, start, end, vitesse):
        # Augmenter de 1 le nombre de voiture ayant spawn dans la simulation :
        self.stats.voitures_apparues += 1

        #  point d'apparition et une destination 
        spawn_coords = start
        destination_coords = end

        # Trouve les chemins possibles entre les deux
        possible_paths = self.network.find_all_paths(spawn_coords, destination_coords,self.max_length)

        # test si les chemins existent 
        if len(possible_paths) == 0:
            #print("Pas de chemin depuis ", spawn_coords, " on retente avec des nouveaux points randoms")
            return

        # On teste le chemin le plus court (en terme de distance de parcourt) parmi ceux de possible_paths
        chemin = possible_paths[0]
        minimun_longueur = longueur_chemin(chemin)
        for path in possible_paths :
            minimum_potentiel = longueur_chemin(path)
            if minimum_potentiel < minimun_longueur:
                minimun_longueur = minimum_potentiel
                chemin = path

        # on spawn la voiture :
        vpython_vehicle = spawn_car_test(spawn_coords)
        voiture = Car(spawn_coords, vitesse, vpython_vehicle, chemin, self.internal_clock)
        self.carsList.append(voiture)
        self.trafficMap.add_car_on_road(chemin[0], chemin[1], voiture)
        return

    
    def create_car_shortest_path_time(self,start,end,vitesse):
        # Augmenter de 1 le nombre de voiture ayant spawn dans la simulation :
        self.stats.voitures_apparues += 1
        #  point d'apparition et une destination 
        spawn_coords = start
        destination_coords = end

        # Trouve les chemins possibles entre les deux
        possible_paths = self.network.find_all_paths(spawn_coords, destination_coords,self.max_length)

        # test si les chemins existent 
        if len(possible_paths) == 0:
            #print("Pas de chemin depuis ", spawn_coords, " on retente avec des nouveaux points randoms")
            return

        # On teste le chemin le plus court (en terme de temps de parcourt) parmi ceux de possible_paths
        chemin = possible_paths[0]
        minimum_temps = temps_chemin(chemin, self)
        for path in possible_paths:
            temps_a_tester = temps_chemin(path, self)
            if temps_a_tester < minimum_temps:
                minimum_temps = temps_a_tester
                chemin = path

        # on spawn la voiture :
        vpython_vehicle = spawn_car_test(spawn_coords)
        voiture = Car(spawn_coords, vitesse, vpython_vehicle, chemin, self.internal_clock)
        self.carsList.append(voiture)
        self.trafficMap.add_car_on_road(chemin[0], chemin[1], voiture)
        return
    # fonction création de la matrice des chemins:

    ### hypothèse : autant de spawn que de destination numéroté par leur indice dans les listes spawn et destination
    # renvoie une matrice m / m[i][j] contient une liste all_paths entre le start i et la destination j
    def matrix_all_paths(self,spawn_points,destination_points) :
        matrix = [[[]for i in range(len(spawn_points)-1) ] for j in range(len(destination_points)-1)]
        for i in range(len(spawn_points)-1) :
            for j in range(len(destination_points)-1) :
                start = spawn_points[i]
                end = destination_points[j]
                matrix[i][j] = self.network.find_all_paths(start,end,self.max_length)
        return matrix
    
    def matrix_all_paths_shortest(self,spawn_points,destination_points) :
        matrix = [[[]for i in range(len(spawn_points)) ] for j in range(len(destination_points))]
        for i in range(len(spawn_points)) :
            for j in range(len(destination_points)) :
                start = spawn_points[i]
                end = destination_points[j]
                liste_chemins = self.network.find_all_paths(start,end,self.max_length)
                pc_chemin = liste_chemins[0]
                for path in liste_chemins :
                    if temps_chemin(path,self) < temps_chemin(pc_chemin,self) :
                        pc_chemin = path
                matrix[i][j] = pc_chemin
        return matrix
    
    # spawn les voitures grâce aux matrices de chemin :

    def create_car_matrix_all_paths(self, matrice) :
        # Augmenter de 1 le nombre de voiture ayant spawn dans la simulation :
        self.stats.voitures_apparues += 1

        # Trouve un point d'apparition et une destination aléatoires parmi ceux possibles
        spawn_coords = randint(0, len(matrice) - 1)
        destination_coords = randint(0, len(matrice[0]) - 1)

        # test si le chemin existe
        chemin = randint(0, len(matrice[spawn_coords][destination_coords]))
        while len(chemin) == 0 :
            chemin = randint(0, len(matrice[spawn_coords][destination_coords]))

        # On fait spawn la voiture
        vitesse = 15
        vpython_vehicle = spawn_car_test(chemin[0])
        voiture = Car(chemin[0], vitesse, vpython_vehicle, chemin, self.internal_clock)
        self.carsList.append(voiture)
        self.trafficMap.add_car_on_road(chemin[0], chemin[1], voiture)