Web VPython 3.2


#################################################################################       SETUP ET CLASS          #########################################################

## ici on modélise les routes, fait avancer les voitures et modifit les graphes en même temps

y_reference = 5
y_voiture = 7
largeur_route = 15
largeur_voiture = 10
hauteur_voiture =10
longueur_voiture = 20

scene.width = scene.height = 1000
scene.range = 200
scene.background = color.white
scene.center = vector(1000,100,1000)

Ux = vector(1, 0, 0)
Uy = vector(0, 1, 0)
Uz = vector(0, 0, 1)

## base orthonormée

scalaire = 100

fleche_x = arrow(pos=vector(0, 100, 0), axis=vector(scalaire, 0, 0), shaftwidth=1)
fleche_y = arrow(pos=vector(0, 100, 0), axis=vector(0, scalaire, 0), shaftwidth=1)
fleche_z = arrow(pos=vector(0, 100, 0), axis=vector(0, 0, scalaire), shaftwidth=1)


class Car:

    def __init__(self, spawnpoint, speed, vehicle,chemin):  ## trajectoire, une fonction donnant la trajectoire de la voiture dans la simulation (propre à chaque lignes/virages) ; chemin, un chemin du graphe représentant l'ensemble des routes (lignes et virages) que la voitures doit empreinter
        (x, y, z) = spawnpoint
        self.position = (x, y, z)  # (x,y,z)
        self.speed = speed  # m.s^(-1)
        self.accel = 0  # m.s^(-2), 0 par défaut car en mvt rect et unif
        self.vehicle = vehicle
        self.trajectoire = trajectoire
        self.chemin = chemin
        self.temps = 0


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
    # Si un sommet (extrêmité de route n'existe pas -> on le créé avec addSommet)
    # start et end sont de la formes (x1, y1, z1) et (x2, y2, z2), curved est un boolean (false = route droite)
    def addEdge(self, start, end, curved=False):
        if start == end:
            raise Exception("Erreur : le départ et l'arrivée d'une route ne peuvent pas être confondus")
        if start not in self.network:
            self.__addSommet(start)
        if end not in self.network:
            self.__addSommet(end)

        self.addConnection(start, end, curved)


# L'objectif ici est d'avoir un visu sur toutes les voitures présentes sur chaque route en tout temps

class TrafficMap:

    def __init__(self):
        self.traffic_map = {}  # Dictionnaire sous la formé k,v : (coordonnées début de route, coordonnées fin de route), liste des voitures sur cette route

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
            for i in range(index, len(cars_on_road) - 1):
                cars_on_road[i] = cars_on_road[i + 1]

        cars_on_road = cars_on_road[:-1]

        self.traffic_map[(start_coords, end_coords)] = cars_on_road


