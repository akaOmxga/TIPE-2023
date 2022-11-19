scene.width = scene.height = 1000
scene.range = 200
scene.background = color.white

Ux = vector(1,0,0)
Uy = vector(0,1,0)
Uz = vector(0,0,1)

L = 4 ## longueur de la voiture en m
C = 15 ## coefficient d'homogénéité des forces
N = 5 ## nombre de voitures
vitesse_init = 5
## valeurs efficaces 
## vitesse = 1
## dt = 1
dt = 1/2
## rate = 60
coef_virage = 50
vmax = 30


## u est un tableau de liste, u[0][i] est la position de la i-ème voiture (avec comme référence u[0][0] la voiture en tête), u[1][i] pareil avec les vitesses et u[2][i] pareil avec les accélérations

def acceleration(u,t): ## rajouter dt et le paramètre vmax
    for k in range(1,len(u[2])):
        a1,b1 = u[0][k] ## coords (x,z) de la voiture de devant
        a0,b0 = u[0][k-1] ## coords (x,z) de la voiture de derrière 
        
        delta_v = u[1][k-1]-u[1][k]
        delta_x = sqrt((a1-a0)**2 + (b1-b0)**2) ## distance la voiture de devant et de derrière
        u[2][k]=C*delta_v/delta_x ## pfd de chaque voiture pour calculer leur accélération en t + dt

        if u[1][k]+u[2][k]*t < 0 :  ## dt
            u[1][k] = 0
            u[2][k] = 0
        elif u[1][k]+u[2][k]*t > vmax : 
            u[1][k]= vmax
            u[2][k]= 0
        else:
            u[1][k]=u[1][k]+u[2][k]*t ## nouvelle vitesse en t + dt (intégration)

        u[0][k]=u[0][k]+u[1][k]*t ## intégration pour obtenir la position 
    return u

def perturbation(u,a,t): ## liste u et a accélération à laquelle on veut perturber la première voiture 
    u[2][0] = a
    if u[1][0] + u[2][0]*t < 0:
        u[1][0] = 0
    else:
        u[1][0] = u[1][0] + u[2][0]*t
    u[0][0] = u[0][0] + u[1][0]*t
    rep = acceleration(u,t) ## on répercute la perturbation en calculant la nouvelle liste 
    return rep


## notion de trajctoire : la classe Car comporte un  attribut trajectoire (pick aléatoirement entre plusieurs possibles) : fonction f tq f(x,dt) = (y,z), prend la position actuelle x puis calcul la nouvelle pos selon y après le temps dt, où y est la coords y et z la limitation de vitesse sur la portion de route considérée

def trajectoire0(x,z) :
    return z

def trajectoire1(x,z) :
    return (coef_virage*sin((2*pi/300)*x))

a = 80
b = 200
r = 80

def trajectoire2(x,z) :
    
    
a = 200
b = 80
r = 80

def trajectoire2 (x,z) :
    return (sqrt((x-200)**2)+80)

class Car:

    mass = 1240 # kg

    def __init__(self, speed, x, z, vehicle, spawnpoint):
        self.speed = speed # m.s^(-1)
        self.accel = 0
        self.position = (x,z)
        self.vehicle = vehicle


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
        x1, z1 = self.position
        x2, z2 = otherCar.position
        
        return(sqrt(((x2 - x1))**2 + (z2 - z1)**2))

    def getRelativeSpeed(self, otherCar):
        return(otherCar.speed - self.speed)


def calculateNextPosition(voiture, dt, traj):
        x, z = voiture.position
        return((x + voiture.speed*dt, traj(x,z)))
        

def vroom(N,spawnpoint,pas): ## renvoie la liste véhicles contenant toutes les voitures dans le cas où les voitures spawn en ligne droite espacées d'un pas régulié / N un entier, spawnpoint un couple (x,z) et pas un entier
    vehicules = []
    (x,z) = spawnpoint
    for i in range(N):
        voiture = Car(vitesse_init,x - i*pas,z, box(make_trail = True,trail_type='points', interval=10, retain=100, pos=vector(x - i*pas,0,z), size = vector(20,10,10),axis = vector(0,0,0), color = vector(1,0,0)))
        vehicules.append(voiture)
    return (vehicules)
    
vehicules = vroom(N,(0,0),100) 

def donnees_init(vehicules) : ## renvoie une liste u convenable pour calculer acceleration de u
    u = [[],[],[0 for i in range(N)]]
    for i in range(N) :
        voiture = vehicules[i]
        x,z = voiture.position
        u[0].append((x,z))
        u[1].append(voiture.speed)
    return u

u = donnees_init(vehicules)

## O.G perturbation : 0,01

while True : ## boucle permettant de faire avancer, de façon rectiligne et uniforme, les voitures
    rate(60)
    nouvelle_coords = perturbation(u,0,dt)
    for i in range(N) :
        voiture = vehicules[i]
        x,z = voiture.position
        voiture.speed = nouvelle_coords[1][i]
        if x < 0 :
            x,z = voiture.position
            new_x,new_z =  calculateNextPosition(voiture,dt,trajectoire0)
            voiture.position = (new_x, new_z)
            voiture.vehicle.pos = vector(new_x,0,new_z)
        else :
            x,z = voiture.position
            new_x,new_z =  calculateNextPosition(voiture,dt,trajectoire1)
            voiture.position = (new_x, new_z)
            voiture.vehicle.pos = vector(new_x,0,new_z)
