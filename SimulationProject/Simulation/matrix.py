#coding: utf8

from Simulation.Simulation import *
from vpython import *

scene.center = vector(0, 800, 1200)

simulation = Simulation()

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



# Cordonnées des routes droites
# Format : (coords départ, coords arrivée, seuil voitures, limitation vitesse en m/s²)
# Avec seuil voitures le nombre maximum de voitures sur la route au dela duquel on ne peut avoir un meilleur flux
straight_roads = list_middle_straight #+ list_top_straight + list_bot_straight

# Coordonnées des virages
# Format : (coords départ, coords arrivée, seuil voitures, limitation vitesse en m/s²)
# Avec seuil voitures le nombre maximum de voitures sur la route au dela duquel on ne peut avoir un meilleur flux
curved_roads = list_middle_curved #+ list_top_curved + list_bot_curved

# Points d'apparitions possibles des voitures
spawn_points = spawn_points_mid #+ spawn_points_top + spawn_points_bot

# Points de "destination" possibles pour les voitures
destination_points = destination_points_mid #+ destination_points_top + destination_points_bot


## fonction création de la matrice :

### hypothèse : autant de spawn que de destination numéroté par leur indice dans les listes spawn et destination
# renvoie une matrice m / m[i][j] contient une liste all_paths entre le start i et la destination j
def matrix_all_paths(spawn_points,destination_points,simulation_object) :
    matrix = [[]]
    graph = simulation_object.network
    for i in range(len(spawn_points)) :
        for j in range(len(destination_points)) :
            start = spawn_points[i]
            end = destination_points[j]
            matrix[i][j] = graph.find_all_paths(start,end,simulation_object.max_length)
    return matrix

### la matrice : 