class Roads:  ## à faire, lorsque l'on créer une ligne ou un virage, il faut ajouter la portion dans la liste reseau

    def __init__(self):
        self.reseau = []

    def createLigne(self, start, end):
        (a, b, c), (x, y, z) = start, end
        longueur = sqrt((x - a) ** 2 + (z - c) ** 2)
        route = box(pos=vector((a + x) / 2, (b + y) / 2, (c + z) / 2),
                    size=vector(longueur, y_reference, largeur_voiture))
        if x != a:
            theta = atan((z - c) / (x - a))
            alpha = atan((y - b) / (x - a))
            rota = Uz.rotate(-theta, vector(0, 1, 0))
            route.rotate(-theta, vector(0, 1, 0))
            route.rotate(alpha, rota)
        else:
            theta = sign(z - c) * pi / 2
            alpha = atan((y - b) / (z - c))
            rota = Uz.rotate(-theta, vector(0, 1, 0))
            route.rotate(-theta, vector(0, 1, 0))
            route.rotate(-alpha, rota)

    def createVirage(self, start, end, reverse = False):
        (a, b, c), (x, y, z) = start, end
        delta_x = x - a
        delta_z = z - c
        r = min(abs(delta_x), abs(delta_z))

        ## par convention, on tourne d'abord, avec un rayon étant le min des distances, puis ensuite lignes droite
        ## on peut obtenir l'inverse en réalisant virage(end,start)!! penser à le faire 
        if abs(delta_x) < abs(delta_z):
            centre_v = vector(a, b, c + sign(delta_z) * r)
            sortie_virage = (a + sign(delta_x) * r, b, c + sign(delta_z) * r)
            if sign(delta_x) > 0 and sign(delta_z) > 0:
                alpha, beta = 0, pi / 2
            elif sign(delta_x) < 0 and sign(delta_z) > 0:
                alpha, beta = pi / 2, pi
            elif sign(delta_x) < 0 and sign(delta_z) < 0:
                alpha, beta = pi, 3 * pi / 2
            else:
                alpha, beta = -pi / 2, 0
        else:
            centre_v = vector(a + sign(delta_x) * r, b, c)
            sortie_virage = (a + sign(delta_x) * r, b, c + sign(delta_z) * r)
            if sign(delta_x) < 0 and sign(delta_z) < 0:
                alpha, beta = 0, pi / 2
            elif sign(delta_x) > 0 and sign(delta_z) < 0:
                alpha, beta = pi / 2, pi
            elif sign(delta_x) > 0 and sign(delta_z) > 0:
                alpha, beta = pi, 3 * pi / 2
            else:
                alpha, beta = -pi / 2, 0 #pi/2 , pi  ## avant 
        centre_virage = (centre_v.x, centre_v.y, centre_v.z)
        ##if et else seulement visuel
        v = extrusion(path=paths.arc(pos=centre_v, radius=r, angle1=alpha, angle2=beta), shape=[shapes.rectangle(width=largeur_route, height=y_reference)])
        ## ligne entre sortie-virage et fin
        (d, e, f) = sortie_virage
        if (d != x) or (e != y) or (f != z):
            longueur = sqrt((x - d) ** 2 + (z - f) ** 2) + 2  # +2 pr rendre smooth la transition
            route = box(pos=vector((d + x) / 2, (e + y) / 2, (f + z) / 2),
                        size=vector(longueur, y_reference, largeur_route))
            theta = atan((z - f) / (x - d))
            route.rotate(-theta, vector(0, 1, 0))


###############################################################################             MODELISATION        ###################################################################################

##### variables du modèle #####

delta_f = 10  ## distance avec laquelle on compare la distance entre deux voitures ; pour freiner
delta_a = 50  ## distance avec laquelle on compare la distance entre deux voitures ; pour accélérer
epsilon = 8  ## distance avec laquelle on compare dm, le pas d'actualisation des voitures ; pour les transitions de route // epsilon = 8 minimun

### IMPLEMENTER LES TRAJECTOIRES ET FAIRE AVANCER LES VOITURES LE LONG D'UN GRAPHE ###

## permet d'avoir un booléen traduisant si la route reliant start et end est un virage 
def est_virage(start, end):
    (a, b, c) = start
    (x, y, z) = end
    if a != x and c != z:
        return (True)  # il s'agit d'un virage
    else:
        return (False)

def distance(point1, point2):
    a, b, c = point1
    x, y, z = point2
    return (sqrt((x - a) ** 2 + (y - b) ** 2 + (z - c) ** 2))


def arctan_2(y, x):
    if (sqrt(x ** 2 + y ** 2) + x == 0):
        return 0

    else:
        return (2 * atan(y / (sqrt(x ** 2 + y ** 2) + x)))
    

def info_virage(start, end):  ## renvoie (centre,r) le centre et le rayon du virage entre les sommets 1 et 2
        (a, b, c), (x, y, z) = start, end
        delta_x = x - a
        delta_z = z - c
        r = min(abs(delta_x), abs(delta_z))
        if abs(delta_x) < abs(delta_z):
            centre_v = vector(a, b, c + sign(delta_z) * r)
            sortie_virage = (a + sign(delta_x) * r, b, c + sign(delta_z) * r)
        else:
            centre_v = vector(a + sign(delta_x) * r, b, c)
            sortie_virage = (a + sign(delta_x) * r, b, c + sign(delta_z) * r)
        centre_virage = (centre_v.x, centre_v.y, centre_v.z)
        return(centre_virage,sortie_virage,r)
    
