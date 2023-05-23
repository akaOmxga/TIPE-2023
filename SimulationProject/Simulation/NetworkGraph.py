class NetworkGraph:

    def __init__(self):
        # Graphe (implémenté par dictionnaire) sous la formé k,v : coordonnées, sommets connectés (liste d'adj)
        self.network = {}

    def __str__(self):
        return f"{self.network}"

    # Créé un sommet correspondant physiquement à l'extrémité d'une route
    # x, y, z sont les coordonnées de l'extrémité de la route
    # Méthode privée car on ne doit a priori pas rajouter un sommet hors de cette classe
    def __add_sommet(self, coords):
        self.network[coords] = []

    # Ajoute une arête entre les sommets start et end (représentés par leurs coordonnées)
    def add_connection(self, start, end, curved, threshold, speed_limit):
        x, y, z = end
        voisins_de_s1 = self.network[start] + [(x, y, z, curved, threshold, speed_limit)]
        self.network[start] = voisins_de_s1

    # Créé les arêtes du graphe.
    # Physiquement, cela correspond à une route ou start et end sont les couples de coordonnées de début et fin de route
    # Si un sommet (extrémité de route) n'existe pas, on le créé avec addSommet
    # start et end sont de la forme (x1, y1, z1) et (x2, y2, z2), curved est un boolean (false = route droite)
    # threshold et speed_limit sont tels que défini dans le fichier scène
    def add_edge(self, start, end, threshold, speed_limit, curved=False):
        if start == end:
            raise Exception("Erreur : le départ et l'arrivée d'une route ne peuvent pas être confondus")
        if start not in self.network:
            self.__add_sommet(start)
        if end not in self.network:
            self.__add_sommet(end)

        self.add_connection(start, end, curved, threshold, speed_limit)
        self.add_connection(end, start, curved, threshold, speed_limit)

    def get_road_parameters(self, start, end):
        if start == end:
            raise Exception("Erreur : le départ et l'arrivée d'une route ne peuvent pas être confondus")
        if start not in self.network:
            start, end = end, start
            if start not in self.network:
                raise Exception("Erreur : la route n'est pas valide (Start : ", start,", End : ", end, ")")

        for edge in self.network[start]:
            x, y, z, curved, threshold, speed_limit = edge
            if end == (x, y, z):
                return curved, threshold, speed_limit
        raise Exception("Erreur : la route n'est pas valide (Start : ", start,", End : ", end, ")")

    def get_road_threshold(self, start, end):
        _, threshold, _ = self.get_road_parameters(start, end)
        return threshold

    def get_road_speed_limit(self, start, end):
        _, _, speed_limit = self.get_road_parameters(start, end)
        return speed_limit

    # Permet de trouver tous les chemins sans cycles entre start et end (start et end des triplets (x, y, z))
    def find_all_paths(self, start, end):
        visited = {}

        for k in self.network.keys():
            visited[k] = False

        return self.__find(start, end, visited, [], [])

    def __find(self, current, end, visited, current_path, paths):
        visited[current] = True
        current_path.append(current)

        if current == end:
            paths.append(current_path.copy())
        elif len(current_path) < 10:
            for i in self.network[current]:
                # i est sous la forme (x, y, z, curved), on veut le repasser en x, y, z
                x, y, z, curved, threshold, speed_limit = i

                current_edge = (x, y, z)

                if not visited[current_edge]:
                    paths = self.__find(current_edge, end, visited, current_path, paths)

        current_path.pop()
        visited[current] = False

        return paths
