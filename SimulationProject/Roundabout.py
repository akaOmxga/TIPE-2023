from Simulation import *
from vpython import *

simulation = Simulation()

straight_roads = [
]

curved_roads = [
    ((850, 0, 1050), (1050, 0, 1150)),
    ((1050, 0, 1150), (1150, 0, 950)),
    ((1150, 0, 950), (950, 0, 850)),
    ((950, 0, 850), (850, 0, 1050))
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
        simulation.spawn_car_test((850, 0, 1050))
        i = 0