def sens (start,end) : ## renvoie, pour le virage compris entre start et end, +1 ou -1 selon le sens de rotation de ce virage, avec la convention : rotation trigonométrique -> =1, rotation horaire -> -1, CF PHOTO tel victor pour plus de détails dans le sens de chaque virage
    centre, sortie, rayon = info_virage(start,end)
    (x0,y0,z0) = centre
    (a,b,c) = start
    (x,y,z) = end
    delta_x = x - a
    delta_z = z - c
    delta_centre = z0 - c 
    if (delta_x < 0) and (delta_z > 0) and (delta_centre > 0) : #type de virage n°1
        return(+1)
    elif (delta_x < 0) and (delta_z < 0) and (delta_centre = 0) : #2
        return(+1)
    elif (delta_x > 0) and (delta_z > 0) and (delta_centre = 0) : #3  
        return(+1)
    elif (delta_x > 0) and (delta_z < 0) and (delta_centre < 0) : #4 
        return(+1)
    elif (delta_x > 0) and (delta_z < 0) and (delta_centre = 0) : #5 
        return(-1)
    elif (delta_x > 0) and (delta_z > 0) and (delta_centre > 0) : #6 
        return(-1)
    elif (delta_x < 0) and (delta_z < 0) and (delta_centre < 0) : #7
        return(-1)
    elif (delta_x < 0) and (delta_z > 0) and (delta_centre = 0) : #8
        return(-1)
    else : 
        return(+1) ## sécurité 
    
    
def rotation_y(triplet,theta) : ## renvoie la rotation du vecteur(triplet) d'un angle theta, selon Ux ## angle theta en radian ou en dregre ??
    (a,b,c) = triplet
    alpha = a*cos(theta)-c*sin(theta)
    beta = b
    gamma = a*sin(theta)+c*cos(theta)
    return(vector(alpha,beta,gamma))


## la fct trajectoire renvoyée sera de R4 dans R3 / trajectoire(x,y,z,l...) ,où (x,y,z) est la position actuelle et l la distance que la voiture peut parcourir pendant dt selon le modèle (double intégration du pfd selon dt), renvoie la nouvelle position (x',y',z') / la voiture ait parcouru l depuis (x,y,z)
def trajectoire(x, y, z, l, start, end, virage):
    if virage == False:
        (x0, y0, z0) = start
        (x1, y1, z1) = end
        d = distance(start, end)
        return (x + l * (x1 - x0) / d, y_voiture, z + l * (z1 - z0) / d) # new_y = y + l * (y1 - y0) / d, ici flm, on considère le cas en 2D
    else:
        ## prendre le vecteur de centre à pos voiture
        centre,sortie, rayon = info_virage(start,end)
        a,b,c = centre #important , pour def v par la suite, vector(centre) ne fonctionne pas mais il faut écrire vector(a,b,c)
        vecteur_centre = vector(a,b,c)
        vecteur_rayon = vector(x,y,z) - vecteur_centre
        ## le rotate de theta autour de vector(0,1,0) en position centre / ou (0,0,0)
        theta = -sens(start,end)*l/rayon
        new_vecteur_rayon = rotation_y((vecteur_rayon.x,vecteur_rayon.y,vecteur_rayon.z),theta)
        ## calculer le nouveau vecteur position noté v
        v = vecteur_centre + new_vecteur_rayon
        ## update la voiture 
        return(v.x,y_voiture ,v.z)

def pfd_test(voiture, dt, network, map, contexte=()):
    return (1)

## constante IDM.py
acc_max = 1 ## accélération maximale 
exp_acc = 4 ## coefficient de smoothness
dec_confortable = 1.5 ## décélération confortable
dec_max = 10 ## décélération maximale
speed_max = 50 ## vitesse maximale ; envisageable : la vitesse maximale dépend de la route sur laquelle on circule
distance_min = 2 ## distance de sécurité, minimale entre deux voitures
temps_reaction = 1 ## temps de réaction du conducteur

