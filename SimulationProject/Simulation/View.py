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

scene.center = vector(500, 100, 500)

Ux = vector(1, 0, 0)
Uy = vector(0, 1, 0)
Uz = vector(0, 0, 1)

# constante IDM.py
acc_max = 30 # accélération maximale : m/s^2
exp_acc = 7  # coefficient de smoothness
dec_confortable = 1.5  # décélération confortable : m/s^2
dec_max = 30  # décélération maximale : m/s^2
distance_min = 20  # distance de sécurité, minimale entre deux voitures : en mètre schant que les voitures en mesure 20
distance_interaction = 100 # distance au-delà de laquelle IDM ne s'active pas
temps_reaction = 1  # temps de réaction du conducteur
coef_embouteillages = 2 # de combien diminue la limitation de vitesse par voiture supplémentaire : m/s


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
    return sqrt((x - a) ** 2 + (y - b) ** 2 + (z - c) ** 2)


def arctan_2(y, x):
    if sqrt(x ** 2 + y ** 2) + x == 0:
        return 0
    else:
        return 2 * atan(y / (sqrt(x ** 2 + y ** 2) + x))


# renvoie (centre, sortie, r) le centre, la sortie et le rayon du virage entre les sommets 1 et 2
def info_virage(start, end):
    (a, b, c), (x, y, z) = start, end
    delta_x = x - a
    delta_z = z - c
    r = min(abs(delta_x), abs(delta_z))
    if abs(delta_x) < abs(delta_z):
        centre_v = vector(a, b, c + sign(delta_z) * r)
        sortie_virage = (int(a + sign(delta_x) * r), b, int(c + sign(delta_z) * r))
    else:
        centre_v = vector(int(a + sign(delta_x) * r), b, c)
        sortie_virage = (int(a + sign(delta_x) * r), b, int(c + sign(delta_z) * r))
    centre_virage = (centre_v.x, centre_v.y, centre_v.z)
    return centre_virage, sortie_virage, r


def est_virage(start, end):
    (a, b, c) = start
    (x, y, z) = end
    if a != x and c != z:
        return True  # il s'agit d'un virage
    else:
        return False


# la fct trajectoire renvoyée est de R4 dans R3 / trajectoire(x,y,z,l...) ,où (x,y,z) est la position actuelle
# l la distance que la voiture peut parcourir pendant dt selon le modèle (double intégration du pfd selon dt)
# Renvoie la nouvelle position (x',y',z') / la voiture ait parcouru l depuis (x,y,z)
def trajectoire(x, y, z, distance_parcourable, start, end, virage):
    if not virage:
        (x0, y0, z0) = start
        (x1, y1, z1) = end
        d = distance(start, end)
        return (x + distance_parcourable * (x1 - x0) / d, y_voiture,
                z + distance_parcourable * (z1 - z0) / d)  # new_y = y + l * (y1 - y0) / d, ici on considère le cas 2D
    else:
        # prendre le vecteur de centre à pos voiture
        centre, sortie, rayon = info_virage(start, end)

        # important, pour def v par la suite, vector(centre) ne fonctionne pas, mais il faut écrire vector(a,b,c)
        a, b, c = centre
        vecteur_centre = vector(a, b, c)
        vecteur_rayon = vector(x, y, z) - vecteur_centre

        # le rotate de theta autour de vector(0,1,0) en position centre / ou (0,0,0)
        if rayon == 0:
            rayon = 1  # TODO : REMOVE // FOR DEBUGGING PURPOSES ONLY
        theta = -sens(start, end) * distance_parcourable / rayon
        new_vecteur_rayon = rotation_y((vecteur_rayon.x, vecteur_rayon.y, vecteur_rayon.z), theta)

        # calculer le nouveau vecteur position noté v
        nouvelle_pos = vecteur_centre + new_vecteur_rayon

        # update la voiture
        return nouvelle_pos.x, y_voiture, nouvelle_pos.z


# Renvoie, pour le virage compris entre start et end, +1 ou -1 selon le sens de rotation de ce virage
# Convention : rotation trigonométrique -> 1, rotation horaire -> -1
def sens(start, end):
    centre, sortie, rayon = info_virage(start, end)

    (x0, y0, z0) = centre
    (a, b, c) = start
    (x, y, z) = end

    delta_x = x - a
    delta_z = z - c
    delta_centre = z0 - c

    if (delta_x < 0) and (delta_z > 0) and (delta_centre > 0):  # type de virage n°1
        return 1
    elif (delta_x < 0) and (delta_z < 0) and (delta_centre == 0):  # 2
        return 1
    elif (delta_x > 0) and (delta_z > 0) and (delta_centre == 0):  # 3
        return 1
    elif (delta_x > 0) and (delta_z < 0) and (delta_centre < 0):  # 4
        return 1
    elif (delta_x > 0) and (delta_z < 0) and (delta_centre == 0):  # 5
        return -1
    elif (delta_x > 0) and (delta_z > 0) and (delta_centre > 0):  # 6
        return -1
    elif (delta_x < 0) and (delta_z < 0) and (delta_centre < 0):  # 7
        return -1
    elif (delta_x < 0) and (delta_z > 0) and (delta_centre == 0):  # 8
        return -1
    else:
        return 1  # sécurité


def rotation_y(triplet, theta):  # renvoie la rotation du vecteur(triplet) d'un angle theta, selon Ux
    (a, b, c) = triplet
    alpha = a * cos(theta) - c * sin(theta)
    beta = b
    gamma = a * sin(theta) + c * cos(theta)

    return vector(alpha, beta, gamma)


