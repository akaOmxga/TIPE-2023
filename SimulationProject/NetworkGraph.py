# class GraphRoad:
#
#     def __init__(self, start, end, curved):
#         self.start = start
#         self.end = end
#         self.curved = curved

class NetworkGraph:

    def __init__(self):
        self.network = {} # Graphe (dictionnaire) sous la formé k,v : coordonnées, sommet

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
    # Si un sommet (extrêmité de route n'existe pas -> on le créé avec addSommet)
    # start et end sont de la formes (x1, y1, z1) et (x2, y2, z2), curved est un boolean (false = route droite)
    def addEdge(self, start, end, curved = False):
        if start == end:
            raise Exception("Erreur : le départ et l'arrivée d'une route ne peuvent pas être confondus")
        if start not in self.network:
            self.__addSommet(start)
        if end not in self.network:
            self.__addSommet(end)

        self.addConnection(start, end, curved)


graph = NetworkGraph()
graph.addEdge((1, 1, 0), (1, 2, 0))
graph.addEdge((1, 1, 0), (1, 3, 0))
graph.addEdge((1, 2, 0), (1, 3, 0))
graph.addEdge((1, 2, 0), (1, 4, 0))
print(graph.network)