def distance_securite(vitesse, delta_vitesse) : ## représente s* dans IDM.py // d'aute modélisation de IDM.py retourne (distance_min + max(0,v*temps_reaction + v*delta_v/sqrt(2acc_max*dec_confortable=)))
    return(distance_min + vitesse*temps_reaction + vitesse*delta_vitesse/sqrt(2*acc_max*dec_confortable))

def pfd_IDM(voiture, dt, network, map,contexte=()):  ## renvoie la l'accélération de la voiture dans les conditions décrites par le contexte (network,map)
    ## contexte est un élément de la modélisation venant modifié le comportement du véhicule. Ex : les stops, les feux rouges ...
    v = prochain_vehicule(voiture, network, map)
    if v = None :
        acceleration =  acc_max*(1-(voiture.speed/speed_max)**exp_acc)
    else :
        pos_voiture = (voiture.pos.x, voiture.pos.y, voiture.pos.z)
        pos_prochaine_voiture = (v.pos.x, v.pos.y, v.pos.z)
        acceleration = acc_max*(1-(voiture.speed/speed_max)**exp_acc - (distance_securite(voiture.speed,(v.speed - voiture.speed))/distance(pos_voiture,pos_prochaine_voiture))**2)
    return (acceleration)
    
def pfd_basic(voiture, dt, network, map) :
    return()
    


def integration(v, accel,dt):  ##  modifiable, ici on intégre 2 fois en considérant les conditions initialses v0 = 0 (à réfléchir) et x0=0 (ce qui est nécessaire)
    return ((1 / 2) * accel * dt ** 2 + v * dt)


def sous_liste(n, liste):  ## renvoie liste[n::]
    rep = []
    for i in range(n, len(liste)):
        rep.append(liste[i])
    return (rep)

def orthogonal_Oxz(v,centre) : ## renvoie le vecteur orthogonal à v dans le plan Oxz par rapport au centre du virage
    (x0,y0,z0) = centre
    (x,y,z) = (v.x,v.y,v.z)
    delta_pos = vector(x - x0, y - y0 , z - z0)
    alpha = -delta_pos.z
    beta = delta_pos.y
    gamma = delta_pos.x
    v = vector(alpha,beta,gamma)
    return(longueur_voiture*norm(v))

def oriente(voiture,virage,start,end): ## oriente la voiture lorsqu'elle tourne dans le virage
    if virage == False :
        (a,b,c) = start
        (x,y,z) = end
        v = vector(x-a,y-b,z-c)
        return(longueur_voiture*norm(v))
    else :
        centre, sortie, rayon = info_virage(start,end)
        vecteur_orientation = orthogonal_Oxz(voiture.pos,centre)
        return(vecteur_orientation)

