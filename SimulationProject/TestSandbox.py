#coding: utf8

from Simulation.Simulation import *
from vpython import *

scene.center = vector(500, 100, 500)

simulation = Simulation()

# Cordonnées des routes droites
# Format : (coords départ, coords arrivée, seuil voitures, limitation vitesse)
# Avec seuil voitures le nombre maximum de voitures sur la route au dela duquel on ne peut avoir un meilleur flux
straight_roads = [
    ((0, 0, 0), (0, 0, 300)),
    ((0, 0, 300), (0, 0, 600)),
    ((200, 0, 400), (200, 0, 600)),
    ((500, 0, 100), (500, 0, 400)),
    ((500, 0, 400), (500, 0, 600)),
    ((0, 0, 0), (300, 0, 0)),
    ((200, 0, 400), (500, 0, 400)),
    ((200, 0, 700), (400, 0, 700)),
    ((200, 0, 700), (200, 0, 600))
]

# Coordonnées des virages
curved_roads = [
    ((0, 0, 300), (200, 0, 400)),
    ((0, 0, 600), (200, 0, 700)),
    ((500, 0, 100), (300, 0, 0)),
    ((200, 0, 700), (300, 0, 600)),
    ((400, 0, 700), (300, 0, 600)),
    ((500, 0, 600), (400, 0, 700)),
]

# Points d'apparitions possibles des voitures
spawn_points = [
    (0, 0, 300)
]

# Points de "destination" possibles pour les voitures
destination_points = [
    (200, 0, 700)
]

# CRÉATION DES ROUTES #

simulation.create_roads(straight_roads)
simulation.create_roads(curved_roads, True)

# STATISTIQUES ET PERFORMANCES #

simulation_run_time = 60 * 100  # Temps (60*temps en secondes) que va durer la simulation avant de s'arrêter

# APPARITION DES VOITURES #

i = 0
car_spawn_cooldown_range = (1, 2)  # Cooldown entre 2 spawn de voitures (en secondes) (bornes incluses)
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
            simulation.create_car_random_path(spawn_points, destination_points, randint(50, 100))
