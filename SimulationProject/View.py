from math import *
from numpy import *
from vpython import *


scene.width = scene.height = 1000
scene.range = 200
scene.background = color.white

Ux = vector(1, 0, 0)
Uy = vector(0, 1, 0)
Uz = vector(0, 0, 1)

## base orthonormée

scalaire = 100

y_reference  = 5
largeur_reference = 15

class View:

    def __init__(self):
        pass

    def create_road(self, start, end, curved):
        if curved:
            self.__create_curve(start, end)
        else:
            self.__create_line(start, end)

    def __create_line(self, start, end):

        (a,b,c), (x,y,z) = start, end
        longueur = sqrt((x-a)**2+(z-c)**2)
        route = box(pos = vector((a+x)/2,(b+y)/2,(c+z)/2), size = vector(longueur, y_reference, largeur_reference))

        if x != a:
            theta = atan((z-c)/(x-a))
            alpha = atan((y-b)/(x-a))
            rota = Uz.rotate(-theta,vector(0,1,0))
            route.rotate(-theta,vector(0,1,0))
            route.rotate(alpha,rota)

        else:
            theta = sign(z-c)*pi/2
            if z != c:
                alpha = atan((y-b)/(z-c))
            else:
                alpha = sign(z-c)*pi/2
            rota = Uz.rotate(-theta,vector(0,1,0))
            route.rotate(-theta,vector(0,1,0))
            route.rotate(-alpha,rota)

    def __create_curve(self, start, end):

        (a,b,c), (x,y,z) = start, end
        delta_x = x-a
        delta_z = z-c

        r = min(abs(delta_x),abs(delta_z))


        ## par convention, on tourne d'abord, avec un rayon étant le min des distances, puis ensuite lignes droite
        ## on peut obtenir l'inverse en réalisant virage(end,start)!! penser à le faire
        if abs(delta_x) < abs(delta_z) :
            centre_v = vector(a,b,c + sign(delta_z)*r)
            sortie_virage = (a + sign(delta_x)*r,b, c + sign(delta_z)*r)
            if sign(delta_x)>0 and sign(delta_z)>0:
                alpha, beta = 0, pi/2
            elif sign(delta_x) < 0 < sign(delta_z):
                alpha, beta = pi/2, pi
            elif sign(delta_x)<0 and sign(delta_z)<0 :
                alpha, beta = pi, 3*pi/2
            else:
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

        extrusion(path=paths.arc(pos=centre_v,radius=r, angle1 = alpha , angle2 = beta), shape = [shapes.rectangle(width=largeur_reference, height=y_reference)])

        ## ligne entre sortie-virage et fin
        (d,e,f) = sortie_virage
        self.__create_line(sortie_virage, end)


        ### MODELISATION ###

        #échelle les voitures font 20 de long soit 5m dans la vraie vie
        #   => 1m = 4
        #   => 100m = 400
        #   => 250m = 1000