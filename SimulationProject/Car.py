from math import *

class Car:

    # Pour créer un objet voiture : ``car = Car(vitesse, x, y)`` exemple : ``maVoiture = new Car(15, 0, 0)``
    def __init__(self, speed, x, y, z):
        self.speed = speed # m.s^(-1)
        self.accel = 0
        self.mass = 1240 # kg

        self.position = (x, y, z)

    def __str__(self):
        return f"Objet voiture, position : {position}"

    def getDistanceBetween(self, otherCar):
        x1, y1, z1 = self.position
        x2, y2, z2 = otherCar.position

        return(sqrt((abs(x2 - x1))**2 + abs(y2 - y1)**2) + abs(z2 - z1)**2)