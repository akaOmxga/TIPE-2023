import View

epsilon = 8  # TODO : modif


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

    # fait dispawn les voitures, avancer les voitures, transition entre les différents noeuds du graphe
    def update(self, simulation_object):

        chemin = self.chemin
        n = len(chemin)

        if n == 1:
            # On a plus de chemin à parcourir, on a fini la route -> on dispawn
            self.dispawn(simulation_object)
            return

        sommet_fin = chemin[1]
        voiture = self.vehicle  # car = objet Car, voiture = objet vpython

        dm = 1  # distance infinitésimale parcourue par la voiture sur dt
        x, y, z = voiture.pos.x, voiture.pos.y, voiture.pos.z

        # Cas où la voiture est proche (à epsilon près) d'une transition de route
        # → on fait la transition vers la prochaine route
        if View.distance(sommet_fin, (x, y, z)) < epsilon:

            # update la position
            View.update_car(self, chemin, None, simulation_object.network)  # dm = none → on change de route

            new_chemin = chemin[1::]
            self.chemin = new_chemin
        else:  # cas où la voiture peut parcourir dm sur la portion de route actuelle
            View.update_car(self, chemin, dm, simulation_object.network)

    def dispawn(self, simulation_object):
        # TODO : Transfer perf data to simulation
        print((simulation_object.internal_clock - self.clock) / 60)

        # Envoyer les infos à vpython + liste voitures dans TrafficMap
        View.dispawn_car(self.vehicle)
        simulation_object.carsList.remove(self)
        del self
