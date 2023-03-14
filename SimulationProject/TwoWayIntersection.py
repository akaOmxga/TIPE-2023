from Simulation import *
from vpython import *

simulation = Simulation()

straight_roads = [
    ((950, 0, 990), (-1000, 0, 990)),
    ((-1000, 0, 1010), (950, 0, 1010)),
    ((1010, 0, 950), (1010, 0, -1000)),
    ((990, 0, -1000), (990, 0, 950)),
    ((1050, 0, 1010), (3000, 0, 1010)),
    ((3000, 0, 990), (1050, 0, 990)),
    ((990, 0, 1050), (990, 0, 3000)),
    ((1010, 0, 3000), (1010, 0, 1050)),
    ((950, 0, 1010), (1050, 0, 1010)),
    ((1010, 0, 1050), (1010, 0, 950)),
    ((1050, 0, 990), (950, 0, 990)),
    ((990, 0, 950), (990, 0, 1050)),
]

curved_roads = [
    ((1010, 0, 950), (950, 0, 1010)),
    ((990, 0, 1050), (950, 0, 1010)),
    ((1010, 0, 1050), (950, 0, 990)),
    ((1010, 0, 1050), (1050, 0, 1010)),
    ((990, 0, 1050), (1050, 0, 990)),
    ((1010, 0, 950), (1050, 0, 990)),
    ((990, 0, 950), (1050, 0, 1010)),
    ((990, 0, 950), (950, 0, 990)),
]

# Points d'apparitions possibles des voitures
spawn_points = [
    (950, 0, 990),
    (-1000, 0, 990),
    (1010, 0, 1050),
    (1010, 0, 950),
    (1050, 0, 990),
    (950, 0, 990),
    (990, 0, 950),
    (990, 0, 1050)
]

# Points de "destination" possibles pour les voitures
destination_points = [
    (950, 0, 990),
    (-1000, 0, 990),
    (1010, 0, 1050),
    (1010, 0, 950),
    (1050, 0, 990),
    (950, 0, 990),
    (990, 0, 950),
    (990, 0, 1050)
]

car_spawn_cooldown_range = (5, 10)  # Cooldown entre 2 spawn de voitures (en secondes) (bornes incluses)

simulation.create_roads(straight_roads)
simulation.create_roads(curved_roads, True)

i = 0
next_spawn_time = 60

# sans ça, le côté vpython sort 1010^1010^1010 erreurs/s
while True:
    rate(60)
    simulation.update()

    i += 1
    if i >= next_spawn_time:
        i = 0
        next_spawn_time = 60 * randint(car_spawn_cooldown_range[0], car_spawn_cooldown_range[1])
        # TODO : spawn car
        simulation.create_car(spawn_points, destination_points)
