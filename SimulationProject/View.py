from numpy import *
from vpython import *

y_reference = 5
y_voiture = 7
largeur_route = 15
largeur_voiture = 10
hauteur_voiture = 10
longueur_voiture = 20

scene.width = scene.height = 1000
scene.range = 200
scene.background = color.white

Ux = vector(1, 0, 0)
Uy = vector(0, 1, 0)
Uz = vector(0, 0, 1)


# Petit helper pour avoir le signe de la variable passée
def sign(x):
    if abs(x) == 0:
        return x
    else:
        return x / abs(x)


# renvoie une fonction trajectoire qui lie les points start et end, en fonction qu'il s'agisse d'un virage ou non #
# la fct trajectoire renvoyée sera de R4 dans R3 / #trajectoire((x,y,z),l)) ,où (x,y,z) est la position actuelle et l
# la distance que la voiture peut parcourir pendant dt selon le modèle (double intégration du pfd selon dt),
# renvoie la nouvelle position (x',y',z') / la voiture a parcouru l depuis (x,y,z)

def distance(point1, point2):
    a, b, c = point1
    x, y, z = point2
    return (sqrt((x - a) ** 2 + (y - b) ** 2 + (z - c) ** 2))


def arctan_2(y, x):
    if (sqrt(x ** 2 + y ** 2) + x == 0):
        return 0
    else:
        return (2 * atan(y / (sqrt(x ** 2 + y ** 2) + x)))


def info_virage(start, end):  # renvoie (centre,r) le centre et le rayon du virage entre les sommets 1 et 2
    (a, b, c), (x, y, z) = start, end
    delta_x = x - a
    delta_z = z - c
    r = min(abs(delta_x), abs(delta_z))
    if abs(delta_x) < abs(delta_z):
        centre_v = vector(a, b, c + sign(delta_z) * r)
    else:
        centre_v = vector(a + sign(delta_x) * r, b, c)
    centre_virage = (centre_v.x, centre_v.y, centre_v.z)
    return (centre_virage, r)


# la fct trajectoire renvoyée sera de R4 dans R3 / trajectoire(x,y,z,l...) ,où (x,y,z) est la position actuelle et l la distance que la voiture peut parcourir pendant dt selon le modèle (double intégration du pfd selon dt), renvoie la nouvelle position (x',y',z') / la voiture ait parcouru l depuis (x,y,z)
def trajectoire(x, y, z, l, start, end, virage):
    if virage == False:
        (x0, y0, z0) = start
        (x1, y1, z1) = end
        d = distance(start, end)
        return (x + l * (x1 - x0) / d, y_voiture,
                z + l * (z1 - z0) / d)  # new_y = y + l * (y1 - y0) / d, ici flm, on considère le cas en 2D
    else:
        # prendre le vecteur de centre à pos voiture
        centre, rayon = info_virage(start, end)
        a, b, c = centre  # important , pour def v par la suite, vector(centre) ne fonctionne pas mais il faut écrire vector(a,b,c)
        vecteur_centre = vector(a, b, c)
        vecteur_rayon = vector(x, y, z) - vecteur_centre
        # le rotate de theta autour de vector(0,1,0) en position centre / ou (0,0,0)
        theta = -sens(start, end) * l / rayon
        new_vecteur_rayon = rotation_y((vecteur_rayon.x, vecteur_rayon.y, vecteur_rayon.z), theta)
        # calculer le nouveau vecteur position noté v
        v = vecteur_centre + new_vecteur_rayon
        # update la voiture
        return (v.x, v.y, v.z)


