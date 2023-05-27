#coding: utf8

from Simulation.Simulation import *
from vpython import *

#scene.center = vector(0, 200, 200)
#scene.center = vector(-200,200,0)
scene.center = vector(400,200,400)
simulation = Simulation(max_length = 10)

#bullshit
N_ville = 10
v_ville = 50


######### différentes routes :


### exemples de virages stylés 
route_1_lignes = []
route_1_virages = [((0,0,0),(150,0,-75), N_ville ,v_ville),((150,0,-75),(-50,0,100),N_ville ,v_ville),((0,0,0),(-50,0,100),N_ville ,v_ville),
                   ((0,0,0),(80,0,-180),N_ville ,v_ville),((-50,0,100),(-100,0,20),N_ville ,v_ville),((-100,0,20),(0,0,0),N_ville ,v_ville),((80,0,-180),(-100,0,20),N_ville ,v_ville)]

### rond_point centré en (0,0)
route_2_virages = [((250,0,0),(0,0,250),N_ville ,v_ville),((-250,0,0),(0,0,250),N_ville ,v_ville),((-250,0,0),(0,0,-250),N_ville ,v_ville),((250,0,0),(0,0,-250),N_ville ,v_ville)]
route_2_lignes = []

### HighWay On Ramp
route_3_lignes = [((-5000,0,-30),(5000,0,-30),N_ville ,v_ville),((-5000,0,-10),(5000,0,-10),N_ville ,v_ville),((-5000,0,10),(5000,0,10),N_ville ,v_ville),((-5000,0,30),(5000,0,30),N_ville ,v_ville),
                  ((-500,0,-30),(-299,0,-50),N_ville ,v_ville),((-301,0,-50),(0,0,-50),N_ville ,v_ville)]
route_3_virages = [((300,0,-300),(0,0,-50),N_ville ,v_ville)]

### Single intersection
route_4_lignes = [((-5000,0,0),(5000,0,0),N_ville ,v_ville),((0,0,-5000),(0,0,5000),N_ville ,v_ville)]
route_4_virages = []

### Two-Way intersection 
route_5_lignes = [((-50,0,-10),(-5000,0,-10),N_ville ,v_ville),((-5000,0,10),(-50,0,10),N_ville ,v_ville),((10,0,-50),(10,0,-5000),N_ville ,v_ville),((-10,0,-5000),(-10,0,-50),N_ville ,v_ville),
                  ((50,0,10),(5000,0,10),N_ville ,v_ville),((5000,0,-10),(50,0,-10),N_ville ,v_ville),((-10,0,50),(-10,0,5000),N_ville ,v_ville),((10,0,5000),(10,0,50),N_ville ,v_ville),
                  ((-50,0,10),(50,0,10),N_ville ,v_ville),((10,0,50),(10,0,-50),N_ville ,v_ville),((50,0,-10),(-50,0,-10),N_ville ,v_ville),((-10,0,-50),(-10,0,50),N_ville ,v_ville)]
route_5_virages = [((10,0,-50),(-50,0,10),N_ville ,v_ville),((-10,0,50),(-50,0,10),N_ville ,v_ville),((10,0,50),(-50,0,-10),N_ville ,v_ville),((10,0,50),(50,0,10),N_ville ,v_ville),
                   ((-10,0,50),(50,0,-10),N_ville ,v_ville),((10,0,-50),(50,0,-10),N_ville ,v_ville),((-10,0,-50),(50,0,10),N_ville ,v_ville),((-10,0,-50),(-50,0,-10),N_ville ,v_ville)]

### Rondabout
route_6_lignes = [((30,0,-90),(-30,0,-90),N_ville ,v_ville),((-90,0,-30),(-90,0,30),N_ville ,v_ville),((-30,0,90),(30,0,90),N_ville ,v_ville),((90,0,30),(90,0,-30),N_ville ,v_ville),
                  ((-10,0,-5000),(-10,0,-250),N_ville ,v_ville),((10,0,-250),(10,0,-5000),N_ville ,v_ville),((-5000,0,10),(-250,0,10),N_ville ,v_ville),((-250,0,-10),(-5000,0,-10),N_ville ,v_ville),
                  ((-10,0,250),(-10,0,5000),N_ville ,v_ville),((10,0,5000),(10,0,250),N_ville ,v_ville),((250,0,10),(5000,0,10),N_ville ,v_ville),((250,0,-10),(5000,0,-10),N_ville ,v_ville)]
