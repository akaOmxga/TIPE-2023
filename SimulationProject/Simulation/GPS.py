# optimisation du chemin des voiture pendant leur trajet en fonction des autres voitures
from Simulation.View import * 


class PositioningSystem :

    def __init__(self, range) :
        self.perspective = True #booléen qui traduit si la vérification des embouteillages s'effectuent grâce à un parcourt en largeur (sinon, si perspective = False => parcourt en profondeur)


    # on cherche tous les chemins entre voiture.chemin[O] et voiture.chemin[self.range] 
    # TODO :par parcourt en largeur/profondeur # on conserve le plus court (en temps)
    
    def optimisation(self,simulation_object,voiture,perspective) :      
        start, end = voiture.chemin[0], voiture.chemin[self.range]
        potential_paths = simulation_object.network.find_all_path(start, end,simulation_object.max_length/3)
        optimal_path = voiture.chemin[0:self.range]
        for path in potential_paths :
            if View.temps_chemin(path,simulation_object) <= View.temps_chemin(optimal_path,simulation_object) :
                optimal_path = path
        return optimal_path!=voiture.chemin,optimal_path



    def traffic_check(self,simulation_object,voiture) : # vérifie pour une voiture donnée si on dispose d'un chemin plus efficace, pour éviter l'embouteillage (seulement sur la range du GPS) : renvoie(bool,chemin)
        # l'optimisation a-t-elle un intérêt ? (rapport complexité/gain)
        if self.range >= len(voiture.chemin): # optimisation sur une trop courte distance, la voiture est bientôt arrivée
            return(False,[])
        else :  
            estimated_time = View.temps_chemin(voiture.chemin[:self.range],simulation_object)
            return(self.optimisation(simulation_object,voiture,self.perspective))
        

    def traffic_update(self,simulation_object, voiture) : # on modifie le chemin de la voiture selon le check précédent
        check, potential_path = self.traffic_check(self,simulation_object, voiture)
        if check == True :
            path = potential_path + voiture.chemin[self.range::]
            voiture.chemin = path
        else :
            return()