def sens(start, end):  # renvoie, pour le virage compris entre start et end, +1 ou -1 selon le sens de rotation de ce virage, avec la convention : rotation trigonométrique -> =1, rotation horaire -> -1
    centre, r = info_virage(start, end)

    (x0, y0, z0) = centre
    (a, b, c) = start
    (x, y, z) = end

    if (a - x > 0) and (c - z < 0) and (c - z0 < 0):  # 1
        return 1
    elif (a - x > 0) and (c - z > 0) and (z - z0 < 0):  # 2
        return 1
    elif (a - x < 0) and (c - z < 0) and (z - z0 > 0):  # 3
        return 1
    elif (a - x < 0) and (c - z < 0) and (c - z0 > 0):  # 4
        return 1
    elif (a - x < 0) and (c - z > 0) and (c - z0 <= 0):  # 5
        return -1
    elif (a - x < 0) and (c - z < 0) and (z - z0 >= 0):  # 6
        return -1
    elif (a - x > 0) and (c - z > 0) and (z - z0 >= 0):  # 7
        return -1
    else:
        return -1


def rotation_y(triplet, theta):  # renvoie la rotation du vecteur(triplet) d'un angle theta, selon Ux
    (a, b, c) = triplet
    alpha = a * cos(theta) - c * sin(theta)
    beta = b
    gamma = a * sin(theta) + c * cos(theta)

    return vector(alpha, beta, gamma)


def orthogonal_Oxz(v):  # renvoie le vecteur orthogonal à v dans le plan Oxz
    (x, y, z) = (v.x, v.y, v.z)
    alpha = -z
    beta = y
    gamma = x
    v = vector(alpha, beta, gamma)
    return (longueur_voiture * norm(v))


def oriente(voiture, virage):  # oriente la voiture lorsqu'elle tourne dans le virage
    if not virage:
        return voiture.axis
    else:
        vecteur_orientation = orthogonal_Oxz(voiture.pos)
        return vecteur_orientation


def update_car(car, chemin, dm, network_graph):
    if dm is None and len(chemin) > 1:  # chemin devrait toujours être strictement supérieur à 1, mais dans le doute..;
        new_x, new_y, new_z = chemin[1]
        car.vehicle.pos = vector(new_x, new_y, new_z)
        return

    start = chemin[0]
    end = chemin[1]

    virage = network_graph.estVirage(start, end)

    x, y, z = car.position
    new_x, new_y, new_z = trajectoire(x, y, z, dm, start, end, virage)
    car.position = (new_x, new_y, new_z)

    vehicle = car.vehicle

    new_pos = vector(new_x, new_y, new_z)
    vehicle.pos = new_pos

    vecteur_orientation = oriente(vehicle, virage)
    vehicle.axis = vecteur_orientation


def dispawn_car(vpython_car):
    vpython_car.visible = False


def spawn_car_test(coords):
    x, y, z = coords
    vehicule_rp = box(pos=vector(x, y, z), size=vector(20, 10, 10), axis=vector(0, 0, 0), color=vector(1, 0, 0))
    return vehicule_rp


class View:

    def __init__(self):
        pass

    def create_road(self, start, end, curved):
        if curved:
            self.__create_curve(start, end)
        else:
            self.__create_line(start, end)

    def __create_line(self, start, end):

        (a, b, c), (x, y, z) = start, end
        longueur = sqrt((x - a) ** 2 + (z - c) ** 2)
        route = box(pos=vector((a + x) / 2, (b + y) / 2, (c + z) / 2),
                    size=vector(longueur, y_reference, largeur_route))

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

    def __create_curve(self, start, end):

        (a, b, c), (x, y, z) = start, end
        delta_x = x - a
        delta_z = z - c

        r = min(abs(delta_x), abs(delta_z))

        # par convention, on tourne d'abord, avec un rayon étant le min des distances, puis ensuite lignes droite
        # on peut obtenir l'inverse en réalisant virage(end,start) !! penser à le faire
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
                alpha, beta = -pi / 2, 0
        extrusion(path=paths.arc(pos=centre_v, radius=r, angle1=alpha, angle2=beta),
                  shape=[shapes.rectangle(width=largeur_route, height=y_reference)])

        # Ligne entre sortie-virage et fin
        (d, e, f) = sortie_virage
        if (d != x) or (e != y) or (f != z):
            self.__create_line(sortie_virage, end)
