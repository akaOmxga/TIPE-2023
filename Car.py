from math import *

class Car:

    mass = 1240 # kg


    # Pour créer un objet voiture : ``car = Car(vitesse, x, y)`` exemple : ``maVoiture = new Car(15, 0, 0)`` 
    def __init__(self, speed, x, y):
        self.speed = speed # m.s^(-1)
        self.accel = 0

        self.position = (x, y)


    # Définit la vitesse de la voiture (en m.s^(-1))
    def setSpeed(self, speedToSet):
        self.speed = speedToSet

    # Définit l'accélération de la voiture (m.s^(-2))
    def setAccel(self, accelToSet):
        self.accel = accelToSet

    # Définit les nouvelles coordonnées de la voiture
    def setPosition(self, x, y):
        self.position = (x, y)

    def getDistanceBetween(self, otherCar):
        x1, y1 = self.position
        x2, y2 = otherCar.position
        
        return(sqrt((abs(x2 - x1))**2 + abs(y2 - y1)**2))


    # Renvoie la vitesse relative entre cet objet et la voiture passée en argument (ne tient pas compte de l'orientation des voitures)
    def getRelativeSpeed(self, otherCar):
        return(otherCar.speed - self.speed)


    # Calcule la prochaine position de la voiture, la définit et la renvoie
    def calculateNextPosition(self, dt):
        
        # Ici, fait pour que ça fonctionne dans le cas unidimensionnel selon x seulement (on ne touche pas à y)
        # En gros : on considère que les vecteurs vitesse et accélération sont selon Ux seulement
        x, y = self.position

        self.position = (x + self.speed*dt, y)
        return(self.position)


    # Trouve la voiture la plus proche de l'objet dans une liste de voiture donnée (qui peut contenir l'objet lui même)
    # Renvoie l'objet de la voiture la plus proche
    # (Complexité : O(n))
    def getNearestCar(self, carList):
        if (len(carList) < 2):
            return None
        
        if (carList[0] == self):
            distanceMin = self.getDistanceBetween(carList[1])
            closestCar = carList[1]
        else:
            distanceMin = self.getDistanceBetween(carList[0])
            closestCar = carList[0]

        for car in carList:
            if (car != self):
                distance = self.getDistanceBetween(car)
                if (distance < distanceMin):
                    distanceMin = distance
                    closestCar = car
        
        return closestCar
