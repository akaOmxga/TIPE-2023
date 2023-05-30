#  Modèle continu :
#
#  - Temps de simu (que l'on définit)
#  - Définir intervalle de spawn
#
#  - Temps moyen de parcours → self.temps_moy
#
#  - Vitesse moyenne des véhicules → self.vitesse_moy
#
#  - Savoir le nombre de voitures qui sont arrivées et le nombre qui a spawn
#    → self.voitures_apparues et self.voitures_arrivees
#
#  - Taux de congestion
#  -


class PerformanceStats:

    def __init__(self, simulation_object):
        self.simulation_object = simulation_object # Objet Simulation
        self.congestion_time = 0 # somme des temps individuel passés en "congestion" avec pour norme : congestion ssi v < 70% limitation de vitesse 
        self.voitures_apparues = 0 # nombre de voitures ayant apparues
        self.voitures_arrivees = 0 # nombre de voitures étant arrivées (len(n'importe quelle liste succédant ceci))
        self.distance = 0 # somme des longueurs de trajets effectués
        self.temps_reel = [] # liste contenant le temps mis par chaque véhicule pour effectuer leur trajet
        self.temps_ideal = [] # liste contenant le temps minimal de chaque véhicule pour effectuer leur trajet
        self.vitesse = [] # liste contenant les vitesse moyennes de chaque véhicule pendant leur parcours
      #  self.densite_max_autoroute = 0 # densité maximale du réseau d'autoroute pendant la simulation (il est envisageable de faire de même avec le min et les autres types de route), l'objectif de l'optimisation étant de minimiser (indirectement) cette densité
        ### envisageable ultérieurement (l'implémentation rencontrera probablement des problèmes de complexité mémoire ...)
      #  self.vitesse_autoroute = [] # liste contenant les vitesse moyennes de chaque véhicule pendant leur parcours sur autoroute
      #  self.vitesse_nationale = [] # liste contenant les vitesse moyennes de chaque véhicule pendant leur parcours sur nationale
      #  self.vitesse_departementale = [] # liste contenant les vitesse moyennes de chaque véhicule pendant leur parcours sur departementale
      #  self.vitesse_ville = [] # liste contenant les vitesse moyennes de chaque véhicule pendant leur parcours en ville
      
    def __str__(self):
        return("Durée simu : " + str(self.simulation_object.internal_clock) +
            "\nTemps de congestion : " + str(self.congestion_time) +  # temps passé à une vitesse inf à 70% de la congestion
            "\nVoitures apparues : " + str(self.voitures_apparues) +
            "\nVoitures arrivées : " + str(self.voitures_arrivees) +
            "\nDistance totale parcourue : " + str(self.distance) +
            "\n\nTemps moyen de parcours : " + str(self.temps_moy()) +
            "\nRetard moyen de parcours : " + str(self.retard_moy()) +
            "\nVitesse moyenne de parcours : " + str(self.vitesse_moy()) +
            "\nFlux moyen : " + str(self.flux_moy()) +
            "\nIndice de congestion : " + str(self.indice_congestion()) +
            "\n\n\nTemps réels total : " + str(self.temps_reel) +
            "\n\nTemps idéaux total : " + str(self.temps_ideal) +
            "\n\nVitesses moyennes : " + str(self.vitesse)
            )

    # temps moyen de parcours (en secondes)
    def temps_moy(self):
        temps_total = 0

        for temps_individuel in self.temps_reel: 
            temps_total += temps_individuel

        return temps_total / self.voitures_arrivees

    # l'écart-type du temps de parcours / moyenne du retard (moyenne de la différence entre temps de parcours réel et idéal) (en s)
    def retard_moy(self):
        retard_total = 0
        N = len(self.temps_reel)

        for i in range(N):
            retard_total += (self.temps_reel[i] - self.temps_ideal[i])

        return retard_total/self.voitures_arrivees

    # vitesse moyenne de parcours (en m/s)
    def vitesse_moy(self):
        vitesse_total = 0
        
        for vitesse in self.vitesse:
            vitesse_total += vitesse

        return vitesse_total/self.voitures_arrivees

    # flux moyen de parcours (nombre de voiture/s)
    def flux_moy(self):
        return self.voitures_apparues / self.simulation_object.internal_clock

    # pourcentage de temps passer en "congestion" avec pour norme : congestion ssi v < 70% limitation de vitesse
    def indice_congestion(self):
        temps_total = 0
        for temps_individuel in self.temps_reel: 
            temps_total += temps_individuel
        return self.congestion_time / temps_total
    