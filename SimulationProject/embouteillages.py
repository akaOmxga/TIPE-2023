#coding: utf8

from Simulation.Simulation import *
from vpython import *

scene.center = vector(0, 800, 1200)

simulation = Simulation()

# constantes de routes : limitation de vitesse (en m/s) et nombre de voitures maximal sur ...
v_autoroute = 130 
N_autoroute = 50
v_nationale = 100 
N_nationale = 30
v_departementale = 70
N_departementale = 20
v_ville = 50
N_ville = 10

list_middle_straight = [((-400,0,0),(400,0,0),N_autoroute,v_autoroute),((-250,0,150),(250,0,150),N_nationale,v_nationale),((-250,0,-150),(250,0,-150),N_nationale,v_nationale),
((400,0,0),(550,0,50),N_departementale,v_departementale),((400,0,0),(550,0,-50),N_departementale,v_departementale),((-550,0,50),(-400,0,0),N_departementale,v_departementale),((-550,0,-50),(-400,0,0),N_departementale,v_departementale),
((250,0,150),(550,0,50),N_nationale,v_nationale),((250,0,-150),(550,0,-50),N_nationale,v_nationale),((-550,0,50),(-250,0,150),N_nationale,v_nationale),((-550,0,-50),(-250,0,-150),N_nationale,v_nationale),
((550,0,50),(550,0,250),N_ville,v_ville),((550,0,-250),(550,0,-50),N_ville,v_ville),((-800,0,50),(-800,0,250),N_ville,v_ville),((-800,0,-250),(-800,0,-50),N_ville,v_ville),
((550,0,250),(800,0,250),N_ville,v_ville),((550,0,-50),(800,0,-50),N_ville,v_ville),((-800,0,250),(-550,0,250),N_ville,v_ville),((-800,0,-50),(-550,0,-50),N_ville,v_ville),
((800,0,250),(800,0,50),N_ville,v_ville),((800,0,-50),(800,0,-250),N_ville,v_ville),((-550,0,250),(-550,0,50),N_ville,v_ville),((-550,0,-50),(-550,0,-250),N_ville,v_ville),
((800,0,50),(550,0,50),N_ville,v_ville),((800,0,-250),(550,0,-250),N_ville,v_ville),((-550,0,50),(-800,0,50),N_ville,v_ville),((-550,0,-250),(-800,0,-250),N_ville,v_ville),
((550,0,50),(550,0,-50),N_nationale,v_nationale),((-550,0,50),(-550,0,-50),N_nationale,v_nationale),((800,0,-50),(800,0,50),N_nationale,v_nationale),((-800,0,-50),(-800,0,50),N_nationale,v_nationale),
((800,0,50),(1000,0,50),N_departementale,v_departementale),((800,0,-50),(1000,0,-50),N_departementale,v_departementale),((-1000,0,50),(-800,0,50),N_departementale,v_departementale),((-1000,0,-50),(-800,0,-50),N_departementale,v_departementale),
((800,0,150),(1000,0,150),N_departementale,v_departementale),((800,0,-150),(1000,0,-150),N_departementale,v_departementale),((-1000,0,150),(-800,0,150),N_departementale,v_departementale),((-1000,0,-150),(-800,0,-150),N_departementale,v_departementale),
((800,0,250),(1000,0,250),N_departementale,v_departementale),((800,0,-250),(1000,0,-250),N_departementale,v_departementale),((-1000,0,250),(-800,0,250),N_departementale,v_departementale),((-1000,0,-250),(-800,0,-250),N_departementale,v_departementale),
((800,0,50),(1000,0,-50),N_nationale,v_nationale),((-1000,0,-50),(-800,0,50),N_nationale,v_nationale),((1000,0,50),(800,0,-50),N_nationale,v_nationale),((-1000,0,50),(-800,0,-50),N_nationale,v_nationale)
]

