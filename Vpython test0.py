#################################################################################       SETUP ET CLASS          #########################################################

## ici on modélise les routes, fait avancer les voitures et modifit les graphes en même temps


y_reference  = 5
largeur_reference = 15


import random 

scene.width = scene.height = 1000
scene.range = 200
scene.background = color.white

Ux = vector(1,0,0)
Uy = vector(0,1,0)
Uz = vector(0,0,1)

## base orthonormée

scalaire = 100

fleche_x = arrow(pos=vector(0,100,0),axis=vector(scalaire,0,0), shaftwidth=1)
fleche_y = arrow(pos=vector(0,100,0),axis=vector(0,scalaire,0), shaftwidth=1)
fleche_z = arrow(pos=vector(0,100,0),axis=vector(0,0,scalaire), shaftwidth=1)

class Car :
    
    def __init__(self, spawnpoint, speed, vehicle, trajectoire, chemin): ## trajectoire, une fonction donnant la trajectoire de la voiture dans la simulation (propre à chaque lignes/virages) ; chemin, un chemin du graphe représentant l'ensemble des routes (lignes et virages) que la voitures doit empreinter
        (x,y,z) = spawnpoint
        self.position = (x,y,z) # (x,y,z)
        self.speed = speed # m.s^(-1)
        self.accel = 0  # m.s^(-2), 0 par défaut car en mvt rect et unif
        self.vehicle = vehicle
        self.trajectoire = trajectoire
        self.chemin = chemin
    
    # Définit la vitesse de la voiture (en m.s^(-1))
    def setSpeed(self, speedToSet):
        self.speed = speedToSet

    # Définit l'accélération de la voiture (m.s^(-2))
    def setAccel(self, accelToSet):
        self.accel = accelToSet

    # Définit les nouvelles coordonnées de la voiture
    def setPosition(self, x, z):
        self.position = (x, z)

    def getDistanceBetween(self, otherCar):
        x1, z1 = self.position
        x2, z2 = otherCar.position
        
        return(sqrt(((x2 - x1))**2 + (z2 - z1)**2))

    def getRelativeSpeed(self, otherCar):
        return(otherCar.speed - self.speed)
        
class NetworkGraph:

    def __init__(self):
        self.network = {} # Graphe (dictionnaire) sous la formé k,v : coordonnées, sommets connectés (liste d'adj)

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
    def addEdge(self, start, end, curved = False):
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
    

class Reseau :
    
    def __init__(self,start,end) : # start = (a,b,c) et end = (x,y,z) sont les coords de début et de fin de la route
        self.start = start
        self.end = end
        
    def ligne(self,start,end) :
        (a,b,c),(x,y,z) = start, end
        longueur = sqrt((x-a)**2+(z-c)**2)
        route = box(pos = vector((a+x)/2,(b+y)/2,(c+z)/2), size = vector(longueur, y_reference, largeur_reference))
        if x != a :
            theta = atan((z-c)/(x-a))
            alpha = atan((y-b)/(x-a))
            rota = Uz.rotate(-theta,vector(0,1,0))
            route.rotate(-theta,vector(0,1,0))
            route.rotate(alpha,rota)
        else : 
            theta = sign(z-c)*pi/2
            alpha = atan((y-b)/(z-c))
            rota = Uz.rotate(-theta,vector(0,1,0))
            route.rotate(-theta,vector(0,1,0))
            route.rotate(-alpha,rota)
        
    def virage (self,start,end) : 
        (a,b,c),(x,y,z) = start, end
        delta_x = x-a
        delta_z = z-c
        r = min(abs(delta_x),abs(delta_z))
        ## par convention, on tourne d'abord, avec un rayon étant le min des distances, puis ensuite lignes droite
        ## on peut obtenir l'inverse en réalisant virage(end,start)!! penser à le faire 
        if abs(delta_x) < abs(delta_z) :
            centre_v = vector(a,b,c + sign(delta_z)*r)
            sortie_virage = (a + sign(delta_x)*r,b, c + sign(delta_z)*r)
            if sign(delta_x)>0 and sign(delta_z)>0 :
                alpha, beta = 0, pi/2
            elif sign(delta_x)<0 and sign(delta_z)>0 :
                alpha, beta = pi/2, pi
            elif sign(delta_x)<0 and sign(delta_z)<0 :
                alpha, beta = pi, 3*pi/2
            else : 
                alpha, beta = -pi/2, 0
        else :
            centre_v = vector(a + sign(delta_x)*r,b,c)
            sortie_virage = (a + sign(delta_x)*r,b, c + sign(delta_z)*r)
            if sign(delta_x)<0 and sign(delta_z)<0 :
                alpha, beta = 0, pi/2
            elif sign(delta_x)>0 and sign(delta_z)<0 :
                alpha, beta = pi/2, pi
            elif sign(delta_x)>0 and sign(delta_z)>0 :
                alpha, beta = pi, 3*pi/2
            else : 
                alpha, beta = -pi/2, 0
        v = extrusion(path=paths.arc(pos=centre_v,radius=r, angle1 = alpha , angle2 = beta), shape = [shapes.rectangle(width=largeur_reference, height=y_reference)]) 
        ## ligne entre sortie-virage et fin
        (d,e,f) = sortie_virage
        if (d != x) or (e != y) or (f != z) :
            longueur = sqrt((x-d)**2+(z-f)**2)+2 #+2 pr rendre smooth la transition
            route = box(pos = vector((d+x)/2,(e+y)/2,(f+z)/2), size = vector(longueur, y_reference, largeur_reference))
            theta = atan((z-f)/(x-d))
            route.rotate(-theta,vector(0,1,0))
            
