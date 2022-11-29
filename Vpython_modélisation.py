Web VPython 3.2

import time 
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
        self.position = spawpoint # (x,y,z)
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
        

y_reference  = 5
largeur_reference = 15

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
            
        ### MODELISATION ###
        
        #échelle les voitures font 20 de long soit 5m dans la vraie vie
        #   => 1m = 4
        #   => 100m = 400
        #   => 250m = 1000
        
## test routes inclinées ## attention ne pas tourner et monter en même temps + les monter sont possibles seulement sur .ligne (pas sur .virage)
#route0 = Reseau()
#route0.ligne((-100,-50,0),(100,50,-0))

## voiture (avec exemple virages)
#voiture_ref = box(pos=vector(0,6,0),size = vector(20,10,10),axis = vector(0,0,0), color = vector(1,0,0))
#voituredebut = box(pos=vector(150,6,-75),size = vector(20,10,10),axis = vector(0,0,0), color = vector(0,1,0))
#voiturefin = box(pos=vector(-50,6,100),size = vector(20,10,10),axis = vector(0,0,0), color = vector(0,0,1))
#voiture_virage_debut = box(pos=vector(-100,6,20),size = vector(20,10,10),axis = vector(0,0,0), color = vector(1,1,1))
#voiture_virage_fin = box(pos=vector(80,6,-180),size = vector(20,10,10),axis = vector(0,0,0), color = vector(1,1,1))
    
## exemple de virages stylés
#route1 = Reseau()
#route1.virage((0,0,0),(150,0,-75))
#route1.virage((150,0,-75),(-50,0,100))
#route1.virage((0,0,0),(-50,0,100))
#route1.virage((0,0,0),(80,0,-180))
#route1.virage((-50,0,100),(-100,0,20))
#route1.virage((-100,0,20),(0,0,0))
#route1.virage((80,0,-180),(-100,0,20))

## grand rond point centrée en 0,0
#rond_point1 = Reseau()
#rond_point1.virage((250,0,0),(0,0,250))
#rond_point1.virage((-250,0,0),(0,0,250))
#rond_point1.virage((-250,0,0),(0,0,-250))
#rond_point1.virage((250,0,0),(0,0,-250))


## route_principale = grande autoroute ligne droite
#route_principale = Reseau()
#route_principale.ligne((-5000, 0, 0),((5000,0, 0)))

##Highway Onramp # attention si on essaye de faire bouger les voitures sur cette route, il est important de recoller les morceaux entre la rampe et l'autoroute cad, de créer une transition, un sommet commun entre la voie d'insertion et l'autoroute puis à noouveau l'autoroute
#route2 = Reseau()
#route2.ligne((-5000,0,-30),(5000,0,-30))
#route2.ligne((-5000,0,-10),(5000,0,-10))
#route2.ligne((-5000,0,10),(5000,0,10))
#route2.ligne((-5000,0,30),(5000,0,30))

#route2.ligne((-500,0,-30),(-299,0,-50))
#route2.ligne((-301,0,-50),(0,0,-50))
#route2.virage((300,0,-300),(0,0,-50))

## Single intersection
#route3 = Reseau()
#route3.ligne((-5000,0,0),(5000,0,0))
#route3.ligne((0,0,-5000),(0,0,5000))

##Two-Way intersection 
#route4 = Reseau()
#route4.ligne((-50,0,-10),(-5000,0,-10))
#route4.ligne((-5000,0,10),(-50,0,10))
#route4.ligne((10,0,-50),(10,0,-5000))
#route4.ligne((-10,0,-5000),(-10,0,-50))
#route4.ligne((50,0,10),(5000,0,10))
#route4.ligne((5000,0,-10),(50,0,-10))
#route4.ligne((-10,0,50),(-10,0,5000))
#route4.ligne((10,0,5000),(10,0,50))

#route4.virage((10,0,-50),(-50,0,10))
#route4.virage((-10,0,50),(-50,0,10))
#route4.ligne((-50,0,10),(50,0,10))

#route4.virage((10,0,50),(-50,0,-10))
#route4.virage((10,0,50),(50,0,10))
#route4.ligne((10,0,50),(10,0,-50))

#route4.virage((-10,0,50),(50,0,-10))
#route4.virage((10,0,-50),(50,0,-10))
#route4.ligne((50,0,-10),(-50,0,-10))

#route4.virage((-10,0,-50),(50,0,10))
#route4.virage((-10,0,-50),(-50,0,-10))
#route4.ligne((-10,0,-50),(-10,0,50))