def actualise(car, dt, network, map, road):  ## dispawn les voitures, avancer les voitures, les transitions entre les différents noeud du graphe si la voiture nous informe que c'est le cas
    c = car.chemin
    n = len(c)
    sommet_fin = c[1]
    v = car.speed
    voiture = car.vehicle  ## car est l'élément du module tant dis que voiture est l'objet Vpython
    dm = 1  # integration(v,pfd_test(voiture,dt,network,map),dt) #distance infinitésimale parcourue par la voiture sur dt
    x, y, z = voiture.pos.x, voiture.pos.y, voiture.pos.z
    if distance(sommet_fin, (x, y,z)) < epsilon and n == 1:  ## cas où la voiture est  proche  (à epsilon près) de son point d'arrivée ; on fait dispawn la voiture
        dispawn(voiture)
    elif distance(sommet_fin, (x, y, z)) < epsilon:  ## cas où la voiture est proche (à epsilon près) d'une transition de route ; on fait la transition vers a la prochaine route, avec toutes les modifications que cela implique
        # update la position
        (new_x, new_y, new_z) = c[1]
        new_chemin = sous_liste(1, c)
        voiture.pos = vector(new_x, y_voiture , new_z)
        # update les propriétés : le chemin
        car.chemin = new_chemin
    else:  ## cas où la voiture peut parcourir dm sur la portion de route actuelle
        start = c[0]
        end = c[1]
        virage = est_virage(start, end)
        if virage == True :
            centre,sortie,rayon = info_virage(start,end)
            if c[1] != sortie :
                new_chemin = [c[0]] + [sortie] + c[1:]
                car.chemin = new_chemin
            debut = car.chemin[0]
            fin = car.chemin[2]
            new_x, new_y, new_z = trajectoire(x, y, z, dm, debut, fin, virage)
            new_pos = vector(new_x, new_y, new_z)
            vecteur_orientation = oriente(voiture,virage,debut,fin)
        else :
            new_x, new_y, new_z = trajectoire(x, y, z, dm, start, end, virage) ## le deuxième start est useless, c'est pour combler
            new_pos = vector(new_x, new_y, new_z)
            vecteur_orientation = oriente(voiture,virage,start,end)
        voiture.axis = vecteur_orientation
        voiture.pos = new_pos
        voiture.up = vector(0,1,0) ## afin qu'elle reste "plaqué" au sol
    return ()


def Simulation(dt, liste_bagnoles, network, map, road):  ## à faire dans une boucle while true
    ## spawner les voitures :

    ## actualise les voitures :
    for voiture in liste_bagnoles:
        actualise(voiture, dt, network, map, road)


def dispawn(voiture):
    voiture_vpython = voiture.vehicle
    voiture_vpython.visible = False
    del voiture_vpython


def calcul_chemin(S1, S2, road):
    if est_virage(S1, S2) == False:
        return (distance(S1, S2))
    else:
        centre,sortie, rayon = info_virage(S1, S2, road)
        (a, b, c) = centre
        (x, y, z) = S2
        if a + sign(x - a) * rayon == x:
            sortie_virage = (a + sign(x - a) * rayon, b, c)
        else:
            sortie_virage = (a, b, c + sign(z - c) * rayon)
        return ((pi / 2) * rayon + distance(sortie_virage, S2))


def longueur_chemin(chemin, road):  ## renvoie la longueur en mètre d'un chemin
    reponse = 0
    for i in range(len(chemin) - 1):
        reponse = reponse + calcul_chemin(chemin[i], chemin[i + 1], road)
    return(reponse)


###############################################################################             SIMULATION          ####################################################################################

########################################### créer la route

#route0 = Roads()   ## ligne droite 
#route0.createLigne((-200,0,0),(-100,0,0)) 
#route0.createLigne((-100,0,0),(100,0,0))
#route0.createLigne((100,0,0),(200,0,0))

#route1 = Roads() ## ligne droite puis virage 
#route1.createLigne((-200,0,0),(0,0,0))
#route1.createVirage((0,0,0),(100,0,-100))

#route2 = Roads() ## virage puis ligne droite
#route2.createVirage((1, 0, 1), (100, 0, 100))
#route2.createLigne((100, 0, 100), (200, 0, 100))

#route3 = Roads()  ## plusieurs voiture sur différentes routes qui ne se croisent pas

#route4 = Roads()  ## plusieurs voitures pas sur le meme reseau

#route5 = Roads()  ## plusieurs voitures sur le meme reseau

## grand rond point centré en 0,0
rond_point = Roads()
rond_point.createVirage((850,0,1050),(1050,0,1150))
rond_point.createVirage((1050,0,1150),(1150,0,950))
rond_point.createVirage((1150,0,950),(950,0,850))
rond_point.createVirage((950,0,850),(850,0,1050))


## test pfd IDM.py ligne droite
#route = Roads()
#route.createLigne((-200,0,0),(200,0,0))

########################################### créer le network

#network0 = NetworkGraph()
#network0.addEdge((-200,0,0),(-100,0,0))
#network0.addEdge((-100,0,0),(100,0,0))
#network0.addEdge((100,0,0),(200,0,0))

