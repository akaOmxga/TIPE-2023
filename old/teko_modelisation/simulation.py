class Simulation:

    def __init__(self):
        self.t = 0.0            # Time marker (i.e. repère temporel)
        self.frame_count = 0    # Frame count
        self.dt = 1/60          # Simulation framerate
        self.roads = []

    def update(self):
        pass

    def run(self):
        pass

    def create_roads(self, roads_to_create):
        for road in roads_to_create:
            self.create_road(road)

    def create_road(self, road):
        self.roads.append(road)
        vpython.createRoad(a, b)
        graphe.addA