##Rondabout
#route5 = Reseau()
#intérieur
#route5.ligne((30,0,-90),(-30,0,-90))
#route5.virage((-90,0,-30),(-30,0,-90))
#route5.ligne((-90,0,-30),(-90,0,30))
#route5.virage((-90,0,30),(-30,0,90))
#route5.ligne((-30,0,90),(30,0,90))
#route5.virage((90,0,30),(30,0,90))
#route5.ligne((90,0,30),(90,0,-30))
#route5.virage((90,0,-30),(30,0,-90))
#sortie virage
#route5.virage((-30,0,-90),(-10,0,-250))
#route5.virage((30,0,-90),(10,0,-250))
#route5.virage((-90,0,30),(-250,0,10))
#route5.virage((-90,0,-30),(-250,0,-10))
#route5.virage((-30,0,90),(-10,0,250))
#route5.virage((30,0,90),(10,0,250))
#route5.virage((90,0,30),(250,0,10))
#route5.virage((90,0,-30),(250,0,-10))
#extérieur
#route5.ligne((-10,0,-5000),(-10,0,-250))
#route5.ligne((10,0,-250),(10,0,-5000))
#route5.ligne((-5000,0,10),(-250,0,10))
#route5.ligne((-250,0,-10),(-5000,0,-10))
#route5.ligne((-10,0,250),(-10,0,5000))
#route5.ligne((10,0,5000),(10,0,250))
#route5.ligne((250,0,10),(5000,0,10))
#route5.ligne((250,0,-10),(5000,0,-10))

##Diverging Diamond Interchange #3D
#route6 = Reseau()
#autoroute :
#route6.ligne((5000,0,-30),(400,0,-30))
#route6.ligne((400,0,-30),(-400,0,-30))
#route6.ligne((-400,0,-30),(-5000,0,-30))

#route6.ligne((-5000,0,-10),(5000,0,-10))
#route6.ligne((-5000,0,10),(5000,0,10))

#route6.ligne((-5000,0,30),(-400,0,30))
#route6.ligne((-400,0,30),(400,0,30))
#route6.ligne((400,0,30),(5000,0,30))

#entrée-sortie :
#route6.ligne((-300,0,-50),(-400,0,-30))
##route6.virage((-300,0,-50),(-200,0,-200))
#route6.virage((-200,0,-200),(-125,0,-245))
#route6.ligne((-400,0,30),(-300,0,50))
#route6.virage((-300,0,50),(-200,0,200))
#route6.virage((-200,0,200),(-125,0,245))
#route6.ligne((400,0,-30),(300,0,-50))
#route6.virage((300,0,-50),(200,0,-200))
#route6.virage((200,0,-200),(125,0,-245))
#route6.ligne((400,0,30),(300,0,50))
#route6.virage((300,0,50),(200,0,200))
#route6.virage((200,0,200),(125,0,245))

#montée et pont :
#route6.ligne((-60,30,-20),(-60,0,-120))
#route6.virage((-125,0,-245),(-60,0,-120))
#route6.ligne((-60,0,20),(-60,30,120))
#route6.virage((-125,0,245),(-60,0,120))
#route6.ligne((-60,30,20),(-60,30,-20))

#route6.ligne((60,30,-20),(60,0,-120))
#route6.virage((125,0,-245),(60,0,-120))
#route6.ligne((60,0,120),(60,30,20))
#route6.virage((125,0,245),(60,0,120))
#route6.ligne((60,30,20),(60,30,-20))

#transitions
#route6.virage((-60,0,-310),(-125,0,-245))
#route6.ligne((-60,0,-5000),(-60,0,-310))
#route6.virage((60,0,-310),(125,0,-245))
#route6.ligne((60,0,-5000),(60,0,-310))
#route6.virage((-60,0,310),(-125,0,245))
#route6.ligne((-60,0,5000),(-60,0,310))
#route6.virage((60,0,310),(125,0,245))
#route6.ligne((60,0,5000),(60,0,310))

#croissements (ou feux-rouges) :
#route6.ligne((-60,0,-180),(60,0,-310))
#route6.ligne((-60,0,-310),(60,0,-180))
#route6.ligne((-60,0,180),(60,0,310))
#route6.ligne((-60,0,310),(60,0,180))


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

