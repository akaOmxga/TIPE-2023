# L'objectif ici est d'avoir un visu sur toutes les voitures présentes sur chaque route en tout temps

class TrafficMap:

    def __init__(self):
        self.traffic_map = {} # Dictionnaire sous la formé k,v : (coordonnées début de route, coordonnées fin de route), liste des voitures sur cette route

    def __str__(self):
        return f"{self.traffic_map}"

    # Ajoute la voiture car sur le segment de route donné
    def addCarOnRoad(self, start_coords, end_coords, car):

        # Si la route n'existe pas dans le dico, on la créée
        if (start_coords, end_coords) not in self.traffic_map:
            self.traffic_map[(start_coords, end_coords)] = []
        if start_coords == end_coords:
            raise Exception("Erreur : la route n'est pas valide")

        cars_on_road = self.traffic_map[(start_coords, end_coords)]
        cars_on_road += [car]

        self.traffic_map[(start_coords, end_coords)] = cars_on_road

    def deleteCarFromRoad(self, start_coords, end_coords, car):
        # Si la route n'existe pas dans le dico, on la créée
        if (start_coords, end_coords) not in self.traffic_map:
            self.traffic_map[(start_coords, end_coords)] = []

        cars_on_road = self.traffic_map[(start_coords, end_coords)]
        if (cars_on_road == []):
            return
        if (car not in cars_on_road):
            raise Exception("Erreur : la voiture n'est pas sur la route")


        # Normalement, la voiture qu'on retire se trouve toujours à l'indice 0, mais on traite le cas général dans le doute.
        index = cars_on_road.index(car)
        n = len(cars_on_road)
        if (index != n - 1):
            for i in range (index, len(cars_on_road) - 1):
                cars_on_road[i] = cars_on_road[i + 1]

        cars_on_road = cars_on_road[:-1]

        self.traffic_map[(start_coords, end_coords)] = cars_on_road