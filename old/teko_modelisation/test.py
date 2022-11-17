from simulation import Simulation

sim = Simulation()

sim.create_roads([
    ((-10, 106), (290, 106)),
    ((-10, 102), (290, 102)),

    ((290, 98), (-10, 98)),
    ((290, 94), (80, 94)),
    ((80, 94), (-10, 94)),
])