## renvoie une fonction trajectoire qui lie les points start et end, en fonction qu'il s'agisse d'un virage ou non
def nouvelle_traj(start,end,virage) :
    if virage == False :
        def traj1(x1): # fonction affine de x, de l'espace reliant start à end 
            a,b,c = start
            x,y,z = end 
            vecteur_start_end = vector(x-a,y-b,z-c) #vecteur directeur de la droite start-end
            l = x1/vecteur_start_end.x
            return(x1,l*vecteur_start_end.y,l*vecteur_start_end.z)
        return(traj1)
    else :
        def traj2(x2): # fonction virage de x, à 90°, en 2D dans le plan (Ox,Oz) reliant start à end 
            (a,b,c),(x,y,z) = start, end
            delta_x = x-a
            delta_z = z-c
            r = min(abs(delta_x),abs(delta_z)) # rayon du cercle
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
            # on dispose du centre du cercle, noté centre_v et de l'angle auquel l'arc doit commencé : alpha, et celui auquel il doit se finir : beta
            # grace à l'équation d'un cercle dans le plan (Ox,Oz) où le centre est (a,b,c) et r le rayon alors z = c -+ sqrt(r**2 - (x-a)**2)
            if alpha == 0 or alpha == pi/2 :
                return(x2,y,centre_v.z + sqrt(r**2 - (x2-centre_v.x)**2))
            else : 
                return(x2,y,centre_v.z + sqrt(r**2 - (x2-centre_v.x)**2))
        return traj2(x) 
    
            
## network = dico de couple (sommet, liste d'adjacence) où la liste d'adjacence = [somme_voisins], chaque sommet est sous la forme (x,y,z)
## soit c un chemin du graphe représentant la trajectoire de la voiture à simuler 
## un chemin "c" d'un graphe "network" est une liste de sommet du graphe tq pr tt i [|0;len(c)-1|], le sommet Si et Si+1 sont reliés dans le graphe par une route
def parcours_voiture(network, voiture): ## on fait avancer d'une étape la voiture sur son chemin en venant réaliser toute les modification nécessaires pour ensuite appliquer notre modèle sur la prochaine portion de route
    current_Sommet = voiture.chemin[0]
    next_Sommet = voiture.chemin[1]
    c = voiture.chemin[1:]
    voiture.chemin = c
    virage = trouver_virage(network[current_Sommet],next_Sommet)
    traj = nouvelle_traj(current_Sommet, next_Sommet, virage)
    voiture.trajectoire = traj 
    
limite_vitesse = 90 #m/s

def parcours_voisins(network, s, aTraiter, antecedent, reponse ,end) :
    if network[s] == [] : ## on est bloqué à s, s n'a pas de voisins accessibles 
        return ()
    elif s == end : ## on trouve un chemin possible
        antecedent.append(s)
        reponse.append(antecedent)
        return()
    elif s in antecedent : ## on retourne sur nos pas => cycle
        return()
    else : ## on continu 
        antecedent.append(s)
        for v in network(s) :
            aTraiter.append(v)
            parcours_voisins(network, v, aTraiter, antecedent, reponse, end)

def all_possible_chemin(network, start, end) : ## génère tous les chemins sans cycle de network entre start et end 
    reponse = []
    aTraiter = Queue()
    aTraiter.append(start)
    empty = Queue()
    while aTraiter != empty :
        s = aTraiter.pop()
        parcours_voisins(network, s, aTraiter, [], reponse, end)
    return(reponse)

def random_chemin(network, start, end) :
    possible_chemin = all_possible_chemin(network,start,end)
    n = randint(0,len(possible_chemin))
    return(possible_chemin[n])
    
## on se donne les listes spawners et dispawners (contenant des sommets) étant les seuls sommets capables de spawn respectivement de dispawn
## le speed de spawn sera par défaut la limite_vitesse

def spawn(spawnpoint,next_Sommet,speed,trajectoire,chemin) : 
    a,b,c= spawnpoint
    vehicle = box(pos=vector(a,b,c),size=vector(20,10,10),axis=vector(0,0,0),color=vector(random(),random(),random()))
    trajectoire = nouvelle_traj(spawnpoint,next_Sommet,trouver_virage(network.(spawnpoint),next_Sommet))
    chemin = random_chemin(network, spawnpoint, dispawners[randint(len(dispawners))])
    return(Car(spawnpoint, speed, vehicle, trajectoire, chemin))

def spawner_tempo(spawnpoint, next_Sommet, tau) ## où spawnpoint est le sommet qui fera spawn les voitures, next_Sommet le prochain sommet (obligatoire pour orienter la première direction des voitures), tau le nombre de voiture que l'on veut faire apparaître en 1minutes (en voiture/min)
    t0 = time.time()
    while time.time(
       spawn(

    
def spawner_continu(spawnpoint, next_Sommet, tau) :

def dispawner(
    
def stop(
