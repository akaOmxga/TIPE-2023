from Simulation import *
from vpython import *

simulation = Simulation()

straight_roads = [
]

curved_roads = [
    ((0, 0, 250), (250, 0, 0)),
    ((-250, 0, 0), (0, 0, 250)),
    ((0, 0, -250), (-250, 0, 0)),
    ((250, 0, 0), (0, 0, -250))
]

simulation.create_roads(straight_roads)
simulation.create_roads(curved_roads, True)

i = 0

# sans ça, le côté vpython sort 10^10^10 erreurs/s
while True:
    rate(60)
    simulation.update()
    i += 1

    if (i >= 300):
        simulation.spawn_car_test((250, 10, 0))
        i = 0
