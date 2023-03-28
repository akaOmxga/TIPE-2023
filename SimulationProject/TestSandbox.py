from SimulationProject.Simulation.Simulation import *
from vpython import *

simulation = Simulation()

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
    (0, 0, 0)
]

# Points de "destination" possibles pour les voitures
destination_points = [
    (200, 0, 600)
]

car_spawn_cooldown_range = (1, 2)  # Cooldown entre 2 spawn de voitures (en secondes) (bornes incluses)

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
        # test
        simulation.create_car_random_path(spawn_points, destination_points, randint(50, 100))
