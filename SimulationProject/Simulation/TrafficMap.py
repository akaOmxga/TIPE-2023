# L'objectif ici est d'avoir un visu sur toutes les voitures présentes sur chaque route en tout temps

class TrafficMap:

    def __init__(self):
        # Dictionnaire sous la forme k, v :
        # k : (coordonnées début de route, coordonnées fin de route)
        # v : liste des voitures sur cette route
        self.traffic_map = {}

    def __str__(self):
        return f"{self.traffic_map}"

    # Ajoute l'objet voiture "car" sur le segment de route donné
    def add_car_on_road(self, start_coords, end_coords, car):

        # Si la route n'existe pas dans le dico, on la créée
        if (start_coords, end_coords) not in self.traffic_map:
            self.traffic_map[(start_coords, end_coords)] = []
        if start_coords == end_coords:
            raise Exception("Erreur : la route n'est pas valide")

        cars_on_road = self.traffic_map[(start_coords, end_coords)]
        cars_on_road += [car]

        self.traffic_map[(start_coords, end_coords)] = cars_on_road

    # Supprime l'objet voiture "car" de la route donnée
    def delete_car_from_road(self, start_coords, end_coords, car):
        # Si la route n'existe pas dans le dico, on la créée
        if (start_coords, end_coords) not in self.traffic_map:
            self.traffic_map[(start_coords, end_coords)] = []

        cars_on_road = self.traffic_map[(start_coords, end_coords)]
        if not cars_on_road:
            return
        if car not in cars_on_road:
            return
            #raise Exception("Erreur : la voiture n'est pas sur la route")

        # Normalement, la voiture qu'on retire se trouve toujours à l'indice 0
        # Mais on traite le cas général dans le doute.
        index = cars_on_road.index(car)
        n = len(cars_on_road)
        if index != n - 1:
            for i in range(index, len(cars_on_road) - 1):
                cars_on_road[i] = cars_on_road[i + 1]

        cars_on_road = cars_on_road[:-1]

        self.traffic_map[(start_coords, end_coords)] = cars_on_road

    def get_cars_on_road(self, start_coords, end_coords):
        if (start_coords, end_coords) in self.traffic_map:
            return self.traffic_map[(start_coords, end_coords)]
        else:
            return []  # Ne devrait pas arriver
