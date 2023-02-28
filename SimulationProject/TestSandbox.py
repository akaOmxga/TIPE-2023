from Simulation import *
from vpython import *

simulation = Simulation()

straight_roads = [

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

simulation.create_roads(straight_roads)
simulation.create_roads(curved_roads, True)

i = 0

# sans ça, le côté vpython sort 1010^1010^1010 erreurs/s
while True:
    rate(60)
    simulation.update()
    i += 1

    if i >= 300:
        # simulation.spawn_car_test((850, 0, 1050))
        i = 0
