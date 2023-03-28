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
        self.voitures_apparues = 0
        self.voitures_arrivees = 0
        self.temps_moy = 0
        self.vitesse_moy = 0
