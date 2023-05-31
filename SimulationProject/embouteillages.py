#coding: utf8


from Simulation.Simulation import *
from vpython import *
#from matrix import matrix_embouteillages_all_paths <- nécessaire pour les spawn avec matrices, mais semble engendrer beaucoup de lag à import 

scene.center = vector(0, 800, 1200)
#scene.center = vector(-1300,700,0)
#scene.center = vector(1200,750,1200)
simulation = Simulation(max_length = 13)

# Constantes de routes : limitation de vitesse (en m/s) et nombre de voitures maximal sur ...
v_autoroute = 130 
N_autoroute = 50
v_nationale = 100 
N_nationale = 30
v_departementale = 70
N_departementale = 20
v_ville = 50
N_ville = 10

# En embouteillage, comme (cf View) coef_embouteillage = 2 (en metre par seconde voiture)
# sur l'autoroute, v appartient [30,130]km/h (en embouteillage pour 30 et au maximun 130)
# sur la nationale, v [40,100]
# sur la departementale, v [30,70]
# en ville, v [30,50]

list_middle_straight = [((-400,0,0),(400,0,0),N_autoroute,v_autoroute),((-250,0,150),(250,0,150),N_nationale,v_nationale),((-250,0,-150),(250,0,-150),N_nationale,v_nationale),
((400,0,0),(550,0,50),N_departementale,v_departementale),((400,0,0),(550,0,-50),N_departementale,v_departementale),((-550,0,50),(-400,0,0),N_departementale,v_departementale),((-550,0,-50),(-400,0,0),N_departementale,v_departementale),
((250,0,150),(550,0,50),N_nationale,v_nationale),((250,0,-150),(550,0,-50),N_nationale,v_nationale),((-550,0,50),(-250,0,150),N_nationale,v_nationale),((-550,0,-50),(-250,0,-150),N_nationale,v_nationale),
((550,0,50),(550,0,250),N_ville,v_ville),((550,0,-250),(550,0,-50),N_ville,v_ville),((-800,0,50),(-800,0,150),N_ville,v_ville),((-800,0,150),(-800,0,250),N_ville,v_ville),
((-800,0,-250),(-800,0,-150),N_ville,v_ville),((-800,0,-150),(-800,0,-50),N_ville,v_ville),
((550,0,250),(800,0,250),N_ville,v_ville),((550,0,-50),(800,0,-50),N_ville,v_ville),((-800,0,250),(-550,0,250),N_ville,v_ville),((-800,0,-50),(-550,0,-50),N_ville,v_ville),
((800,0,250),(800,0,150),N_ville,v_ville),((800,0,150),(800,0,50),N_ville,v_ville)
,((800,0,-50),(800,0,-150),N_ville,v_ville),((800,0,-150),(800,0,-250),N_ville,v_ville)
,((-550,0,250),(-550,0,50),N_ville,v_ville),((-550,0,-50),(-550,0,-250),N_ville,v_ville),
((800,0,50),(550,0,50),N_ville,v_ville),((800,0,-250),(550,0,-250),N_ville,v_ville),((-550,0,50),(-800,0,50),N_ville,v_ville),((-550,0,-250),(-800,0,-250),N_ville,v_ville),
((550,0,50),(550,0,-50),N_nationale,v_nationale),((-550,0,50),(-550,0,-50),N_nationale,v_nationale),((800,0,-50),(800,0,50),N_nationale,v_nationale),((-800,0,-50),(-800,0,50),N_nationale,v_nationale),
((800,0,50),(1000,0,50),N_departementale,v_departementale),((800,0,-50),(1000,0,-50),N_departementale,v_departementale),((-1000,0,50),(-800,0,50),N_departementale,v_departementale),((-1000,0,-50),(-800,0,-50),N_departementale,v_departementale),
((800,0,150),(1000,0,150),N_departementale,v_departementale),((800,0,-150),(1000,0,-150),N_departementale,v_departementale),((-1000,0,150),(-800,0,150),N_departementale,v_departementale),((-1000,0,-150),(-800,0,-150),N_departementale,v_departementale),
((800,0,250),(1000,0,250),N_departementale,v_departementale),((800,0,-250),(1000,0,-250),N_departementale,v_departementale),((-1000,0,250),(-800,0,250),N_departementale,v_departementale),((-1000,0,-250),(-800,0,-250),N_departementale,v_departementale),
((800,0,50),(1000,0,-50),N_nationale,v_nationale),((-1000,0,-50),(-800,0,50),N_nationale,v_nationale),((1000,0,50),(800,0,-50),N_nationale,v_nationale),((-1000,0,50),(-800,0,-50),N_nationale,v_nationale)
]