#network1 = NetworkGraph()
#network1.addEdge((-200,0,0),(0,0,0))
#network1.addEdge((0,0,0),(100,0,-100))

#network2 = NetworkGraph()
#network2.addEdge((1, 0, 1), (100, 0, 100), True)
#network2.addEdge((100, 0, 100), (200, 0, 100))

network_rp = NetworkGraph() ## network du rond_point
network_rp.addEdge((850,0,1050),(1050,0,1150),True)
network_rp.addEdge((1050,0,1150),(1150,0,950),True)
network_rp.addEdge((1150,0,950),(950,0,850),True)
network_rp.addEdge((950,0,850),(850,0,1050),True)

#network = NetworkGraph()
########################################### créer la voiture initiale

y_voiture = 7
#vehicule0= box(pos=vector(-200,y_voiture,0),size = vector(20,10,10),axis = vector(0,0,0), color = vector(1,0,0))
#vehicule1= box(pos=vector(-200,y_voiture,0),size = vector(20,10,10),axis = vector(0,0,0), color = vector(1,0,0))
#vehicule2 = box(pos=vector(1, y_voiture, 1), size=vector(20, 10, 10), axis=vector(0, 0, 0), color=vector(1, 0, 0))
vehicule_rp = box(pos=vector(850, y_voiture, 1050), size=vector(20, 10, 10), axis=vector(0, 0, 0), color=vector(1, 0, 0))

## test pfd IDM.py
#vehicule_test_1 = box(pos=vector(-200,y_voiture,0),size = vector(20,10,10),axis = vector(0,0,0), color = vector(1,0,0))
#vehicule_test_2 = box(pos=vector(-150,y_voiture,0),size = vector(20,10,10),axis = vector(0,0,0), color = vector(1,0,0))

########################################## créer la traffic_map

#map0 = TrafficMap()
#map0.addCarOnRoad((-200,0,0),(-100,0,0),vehicule0)

#map1 = TrafficMap()
#map1.addCarOnRoad((-200,0,0),(0,0,0),vehicule1)

#map2 = TrafficMap()
#map2.addCarOnRoad((1, 0, 1), (100, 0, 100), vehicule2)

map_rp = TrafficMap()
map_rp.addCarOnRoad((850,0,1050),(1050,0,1150),vehicule_rp)

#map = TrafficMap()
#map.addCarOnRoad((-200,0,0),(200,0,0),vehicule_test_1)
#map.addCarOnRoad((-200,0,0),(200,0,0),vehicule_test_2)

########################################## créer la trajectoire initiale/le chemin associée

#chemin0 = [(-200,0,0),(-100,0,0),(100,0,0),(200,0,0)]

#chemin1 = [(-200,0,0),(0,0,0),(100,0,-100)]

#chemin2 = [(1, 0, 1), (100, 0, 100), (150, 0, 100)]

chemin_rp = [(850,0,1050),(1050,0,1150),(1150,0,950),(950,0,850),(850,0,1050)]

#chemin1 = [(-200,0,0),(200,0,0)]
#chemin2 = [(-200,0,0),(200,0,0)]

########################################## créer la car initiale

vitesse = 50  ## m/s

#car0 = Car((-200,y_voiture,0), vitesse, vehicule0, chemin0)
#car1 = Car((-200,y_voiture,0), vitesse, vehicule1, chemin1)
#car2 = Car((1, y_voiture, 1), vitesse, vehicule2, chemin2)
car_rp = Car((850,0,1050) , vitesse, vehicule_rp, chemin_rp)

#car_test_1 = Car((-200,0,0), 500, vehicule_test_1, chemin1) ## voiture derrière
#car_test_2 = Car((-200,0,0),3 , vehicule_test_2, chemin2) ## voiture devant

########################################### créer la liste des cars initiales

L = [car_rp]

#L_test = [car_test_1,car_test_2]

########################################### actualiser les voitures

dt = 1 / 60

while True:
    rate(60)
    Simulation(dt, L, network_rp, map_rp, rond_point)
