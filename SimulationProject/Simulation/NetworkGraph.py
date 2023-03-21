class NetworkGraph:

    def __init__(self):
        self.network = {}  # Graphe (dictionnaire) sous la formé k,v : coordonnées, sommets connectés (liste d'adj)

    def __str__(self):
        return f"{self.network}"

    # Créé un sommet correspondant physiquement à l'extrémité d'une route
    # x, y, z sont les coordonnées de l'extrémité de la route
    # Méthode privée car on ne doit a priori pas en rajouter un hors de cette classe
    def __addSommet(self, coords):
        self.network[coords] = []

    # Ajoute une arête entre les sommets start et end (représentés par leurs coordonnées)
    def addConnection(self, start, end, curved):
        x, y, z = end
        voisins_de_s1 = self.network[start] + [(x, y, z, curved)]
        self.network[start] = voisins_de_s1

    # Créé les arêtes du graphe.
    # Physiquement, cela correspond à une route ou start et end sont les couples de coordonnées de début et fin de route
    # Si un sommet (extrémité de route) n'existe pas, on le créé avec addSommet
    # start et end sont de la forme (x1, y1, z1) et (x2, y2, z2), curved est un boolean (false = route droite)
    def addEdge(self, start, end, curved=False):
        if start == end:
            raise Exception("Erreur : le départ et l'arrivée d'une route ne peuvent pas être confondus")
        if start not in self.network:
            self.__addSommet(start)
        if end not in self.network:
            self.__addSommet(end)

        self.addConnection(start, end, curved)
        self.addConnection(end, start, curved)

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
        else:
            for i in self.network[current]:
                x, y, z, curved = i  # i est sous la forme (x, y, z, curved), on veut le repasser en x, y, z
                current_edge = (x, y, z)

                if not visited[current_edge]:
                    paths = self.__find(current_edge, end, visited, current_path, paths)

        current_path.pop()
        visited[current] = False

        return paths