list_middle_curved = []
list_top_straight = [((-400,0,-350),(400,0,-350),N_autoroute,v_autoroute),((-250,0,-550),(250,0,-550),N_autoroute,v_autoroute),
                     ((400,0,350),(550,0,250),N_departementale,v_departementale),((-550,0,-250),(-400,0,-350),N_departementale,v_departementale),
                     ((400,0,-350),(550,0,-400),N_departementale,v_departementale),((-550,0,-400),(-400,0,-350),N_departementale,v_departementale),
                     ((250,0,-550),(550,0,-700),N_nationale,v_nationale),((-550,0,-700),(-250,0,-550),N_nationale,v_nationale),
                     ((550,0,-700),(550,0,-400),N_ville,v_ville),((-800,0,-700),(-800,0,-400),N_ville,v_ville),
                     ((550,0,-400),(800,0,-400),N_ville,v_ville),((-800,0,-400),(-550,0,-400),N_ville,v_ville),
                     ((800,0,-400),(800,0,-700),N_ville,v_ville),((-550,0,-400),(-550,0,-700),N_ville,v_ville),
                     ((800,0,-700),(550,0,-700),N_ville,v_ville),((-550,0,-700),(-800,0,-700),N_ville,v_ville),
                     ((800,0,-400),(1000,0,-450),N_departementale,v_departementale),((-1000,0,-450),(-800,0,-400),N_departementale,v_departementale),
                     ((800,0,-550),(1000,0,-600),N_departementale,v_departementale),((-1000,0,-600),(-800,0,-550),N_departementale,v_departementale),
                     ((800,0,-700),(1000,0,-750),N_departementale,v_departementale),((-1000,0,-750),(-800,0,-700),N_departementale,v_departementale)
                     ]
list_top_curved = []
list_bot_straight = [((-400,0,350),(400,0,350),N_autoroute,v_autoroute),((-250,0,550),(250,0,550),N_autoroute,v_autoroute),
                    ((400,0,-350),(550,0,-250),N_departementale,v_departementale),((-550,0,250),(-400,0,350),N_departementale,v_departementale),
                    ((400,0,350),(550,0,400),N_departementale,v_departementale),((-550,0,400),(-400,0,350),N_departementale,v_departementale),
                    ((250,0,550),(550,0,700),N_nationale,v_nationale),((-550,0,700),(-250,0,550),N_nationale,v_nationale),
                    ((550,0,400),(550,0,700),N_ville,v_ville),((-800,0,400),(-800,0,700),N_ville,v_ville),
                    ((550,0,700),(800,0,700),N_ville,v_ville),((-800,0,700),(-550,0,700),N_ville,v_ville),
                    ((800,0,700),(800,0,400),N_ville,v_ville),((-550,0,700),(-550,0,400),N_ville,v_ville),
                    ((800,0,400),(550,0,400),N_ville,v_ville),((-550,0,400),(-800,0,400),N_ville,v_ville),
                    ((800,0,400),(1000,0,450),N_departementale,v_departementale),((-1000,0,450),(-800,0,400),N_departementale,v_departementale),
                    ((800,0,550),(1000,0,600),N_departementale,v_departementale),((-1000,0,600),(-800,0,550),N_departementale,v_departementale),
                    ((800,0,700),(1000,0,750),N_departementale,v_departementale),((-1000,0,750),(-800,0,700),N_departementale,v_departementale)
                     ]
list_bot_curved = []
spawn_points_mid = [(-1000,0,-250),(-1000,0,-150),(-1000,0,-50),(-1000,0,50),(-1000,0,150),(-1000,0,250)]
spawn_points_top = [(-1000,0,-450),(-1000,0,-600),(-1000,0,-750)]
spawn_points_bot = [(-1000,0,450),(-1000,0,600),(-1000,0,750)]
destination_points_mid = [(1000,0,-250),(1000,0,-150),(1000,0,-50),(1000,0,50),(1000,0,150),(1000,0,250)]
destination_points_top = [(1000,0,-450),(1000,0,-600),(1000,0,-750)]
destination_points_bot = [(1000,0,450),(1000,0,600),(1000,0,750)]

