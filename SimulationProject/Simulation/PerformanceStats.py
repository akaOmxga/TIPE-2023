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


class Perfs:

    def __init__(self):
        self.simulation_time = 0 # durée de la simulation
        self.congestion_time = 0 # somme des temps individuel passés en "congestion" avec pour norme : congestion ssi v < 70% limitation de vitesse 
        self.voitures_apparues = 0 # nombre de voitures ayant apparues
        self.voitures_arrivees = 0 # nombre de voitures étant arrivées (len(n'importe quelle liste succédant ceci))
        self.distance = 0 # somme des longueurs de trajets effectués
        self.temps_reel = [] # liste contenant le temps mis par chaque véhicule pour effectuer leur trajet
        self.temps_ideal = [] # liste contenant le temps minimal de chaque véhicule pour effectuer leur trajet
        self.vitesse = [] # liste contenant les vitesse moyennes de chaque véhicule pendant leur parcourt
        self.vitesse_autoroute = [] # liste contenant les vitesse moyennes de chaque véhicule pendant leur parcourt sur autoroute
        self.vitesse_nationale = [] # liste contenant les vitesse moyennes de chaque véhicule pendant leur parcourt sur nationale
        self.vitesse_departementale = [] # liste contenant les vitesse moyennes de chaque véhicule pendant leur parcourt sur departementale
        self.vitesse_ville = [] # liste contenant les vitesse moyennes de chaque véhicule pendant leur parcourt en ville
        self.densite_max_autoroute = 0 # densité maximale du réseau d'autoroute pendant la simulation (il est envisageable de faire de même avec le min et les autres types de route), l'objectif de l'optimisation étant de minimiser (indirectement) cette densité


    def temps_moy(self) : # temps moyen de parcourt : s
        temps_total = 0
        for temps_individuel in temps_reel : 
            temps_total += temps_individuel
        return(temps_total/self.voitures_apparues)

    def retard_moy(self) : # l'écart-type du temps de parcours / moyenne du retard (moyenne de la différence entre temps de parcourt réel et idéal) : s
        retard_total = 0
        N = len(self.temps_reel)
        for i in range(N) :
            retard_total += (self.temps_reel[i] - self.temps_ideal[i])
        return(retard_total/self.voitures_apparues)

    def vitesse_moy(self) : # vitesse moyenne de parcourt : m/s
        vitesse_total = 0
        for vitesse in self.vitesse :
            vitesse_total += vitesse
        return(vitesse_total/self.voitures_apparues)

    def flux_moy(self) : # flux moyen de parcourt : nombre de voiture/s 
        return(self.voitures_apparues/self.simulation_time)

    def indice_congestion(self) : # pourcentage de temps passer en "congestion" avec pour norme : congestion ssi v < 70% limitation de vitesse
        temps_total = 0
        for temps_individuel in self.temps_reel : 
            temps_total += temps_individuel
        return (self.congestion_time/temps_total)