###############################################################################             MODELISATION        ###################################################################################

##### variables du modèle #####

delta_f = 10 ## distance avec laquelle on compare la distance entre deux voitures ; pour freiner
delta_a = 50 ## distance avec laquelle on compare la distance entre deux voitures ; pour accélérer 
epsilon = 5 ## distance avec laquelle on compare dm, le pas d'actualisation des voitures ; pour les transitions de route
## il faut trouver un équilibre dans cette variable pour que les transitions de routes soit smooth 
        


 ### IMPLEMENTER LES TRAJECTOIRES ET FAIRE AVANCER LES VOITURES LE LONG D'UN GRAPHE ###
        
## supposons disposer de deux types de données, des graphes G = {S1 = (x1,y1,z1) ; liste d'adjacence = [(voisin = (x,y,z), virage = bool)]} où virage est un booléen valant true si il s'agit d'une liaison virage et false si c'est une ligne 

## permet de trouver, dans L = [(voisin,virage)], le virage bool virage associé au voisin S
def trouver_virage(L,S) :
    n = len(L)
    (x,y,z) = S
    answer = False 
    for i in range(n):
        voisin = L[i][0] 
        (a,b,c) = voisin
        if a == x and b == y and c == z :
            answer = L[i][1]
    return answer
    
## permet d'avoir un booléen traduisant si la route reliant start et end est un virage 
def est_virage(start,end):
    (a,b,c) = start
    (x,y,z) = end
    if a!=x and c!=z : 
        return(True) # il s'agit d'un virage
    else :
        return(False)

## renvoie une fonction trajectoire qui lie les points start et end, en fonction qu'il s'agisse d'un virage ou non
## la fct trajectoire renvoyée sera de R4 dans R3 /
##trajectoire((x,y,z),l)) ,où (x,y,z) est la position actuelle et l la distance que la voiture peut parcourir pendant dt selon le modèle (double intégration du pfd selon dt), 
##renvoie la nouvelle position (x',y',z') / la voiture ait parcouru l depuis (x,y,z)
def distance(point1, point2) :
    a,b,c = point1
    x,y,z = point2
    return( sqrt( (x-a)**2 + (y-b)**2 + (z-c)**2 ) )

#def nouvelle_traj(start,end,virage) : 
#    (x0,y0,z0) = start
#    (x1,y1,z1) = end
#    if virage = False :
#        d = distance(start,end)
#        def traj(x,y,z,l) :
#            return(x + l*(x1-x0)/d, y +l*(y1-y0)/d, z + l*(z1-z0)/d)
#        return traj
#    else :
#        return()

def nouvelle_traj(start,end):
    (x0,y0,z0) = start
    (x1,y1,z1) = end
    d = distance(start,end)
    def traj(x,y,z,l) :
        return(x + l*(x1-x0)/d, y +l*(y1-y0)/d, z + l*(z1-z0)/d)
    return traj
 
def prochain_vehicule(voiture,network,map) : ##renvoie le véhicule le plus proche situé devant voiture
    c = voiture.chemin
    sommet_depart = c[0]
    if map[sommet_depart]== []: ## cas où il n'y a pas de voiture sur la route 
        return()
    else : ## sinon
        return()
        
def pfd_test(voiture,dt,network,map,contexte =()) :
    return(0)