# renvoie le vecteur orthogonal au vecteur appelé vecteur dans le plan Oxz par rapport au centre du virage
def orthogonal_Oxz(vecteur, centre):
    (x0, y0, z0) = centre
    (x, y, z) = (vecteur.x, vecteur.y, vecteur.z)
    delta_pos = vector(x - x0, y - y0, z - z0)
    alpha = -delta_pos.z
    beta = delta_pos.y
    gamma = delta_pos.x
    vecteur = vector(alpha, beta, gamma)
    return longueur_voiture * norm(vecteur)


# oriente la voiture lorsqu'elle tourne dans le virage
def oriente(voiture, virage, start, end):
    if not virage:
        (a, b, c) = start
        (x, y, z) = end
        vecteur = vector(x - a, y - b, z - c)
        return longueur_voiture * norm(vecteur)
    else:
        centre, sortie, rayon = info_virage(start, end)
        vecteur_orientation = orthogonal_Oxz(voiture.pos, centre)
        return vecteur_orientation


def update_car(car, chemin, dm):
    vehicle = car.vehicle
    x, y, z = car.position

    '''if dm is None and len(chemin) > 1:  # chemin devrait toujours être strictement supérieur à 1, mais dans le doute..;
        new_x, new_y, new_z = chemin[1]
        vehicle.pos = vector(new_x, y_voiture, new_z)
        return'''

    start = chemin[0]
    end = chemin[1]

    virage = est_virage(start, end)

    if virage:
        centre, sortie, rayon = info_virage(start, end)
        if end != sortie:
            new_chemin = [start] + [sortie] + chemin[1:]
            car.chemin = new_chemin

        fin_virage = car.chemin[2]

        new_x, new_y, new_z = trajectoire(x, y, z, dm, start, fin_virage, virage)
        new_pos = vector(new_x, new_y, new_z)
        vecteur_orientation = oriente(vehicle, virage, start, fin_virage)
    else:
        # le deuxième start est useless, c'est pour combler
        new_x, new_y, new_z = trajectoire(x, y, z, dm, start, end, virage)

        new_pos = vector(new_x, new_y, new_z)
        vecteur_orientation = oriente(vehicle, virage, start, end)

    car.position = (new_x, new_y, new_z)

    vehicle.pos = new_pos
    vehicle.axis = vecteur_orientation
    vehicle.up = vector(0, 1, 0)  # afin qu'elle reste "plaqué" au sol


def dispawn_car(vpython_car):
    vpython_car.visible = False


def spawn_car_test(coords):
    x, y, z = coords
    vehicle_rp = box(pos=vector(x, y, z), size=vector(20, 10, 10), axis=vector(0, 0, 0), color=vector(1, 0, 0))
    return vehicle_rp


# Ici on intégre 2 fois en considérant les conditions initialses v0 = 0 (à réfléchir) et x0=0 (ce qui est nécessaire)
def integration(v, accel, dt):
    return (1 / 2) * accel * dt ** 2 + v * dt


# renvoie la l'accélération de la voiture dans les conditions décrites par le contexte (network,map)
# contexte est un élément de la modélisation venant modifié le comportement du véhicule. Ex : les stops,
# les feux rouges ...

def distance_securite(vitesse, delta_vitesse) : ## représente s* dans IDM.py // d'aute modélisation de IDM.py retourne (distance_min + max(0,v*temps_reaction + v*delta_v/sqrt(2acc_max*dec_confortable=)))
    return(distance_min + vitesse*temps_reaction + vitesse*delta_vitesse/sqrt(2*acc_max*dec_confortable))

def speed_on_road(voiture,simulation_object): # calcul la limitation de vitesse relative ! à un instant donné sur la route 
    network = simulation_object.network
    traffic = simulation_object.trafficMap
    start, end = voiture.chemin[0], voiture.chemin[1]
    curved, threshold,speed_limit = network.get_road_parameters(start,end) 
    if len(traffic[(start,end)]) >= threshold :
        limitation_vitesse = speed_limit - coef_embouteillages*threshold
    else :
        limitation_vitesse = speed_limit - coef_embouteillages*(len(traffic[(start,end)]))
    return limitation_vitesse

def pfd_IDM(voiture, dt, simulation_object):
    next_voiture = voiture.get_next_car(simulation_object)
    if (next_voiture == None) :
        acceleration = acc_max * (1 - (voiture.speed /speed_on_road(voiture,simulation_object)) ** exp_acc)
    else :
        pos_voiture = voiture.position
        pos_prochaine_voiture = next_voiture.position
        if (distance(pos_voiture,pos_prochaine_voiture) > distance_interaction) :
            acceleration = acc_max * (1 - (voiture.speed / speed_on_road(voiture,simulation_object)) ** exp_acc)
        else:
            acceleration = acc_max * (1 - (voiture.speed / speed_on_road(voiture,simulation_object)) ** exp_acc - (distance_securite(voiture.speed, (next_voiture.speed - voiture.speed)) / distance(pos_voiture,
                                                                                                      pos_prochaine_voiture)) ** 2)
    return acceleration


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

        # Par convention, on tourne d'abord, avec un rayon étant le min des distances, puis lignes droites
        # On peut obtenir l'inverse en réalisant virage(end,start) !! penser à le faire
        if abs(delta_x) < abs(delta_z):
            centre_v = vector(a, b, c + sign(delta_z) * r)
            sortie_virage = (a + sign(delta_x) * r, b, c + sign(delta_z) * r)
            if sign(delta_x) > 0 and sign(delta_z) > 0:
                alpha, beta = 0, pi / 2
            elif sign(delta_x) < 0 < sign(delta_z):
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
            elif sign(delta_x) > 0 > sign(delta_z):
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
