#coding: utf8

from Simulation.Simulation import *
from vpython import *

scene.center = vector(0, 300, 300)

simulation = Simulation()

# Cordonnées des routes droites
# Format : (coords départ, coords arrivée, seuil voitures, limitation vitesse en m/s²)
# Avec seuil voitures le nombre maximum de voitures sur la route au dela duquel on ne peut avoir un meilleur flux
straight_roads = [
    ((-500, 0, 0), (0, 0, 0), 10, 30),
    ((0, 0, 0), (500, 0, 0), 10, 30)
]

# Coordonnées des virages
# Format : (coords départ, coords arrivée, seuil voitures, limitation vitesse en m/s²)
# Avec seuil voitures le nombre maximum de voitures sur la route au dela duquel on ne peut avoir un meilleur flux
curved_roads = [
]

# Points d'apparitions possibles des voitures
spawn_points = [
    (-500, 0, 0)
]

# Points de "destination" possibles pour les voitures
destination_points = [
    (500, 0, 0)
]

# CRÉATION DES ROUTES #

simulation.create_roads(straight_roads)
simulation.create_roads(curved_roads, True)

# STATISTIQUES ET PERFORMANCES #

simulation_run_time = 60 * 100  # Temps (60*temps en secondes) que va durer la simulation avant de s'arrêter

# APPARITION DES VOITURES #

vitesse = 13.9

i = 0 # compteur
car_spawn_cooldown_range = (1, 3)  # Cooldown entre 2 spawn de voitures (en secondes) (bornes incluses)

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
            # spawn car
            #start, end = spawn_points[randint(0,len(spawn_points)-1)], destination_points[randint(0,len(destination_points)-1)]
            #simulation.create_car_shortest_path(start, end, vitesse)
            #ou 
            simulation.create_car_random_path(spawn_points,destination_points,vitesse)
            
