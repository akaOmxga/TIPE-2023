from math import *
from numpy import *
from vpython import *


scene.width = scene.height = 1000
scene.range = 200
scene.background = color.white

Ux = vector(1, 0, 0)
Uy = vector(0, 1, 0)
Uz = vector(0, 0, 1)

y_reference  = 5
largeur_reference = 15

# Petit helper pour avoir le signe de la variable passée
def sign(x):
    if (abs(x) == 0):
        return x
    else:
        return x/abs(x)

class Roads:

    def __init__(self):
        self.reseau = []

    def create_line(self, start, end):

        (a,b,c), (x,y,z) = start, end
        longueur = sqrt((x-a)**2 + (z-c)**2)
        route = box(pos = vector((a+x)/2, (b+y)/2, (c+z)/2), size = vector(longueur, y_reference, largeur_reference))

        if x != a:
            theta = atan((z-c)/(x-a))
            alpha = atan((y-b)/(x-a))
            rota = Uz.rotate(-theta, vector(0, 1, 0))
            route.rotate(-theta, vector(0, 1, 0))
            route.rotate(alpha, rota)

        else:
            theta = sign(z-c)*pi/2
            alpha = atan((y-b)/(z-c))
            rota = Uz.rotate(-theta, vector(0, 1, 0))
            route.rotate(-theta, vector(0, 1, 0))
            route.rotate(-alpha, rota)
        self.reseau.append((start, end, route, (0, 0, 0), 0))


    def create_curve(self, start, end):

        (a,b,c), (x,y,z) = start, end
        delta_x = x-a
        delta_z = z-c

        r = min(abs(delta_x), abs(delta_z))


        ## par convention, on tourne d'abord, avec un rayon étant le min des distances, puis ensuite lignes droite
        ## on peut obtenir l'inverse en réalisant virage(end,start)!! penser à le faire
        if abs(delta_x) < abs(delta_z):
            centre_v = vector(a, b, c + sign(delta_z)*r)
            sortie_virage = (a + sign(delta_x)*r, b, c + sign(delta_z)*r)
            if sign(delta_x) > 0 and sign(delta_z) > 0:
                alpha, beta = 0, pi/2
            elif sign(delta_x) < 0 and sign(delta_z) > 0:
                alpha, beta = pi/2, pi
            elif sign(delta_x) < 0 and sign(delta_z) < 0:
                alpha, beta = pi, 3*pi/2
            else:
                alpha, beta = -pi/2, 0

        else:
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
        centre_virage = (centre_v.x,centre_v.y,centre_v.z)
        v = extrusion(path=paths.arc(pos=centre_v,radius=r, angle1 = alpha , angle2 = beta), shape = [shapes.rectangle(width=largeur_reference, height=y_reference)])
        self.reseau.append((start,sortie_virage,v,centre_virage,r))

        ## ligne entre sortie-virage et fin
        (d,e,f) = sortie_virage
        if (d != x) or (e != y) or (f != z):
            self.create_line(sortie_virage, end)

        ### MODELISATION ###

        #échelle les voitures font 20 de long soit 5m dans la vraie vie
        #   => 1m = 4
        #   => 100m = 400
        #   => 250m = 1000

# Recréer est_virage(start, end)

def est_virage(start,end):
    (a,b,c) = start
    (x,y,z) = end
    if a!=x and c!=z :
        return True  # il s'agit d'un virage
    else :
        return False

def info_virage(sommet1,sommet2,road): ## renvoie (c,r) le centre et le rayon du virage entre les sommets 1 et 2
    if est_virage(sommet1,sommet2) == False :
        return((0,0,0),0)
    else :
        reseau = road.reseau
        n = len(reseau)
        for i in range(n):
            (s3,s4,route,centre,rayon) = reseau[i]
            if sommet1 == s3 and sommet2 == s4:
                return((centre,rayon))
            return((0,0,0),0)

routes = Roads()
routes.create_curve((0, 0, 0), (100, 0, 100))
print(info_virage((0, 0, 0), (100, 0, 100), routes))

while True:
    rate(1)