### détails simulation :
# sphère verte : spawn_point
sp1 = sphere(pos = vector(-1000,50,-750), radius = 20, color = vector(0,1,0))
sp2 = sphere(pos = vector(-1000,50,-600), radius = 20, color = vector(0,1,0))
sp3 = sphere(pos = vector(-1000,50,-450), radius = 20, color = vector(0,1,0))
sp4 = sphere(pos = vector(-1000,50,-250), radius = 20, color = vector(0,1,0))
sp5 = sphere(pos = vector(-1000,50,-150), radius = 20, color = vector(0,1,0))
sp6 = sphere(pos = vector(-1000,50,-50), radius = 20, color = vector(0,1,0))
sp7 = sphere(pos = vector(-1000,50,50), radius = 20, color = vector(0,1,0))
sp8 = sphere(pos = vector(-1000,50,150), radius = 20, color = vector(0,1,0))
sp9 = sphere(pos = vector(-1000,50,250), radius = 20, color = vector(0,1,0))
sp10 = sphere(pos = vector(-1000,50,450), radius = 20, color = vector(0,1,0))
sp11 = sphere(pos = vector(-1000,50,600), radius = 20, color = vector(0,1,0))
sp12 = sphere(pos = vector(-1000,50,750), radius = 20, color = vector(0,1,0))

# sphère rouge : destination_point 
dp1 = sphere(pos = vector(1000,50,-750), radius = 20, color = vector(1,0,0))
dp2 = sphere(pos = vector(1000,50,-600), radius = 20, color = vector(1,0,0))
dp3 = sphere(pos = vector(1000,50,-450), radius = 20, color = vector(1,0,0))
dp4 = sphere(pos = vector(1000,50,-250), radius = 20, color = vector(1,0,0))
dp5 = sphere(pos = vector(1000,50,-150), radius = 20, color = vector(1,0,0))
dp6 = sphere(pos = vector(1000,50,-50), radius = 20, color = vector(1,0,0))
dp7 = sphere(pos = vector(1000,50,50), radius = 20, color = vector(1,0,0))
dp8 = sphere(pos = vector(1000,50,150), radius = 20, color = vector(1,0,0))
dp9 = sphere(pos = vector(1000,50,250), radius = 20, color = vector(1,0,0))
dp10 = sphere(pos = vector(1000,50,450), radius = 20, color = vector(1,0,0))
dp11 = sphere(pos = vector(1000,50,600), radius = 20, color = vector(1,0,0))
dp12 = sphere(pos = vector(1000,50,750), radius = 20, color = vector(1,0,0))

# Cordonnées des routes droites
# Format : (coords départ, coords arrivée, seuil voitures, limitation vitesse en m/s²)
# Avec seuil voitures le nombre maximum de voitures sur la route au dela duquel on ne peut avoir un meilleur flux
straight_roads = list_middle_straight + list_top_straight + list_bot_straight

# Coordonnées des virages
# Format : (coords départ, coords arrivée, seuil voitures, limitation vitesse en m/s²)
# Avec seuil voitures le nombre maximum de voitures sur la route au dela duquel on ne peut avoir un meilleur flux
curved_roads = list_middle_curved + list_top_curved + list_bot_curved

# Points d'apparitions possibles des voitures
spawn_points = spawn_points_mid + spawn_points_top + spawn_points_bot

# Points de "destination" possibles pour les voitures
destination_points = destination_points_mid + destination_points_top + destination_points_bot

# CRÉATION DES ROUTES #

simulation.create_roads(straight_roads)
simulation.create_roads(curved_roads, True)

# STATISTIQUES ET PERFORMANCES #

simulation_run_time = 60 * 100  # Temps (60*temps en secondes) que va durer la simulation avant de s'arrêter

# APPARITION DES VOITURES #

i = 0 # compteur
car_spawn_cooldown_range = (2, 3)  # Cooldown entre 2 spawn de voitures (en secondes) (bornes incluses)

next_spawn_time = 60

# LA SIMULATION #

while True:

    # Si on arrive à la fin de la simulation, on change juste de cas
    # ça permet de ne pas couper la boucle, et de ne pas générer d'erreurs venant de vpython
    # On change rate à 1 pour soulager python (i.e. moins d'actualisations/seconde)
    if simulation.internal_clock >= simulation_run_time:
        rate(1)
    else:
        rate(60)
        simulation.update()

        i += 1
        if i >= next_spawn_time:
            i = 0
            next_spawn_time = 60 * randint(car_spawn_cooldown_range[0], car_spawn_cooldown_range[1])
            # TODO : spawn car
            simulation.create_car_random_path(spawn_points, destination_points, randint(30, 60))
            
