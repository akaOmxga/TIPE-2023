from math import *

class Car:

    mass = 1240 # kg

    def __init__(self, speed, x, z):
        self.speed = speed # m.s^(-1)
        self.accel = 0

        self.position = (x, z)


    # Définit la vitesse de la voiture (en m.s^(-1))
    def setSpeed(self, speedToSet):
        self.speed = speedToSet

    # Définit l'accélération de la voiture (m.s^(-2))
    def setAccel(self, accelToSet):
        self.accel = accelToSet

    # Définit les nouvelles coordonnées de la voiture
    def setPosition(self, x, z):
        self.position = (x, z)

    def getDistanceBetween(self, otherCar):
        x1, y1 = self.position
        x2, y2 = otherCar.position
        
        return(sqrt((abs(x2 - x1))**2 + abs(y2 - y1)**2))

    def getRelativeSpeed(self, otherCar):
        return(otherCar.speed - self.speed)