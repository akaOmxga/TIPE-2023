from Simulation import *
from vpython import *

simulation = Simulation()


straight_roads = [
    ((-50,0,-10), (-5000,0,-10)),
    ((-5000,0,10),(-50,0,10)),
    ((10,0,-50),(10,0,-5000)),
    ((-10,0,-5000),(-10,0,-50)),
    ((50,0,10),(5000,0,10)),
    ((5000,0,-10),(50,0,-10)),
    ((-10,0,50),(-10,0,5000)),
    ((10,0,5000),(10,0,50)),
    ((-50,0,10),(50,0,10)),
    ((10,0,50),(10,0,-50)),
    ((50,0,-10),(-50,0,-10)),
    ((-10,0,-50),(-10,0,50)),
]

curved_roads = [
    ((10,0,-50),(-50,0,10)),
    ((-10,0,50),(-50,0,10)),
    ((10,0,50),(-50,0,-10)),
    ((10,0,50),(50,0,10)),
    ((-10,0,50),(50,0,-10)),
    ((10,0,-50),(50,0,-10)),
    ((-10,0,-50),(50,0,10)),
    ((-10,0,-50),(-50,0,-10)),
]



simulation.create_roads(straight_roads)
simulation.create_roads(curved_roads, True)

print(simulation.network)
print(simulation.trafficMap)

# sans ça, le côté vpython sort 10^10^10 erreurs/s
while True:
    rate(60)