def pfd(voiture,dt,network,map,contexte = ()) : ## renvoie la l'accélération de la voiture dans les conditions décrites par le contexte (network,map)
## contexte est un élément de la modélisation venant modifié le comportement du véhicule. Ex : les stops, les feux rouges ...
    v = prochain_vehicule(voiture,network,map)
    pos_voiture = (voiture.pos.x,voiture.pos.y,voiture.pos.z)
    pos_prochain_vehicule = (v.pos.x,v.pos.y,v.pos.z)
    if distance(pos_voiture,pos_prochain_vehicule) < delta_f : ## la voiture doit freiner, autre voiture proche
        return()
    elif distance(pos_voiture,pos_prochain_vehicule) < delta_a : ## la voiture doit garder le rythme, autre voiture modérément proche
        return()
    else : ## la voiture doit accélérer 
        return ()

def integration(v,accel,dt): ##  modifiable, ici on intégre 2 fois en considérant les conditions initialses v0 = 0 (à réfléchir) et x0=0 (ce qui est nécessaire)
    return((1/2)*accel*dt**2 + v*dt)
    
def sous_liste(n,liste) : ## renvoie liste[n::]
    rep = []
    for i in range(n,len(liste)) :
        rep.append(liste[i])
    return(rep)

def actualise(car,dt,network,map) :: ## dispawn les voitures, avancer les voitures, les transitions entre les différents noeud du graphe si la voiture nous informe que c'est le cas
    c = car.chemin
    n = len(c) 
    sommet_fin = c[1]
    v = car.speed
    voiture = car.vehicle ## car est l'élément du module tant dis que voiture est l'objet Vpython
    dm = integration(v,pfd_test(voiture,dt,network,map),dt) #distance infinitésimale parcourue par la voiture sur dt
    (x,y,z) = (voiture.pos.x,voiture.pos.y,voiture.pos.z)
    if distance(sommet_fin,(x,y,z)) < dm and n == 1 : ## cas où la voiture est  proche  (à dm près) de son point d'arrivée ; on fait dispawn la voiture
        dispawn(voiture)
    elif distance(sommet_fin,(x,y,z)) < dm : ## cas où la voiture est proche (à dm près) d'une transition de route ; on fait la transition vers a la prochaine route, avec toutes les modifications que cela implique
        # update la position
        (new_x,new_y,new_z) = c[1]
        new_chemin = sous_liste(1,c)
        voiture.pos = vector(new_x,new_y,new_z)
        # update les propriétés : le chemin, la trajectoire
        new_traj = nouvelle_traj(new_chemin[0],new_chemin[1],est_virage(new_chemin[0],new_chemin[1]))
        car.chemin = new_chemin
        car.trajectoire = new_traj
    else : ## cas où la voiture peut parcourir dm sur la portion de route actuelle
        f = car.trajectoire
        (new_x,new_y,new_z) = f(x,y,z,dm)
        voiture.pos = vector(new_x,new_y,new_z)
    return()

    
def Simulation(dt,liste_bagnoles,network,map) : ## à faire dans une boucle while true
    ## actualise les voitures :
    for voiture in liste_bagnoles :
        actualise(voiture,dt,network,map)
    return()

def dispawn(voiture) :  
    voiture_vpython = voiture.vehicle
    voiture_vpython.visible = False
    del voiture_vpython

            
###############################################################################             SIMULATION          ####################################################################################

## créer la route

route0 = Reseau()
route0.ligne((-200,0,0),(-100,0,0))
route0.ligne((-100,0,0),(100,0,0))
route0.ligne((100,0,0),(200,0,0))

## créer le network

network = NetworkGraph()
network.addEdge((-200,0,0),(-100,0,0))
network.addEdge((-100,0,0),(100,0,0))
network.addEdge((100,0,0),(200,0,0))

## créer la traffic_map

map = TrafficMap() 
map.addCarOnRoad((-200,0,0),(-100,0,0),vehicule0)


## créer la voiture initiale

y_voiture=7
vehicule0 = box(pos=vector(-200,y_voiture,0),size = vector(20,10,10),axis = vector(0,0,0), color = vector(1,0,0))

## créer la car associée

chemin0 = [(-200,0,0),(-100,0,0),(100,0,0),(100,0,0)]
trajectoire0 = nouvelle_traj((-200,0,0),(-100,0,0))


vitesse = 50 ## m/s
car0 = Car((-200,y_voiture,0), vitesse, vehicule0, trajectoire0, chemin0)

L = [car0]

## faire spawn la voiture



## actualiser la voiture

dt = 1/60

while True :
    rate(60)
    Simulation(dt,L)
