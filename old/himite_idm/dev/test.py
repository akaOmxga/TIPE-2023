from trafficSimulator import *

# Create simulation
sim = Simulation()

# Curve resolution
n = 15

# Add multiple roads
sim.create_roads([
    ((-10, 106), (290, 106)),
    ((-10, 102), (290, 102)),

    ((290, 98), (-10, 98)),
    ((290, 94), (80, 94)),
    ((80, 94), (-10, 94)),
])


# Start simulation
win = Window(sim)
win.offset = (-145, -95)
win.zoom = 8
win.run(steps_per_update=5)