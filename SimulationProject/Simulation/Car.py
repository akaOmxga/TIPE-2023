from Simulation.View import * 

epsilon = 5  # TODO : Trouver une valeur correcte
dt = 1/60


class Car:

    # Trajectoire, une fonction donnant la trajectoire de la voiture dans la simulation (propre à chaque
    # lignes/virages) ; chemin, un chemin du graphe représentant l'ensemble des routes (lignes et virages) que la
    # voiture doit emprunter c.f. Victor si on a un problème
    def __init__(self, spawn_coordinates, speed, vehicle, chemin, start_clock):
        self.start_clock = start_clock

        self.position = spawn_coordinates  # (x,y,z)
        self.speed = speed  # m.s^(-1)
        self.speed_data = [] # liste dans laquelle on ajoute de façon régulière la vitesse la voiture afin d'en mesurer la vitesse moyenne pendant le trajet
        self.accel = 0  # m.s^(-2), 0 par défaut, car en mouvement rectiligne et uniforme
        self.vehicle = vehicle # objet vpython
        self.chemin = chemin # liste de sommet (x,y,z)
        self.chemin_init = chemin # chemin initiale que l'on ne modifiera pas 
        self.congestion_time = 0 # nombre de tic passés en mode congestion avec la convention : congestion ssi v < 70% limitation vitesse

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

        accel = pfd_IDM(self, dt, simulation_object)
        new_speed = self.speed + dt*accel
        self.speed = new_speed
        # si new_speed < 70%*limitation de vitesse : alors nous sommes en congestion, on ajoute un tic d'update à congestion_time : 
        
        start = self.chemin[0]
        end = self.chemin[1]

        if (new_speed < (80/100)*simulation_object.network.get_road_speed_limit(start,end)) and (simulation_object.internal_clock - self.start_clock > 90):
            self.congestion_time += 1

        # si le délai delta_t est écouler, on prélève la vitesse de la voiture dans speed_data :

        delta_t = 30 # échelle : delta_t = 60 => toutes les secondes 
        if (simulation_object.internal_clock)%(delta_t) == 1 :
            self.speed_data.append(self.speed)

        # update de la position :

        dm = integration(self.speed, accel, dt)  # distance infinitésimale parcourue par la voiture sur dt
        x, y, z = voiture.pos.x, voiture.pos.y, voiture.pos.z

        # Cas où la voiture est proche (à epsilon près) d'une transition de route
        # → on fait la transition vers la prochaine route
        if distance(sommet_fin, (x, y, z)) < epsilon + 5:
            # update la position
            update_car(self, chemin, dm, simulation_object)

            new_chemin = chemin[1::]
            self.chemin = new_chemin
            
            # On se supprime de la portion de route dans trafficMap
            simulation_object.trafficMap.delete_car_from_road(chemin[0], sommet_fin, self)
        else:  # cas où la voiture peut parcourir dm sur la portion de route actuelle
            update_car(self, chemin, dm, simulation_object)

    def dispawn(self, simulation_object):
        # Transférer les données de la voiture au module PerformanceStats
        stats_object = simulation_object.stats
        stats_object.voitures_arrivees += 1
        stats_object.congestion_time += round(self.congestion_time / 60, 2)
        stats_object.distance += round(longueur_chemin(self.chemin_init), 2)
        stats_object.temps_reel.append(round((simulation_object.internal_clock - self.start_clock)/60, 2))
        stats_object.temps_ideal.append(round(temps_chemin(self.chemin_init, simulation_object), 2))
        stats_object.vitesse.append(round(moyenne(self.speed_data), 2))
        
        # Envoyer les infos à vpython + liste voitures dans TrafficMap
        dispawn_car(self.vehicle)
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
