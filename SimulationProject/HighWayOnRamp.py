from Simulation import *

simulation = Simulation()

straight_roads = [
    ((-5000, 0, -30), (5000, 0, -30)),
    ((-5000, 0, -10), (5000, 0, -10)),
    ((-5000, 0, 10), (5000, 0, 10)),
    ((-5000, 0, 30), (5000, 0, 30)),
    ((-500, 0, -30), (-299, 0, -50)),
    ((-301, 0, -50), (0, 0, -50))
]

curved_roads = [
    ((300, 0, -300), (0, 0, -50))
]

simulation.create_roads(straight_roads)
simulation.create_roads(curved_roads, True)

print(simulation.network)
print(simulation.trafficMap)