route_6_virages = [((-90,0,-30),(-30,0,-90),N_ville ,v_ville),((-90,0,30),(-30,0,90),N_ville ,v_ville),((90,0,30),(30,0,90),N_ville ,v_ville),((90,0,-30),(30,0,-90),N_ville ,v_ville),
                   ((-30,0,-90),(-10,0,-250),N_ville ,v_ville),((30,0,-90),(10,0,-250),N_ville ,v_ville),((-90,0,30),(-250,0,10),N_ville ,v_ville),((-90,0,-30),(-250,0,-10),N_ville ,v_ville),
                   ((-30,0,90),(-10,0,250),N_ville ,v_ville),((30,0,90),(10,0,250),N_ville ,v_ville),((90,0,30),(250,0,10),N_ville ,v_ville),((90,0,-30),(250,0,-10),N_ville ,v_ville)]

### Diverging Diamond Interchange :
route_7_lignes = [((-60,0,-180),(60,0,-310),N_ville ,v_ville),((-60,0,-310),(60,0,-180),N_ville ,v_ville),((-60,0,180),(60,0,310),N_ville ,v_ville),((-60,0,310),(60,0,180),N_ville ,v_ville),
                 ((60,0,5000),(60,0,310),N_ville ,v_ville),((-60,0,5000),(-60,0,310),N_ville ,v_ville),((60,0,-5000),(60,0,-310),N_ville ,v_ville),((-60,0,-5000),(-60,0,-310),N_ville ,v_ville),
                 ((60,30,20),(60,30,-20),N_ville ,v_ville),((60,0,120),(60,30,20),N_ville ,v_ville),((60,30,-20),(60,0,-120),N_ville ,v_ville),((-60,30,20),(-60,30,-20),N_ville ,v_ville),
                 ((-60,30,-20),(-60,0,-120),N_ville ,v_ville),((-60,0,20),(-60,30,120),N_ville ,v_ville),((400,0,30),(300,0,50),N_ville ,v_ville),((400,0,-30),(300,0,-50),N_ville ,v_ville),
                 ((400,0,-30),(300,0,-50),N_ville ,v_ville),((-400,0,30),(-300,0,50),N_ville ,v_ville),((-300,0,-50),(-400,0,-30),N_ville ,v_ville),((400,0,30),(5000,0,30),N_ville ,v_ville),
                 ((-400,0,30),(400,0,30),N_ville ,v_ville),((-5000,0,30),(-400,0,30),N_ville ,v_ville),((-5000,0,10),(5000,0,10),N_ville ,v_ville),((-5000,0,-10),(5000,0,-10),N_ville ,v_ville),
                ((-400,0,-30),(-5000,0,-30),N_ville ,v_ville),((400,0,-30),(-400,0,-30),N_ville ,v_ville),((5000,0,-30),(400,0,-30),N_ville ,v_ville)]
route_7_virages = [((60,0,310),(125,0,245),N_ville ,v_ville),((-60,0,310),(-125,0,245),N_ville ,v_ville),((60,0,-310),(125,0,-245),N_ville ,v_ville),((-60,0,-310),(-125,0,-245),N_ville ,v_ville),
                   ((125,0,245),(60,0,120),N_ville ,v_ville),((125,0,-245),(60,0,-120),N_ville ,v_ville),((-125,0,245),(-60,0,120),N_ville ,v_ville),((-125,0,-245),(-60,0,-120),N_ville ,v_ville),
                   ((200,0,200),(125,0,245),N_ville ,v_ville),((300,0,50),(200,0,200),N_ville ,v_ville),((200,0,-200),(125,0,-245),N_ville ,v_ville),((300,0,-50),(200,0,-200),N_ville ,v_ville),
                   ((-200,0,200),(-125,0,245),N_ville ,v_ville),((-300,0,50),(-200,0,200),N_ville ,v_ville),((-200,0,-200),(-125,0,-245),N_ville ,v_ville),((-300,0,-50),(-200,0,-200),N_ville ,v_ville)]


###################### SIMULATION #######################



# Cordonnées des routes droites
# Format : (coords départ, coords arrivée, seuil voitures, limitation vitesse en m/s²)
# Avec seuil voitures le nombre maximum de voitures sur la route au dela duquel on ne peut avoir un meilleur flux
straight_roads = route_7_lignes

# Coordonnées des virages
# Format : (coords départ, coords arrivée, seuil voitures, limitation vitesse en m/s²)
# Avec seuil voitures le nombre maximum de voitures sur la route au dela duquel on ne peut avoir un meilleur flux
curved_roads = route_7_virages

# Points d'apparitions possibles des voitures
spawn_points = []

# Points de "destination" possibles pour les voitures
destination_points = []

# CRÉATION DES ROUTES #

simulation.create_roads(straight_roads)
simulation.create_roads(curved_roads, True)