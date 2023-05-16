import Simulation.View as View

epsilon = 8  # TODO : modif
dt = 1/60


class Car:

    # Trajectoire, une fonction donnant la trajectoire de la voiture dans la simulation (propre à chaque
    # lignes/virages) ; chemin, un chemin du graphe représentant l'ensemble des routes (lignes et virages) que la
    # voiture doit emprunter c.f. Victor si on a un problème
    def __init__(self, spawn_coordinates, speed, vehicle, chemin, start_clock):
        self.clock = start_clock

        self.position = spawn_coordinates  # (x,y,z)
        self.speed = speed  # m.s^(-1)
        self.accel = 0  # m.s^(-2), 0 par défaut, car en mouvement rectiligne et uniforme
        self.vehicle = vehicle
        self.chemin = chemin

    def __str__(self):
        return f"Objet voiture, position : {self.position}"

    # fait dispawn les voitures, avancer les voitures, transition entre les différents nœuds du graphe
    def update(self, simulation_object):
        network = simulation_object.network
        traffic_map = simulation_object.trafficMap


        chemin = self.chemin
        n = len(chemin)

        if n == 1:
            # On a plus de chemin à parcourir, on a fini la route -> on dispawn
            self.dispawn(simulation_object)
            return

        sommet_fin = chemin[1]
        voiture = self.vehicle  # car = objet Car, voiture = objet vpython

        accel = View.pfd_IDM(self, dt, simulation_object)

        dm = View.integration(self.speed, accel, dt) # distance infinitésimale parcourue par la voiture sur dt
        x, y, z = voiture.pos.x, voiture.pos.y, voiture.pos.z

        # Cas où la voiture est proche (à epsilon près) d'une transition de route
        # → on fait la transition vers la prochaine route
        if View.distance(sommet_fin, (x, y, z)) < epsilon:
            # update la position
            View.update_car(self, chemin, None)  # dm = none → on change de route

            new_chemin = chemin[1::]
            self.chemin = new_chemin

            # On se supprime de la portion de route dans trafficMap
            simulation_object.trafficMap.delete_car_from_road(chemin[0], sommet_fin, self)
        else:  # cas où la voiture peut parcourir dm sur la portion de route actuelle
            View.update_car(self, chemin, dm)

    def dispawn(self, simulation_object):
        # TODO : Transfer perf data to simulation
        # print((simulation_object.internal_clock - self.clock) / 60)

        # Envoyer les infos à vpython + liste voitures dans TrafficMap
        View.dispawn_car(self.vehicle)
        simulation_object.carsList.remove(self)
        del self

    def get_next_car(self, simulation_object):
        cars = simulation_object.trafficMap.get_cars_on_road(self.chemin[0], self.chemin[1])

        if cars:

            # Si cars[0] est self, alors on est la première voiture sur la route
            # Dans ce cas, on regarde sur les routes suivantes
            if cars[0] == self:
                if len(self.chemin) > 2:
                    prochaines_voitures = simulation_object.trafficMap.get_cars_on_road(self.chemin[1], self.chemin[2])

                    if prochaines_voitures is not None and prochaines_voitures != []:
                        return prochaines_voitures[len(prochaines_voitures) - 1]
            else:
                return cars[0]

        return None