braess = [
((550,0,50),(550,0,250),N_ville,v_ville),((550,0,-250),(550,0,-50),N_ville,v_ville),((-800,0,50),(-800,0,150),N_ville,v_ville),((-800,0,150),(-800,0,250),N_ville,v_ville),
((-800,0,-250),(-800,0,-150),N_ville,v_ville),((-800,0,-150),(-800,0,-50),N_ville,v_ville),
((550,0,250),(800,0,250),N_ville,v_ville),((550,0,-50),(800,0,-50),N_ville,v_ville),((-800,0,250),(-550,0,250),N_ville,v_ville),((-800,0,-50),(-550,0,-50),N_ville,v_ville),
((800,0,250),(800,0,150),N_ville,v_ville),((800,0,150),(800,0,50),N_ville,v_ville)
,((800,0,-50),(800,0,-150),N_ville,v_ville),((800,0,-150),(800,0,-250),N_ville,v_ville)
,((-550,0,250),(-550,0,50),N_ville,v_ville),((-550,0,-50),(-550,0,-250),N_ville,v_ville),
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
                     ((550,0,-700),(550,0,-400),N_ville,v_ville),((-800,0,-700),(-800,0,-550),N_ville,v_ville),((-800,0,-550),(-800,0,-400),N_ville,v_ville),
                     ((550,0,-400),(800,0,-400),N_ville,v_ville),((-800,0,-400),(-550,0,-400),N_ville,v_ville),
                     ((800,0,-400),(800,0,-550),N_ville,v_ville),((800,0,-550),(800,0,-700),N_ville,v_ville),
                     ((-550,0,-400),(-550,0,-700),N_ville,v_ville),
                     ((800,0,-700),(550,0,-700),N_ville,v_ville),((-550,0,-700),(-800,0,-700),N_ville,v_ville),
                     ((800,0,-400),(1000,0,-450),N_departementale,v_departementale),((-1000,0,-450),(-800,0,-400),N_departementale,v_departementale),
                     ((800,0,-550),(1000,0,-600),N_departementale,v_departementale),((-1000,0,-600),(-800,0,-550),N_departementale,v_departementale),
                     ((800,0,-700),(1000,0,-750),N_departementale,v_departementale),((-1000,0,-750),(-800,0,-700),N_departementale,v_departementale),
                     ((550,0,-400),(550,0,-250),N_nationale,v_nationale),((800,0,-250),(800,0,-400),N_nationale,v_nationale)
                     ]

list_top_curved = []
list_bot_straight = [((-400,0,350),(400,0,350),N_autoroute,v_autoroute),((-250,0,550),(250,0,550),N_autoroute,v_autoroute),
                    ((400,0,-350),(550,0,-250),N_departementale,v_departementale),((-550,0,250),(-400,0,350),N_departementale,v_departementale),
                    ((400,0,350),(550,0,400),N_departementale,v_departementale),((-550,0,400),(-400,0,350),N_departementale,v_departementale),
                    ((250,0,550),(550,0,700),N_nationale,v_nationale),((-550,0,700),(-250,0,550),N_nationale,v_nationale),
                    ((550,0,400),(550,0,700),N_ville,v_ville),((-800,0,550),(-800,0,700),N_ville,v_ville),((-800,0,400),(-800,0,550),N_ville,v_ville),
                    ((550,0,700),(800,0,700),N_ville,v_ville),((-800,0,700),(-550,0,700),N_ville,v_ville),
                    ((800,0,700),(800,0,550),N_ville,v_ville),((800,0,550),(800,0,400),N_ville,v_ville),((-550,0,700),(-550,0,400),N_ville,v_ville),
                    ((800,0,400),(550,0,400),N_ville,v_ville),((-550,0,400),(-800,0,400),N_ville,v_ville),
                    ((800,0,400),(1000,0,450),N_departementale,v_departementale),((-1000,0,450),(-800,0,400),N_departementale,v_departementale),
                    ((800,0,550),(1000,0,600),N_departementale,v_departementale),((-1000,0,600),(-800,0,550),N_departementale,v_departementale),
                    ((800,0,700),(1000,0,750),N_departementale,v_departementale),((-1000,0,750),(-800,0,700),N_departementale,v_departementale),
                    ((550,0,250),(550,0,400),N_nationale,v_nationale),((800,0,400),(800,0,250),N_nationale,v_nationale)
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
straight_roads = braess + list_top_straight + list_bot_straight

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

simulation_run_time = 60 * 50  # Temps (60*temps en secondes) que va durer la simulation avant de s'arrêter


# APPARITION DES VOITURES #

vitesse = 13.9

i = 0 # compteur
car_spawn_cooldown_range = (1, 2)  # Cooldown entre 2 spawn de voitures (en secondes) (bornes incluses)

next_spawn_time = 60
next_check_time = 120

# LA SIMULATION #

# TEMPO : Pour faire spawn 2 listes de points (bool qui permet de savoir si on choisit la première ou non)
spawnPremiereListe = True

while True:

    # Si on arrive à la fin de la simulation, on change juste de cas
    # ça permet de ne pas couper la boucle, et de ne pas générer d'erreurs venant de vpython
    # On change rate à 1 pour soulager python (i.e. moins d'actualisations/seconde)
    if simulation.internal_clock >= simulation_run_time:
        if (simulation.internal_clock == simulation_run_time):
            print("\n\n\nSIMULATION TERMINÉE\n\n\n")
            print("Statistiques globales :\n\n")
            print(simulation.stats)
            simulation.internal_clock += 1
        rate(1)
    else:
        rate(60)
        simulation.update()

        i += 1
        if i >= next_spawn_time:
            i = 0
            #next_spawn_time = 60 * randint(car_spawn_cooldown_range[0], car_spawn_cooldown_range[1])
            next_spawn_time = 60 * 1 # cooldown de spawn = 2 secondes fixes

            #simulation.create_car_random_path(spawn_points, destination_points, randint(30, 60))
            #ou
            #chemin = ...
            #simulation.create_car(chemin):
            #ou
            #start, end = spawn_points[randint(0,len(spawn_points)-1)], destination_points[randint(0,len(destination_points)-1)]
            #simulation.create_car_random_gps(start,end,vitesse)
            #ou 
            start, end = spawn_points[randint(0, len(spawn_points) - 1)], destination_points[randint(0, len(destination_points) - 1)]
            

            # POUR FAIRE SPAWN PLUSIEURS VOITURES À LA FOIS DEPUIS 2 LISTES DE POINTS DE SPAWN
            start_points_1 = [(-1000,0,-450), (-1000,0,-750), (-1000,0,-50), (-1000,0,150), (-1000,0,450), (-1000,0,750)]
            start_points_2 = [(-1000,0,-600), (-1000,0,-250), (-1000,0,-150), (-1000,0,50), (-1000,0,250), (-1000,0,600)]

            if (spawnPremiereListe):
                for elt in start_points_1:
                    simulation.create_car_shortest_path_time(elt, end, vitesse)
            else:
                for elt in start_points_2:
                    simulation.create_car_shortest_path_time(elt, end, vitesse)

            spawnPremiereListe = not spawnPremiereListe

            #simulation.create_car_shortest_path_time(start, end, vitesse)
            
            ########## avec les matrices de chemin :
            #simulation.create_car_matrix_all_paths(matrix_embouteillages_all_paths)

        if i >= next_check_time : # on optimise le chemin de certaines voitures pour certains temps (toutes les 5 secondes, soit 30 tick) afin de minimiser la complexité 
            if (simulation.carsList != []):
                carIndex = randint(0, len(simulation.carsList) - 1)
                car = simulation.carsList[carIndex]
                simulation.gps.traffic_update(simulation,car)

